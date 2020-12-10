import urllib
import urllib.parse
import urllib.request
import json
from Movie import Movie
import requests

def fetch_movie:
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
            js = req.json()
            movie = Movie(js["adult"], js["belongs_to_collection"], js["budget"], js["genres"], js["homepage"],
                          js["id"], js["imdb_id"], js["original_title"]
                          , js["original_language"], js["overview"], js["popularity"], js["release_date"],
                          js["revenue"], js["runtime"],
                          js["spoken_languages"], js["status"], js["vote_count"], js["vote_average"])
            movies.append(movie)

def fetch_TV_Show:
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
            js = req.json()
            movie = Movie(js["adult"], js["belongs_to_collection"], js["budget"], js["genres"], js["homepage"],
                          js["id"], js["imdb_id"], js["original_title"]
                          , js["original_language"], js["overview"], js["popularity"], js["release_date"],
                          js["revenue"], js["runtime"],
                          js["spoken_languages"], js["status"], js["vote_count"], js["vote_average"])
            movies.append(movie)

def main():
      fetch_movie()
      fetch_TV_Show()
      print("hi")


if __name__ == "__main__":
    main()
