from flask import Flask


app = Flask(__name__)

"""
make connection between url '/index' and function index
e.g. we have the ip address '127.0.0.1:5000', then if we add '/index' at the end, '127.0.0.1:5000/index'
the result "Hello World" will pop out. 
"""

@app.route('/index')
def index():
    return "Hello World"


if __name__ == '__main__':
    app.run()