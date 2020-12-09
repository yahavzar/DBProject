import urllib
import urllib.parse
import urllib.request
import json
import Movie

def main():
    NUM_OF_MOVIES = 1
    start_url = "https://api.themoviedb.org/3/movie/"
    end_url = "?api_key=d005091db9214b502565db95dea43fc7"
    movies = []
    id = 0
    while NUM_OF_MOVIES > 0:
        full_url = start_url + str(id) + end_url
        print(full_url)
        try:
            req = urllib.request.urlopen(full_url).read()
            js = json.loads(req)
            print("adultttt ==== ",js["adult"])
            Movie.printMovie(10)
            movie = Movie.Movie(js["adult"])
            # movie = Movie(js["adult"], js["belongs_to_collection"], js["budget"], js["genres"], js["homepage"], js["id"], js["imdb_id"], js["original_title"]
            #               ,js["original_language"], js["overview"], js["popularity"], js["release_date"], js["revenue"], js["runtime"],
            #               js["spoken_languages"], js["status"], js["vote_count"], js["vote_average"])
            print("here2")
            movies.append(movie)
            print("success")
            NUM_OF_MOVIES -= 1
        except:
            print("failed")
            pass
        id += 1

    print(movies[0])



if __name__ == "__main__":
    main()
