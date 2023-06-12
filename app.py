from flask import Flask,request,render_template
import os
from src.components.data_transformation import gen_para_file
from werkzeug.utils import secure_filename

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
    return render_template('home.html')

@app.route('/upload',methods=['GET','POST'])
def upload():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        file =request.files['file-upload']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            paragraphs = gen_para_file(filename)
            print(len(paragraphs))
            text = ''.join(paragraphs)
            print(len(text))
            return render_template('home.html',results=text)
        return render_template('home.html')

@app.route('/search_url',methods=['GET','POST'])
def search_url():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        text=request.form.get('web-address-search')
        # print(text)
        return render_template('home.html',results=text)


if __name__=="__main__":
    app.run(port=8000,debug=True)
