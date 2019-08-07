from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def index():
    return 'OK!'


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=os.environ['PORT'])