import urllib
import urllib.parse
import urllib.request
import json

import pymysql

import CreateTables
from Movie import Movie
from Show import Show
import requests


def fetch_movie():
    url = "https://api.themoviedb.org/3/discover/movie"
    movies = []
    for i in range(1, 501):
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
                movie = Movie(js["adult"], js["belongs_to_collection"], js["budget"]
                              , js["genres"], js["homepage"], js["id"], js["imdb_id"],
                              js["original_language"], js["original_title"], js["overview"], js["popularity"]
                              , js["release_date"], js["revenue"]
                              , js["runtime"], js["spoken_languages"]
                              , js["status"], js["vote_count"], js["vote_average"])
                movies.append(movie)
            except Exception as e:
                print("Exeception occured:{}".format(e))
                continue
    return movies


def fetch_TV_Show():
    connectionObject = pymysql.connect(host="127.0.0.1", user="DbMysql03", password="DbMysql03", db="DbMysql03",
                                       port=3305)
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

    lang = {}
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
                CreateTables.InsertShow(connectionObject,show)
                CreateTables.insertShowOverview(connectionObject,js["id"],js["overview"])
                for e in js["genres"]:
                    if e["id"] in genres:
                        pass
                    else:
                        genres[e["id"]] = e["name"]
                        CreateTables.insertGenres(connectionObject, e["id"], e["name"])
                    CreateTables.insertShowGenere(connectionObject,e["id"],js["id"])
                for l in js["spoken_languages"]:
                    CreateTables.insertShowSpokenLang(connectionObject,  l["iso_639_1"], js["id"])
                for c in js["created_by"]:
                    if c["id"] in producer:
                        CreateTables.insertProducersShow(connectionObject,c["id"],js["id"])
                    else:
                        producer["id"] = c["name"]
                        CreateTables.insertProducers(connectionObject,c["id"],c["name"])
                        CreateTables.insertProducersShow(connectionObject,c["id"],js["id"])




            except Exception as e:
                print("Exeception occured:{}".format(e))


def fetchLanguage():
    url = "https://api.themoviedb.org/3/discover/movie"
    languege = {}
    count = 1
    for i in range(1, 501):
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
                    count += 1
            except Exception as e:
                print("Exeception occured:{}".format(e))
    return languege


def fetchActors():
    connectionObject = pymysql.connect(host="127.0.0.1", user="DbMysql03", password="DbMysql03", db="DbMysql03",
                                       port=3305)

    url = "https://api.themoviedb.org/3/discover/movie"
    actors = {}
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
                            CreateTables.insertActors(connectionObject, e["id"], e["name"], e["gender"])


            except Exception as e:
                print("Exeception occured:{}".format(e))


def fetchCreditsActors():
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
    for i in range(2,501):
        print("Start page ", i)
        data = {'api_key': 'd005091db9214b502565db95dea43fc7','page': str(i)}
        req = requests.get(url, data)
        tv_list = req.json()['results']
        for tv in tv_list:
            tv_url = f"https://api.themoviedb.org/3/movie/{tv['id']}/credits?api_key=d005091db9214b502565db95dea43fc7"
            req = requests.get(tv_url, data)
            try:
                js = req.json()
                for a in js["cast"]:
                    if a["known_for_department"] == "Acting":
                        if a["id"] in actors:
                            pass
                        else:
                            actors[a["id"]] = a["name"]
                            CreateTables.insertActors(connectionObject, a["id"],a["name"],a["gender"])
                        CreateTables.InsertShowActors(connectionObject, js["id"], a["id"])

            except Exception as e:
                print("Exeception occured:{}".format(e))

def fetchGenreOverview():
    connectionObject = pymysql.connect(host="127.0.0.1", user="DbMysql03", password="DbMysql03", db="DbMysql03",
                                       port=3305)
    url = "https://api.themoviedb.org/3/discover/movie"
    genres = {}
    for i in range(110, 501):
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
                for e in js["genres"]:
                    if e["id"] in genres:
                        continue
                    else:
                        genres[e["id"]] = e["name"]
                        CreateTables.insertGenres(connectionObject, e["id"], e["name"])

                CreateTables.insertOverview(connectionObject, js["id"], js["overview"])

            except Exception as e:
                print("Exeception occured:{}".format(e))


def fetchDirectors():
    connectionObject = pymysql.connect(host="127.0.0.1", user="DbMysql03", password="DbMysql03", db="DbMysql03",
                                       port=3305)
    url = "https://api.themoviedb.org/3/discover/movie"
    directors = {}
    for i in range(1, 501):
        print("Start page ", i)
        data = {'api_key': 'd005091db9214b502565db95dea43fc7', 'page': str(i)}
        req = requests.get(url, data)
        movie_list = req.json()['results']
        for movie in movie_list:
            movie_url = f"https://api.themoviedb.org/3/movie/{movie['id']}/credits?api_key=d005091db9214b502565db95dea43fc7"
            # data = {'api_key': 'd005091db9214b502565db95dea43fc7'}
            req = requests.get(movie_url, data)
            try:
                js = req.json()
                for e in js["crew"]:
                    if e["known_for_department"] == "Directing":
                        if e["job"] == "Director":
                            if e["id"] in directors:
                                continue
                            else:
                                directors[e["id"]] = e["name"]
                                CreateTables.insertDirectors(connectionObject, e["id"], e["name"])


            except Exception as e:
                print("Exeception occured:{}".format(e))


def fetchGenreSpokenlang():
    connectionObject = pymysql.connect(host="127.0.0.1", user="DbMysql03", password="DbMysql03", db="DbMysql03",
                                       port=3305)
    cursorObject = connectionObject.cursor()
    sqlQuery = "SELECT * FROM Language"
    cursorObject.execute(sqlQuery)
    rows = cursorObject.fetchall()
    lang = {}
    for row in rows:
        lang[row[0]] = row[1]
    url = "https://api.themoviedb.org/3/discover/movie"
    for i in range(193, 501):
        print("Start page ", i)
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
                for e in js["genres"]:
                    CreateTables.insertMovieGenere(connectionObject, e["id"], js["id"])
                for l in js["spoken_languages"]:
                    langid = CreateTables.get_key(lang, l["iso_639_1"])
                    CreateTables.insertMovieSpokenLang(connectionObject, langid, js["id"])
            except Exception as e:
                print("Exception occured:{}".format(e))
                continue

def fetchActorDirector():
    connectionObject = pymysql.connect(host="127.0.0.1", user="DbMysql03", password="DbMysql03", db="DbMysql03",
                                       port=3305)
    url = "https://api.themoviedb.org/3/discover/movie"
    for i in range(396, 501):
        print("Start page ", i)
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
                            CreateTables.insertMovieActor(connectionObject, e["id"], js["id"])
                for e in js["crew"]:
                    if e["known_for_department"] == "Directing":
                        if e["job"] == "Director":
                            CreateTables.insertMovieDirector(connectionObject, e["id"], js["id"])


            except Exception as e:
                print("Exeception occured:{}".format(e))

def main():
    movies = fetch_movie()
    shows = fetch_TV_Show()
    print("hi")


if __name__ == "__main__":
    main()
