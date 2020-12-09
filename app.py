import RetrieveData
from flask import Flask

app = Flask(__name__)


@app.route("/")
def test():
    return "hello"


if __name__ == '__main__':
    RetrieveData.main()
