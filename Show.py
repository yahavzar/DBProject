from Media import  *
class Show(Media):
  def __init__(self, genre, homepage, api_id, original_language, title, overview,
               popularity, release_date, runtime, spoken_languages, status, vote_count, vote_avg,seasons,last_episode,next_episode,creators):
    super().__init__(genre, homepage, api_id, original_language, title, overview,
                       popularity, release_date, runtime, spoken_languages, status, vote_count, vote_avg)

    if (len(seasons)==0):
      self.seasons=None
    self.seasons=seasons[len(seasons)-1]["season_number"]
    if last_episode!=None:
      self.last_episode=last_episode["id"]
    else:
      self.last_episode =None
    if next_episode!=None:
      self.next_episode=next_episode["id"]
    else:
      self.next_episode=None
    self.creators=creators



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
