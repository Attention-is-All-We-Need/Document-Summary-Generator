from flask import Flask,request,render_template
import os
from src.components.data_transformation import gen_para_file
from werkzeug.utils import secure_filename
from src.utils import LED,Embeddings
from src.exception import CustomException
from src.logger import logging
from src.components.web_scraping import get_website
from src.components.web_scraping import get_yt
import numpy as np
import hnswlib
import re
from urllib.parse import urlparse, parse_qs
from contextlib import suppress

def allowed_file(file_name):
    file_extension = os.path.splitext(file_name)[1]
    if file_extension=='.pdf' or file_extension == '.doc' or file_extension == '.docx' or file_extension == '.txt':
        return True
    return False


app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(),'UPLOAD_FOLDER')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('home.html',files=os.listdir(UPLOAD_FOLDER))

@app.route('/upload',methods=['GET','POST'])
def upload():
    if request.method == 'GET':
        return render_template('home.html',files=os.listdir(UPLOAD_FOLDER))
    else:
        file =request.files['file-upload']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            paragraphs = gen_para_file(filename)
            text = ''.join(paragraphs)
            return render_template('home.html',results=text, files=os.listdir(UPLOAD_FOLDER))
        return render_template('home.html', files=os.listdir(UPLOAD_FOLDER))
    
# @app.route('/search_url',methods=['GET','POST'])
# def search_url():
#     if request.method == 'GET':
#         return render_template('home.html', files=os.listdir(UPLOAD_FOLDER))
#     else:
#         url=request.form.get('web-address-search')
#         text = get_website(url)
#         return render_template('home.html',results=text, files=os.listdir(UPLOAD_FOLDER))

@app.route('/search_url',methods=['GET','POST'])
def search_url():
    if request.method == 'GET':
        return render_template('home.html', files=os.listdir(UPLOAD_FOLDER))
    else:
        url = request.form.get('web-address-search')

        if re.match(r'^https?://(?:www\.)?youtube\.com/', url):
            text = get_yt(url)
        else:
            text = get_website(url)
        
        return render_template('home.html', results=text, files=os.listdir(UPLOAD_FOLDER))

@app.route('/showtext',methods=['GET','POST'])
def showtext():
    if request.method == 'GET':
        return render_template('home.html',files=os.listdir(UPLOAD_FOLDER))
    else:
        uploaded_files =request.form.getlist('files')
        text=[]
        for file in uploaded_files:
            file_text=gen_para_file(file)
            text.append(' '.join(file_text))
        text = ' '.join(text)
        return render_template('home.html', files=os.listdir(UPLOAD_FOLDER), results=text)

@app.route('/summary',methods=['GET','POST'])
def summary():
    if request.method == 'GET':
        return render_template('home.html', files=os.listdir(UPLOAD_FOLDER))
    else:
        
        text=request.form.get('inputtext')
        num_chars=1000
        if (num_chars):
            num_chars = int(request.form.get("num-chars"))
        key_word = request.form.get("keywordsearch")

        logging.info('Input received.')
        if (key_word):
            text_lines = text.split('.')
            emb= Embeddings()
            input_embeddings=[]
            for line in text_lines:
                input_embeddings.append(emb.embeddings(line))
            logging.info('Generated embeddings for input text.')
            input_embeddings=np.array(input_embeddings)
            key_embed = emb.embeddings(key_word)
            key_embed=np.array(key_embed)
            logging.info('Generated embeddings for keyword.')

            num_elements = len(input_embeddings)
            ids = np.arange(num_elements)
            dim = input_embeddings.shape[1]

            p = hnswlib.Index(space = 'cosine', dim = dim)
            p.init_index(max_elements = num_elements, ef_construction = 200, M = 16)
            logging.info('Initialised hnswlib.')
            p.add_items(input_embeddings, ids)
            p.set_ef(50)
            logging.info('Added items to hnswlib.')

            labels, distances = p.knn_query(key_embed, k = min(20,num_elements))
            answer=''
            for i in labels[0]:
                answer+= ''.join(text_lines[i])
            led = LED()
            summary =led.summarize(answer, max_length=num_chars)
            return render_template('home.html',results=text,results2=summary, files=os.listdir(UPLOAD_FOLDER))
        else :
            led = LED()
            summary =led.summarize(text, max_length=num_chars)
            return render_template('home.html',results=text,results2=summary, files=os.listdir(UPLOAD_FOLDER))


if __name__=="__main__":
    app.run(port=8000,debug=True)
