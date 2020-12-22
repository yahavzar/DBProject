import datetime


def popularMovie(connectionObject):
    ## (query 2)
    cursorObject = connectionObject.cursor()
    sqlQuery = "select m1.title, m1.voteAvg, m1.langId" \
               " from Movie m1 ,(select max(m2.voteAvg) as voteAvg, m2.langId from Movie m2 where " \
               "m2.voteCount >= (select avg(voteCount) from Movie m where m.langId = m2.langId)" \
               " group by langId) as something where m1.langId = something.langId and m1.voteAvg = something.voteAvg"
    cursorObject.execute(sqlQuery)
    rows = cursorObject.fetchall()
    for row in rows:
        print(row[0]+"\t"+row[1]+"\t"+row[2])
    return rows

def winning_combination(connectionObject):
    ## (query 4)
    cursorObject = connectionObject.cursor()
    sqlQuery = "select a.actorName,d.directorName, count(*) from Actors a, ActorsMovie am" \
               ",Directors d,DirectorsMovie dm , Movie m where a.actorId= am.actorId and " \
               "d.directorId=dm.directorId and am.filmId=dm.filmId and m.apiId=am.filmId " \
               "and m.voteAvg>5 group by a.actorName,d.directorName Having count(*)>7"
    cursorObject.execute(sqlQuery)
    rows = cursorObject.fetchall()
    for row in rows:
        print(row[0]+"\t"+row[1]+"\t"+row[2])
    return rows

def competing_film(connectionObject):
    ## (query 5)
    firstdate=input("enter first release date: ")
    secondate=input("enter second release date: ")
    cursorObject = connectionObject.cursor()
    sqlQuery = "select distinct m1.title from Movie m1,MoviesGenre mg1 , Movie m2, MoviesGenre" \
               " mg2 where m1.releaseDay between %s and %s and m1.apiId=mg1.apiId" \
               " and m2.apiId=mg2.apiId and mg1.genreId=mg2.genreId and m2.langId= m1.langId"
    values = (firstdate,secondate)
    cursorObject.execute(sqlQuery,values)
    rows = cursorObject.fetchall()
    for row in rows:
        print(row[0]+"\n")
    return rows

def competing_film_diff_director(connectionObject):
    ## (query 5.5)
    firstdate=input("enter first release date: ")
    secondate=input("enter second release date: ")
    cursorObject = connectionObject.cursor()
    sqlQuery = "select distinct m1.title from Movie m1,MoviesGenre mg1 , Movie m2, MoviesGenre mg2" \
               " , DirectorsMovie d1, DirectorsMovie d2 where m1.releaseDay between  %s and" \
               "  %s and m1.apiId=mg1.apiId and m2.apiId=mg2.apiId and mg1.genreId=mg2.genreId " \
               "and m2.langId= m1.langId and d1.filmId=m1.apiId and d2.filmId=m2.apiId and d1.directorId <> d2.directorId"
    values = (firstdate,secondate)
    cursorObject.execute(sqlQuery,values)
    rows = cursorObject.fetchall()
    for row in rows:
        print(row[0]+"\n")
    return rows

def active_actor(connectionObject):
    ## (query 6)
    firstdate=input("enter first release date: ")
    secondate=input("enter second release date: ")
    numberofMovies=input("enter number of movies, that the actor participated ")
    cursorObject = connectionObject.cursor()
    sqlQuery = "select a1.actorId,a1.actorName,count(*)   from Movie m1 , Actors a1 , ActorsMovie am1 " \
               " where a1.actorId=am1.actorId and m1.apiId=am1.filmId and m1.releaseDay " \
               "between %s and %s group by a1.actorId  having count(*)>%s"
    values = (firstdate,secondate,numberofMovies)
    cursorObject.execute(sqlQuery,values)
    rows = cursorObject.fetchall()
    for row in rows:
        print(row[0],"\t",row[1],'\t',row[2],'\n')
    return rows

def get_list_of_movies(connectionObject):
    ## (query 8)

    actorid=input("enter actor id: ")
    firstdate=input("enter first release date: ")
    secondate=input("enter second release date: ")
    cursorObject = connectionObject.cursor()
    sqlQuery = "select m.title from ActorsMovie am , Movie m where am.actorId=%s and m.releaseDay between %s and %s and am.filmId=m.apiId"
    values = (actorid,firstdate,secondate)
    cursorObject.execute(sqlQuery,values)
    rows = cursorObject.fetchall()
    for row in rows:
        print(row[0],"\n")
    return rows

def active_and_success_actor(connectionObject):
    ## (query 7)
    firstdate=input("enter first release date: ")
    secondate=input("enter second release date: ")
    numberofMovies=input("enter number of movies, that the actor participated ")
    revenue = input ("enter revenue : ")
    popularity = input ("enter popularity: ")
    cursorObject = connectionObject.cursor()
    sqlQuery = "select a1.actorId,a1.actorName,count(*)   from Movie m1 , Actors a1 , ActorsMovie am1 " \
               " where a1.actorId=am1.actorId and m1.apiId=am1.filmId and m1.releaseDay " \
               "between %s and %s  and m1.revenue>%s and m1.popularity>%s group by a1.actorId  having count(*)>%s"
    values = (firstdate,secondate,revenue,popularity,numberofMovies)
    cursorObject.execute(sqlQuery,values)
    rows = cursorObject.fetchall()
    for row in rows:
        print(row[0],"\t",row[1],'\t',row[2],'\n')
    return rows