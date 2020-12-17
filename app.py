import RetrieveData
import CreateTables
from flask import Flask
import pymysql

app = Flask(__name__)


@app.route("/")
def test():
    return "hello"


if __name__ == '__main__':
    CreateTables.CreateTables()
    print("Done")
