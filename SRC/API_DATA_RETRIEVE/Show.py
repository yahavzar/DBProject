from SRC.API_DATA_RETRIEVE.Media import  *
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


