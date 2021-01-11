
def moviesInGenre(connectionObject):
    genreName = input("Enter the genere: ")
    cursorObject = connectionObject.cursor()
    sqlQuery = '''SELECT Movie.title, Movie.popularity FROM Movie, Genre, MoviesGenre WHERE Movie.apiId=MoviesGenre.apiId and MoviesGenre.genreId=Genre.genreId and Genre.genreName="%s" GROUP BY Movie.title''' %(genreName)
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


