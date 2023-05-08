from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

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