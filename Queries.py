import pymysql
import requests

import RetrieveData
from Movie import Movie

def moviesWithActor(connectionObject, actorName):
    cursorObject = connectionObject.cursor()
    sqlQuery = '''SELECT Actors.actorName, Movie.title From Actors, ActorsMovie, Movie Where Actors.actorName = "%s" and Actors.actorId=ActorsMovie.actorId and ActorsMovie.filmId=Movie.apiId''' %(actorName)
    cursorObject.execute(sqlQuery)
    rows = cursorObject.fetchall()
    for row in rows:
        print(row[1]+"\n")
