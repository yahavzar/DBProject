import pymysql
import requests

import RetrieveData
from Movie import Movie


def InsertMovies(connectionObject):
    count = 0
    movies = RetrieveData.fetch_movie()
    for movie in movies:
        try:
            # Create a cursor object
            cursorObject = connectionObject.cursor()

            # SQL query string


            sqlQueryMovie = "INSERT INTO Movie (apiId,title,langId,releaseDay,length,budget,revenue,collection,imdbId,homePage,status,popularity,voteCount,voteAvg,adult) VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            values = (movie.api_id, movie.title, 0, movie.release_date, movie.runtime, movie.budget, movie.revenue,
                      movie.collection, movie.imdb_id, movie.homepage, movie.status, movie.popularity, movie.vote_count,
                      movie.vote_avg, movie.adult)
            # Execute the sqlQuery

            cursorObject.execute(sqlQueryMovie, values)
            connectionObject.commit()
        except Exception as e:
            print("Exeception occured:{}".format(e))
            count += 1
            continue

    print("number of failed is ", count)

def InsertShow(connectionObject,Show):
    cursorObject = connectionObject.cursor()
    sqlQuery = "SELECT * FROM Language"
    cursorObject.execute(sqlQuery)
    rows = cursorObject.fetchall()
    lang = {}
    for row in rows:
        lang[row[0]] = row[1]
    cursorObject = connectionObject.cursor()
    sqlQuery = "INSERT INTO Shows (apiId,title,langId,releaseDay,length,homePage,status,popularity,voteCount,voteAvg,seasons,lastEpisodeId,nextEpisodeId) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    langId=get_key(lang,Show.original_language)
    if (langId==None):
        cursorObject = connectionObject.cursor()
        sqlQuery = "INSERT INTO Language (languageId,languageName) VALUES (%s,%s)"
        langId=max(lang)+1
        values = (langId,Show.original_language)
        lang[langId]=Show.original_language
        cursorObject.execute(sqlQuery, values)
        connectionObject.commit()
    values = (Show.api_id, Show.title,langId,Show.release_date,Show.runtime,Show.homepage,Show.status,Show.popularity,Show.vote_count,Show.vote_avg,Show.seasons,Show.last_episode,Show.next_episode)
    cursorObject.execute(sqlQuery, values)
    connectionObject.commit()
def InsertToLang(connectionObject):
    language= RetrieveData.fetchLanguage()
    for lang in language :
        try:
            cursorObject = connectionObject.cursor()
            sqlQuery = "INSERT INTO Language (languageId,languageName) VALUES (%s,%s)"
            values= (lang, language[lang])
            cursorObject.execute(sqlQuery, values)
            connectionObject.commit()
        except Exception as e:
            print("Exeception occured:{}".format(e))

def get_key(dict, val):
    for key, value in dict.items():
         if val == value:
             return key
    return None

def UpdateLangforMovie(connectionObject):
    cursorObject = connectionObject.cursor()
    sqlQuery = "SELECT * FROM Language"
    cursorObject.execute(sqlQuery)
    rows= cursorObject.fetchall()
    lang={}
    for row in rows :
        lang[row[0]]=row[1]
    movies = RetrieveData.fetch_movie()
    for movie in movies:
        try:
            # Create a cursor object
            cursorObject = connectionObject.cursor()


            sqlQueryMovie = "UPDATE  Movie SET langId = %s WHERE Movie.apiId = %s"
            num = get_key(lang,movie.original_language)
            values = (num,movie.api_id)
            # Execute the sqlQuery

            cursorObject.execute(sqlQueryMovie, values)
            connectionObject.commit()
        except Exception as e:
            print("Exeception occured:{}".format(e))
            continue

def updatelastlang(connectionObject):
    cursorObject = connectionObject.cursor()
    sqlQuery = "SELECT * FROM Language"
    cursorObject.execute(sqlQuery)
    rows = cursorObject.fetchall()
    lang = {}
    for row in rows:
        lang[row[0]] = row[1]
    sqlQuery = "SELECT * FROM Movie Where Movie.langId=0"
    cursorObject.execute(sqlQuery)
    rows = cursorObject.fetchall()
    for row in rows:
        try:
            movie_url = f"https://api.themoviedb.org/3/movie/{row[0]}"
            data = {'api_key': 'd005091db9214b502565db95dea43fc7'}
            req = requests.get(movie_url, data)
            sqlQueryMovie = "UPDATE  Movie SET langId = %s WHERE Movie.apiId = %s"
            js = req.json()
            num = get_key(lang, js['original_language'])
            values = (num,js['id'])
            cursorObject.execute(sqlQueryMovie, values)
            connectionObject.commit()
        except Exception as e:
            print("Exeception occured:{}".format(e))
            continue

def updateMovies(connectionObject):
    cursorObject = connectionObject.cursor()
    sqlQuery = "SELECT MovieOverview.filmId FROM MovieOverview LEFT JOIN Movie  ON Movie.apiId = MovieOverview.filmId WHERE Movie.apiId IS NULL"
    cursorObject.execute(sqlQuery)
    rows = cursorObject.fetchall()

    for row in rows:
        try:
            movie_url = f"https://api.themoviedb.org/3/movie/{row[0]}"
            data = {'api_key': 'd005091db9214b502565db95dea43fc7'}
            req = requests.get(movie_url, data)
            js = req.json()
            movie = Movie(js["adult"], js["belongs_to_collection"], js["budget"]
                              , js["genres"], js["homepage"], js["id"], js["imdb_id"],
                              js["original_language"], js["original_title"], js["overview"], js["popularity"]
                              , js["release_date"], js["revenue"]
                              , js["runtime"], js["spoken_languages"]
                              , js["status"], js["vote_count"], js["vote_average"])
            sqlQueryMovie = "INSERT INTO Movie (apiId,title,langId,releaseDay,length,budget,revenue,collection,imdbId,homePage,status,popularity,voteCount,voteAvg,adult) VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            values = (movie.api_id, movie.title, 0, movie.release_date, movie.runtime, movie.budget, movie.revenue,
                          movie.collection, movie.imdb_id, movie.homepage, movie.status, movie.popularity, movie.vote_count,
                          movie.vote_avg, movie.adult)
            cursorObject.execute(sqlQueryMovie, values)
            connectionObject.commit()
        except Exception as e:
            print("Exeception occured:{}".format(e))
            continue
def insertActors(connectionObject,actor, name,gender):
        cursorObject = connectionObject.cursor()
        sqlQuery = "INSERT INTO Actors (actorId,actorName,gender) VALUES (%s,%s,%s)"
        values = (actor, name,gender)
        cursorObject.execute(sqlQuery, values)
        connectionObject.commit()


def insertDirectors(connectionObject, directorId, directorName):
    cursorObject = connectionObject.cursor()
    sqlQuery = "INSERT INTO Directors (directorId,directorName) VALUES (%s,%s)"
    values = (directorId, directorName)
    cursorObject.execute(sqlQuery, values)
    connectionObject.commit()

def insertProducers(connectionObject, producerId, producerName):
    cursorObject = connectionObject.cursor()
    sqlQuery = "INSERT INTO Producers (producerId,producerName) VALUES (%s,%s)"
    values = (producerId, producerName)
    cursorObject.execute(sqlQuery, values)
    connectionObject.commit()

def insertGenres(connectionObject, id, name):
    cursorObject = connectionObject.cursor()
    sqlQuery = "INSERT INTO Genre (genreId,genreName) VALUES (%s,%s)"
    values = (id, name)
    cursorObject.execute(sqlQuery, values)
    connectionObject.commit()

def insertOverview(connectionObject, id, overview):
    cursorObject = connectionObject.cursor()
    sqlQuery = "INSERT INTO MovieOverview (FilmId,overview) VALUES (%s,%s)"
    values = (id, overview)
    cursorObject.execute(sqlQuery, values)
    connectionObject.commit()

def insertShowOverview(connectionObject, id, overview):
    cursorObject = connectionObject.cursor()
    sqlQuery = "INSERT INTO ShowOverview (showId,overview) VALUES (%s,%s)"
    values = (id, overview)
    cursorObject.execute(sqlQuery, values)
    connectionObject.commit()

def updateOverview(connectionObject):
    cursorObject = connectionObject.cursor()
    sqlQuery = "SELECT Movie.apiId FROM Movie LEFT JOIN MovieOverview  ON Movie.apiId = MovieOverview.filmId WHERE MovieOverview.filmId IS NULL"
    cursorObject.execute(sqlQuery)
    rows = cursorObject.fetchall()

    for row in rows:
        try:
            movie_url = f"https://api.themoviedb.org/3/movie/{row[0]}"
            data = {'api_key': 'd005091db9214b502565db95dea43fc7'}
            req = requests.get(movie_url, data)
            js = req.json()
            sqlQuery = "INSERT INTO MovieOverview (FilmId,overview) VALUES (%s,%s)"
            values = (js["id"], js["overview"])
            cursorObject.execute(sqlQuery, values)
            connectionObject.commit()

        except Exception as e:
            print("Exeception occured:{}".format(e))
            continue
def insertMovieGenere(connectionObject,genreId,apiId):
    cursorObject = connectionObject.cursor()
    sqlQuery = "INSERT INTO MoviesGenre (genreId,apiId) VALUES (%s,%s)"
    values = (genreId,apiId)
    cursorObject.execute(sqlQuery, values)
    connectionObject.commit()

def insertShowGenere(connectionObject,genreId,apiId):
    cursorObject = connectionObject.cursor()
    sqlQuery = "INSERT INTO ShowGenre (genreId,apiId) VALUES (%s,%s)"
    values = (genreId,apiId)
    cursorObject.execute(sqlQuery, values)
    connectionObject.commit()

def insertMovieSpokenLang(connectionObject, languageId, movieId):

    cursorObject = connectionObject.cursor()
    sqlQuery = "INSERT INTO LanguageMovie (languageId,movieId) VALUES (%s,%s)"
    values = (languageId, movieId)
    cursorObject.execute(sqlQuery, values)
    connectionObject.commit()

def insertShowSpokenLang(connectionObject, languageId, showId):
    cursorObject = connectionObject.cursor()
    sqlQuery = "SELECT * FROM Language"
    cursorObject.execute(sqlQuery)
    rows = cursorObject.fetchall()
    lang = {}
    for row in rows:
        lang[row[0]] = row[1]
    langId = get_key(lang, languageId)
    if (langId == None):
        cursorObject = connectionObject.cursor()
        sqlQuery = "INSERT INTO Language (languageId,languageName) VALUES (%s,%s)"
        langId = max(lang) + 1
        values = (langId, languageId)
        lang[langId] = languageId
        cursorObject.execute(sqlQuery, values)
        connectionObject.commit()
    cursorObject = connectionObject.cursor()
    sqlQuery = "INSERT INTO LanguageShow (languageId,showId) VALUES (%s,%s)"
    values = (langId, showId)
    cursorObject.execute(sqlQuery, values)
    connectionObject.commit()

def insertMovieActor(connectionObject,actorId,filmId):
    cursorObject = connectionObject.cursor()
    sqlQuery = "INSERT INTO ActorsMovie (actorId,filmId) VALUES (%s,%s)"
    values = (actorId,filmId)
    cursorObject.execute(sqlQuery, values)
    connectionObject.commit()

def insertMovieDirector(connectionObject,directorId,filmId):
    cursorObject = connectionObject.cursor()
    sqlQuery = "INSERT INTO DirectorsMovie  (directorId,filmId) VALUES (%s,%s)"
    values = (directorId,filmId)
    cursorObject.execute(sqlQuery, values)
    connectionObject.commit()

def insertProducersShow(connectionObject,producerId,showId):
    cursorObject = connectionObject.cursor()
    sqlQuery = "INSERT INTO ProducersShow  (producerId,showId) VALUES (%s,%s)"
    values = (producerId,showId)
    cursorObject.execute(sqlQuery, values)
    connectionObject.commit()

def InsertToTables():
    connectionObject = pymysql.connect(host="127.0.0.1", user="DbMysql03", password="DbMysql03", db="DbMysql03",port=3305)
    #InsertMovies(connectionObject);
    #shows = RetrieveData.fetch_TV_Show()
    #InsertToLang(connectionObject)
    #UpdateLangforMovie(connectionObject)
    #updateOverview(connectionObject)
    #updatelastlang(connectionObject)


