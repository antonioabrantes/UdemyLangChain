# https://github.com/templates-back4app/containers-python-flask-sample
# configuração do arquivo Docker do back4app
# https://www.back4app.com/docs-containers/run-a-python-container-app

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello():
    name = "ola mundo, tudo bem com voce!"
    return render_template("index.html",name=name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)