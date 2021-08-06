from flask import Flask, render_template


app = Flask(__name__)

"""
render_template: used to generate output from a template file based on the Jinja2 engine

The template files are stored in ./templates folder 
"""

@app.route('/')
def index():
    return render_template('index1.html')


if __name__ == '__main__':
    app.run()