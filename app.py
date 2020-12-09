from flask import Flask
import urllib
import json
import zlib
import time

app = Flask(__name__)


@app.route('/')
def hello_world():
    url = "https://api.themoviedb.org/3/movie/550?api_key="
    key = "d005091db9214b502565db95dea43fc7"
    res=urllib.urlopen(url+key).read()

if __name__ == '__main__':
    app.run()
