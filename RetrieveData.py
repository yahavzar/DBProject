import urllib
import urllib.parse
import urllib.request
import json
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
            try :
                js = req.json()
                movie=Movie(js["adult"], js["belongs_to_collection"], js["budget"]
                            , js["genres"] ,js["homepage"], js["id"], js["imdb_id"],
                 js["original_language"],js["original_title"], js["overview"], js["popularity"]
                            , js["release_date"], js["revenue"]
                , js["runtime"], js["spoken_languages"]
                , js["status"], js["vote_count"], js["vote_average"])
                movies.append(movie)
            except Exception as e:
                print("Exeception occured:{}".format(e))
                continue
    return  movies

def fetch_TV_Show():
    url = "https://api.themoviedb.org/3/discover/tv"
    shows = []
    for i in range(1, 2):
        data = {'api_key': 'd005091db9214b502565db95dea43fc7',
                'page': str(i)}
        req = requests.get(url, data)
        show_list = req.json()['results']
        for show in show_list:
            movie_url = f"https://api.themoviedb.org/3/tv/{show['id']}"
            data = {'api_key': 'd005091db9214b502565db95dea43fc7'}
            req = requests.get(movie_url, data)
            js = req.json()
            show = Show(js["genres"], js["homepage"],js["id"]
            ,js["original_language"],js["name"], js["overview"], js["popularity"]
                , js["first_air_date"],js["episode_run_time"],js["spoken_languages"]
                ,js["status"], js["vote_count"], js["vote_average"],js["seasons"],js["last_episode_to_air"],js["next_episode_to_air"],js["created_by"])
            shows.append(show)
    return shows

def main():
      movies=fetch_movie()
      shows =fetch_TV_Show()
      print("hi")


if __name__ == "__main__":
    main()
