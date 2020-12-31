import pymysql

from SRC import RetrieveData
from SRC import Queries
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    #connectionObject = pymysql.connect(host="127.0.0.1", user="DbMysql03", password="DbMysql03", db="DbMysql03",port=3305)
   app.run()