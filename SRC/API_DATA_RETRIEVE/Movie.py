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


  # def __repr__(self):
  #   x = str(self.adult) + "\n" + \
  #       str(self.collection) + "\n" + \
  #       str(self.budget) + "\n" + \
  #       str(self.genre) + "\n" + \
  #       str(self.homepage) + "\n" + \
  #       str(self.api_id) + "\n" + \
  #       str(self.imdb_id) + "\n" + \
  #       str(self.original_language) + "\n" + \
  #       str(self.title) + "\n" + \
  #       str(self.overview) + "\n" + \
  #       str(self.popularity) + "\n" + \
  #       str(self.release_date) + "\n" + \
  #       str(self.revenue) + "\n" + \
  #       str(self.runtime) + "\n" + \
  #       str(self.spoken_languages) + "\n" + \
  #       str(self.status) + "\n" + \
  #       str(self.vote_count) + "\n" + \
  #       str(self.vote_avg) + "\n"
  #   return x


def printMovie(param):
  return None