class Show:
  def __init__(self,creator,api_id,name,runtime,language):
    self.creator=creator
    self.api_id=api_id
    self.name=name
    self.runtime=runtime
    self.language=language


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
