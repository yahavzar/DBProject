class Movie:
  def printMovie(self):
    pass
  def __init__(self, adult, collection, budget, genre, homepage, api_id, imdb_id, original_language, title, overview,
               popularity, release_date, revenue, runtime, spoken_languages, status, vote_count, vote_avg):
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
    x = str(self.adult) + "\n" + \
        str(self.collection) + "\n" + \
        str(self.budget) + "\n" + \
        str(self.genre) + "\n" + \
        str(self.homepage) + "\n" + \
        str(self.api_id) + "\n" + \
        str(self.imdb_id) + "\n" + \
        str(self.original_language) + "\n" + \
        str(self.title) + "\n" + \
        str(self.overview) + "\n" + \
        str(self.popularity) + "\n" + \
        str(self.release_date) + "\n" + \
        str(self.revenue) + "\n" + \
        str(self.runtime) + "\n" + \
        str(self.spoken_languages) + "\n" + \
        str(self.status) + "\n" + \
        str(self.vote_count) + "\n" + \
        str(self.vote_avg) + "\n"
    return x


def printMovie(param):
  return None