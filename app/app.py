from flask import Flask, request, send_from_directory,render_template,jsonify
import json
import sys
from vision import WatsonVision
app = Flask(__name__, static_url_path='', template_folder='./templates')

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
        print(data['data']['links'], file=sys.stderr)
        links = data['data']['links']
        linkList = []
        for link in links:
            linkList.append(link['link'])
        visionUtil = WatsonVision()
        return jsonify({'file':visionUtil.zipper(linkList, data['data']['name'])})

    else:
        return jsonify({'result':'what the fuck'})
    
    

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)




if __name__ == "__main__":
    app.run()