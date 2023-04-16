from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<html><body><p>hello world</p></body></html>'