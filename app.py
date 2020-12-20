import RetrieveData
import CreateTables
from flask import Flask
import pymysql

app = Flask(__name__)


@app.route("/")
def test():
    return "hello"


if __name__ == '__main__':
    #CreateTables.InsertToTables()
    # connectionObject = pymysql.connect(host="127.0.0.1", user="DbMysql03", password="DbMysql03", db="DbMysql03",port=3305)
    #CreateTables.updateMovies(connectionObject)
    #RetrieveData.fetchDirectors()
    #RetrieveData.fetchGenreSpokenlang()
    #RetrieveData.fetchActorDirector()
    #RetrieveData.fetch_TV_Show()
    RetrieveData.fetchCreditsActors()