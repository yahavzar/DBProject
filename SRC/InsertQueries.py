


def get_key(dict, val):
    for key, value in dict.items():
         if val == value:
             return key
    return None

def InsertMovies(connectionObject,movie):
            cursorObject = connectionObject.cursor()
            sqlQueryMovie = "INSERT INTO Movie (apiId,title,langId,releaseDay,length,budget,revenue,collection,imdbId,homePage,status,popularity,voteCount,voteAvg,adult) VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            values = (movie.api_id, movie.title, movie.original_language, movie.release_date, movie.runtime, movie.budget, movie.revenue,
                      movie.collection, movie.imdb_id, movie.homepage, movie.status, movie.popularity, movie.vote_count,
                      movie.vote_avg, movie.adult)
            cursorObject.execute(sqlQueryMovie, values)
            connectionObject.commit()
def InsertShowActors(connectionObject, showId, actorId):
    cursorObject = connectionObject.cursor()
    sqlQuery = "INSERT INTO ActorsShow (actorId, showId) VALUES (%s,%s)"
    values = (actorId, showId)
    cursorObject.execute(sqlQuery, values)
    connectionObject.commit()
def InsertShow(connectionObject,Show):
    cursorObject = connectionObject.cursor()
    sqlQuery = "SELECT * FROM Language"
    cursorObject.execute(sqlQuery)
    rows = cursorObject.fetchall()
    lang = {}
    for row in rows:
        lang[row[0]] = row[1]
    cursorObject = connectionObject.cursor()
    sqlQuery = "INSERT INTO Shows (apiId,title,langId,releaseDay,length,homePage,status,popularity,voteCount,voteAvg,seasons,lastEpisodeId,nextEpisodeId) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    langId = get_key(lang,Show.original_language)
    if (langId==None):
        cursorObject = connectionObject.cursor()
        sqlQuery = "INSERT INTO Language (languageId,languageName) VALUES (%s,%s)"
        langId=max(lang)+1
        values = (langId,Show.original_language)
        lang[langId]=Show.original_language
        cursorObject.execute(sqlQuery, values)
        connectionObject.commit()
    values = (Show.api_id, Show.title,langId,Show.release_date,Show.runtime,Show.homepage,Show.status,Show.popularity,Show.vote_count,Show.vote_avg,Show.seasons,Show.last_episode,Show.next_episode)
    cursorObject.execute(sqlQuery, values)
    connectionObject.commit()
def InsertToLang(connectionObject,langId,langName):
            cursorObject = connectionObject.cursor()
            sqlQuery = "INSERT INTO Language (languageId,languageName) VALUES (%s,%s)"
            values= (langId, langName)
            cursorObject.execute(sqlQuery, values)
            connectionObject.commit()
def insertActors(connectionObject, actor, name, gender):
    cursorObject = connectionObject.cursor()
    sqlQuery = "INSERT INTO Actors (actorId,actorName,gender) VALUES (%s,%s,%s)"
    values = (actor, name, gender)
    cursorObject.execute(sqlQuery, values)
    connectionObject.commit()
def insertDirectors(connectionObject, directorId, directorName):
    cursorObject = connectionObject.cursor()
    sqlQuery = "INSERT INTO Directors (directorId,directorName) VALUES (%s,%s)"
    values = (directorId, directorName)
    cursorObject.execute(sqlQuery, values)
    connectionObject.commit()
def insertProducers(connectionObject, producerId, producerName):
    cursorObject = connectionObject.cursor()
    sqlQuery = "INSERT INTO Producers (producerId,producerName) VALUES (%s,%s)"
    values = (producerId, producerName)
    cursorObject.execute(sqlQuery, values)
    connectionObject.commit()
def insertGenres(connectionObject, id, name):
    cursorObject = connectionObject.cursor()
    sqlQuery = "INSERT INTO Genre (genreId,genreName) VALUES (%s,%s)"
    values = (id, name)
    cursorObject.execute(sqlQuery, values)
    connectionObject.commit()
def insertOverview(connectionObject, id, overview):
    cursorObject = connectionObject.cursor()
    sqlQuery = "INSERT INTO MovieOverview (FilmId,overview) VALUES (%s,%s)"
    values = (id, overview)
    cursorObject.execute(sqlQuery, values)
    connectionObject.commit()
def insertShowOverview(connectionObject, id, overview):
    cursorObject = connectionObject.cursor()
    sqlQuery = "INSERT INTO ShowOverview (showId,overview) VALUES (%s,%s)"
    values = (id, overview)
    cursorObject.execute(sqlQuery, values)
    connectionObject.commit()
def insertMovieGenere(connectionObject,genreId,apiId):
    cursorObject = connectionObject.cursor()
    sqlQuery = "INSERT INTO MoviesGenre (genreId,apiId) VALUES (%s,%s)"
    values = (genreId,apiId)
    cursorObject.execute(sqlQuery, values)
    connectionObject.commit()
def insertShowGenere(connectionObject,genreId,apiId):
    cursorObject = connectionObject.cursor()
    sqlQuery = "INSERT INTO ShowGenre (genreId,apiId) VALUES (%s,%s)"
    values = (genreId,apiId)
    cursorObject.execute(sqlQuery, values)
    connectionObject.commit()
def insertMovieSpokenLang(connectionObject, languageId, movieId):

    cursorObject = connectionObject.cursor()
    sqlQuery = "INSERT INTO LanguageMovie (languageId,movieId) VALUES (%s,%s)"
    values = (languageId, movieId)
    cursorObject.execute(sqlQuery, values)
    connectionObject.commit()
def insertShowSpokenLang(connectionObject, languageId, showId):
    cursorObject = connectionObject.cursor()
    sqlQuery = "SELECT * FROM Language"
    cursorObject.execute(sqlQuery)
    rows = cursorObject.fetchall()
    lang = {}
    for row in rows:
        lang[row[0]] = row[1]
    langId = get_key(lang, languageId)
    if (langId == None):
        cursorObject = connectionObject.cursor()
        sqlQuery = "INSERT INTO Language (languageId,languageName) VALUES (%s,%s)"
        langId = max(lang) + 1
        values = (langId, languageId)
        lang[langId] = languageId
        cursorObject.execute(sqlQuery, values)
        connectionObject.commit()
    cursorObject = connectionObject.cursor()
    sqlQuery = "INSERT INTO LanguageShow (languageId,showId) VALUES (%s,%s)"
    values = (langId, showId)
    cursorObject.execute(sqlQuery, values)
    connectionObject.commit()
def insertMovieActor(connectionObject,actorId,filmId):
    cursorObject = connectionObject.cursor()
    sqlQuery = "INSERT INTO ActorsMovie (actorId,filmId) VALUES (%s,%s)"
    values = (actorId,filmId)
    cursorObject.execute(sqlQuery, values)
    connectionObject.commit()
def insertMovieDirector(connectionObject,directorId,filmId):
    cursorObject = connectionObject.cursor()
    sqlQuery = "INSERT INTO DirectorsMovie  (directorId,filmId) VALUES (%s,%s)"
    values = (directorId,filmId)
    cursorObject.execute(sqlQuery, values)
    connectionObject.commit()
def insertProducersShow(connectionObject,producerId,showId):
    cursorObject = connectionObject.cursor()
    sqlQuery = "INSERT INTO ProducersShow  (producerId,showId) VALUES (%s,%s)"
    values = (producerId,showId)
    cursorObject.execute(sqlQuery, values)
    connectionObject.commit()



