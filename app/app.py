from flask import Flask, request, send_from_directory,render_template,jsonify
import json
import sys
app = Flask(__name__, static_url_path='', template_folder='./templates')

@app.route('/')
def signin():
    return render_template('signin.html')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/data', methods=('GET', 'POST'))
def data():
    if request.method == 'POST':
        print(request.form['data'], file=sys.stderr)
        data = request.form['data']
        return json.dumps(json.loads(data))
    else:
        return jsonify({'result':'what the fuck'})
    
    

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)




if __name__ == "__main__":
    app.run()