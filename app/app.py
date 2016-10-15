from flask import Flask, request, send_from_directory,render_template,jsonify,flash, redirect,send_file
import json
import sys
import os
from vision import WatsonVision
from werkzeug import secure_filename
app = Flask(__name__, static_url_path='', template_folder='./templates')
app.config['UPLOAD_FOLDER'] = os.path.abspath('') + "/img/"
ALLOWED_EXTENSIONS = ['jpg,png']
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'pizza'
@app.route('/')
def signin():
    return render_template('signin.html')
@app.route('/home', methods=('GET', 'POST'))
def home():
    return render_template('home.html')

@app.route('/data', methods=('GET', 'POST'))
def data():
    if request.method == 'POST':
        data = request.form['data']
        data = json.loads(data)
        links = data['data']['links']
        linkList = []
        for link in links:
            linkList.append(link['link'])
        visionUtil = WatsonVision()
        filename = visionUtil.zipper(linkList, data['data']['name'])
        return jsonify({'file':'new'})

    else:
        return jsonify({'result':'what the fuck'})
    



@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/img/<path:path>', methods = ("GET",))
def sendImage(path):
    return send_file(os.path.abspath('') + "/" + path)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      return redirect('/img/' + f.filename)
      #return 'file uploaded successfully'
    else:
        return render_template('upload.html')




if __name__ == "__main__":
    app.run()