from flask import Flask, request, send_from_directory,render_template,jsonify,flash, redirect,send_file
from werkzeug.contrib.cache import SimpleCache
import json
import sys
import socket
import os
from vision import WatsonVision
from werkzeug import secure_filename
import requests 
app = Flask(__name__, static_url_path='/static', template_folder='./templates')
app.config['UPLOAD_FOLDER'] = os.path.abspath('') + "/img/"
ALLOWED_EXTENSIONS = ['jpg,png']
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'pizza'



@app.route('/dropzone')
def drop():
    return render_template('dropzone.html')
@app.route('/coming_soon')
def coming():
    return render_template('coming-soon.html')

@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/scrape')
def signin():
    return render_template('signin.html')
@app.route('/', methods=('GET', 'POST'))
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
        visionUtil.createClassifier([filename], data['data']['name'])

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
      img = open(f.filename, 'rb')
      url = 'http://uploads.im/api?upload'
      files = {'file': img}
      r = requests.post(url, files=files)
      rawJson = r.json()
      img_path = rawJson['data']['img_url'].encode('utf8')
      visionUtil = WatsonVision()
      result = visionUtil.splitPredict(img_path, 'ppl_1905871502')
      return jsonify({'result':result})
      #return 'file uploaded successfully'
    else:
        return render_template('upload.html')




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
