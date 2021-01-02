import csv
import pymysql
from SRC import InsertQueries
from SRC.API_DATA_RETRIEVE.Movie import Movie
from SRC.API_DATA_RETRIEVE.Show import Show
import requests


def fetch_movie():
    # Fetch data for movies from api
    connectionObject = pymysql.connect(host="127.0.0.1", user="DbMysql03", password="DbMysql03", db="DbMysql03",
                                       port=3305)
    genres = {}
    languege = {}
    url = "https://api.themoviedb.org/3/discover/movie"
    count=1
    for i in range(1, 501):
        #in api the films are divided into 500 pages, with 20 films per page
        data = {'api_key': 'd005091db9214b502565db95dea43fc7',
                'page': str(i)}
        req = requests.get(url, data)
        movie_list = req.json()['results']
        for movie in movie_list:
            movie_url = f"https://api.themoviedb.org/3/movie/{movie['id']}"
            data = {'api_key': 'd005091db9214b502565db95dea43fc7'}
            req = requests.get(movie_url, data)
            try:
                js = req.json()
                if js['original_language'] in languege.values():
                    continue
                else:
                    languege[count] = js['original_language']
                    InsertQueries.InsertToLang(connectionObject,count, js["original_language"])
                    count+=1
                langId = InsertQueries.get_key(languege, js['original_language'])
                movie = Movie(js["adult"], js["belongs_to_collection"], js["budget"]
                              , js["genres"], js["homepage"], js["id"], js["imdb_id"],
                              langId, js["original_title"], js["overview"], js["popularity"]
                              , js["release_date"], js["revenue"]
                              , js["runtime"], js["spoken_languages"]
                              , js["status"], js["vote_count"], js["vote_average"])
                InsertQueries.InsertMovies(connectionObject, movie)
                InsertQueries.insertOverview(connectionObject, js["id"], js["overview"])
                for e in js["genres"]:
                    if e["id"] in genres:
                        continue
                    else:
                        genres[e["id"]] = e["name"]
                        InsertQueries.insertGenres(connectionObject, e["id"], e["name"])
                    InsertQueries.insertMovieGenere(connectionObject, e["id"], js["id"])
                for l in js["spoken_languages"]:
                    InsertQueries.insertShowSpokenLang(connectionObject, l["iso_639_1"], js["id"])
            except Exception as e:
                print("Exeception occured:{}".format(e))
                continue
def fetch_TV_Show():

    url = "https://api.themoviedb.org/3/discover/tv"
    shows = []
    connectionObject = pymysql.connect(host="127.0.0.1", user="DbMysql03", password="DbMysql03", db="DbMysql03",
                                       port=3305)
    cursorObject = connectionObject.cursor()
    sqlQuery = "SELECT * FROM Genre"
    cursorObject.execute(sqlQuery)
    rows = cursorObject.fetchall()
    lang = {}
    genres={}

    for row in rows:
        genres[row[0]] = row[1]
    producer={}
    for i in range(1, 500):
        print("Start page ", i)
        data = {'api_key': 'd005091db9214b502565db95dea43fc7',
                'page': str(i)}
        req = requests.get(url, data)
        show_list = req.json()['results']
        for show in show_list:
            movie_url = f"https://api.themoviedb.org/3/tv/{show['id']}"
            data = {'api_key': 'd005091db9214b502565db95dea43fc7'}
            req = requests.get(movie_url, data)
            try :
                js = req.json()
                show = Show(js["genres"], js["homepage"], js["id"]
                            , js["original_language"], js["name"], js["overview"], js["popularity"]
                            , js["first_air_date"], (js["episode_run_time"])[0], js["spoken_languages"]
                            , js["status"], js["vote_count"], js["vote_average"], js["seasons"], (js["last_episode_to_air"]),
                            (js["next_episode_to_air"]), js["created_by"])
                InsertQueries.InsertShow(connectionObject, show)
                InsertQueries.insertShowOverview(connectionObject, js["id"], js["overview"])
                for e in js["genres"]:
                    if e["id"] in genres:
                        pass
                    else:
                        genres[e["id"]] = e["name"]
                        InsertQueries.insertGenres(connectionObject, e["id"], e["name"])
                    InsertQueries.insertShowGenere(connectionObject, e["id"], js["id"])
                for l in js["spoken_languages"]:
                    InsertQueries.insertShowSpokenLang(connectionObject, l["iso_639_1"], js["id"])
                for c in js["created_by"]:
                    if c["id"] in producer:
                        pass
                    else:
                        producer["id"] = c["name"]
                        InsertQueries.insertProducers(connectionObject, c["id"], c["name"])
                    InsertQueries.insertProducersShow(connectionObject, c["id"], js["id"])





            except Exception as e:
                print("Exeception occured:{}".format(e))
def fetch_movie_from_csv():
    connectionObject = pymysql.connect(host="127.0.0.1", user="DbMysql03", password="DbMysql03", db="DbMysql03",
                                       port=3305)
    cursorObject = connectionObject.cursor()
    sqlQuery = "SELECT * FROM Language"
    cursorObject.execute(sqlQuery)
    rows = cursorObject.fetchall()
    lang = {}
    for row in rows:
        lang[row[0]] = row[1]
    count=0
    sqlQuery = "SELECT * FROM Genre"
    cursorObject.execute(sqlQuery)
    rows = cursorObject.fetchall()
    genres = {}

    for row in rows:
        genres[row[0]] = row[1]
    with open('movies_metadata.csv', 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        while (count < 5000):
            try:
                 for row in reader:
                    langid = InsertQueries.get_key(lang, row["original_language"])
                    if (langid == None):
                        cursorObject = connectionObject.cursor()
                        sqlQuery = "INSERT INTO Language (languageId,languageName) VALUES (%s,%s)"
                        langId = max(lang) + 1
                        values = (langId, row["original_language"])
                        lang[langId] = row["original_language"]
                        cursorObject.execute(sqlQuery, values)
                        connectionObject.commit()

                    adult=0
                    if row["adult"]=="true":
                        adult=1
                    if row["belongs_to_collection"]!="":
                        collection = eval(row["belongs_to_collection"])
                    else:
                        collection=None
                    movie = Movie(adult,collection , int(row["budget"])
                                  , row["genres"], row["homepage"], row["id"], row["imdb_id"],
                                  langid, row["original_title"],row["overview"],float(row["popularity"])
                                  , row["release_date"], int(row["revenue"])
                                  , int(float(row["runtime"])), eval(row["spoken_languages"])
                                  , row["status"],int(row["vote_count"]),float(row["vote_average"]))
                    InsertQueries.InsertMovies(connectionObject, movie)
                    InsertQueries.insertOverview(connectionObject, row["id"], row["overview"])
                    js = eval(row["genres"])
                    for r in js:
                        if r["id"] in genres:
                            pass
                        else:
                            genres[e["id"]] = e["name"]
                            InsertQueries.insertGenres(connectionObject, e["id"], e["name"])
                        InsertQueries.insertMovieGenere(connectionObject, r["id"], row["id"])
                    js = eval(row["spoken_languages"])
                    for l in js:
                        langid = InsertQueries.get_key(lang, l["iso_639_1"])
                        if (langid == None):
                            cursorObject = connectionObject.cursor()
                            sqlQuery = "INSERT INTO Language (languageId,languageName) VALUES (%s,%s)"
                            langId = max(lang) + 1
                            values = (langId, row["original_language"])
                            lang[langId] = row["original_language"]
                            cursorObject.execute(sqlQuery, values)
                            connectionObject.commit()
                        InsertQueries.insertMovieSpokenLang(connectionObject, langid, row["id"])
                    count+=1
            except Exception as e:
                        print("Exeception occured:{}".format(e))
def fetch_Credits_TV_shows():
    # fetch actors of tv-shows, using credits
    connectionObject = pymysql.connect(host="127.0.0.1", user="DbMysql03", password="DbMysql03", db="DbMysql03",
                                       port=3305)
    url = "https://api.themoviedb.org/3/discover/tv"

    cursorObject = connectionObject.cursor()

    sqlQuery = "SELECT * FROM Actors"
    cursorObject.execute(sqlQuery)
    rows = cursorObject.fetchall()
    actors = {}
    for row in rows:
        actors[row[0]] = row[1]
    for i in range(1, 501):
        print("Start page ", i)
        data = {'api_key': 'd005091db9214b502565db95dea43fc7', 'page': str(i)}
        req = requests.get(url, data)
        tv_list = req.json()['results']
        for tv in tv_list:
            tv_url = f"https://api.themoviedb.org/3/tv/{tv['id']}/credits?api_key=d005091db9214b502565db95dea43fc7"
            req = requests.get(tv_url, data)
            try:
                js = req.json()
                for a in js["cast"]:
                    if a["known_for_department"] == "Acting":
                        if a["id"] in actors:
                            pass
                        else:
                            actors[a["id"]] = a["name"]
                            InsertQueries.insertActors(connectionObject, a["id"], a["name"], a["gender"])
                        InsertQueries.InsertShowActors(connectionObject, js["id"], a["id"])


            except Exception as e:
                print("Exeception occured:{}".format(e))
def fetch_Credits_movies():
    #fetch actors of moving, using credits
    connectionObject = pymysql.connect(host="127.0.0.1", user="DbMysql03", password="DbMysql03", db="DbMysql03",
                                       port=3305)
    url = "https://api.themoviedb.org/3/discover/movie"
    actors = {}
    directors={}
    for i in range(1, 501):
        data = {'api_key': 'd005091db9214b502565db95dea43fc7',
                'page': str(i)}
        req = requests.get(url, data)
        movie_list = req.json()['results']
        for movie in movie_list:
            movie_url = f"https://api.themoviedb.org/3/movie/{movie['id']}/credits?api_key=d005091db9214b502565db95dea43fc7"
            # data = {'api_key': 'd005091db9214b502565db95dea43fc7'}
            req = requests.get(movie_url, data)
            try:
                js = req.json()
                for e in js["cast"]:
                    if e["known_for_department"] == "Acting":
                        if e["id"] in actors:
                            continue
                        else:
                            actors[e["id"]] = (e["name"], e["gender"])
                            InsertQueries.insertActors(connectionObject, e["id"], e["name"], e["gender"])
                        InsertQueries.insertMovieActor(connectionObject, e["id"], js["id"])
                for e in js["crew"]:
                    if e["known_for_department"] == "Directing":
                        if e["job"] == "Director":
                            if e["id"] in directors:
                                pass
                            else:
                                directors[e["id"]] = e["name"]
                                InsertQueries.insertDirectors(connectionObject, e["id"], e["name"])
                            InsertQueries.insertMovieDirector(connectionObject, e["id"], js["id"])
            except Exception as e:
                print("Exeception occured:{}".format(e))



def fetch_image():
    # Fetch data for movies from api
    connectionObject = pymysql.connect(host="127.0.0.1", user="DbMysql03", password="DbMysql03", db="DbMysql03",
                                       port=3305)
    cursorObject = connectionObject.cursor()
    sqlQuery = "SELECT t1.apiId FROM Movie t1 LEFT JOIN PosterMovie t2 ON t2.apiId = t1.apiId WHERE t2.apiId IS NULL"
    cursorObject.execute(sqlQuery)
    rows = cursorObject.fetchall()
    movies = {}
    for row in rows:
        movies[row[0]] = row[0]

    for movie in movies:
        movie_url = f"https://api.themoviedb.org/3/movie/{movie}"
        data = {'api_key': 'd005091db9214b502565db95dea43fc7'}
        req = requests.get(movie_url, data)
        try:
            js = req.json()
            id = js['id']
            poster = js['poster_path']
            InsertQueries.insertPosterMovie(connectionObject, id ,poster)

        except Exception as e:
            print("Exeception occured:{}".format(e))
            InsertQueries.insertPosterMovie(connectionObject, movie ,None)

            continue


def fetch_showimage():
    # Fetch data for movies from api
    connectionObject = pymysql.connect(host="127.0.0.1", user="DbMysql03", password="DbMysql03", db="DbMysql03",
                                       port=3305)
    cursorObject = connectionObject.cursor()
    sqlQuery = "SELECT t1.apiId FROM Shows t1 LEFT JOIN PosterShow t2 ON t2.apiId = t1.apiId WHERE t2.apiId IS NULL"
    cursorObject.execute(sqlQuery)
    rows = cursorObject.fetchall()
    shows = {}
    for row in rows:
        shows[row[0]] = row[0]

    for show in shows:
        show_url = f"https://api.themoviedb.org/3/tv/{show}"
        data = {'api_key': 'd005091db9214b502565db95dea43fc7'}
        req = requests.get(show_url, data)
        try:
            js = req.json()
            id = js['id']
            poster = js['poster_path']
            InsertQueries.insertPosterShows(connectionObject, id ,poster)

        except Exception as e:
            print("Exeception occured:{}".format(e))
            InsertQueries.insertPosterShows(connectionObject, show ,None)
            continue
def fetch_Data():
    pass
    #fetch_movie()
    #fetch_Credits_movies()
    #fetch_Credits_TV_shows()
    #fetch_TV_Show()
    #fetch_Credits_TV_shows()














