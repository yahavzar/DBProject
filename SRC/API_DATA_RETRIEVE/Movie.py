from SRC.API_DATA_RETRIEVE.Media import Media



class Movie(Media):
  def printMovie(self):
    pass
  def __init__(self, adult, collection, budget, genre, homepage, api_id, imdb_id, original_language, title, overview,
               popularity, release_date, revenue, runtime, spoken_languages, status, vote_count, vote_avg):
      super().__init__( genre, homepage, api_id, original_language, title, overview,
               popularity, release_date, runtime, spoken_languages, status, vote_count, vote_avg)
      self.adult = adult
      if (collection!= None):
        self.collection = collection['name']
      else:
        self.collection = None
      self.budget = budget
      self.imdb_id = imdb_id
      self.revenue = revenue



