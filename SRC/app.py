import pymysql

from SRC import RetrieveData, Queries
from flask import Flask

app = Flask(__name__)


@app.route("/")
def test():
    return "hello"


if __name__ == '__main__':
    connectionObject = pymysql.connect(host="127.0.0.1", user="DbMysql03", password="DbMysql03", db="DbMysql03",
                                       port=3305)
