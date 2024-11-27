# A very simple Flask Hello World app for you to get started with...
# mkvirtualenv myvirtualenv --python=/usr/bin/python3.10
# /home/[seu login]/.virtualenvs/myvirtualenv

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    name = "Ola mundo tudo bem !"
    return render_template('index.html',name=name)