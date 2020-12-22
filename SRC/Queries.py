def moviesWithActor(connectionObject):
    actorName = input("Enter actor's name: ")
    cursorObject = connectionObject.cursor()
    sqlQuery = '''SELECT Movie.title, Actors.actorName From Actors, ActorsMovie, Movie Where Actors.actorName = "%s" and Actors.actorId=ActorsMovie.actorId and ActorsMovie.filmId=Movie.apiId GROUP BY Movie.title''' %(actorName)
    cursorObject.execute(sqlQuery)
    rows = cursorObject.fetchall()
    for row in rows:
        print(row[0]+"\n")
    return rows

def moviesInLanguage(connectionObject):
    langName = input("Enter the language's name (In shortened form): ")
    cursorObject = connectionObject.cursor()
    sqlQuery = '''SELECT Movie.title, Language.languageName FROM Movie, Language WHERE Movie.langId=Language.languageId and Language.languageName="%s" GROUP BY Movie.title''' %(langName)
    cursorObject.execute(sqlQuery)
    rows = cursorObject.fetchall()
    for row in rows:
        print(row[1]+"\n")

def moviesInGenre(connectionObject):
    genreName = input("Enter the genere: ")
    cursorObject = connectionObject.cursor()
    sqlQuery = '''SELECT Movie.title, Genre.genreName FROM Movie, Genre, MoviesGenre WHERE Movie.apiId=MoviesGenre.apiId and MoviesGenre.genreId=Genre.genreId and Genre.genreName="%s" GROUP BY Movie.title''' %(genreName)
    cursorObject.execute(sqlQuery)
    rows = cursorObject.fetchall()
    for row in rows:
        print(row[1]+"\n")

def movieInGenreAboveRating(connectionObject):
    genreName = input("Enter the genere: ")
    rating = input("Enter the desired rating: ")
    cursorObject = connectionObject.cursor()
    sqlQuery = '''SELECT Movie.title, Genre.genreName, Movie.voteAvg  FROM Movie, Genre, MoviesGenre WHERE Movie.apiId=MoviesGenre.apiId and MoviesGenre.genreId=Genre.genreId and Genre.genreName="%s" and Movie.voteAvg > "%f" GROUP BY Movie.title''' %(genreName,rating)
    cursorObject.execute(sqlQuery)
    rows = cursorObject.fetchall()
    for row in rows:
        print(row[1]+"\n")

def showsWithStatus(connectionObject):
    status = input("Enter the status (Ended, Canceled, Returning Series, In Production): ")
    cursorObject = connectionObject.cursor()
    sqlQuery = '''SELECT Shows.title, Shows.status FROM Shows WHERE Shows.status="%s" GROUP BY Shows.title''' %(status)
    cursorObject.execute(sqlQuery)
    rows = cursorObject.fetchall()
    for row in rows:
        print(row[1]+"\n")

def moviesInYears(connectionObject):
    firstYear = input("Enter the earlies year (In yyyy format): ")
    lastYear = input("Enter the earlies year (In yyyy format): ")
    cursorObject = connectionObject.cursor()
    sqlQuery = '''SELECT Movie.title, Movie.releaseDay FROM Movie WHERE Movie.releaseDay BETWEEN "%d-01-01" AND "%d-01-01" AND Movie.releaseDay != "%d-01-01" GROUP BY Movie.title''' %(firstYear,lastYear,lastYear)
    cursorObject.execute(sqlQuery)
    rows = cursorObject.fetchall()
    for row in rows:
        print(row[1] + "\n")

def moviesRelseadInNMonths(connectionObject):
    months = input("Enter the number of months: ")
    cursorObject = connectionObject.cursor()
    sqlQuery = '''SELECT Movie.title, Movie.releaseDay FROM Movie WHERE Movie.releaseDay >= DATE_ADD(NOW(), INTERVAL %d MONTH) GROUP BY Movie.title''' %(months)
    cursorObject.execute(sqlQuery)
    rows = cursorObject.fetchall()
    for row in rows:
        print(row[1] + "\n")

def showsWithNSeasons(connectionObject):
    seasons = input("Enter the number of seasons: ")
    cursorObject = connectionObject.cursor()
    sqlQuery = '''SELECT Shows.title, Shows.seasons FROM Shows WHERE Shows.seasons>= %d GROUP BY Shows.title''' %(seasons)
    cursorObject.execute(sqlQuery)
    rows = cursorObject.fetchall()
    for row in rows:
        print(row[1] + "\n")

def showsWithLength(connectionObject):
    length = input("Enter show length: ")
    cursorObject = connectionObject.cursor()
    sqlQuery = '''SELECT Shows.title, Shows.length FROM Shows WHERE Shows.length>= %d GROUP BY Shows.title''' %(length)
    cursorObject.execute(sqlQuery)
    rows = cursorObject.fetchall()
    for row in rows:
        print(row[1] + "\n")

def actorsInShowsWithStatus(connectionObject):
    status = input("Enter the status (Ended, Canceled, Returning Series, In Production): ")
    cursorObject = connectionObject.cursor()
    sqlQuery = '''SELECT Actors.actorName FROM Actors, Shows, ActorsShow WHERE Actors.actorId=ActorsShow.actorId AND ActorsShow.showId=Shows.apiId AND Shows.status="%s" GROUP BY Actors.actorName''' %(status)
    cursorObject.execute(sqlQuery)
    rows = cursorObject.fetchall()
    for row in rows:
        print(row[1] + "\n")

def movieToOverview(connectionObject):
    title = input("Enter the movie's title: ")
    cursorObject = connectionObject.cursor()
    sqlQuery = '''SELECT Movie.title, MovieOverview.overview FROM Movie, MovieOverview WHERE Movie.apiId=MovieOverview.filmId AND Movie.title="%s" GROUP BY Movie.title''' %(title)
    cursorObject.execute(sqlQuery)
    rows = cursorObject.fetchall()
    for row in rows:
        print(row[1] + "\n")

def showToOverview(connectionObject):
    title = input("Enter the show's title: ")
    cursorObject = connectionObject.cursor()
    sqlQuery = '''SELECT Shows.title, ShowOverview.overview FROM Shows, ShowOverview WHERE Shows.apiId=ShowOverview.showId AND Shows.title="%s" GROUP BY Shows.title''' %(title)
    cursorObject.execute(sqlQuery)
    rows = cursorObject.fetchall()
    for row in rows:
        print(row[1] + "\n")

def movieHomepage(connectionObject):
    title = input("Enter the movie's title: ")
    cursorObject = connectionObject.cursor()
    sqlQuery = '''SELECT Movie.title, Movie.homePage FROM Movie WHERE Movie.title="%s" GROUP BY Movie.title''' %(title)
    cursorObject.execute(sqlQuery)
    rows = cursorObject.fetchall()
    for row in rows:
        print(row[1] + "\n")

def movieReleaseDate(connectionObject):
    date = input("Entre the date in a (yyyy-mm-dd format): ")
    cursorObject = connectionObject.cursor()
    sqlQuery = '''SELECT Movie.title, Movie.releaseDay FROM Movie WHERE Movie.releaseDay="%s" GROUP BY Movie.title''' %(date)
    cursorObject.execute(sqlQuery)
    rows = cursorObject.fetchall()
    for row in rows:
        print(row[1] + "\n")




# def moviesWithActors(connectionObject):
#     cursorObject = connectionObject.cursor()
#     actors = input("Enter names of actors, separated by a comma: ")
#     actors = actors.split(",")
#     for a in actors:

