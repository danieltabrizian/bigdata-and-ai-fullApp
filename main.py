from flask import Flask, render_template, jsonify, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<path:filename>')
def public_files(filename):
    public_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    return send_from_directory(public_folder, filename)

@app.route('/endpoint1')
def endpoint1():
    data = {'message': 'Hello from endpoint1'}
    return jsonify(data)

@app.route('/endpoint2')
def endpoint2():
    data = {'message': 'Hello from endpoint2'}
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)