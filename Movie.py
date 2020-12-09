class Movie:
  def printMovie(self):
    print("hello i am movie")

  def __init__(self):
    return

  def __init__(self, adult):
      print("HERE")
      self.adult = adult

  def __init__(self, adult, collection, budget, genre, homepage, api_id, imdb_id, original_language, title, overview,
               popularity, release_date, revenue, runtime, spoken_languages, status, vote_count, vote_avg):
      print("constructor")
      self.adult = adult
      self.collection = collection
      self.budget = budget
      self.genre = genre
      self.homepage = homepage
      self.api_id = api_id
      self.imdb_id = imdb_id
      self.original_language = original_language
      self.title = title
      self.overview = overview
      self.popularity = popularity
      self.release_date = release_date
      self.revenue = revenue
      self.runtime = runtime
      self.spoken_languages = spoken_languages
      self.status = status
      self.vote_count = vote_count
      self.vote_avg = vote_avg


  def __repr__(self):
    print(self.adult, "\n",
          self.collection, "\n",
          self.budget, "\n",
          self.genre, "\n",
          self.homepage, "\n",
          self.api_id, "\n",
          self.imdb_id, "\n",
          self.original_language, "\n",
          self.title, "\n",
          self.overview, "\n",
          self.popularity, "\n",
          self.release_date, "\n",
          self.revenue, "\n",
          self.runtime, "\n",
          self.spoken_languages, "\n",
          self.status, "\n",
          self.vote_count, "\n",
          self.vote_avg, "\n")


def printMovie(param):
  return None