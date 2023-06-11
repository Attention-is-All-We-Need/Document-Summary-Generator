from flask import Flask,request,render_template

from src.components.data_transformation import gen_para_file

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/upload',methods=['GET','POST'])
def upload():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        file_name=request.form.get('file-upload')
        print(file_name)
        paragraphs = gen_para_file(file_name)
        print(len(paragraphs))
        text = ''.join(paragraphs)
        print(len(text))
        return render_template('home.html',results=text)

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
