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


def recommended_actor_by_genre(connectionObject):
    ## (query 2)
    GenreName=input("enter Genre Name: ")
    voteavg=input("enter vote avg: ")
    cursorObject = connectionObject.cursor()
    sqlQuery = "select a.actorId, a.actorName , count(*) from Actors a, MoviesGenre mg, Movie m ," \
               " ActorsMovie am , Genre g , (select Genre.genreId as id from Genre where" \
               " genreName=%s) AS temp, (select g.genreId,g.genreName,avg(voteCount) as" \
               " avgvotecount from Movie m , Genre g, MoviesGenre mg where m.apiId=mg.apiId " \
               "and g.genreId=mg.genreId group by g.genreId ) as GenreAvgVoteCount where" \
               " m.apiId=mg.apiId and a.actorId=am.actorId and am.filmId=m.apiId and g.genreName=%s " \
               "and  temp.id=mg.genreId and  m.voteCount>GenreAvgVoteCount.avgvotecount and m.voteAvg>%s" \
               " and temp.id= GenreAvgVoteCount.genreId group by a.actorId order by -count(*)"
    values = (GenreName,GenreName,voteavg)
    cursorObject.execute(sqlQuery,values)
    rows = cursorObject.fetchall()
    for row in rows:
        print(row[0],"\t",row[1],'\t',row[2],'\n')
    return rows

def recommended_actor_by_genre(connectionObject):
    ## (query 2)
    GenreName=input("enter Genre Name: ")
    voteavg=input("enter vote avg: ")
    cursorObject = connectionObject.cursor()
    sqlQuery = "select a.actorId, a.actorName , count(*) from Actors a, MoviesGenre mg, Movie m ," \
               " ActorsMovie am , Genre g , (select Genre.genreId as id from Genre where" \
               " genreName=%s) AS temp, (select g.genreId,g.genreName,avg(voteCount) as" \
               " avgvotecount from Movie m , Genre g, MoviesGenre mg where m.apiId=mg.apiId " \
               "and g.genreId=mg.genreId group by g.genreId ) as GenreAvgVoteCount where" \
               " m.apiId=mg.apiId and a.actorId=am.actorId and am.filmId=m.apiId and g.genreName=%s " \
               "and  temp.id=mg.genreId and  m.voteCount>GenreAvgVoteCount.avgvotecount and m.voteAvg>%s" \
               " and temp.id= GenreAvgVoteCount.genreId group by a.actorId order by -count(*)"
    values = (GenreName,GenreName,voteavg)
    cursorObject.execute(sqlQuery,values)
    rows = cursorObject.fetchall()
    for row in rows:
        print(row[0],"\t",row[1],'\t',row[2],'\n')
    return rows

def recommended_foreign_language(connectionObject):
    ## (query 11)
    voteavg = input("enter vote avg: ")
    cursorObject = connectionObject.cursor()
    sqlQuery = "select m.title , l.languageName from Movie m,Language l, (select m.langId as lang, avg(m.budget) " \
               "as budget from Movie m, Movie m2 where m.langId = m2.langId and m.budget is not null group by" \
               " m.langId) as budgetAvg , (select m.langId as lang, avg(m.revenue) as revenue from Movie m," \
               " Movie m2 where m.langId = m2.langId and m.revenue is not null group by m.langId) as revenueAvg," \
               "(select m.langId as langId,avg(m.voteCount) as avgVote from Movie m,Movie m2 where m.langId = m2.langId " \
               "group by m.langId) as voteCountByLang where m.langId  = budgetAvg.lang and m.langId=revenueAvg.lang and " \
               "m.budget >budgetAvg.budget and m.revenue > revenueAvg.revenue and m.langId <> 2 and voteCountByLang.langId=m.langId" \
               "  and m.voteCount>voteCountByLang.avgVote and m.voteAvg>%s and l.languageId = m.langId"
    values = ( voteavg)
    cursorObject.execute(sqlQuery, values)
    rows = cursorObject.fetchall()
    for row in rows:
        print(row[0], "\t", row[1], '\n')
    return rows

def similar_movie(connectionObject):
    ##query 9
    title = input("enter title : ")
    cursorObject = connectionObject.cursor()
    sqlQuery = "select Movie.apiId from Movie where Movie.title=%s"
    values = (title)
    cursorObject.execute(sqlQuery, values)
    rows = cursorObject.fetchall()
    for row in rows:
        apiId= row[0]
    sqlQuery = "select distinct commonMovie.title  from (SELECT m2.apiId as id,m2.title as title, " \
               "count(*) as count FROM Movie as m, Movie as m2, Actors as a, ActorsMovie as am, " \
               "ActorsMovie as am2 WHERE m.apiId=%s AND am.filmId<>am2.filmId AND am.filmId=m.apiId" \
               " AND am.actorId=a.actorId AND am2.filmId=m2.apiId AND am.actorId=am2.actorId AND" \
               " m.langId=m2.langId GROUP BY m2.apiId) as commonMovie  , (SELECT distinct m2.apiId " \
               "as id, m2.title as title, count(*) as count FROM Movie as m, Movie as m2, Genre as g" \
               ", MoviesGenre as mg, MoviesGenre as mg2 WHERE m.apiId=%s AND mg.apiId<>mg2.apiId AND " \
               "mg.apiId=m.apiId AND mg.genreId=g.genreId AND mg2.apiId=m2.apiId AND mg.genreId=mg2.genreId " \
               "GROUP BY m2.apiId) as commonGenre , Movie m1 where commonMovie.count >4 and commonGenre.count>2" \
               " and m1.apiId=commonMovie.id and m1.apiId=commonGenre.id"
    values = (apiId,apiId)
    cursorObject.execute(sqlQuery, values)
    rows = cursorObject.fetchall()
    for row in rows:
        print(row[0], '\n')
    return rows


def similar_movie_To_Show(connectionObject):
    ##query 10
    title = input("enter title : ")
    cursorObject = connectionObject.cursor()
    sqlQuery = "select Movie.apiId from Movie where Movie.title=%s"
    values = (title)
    cursorObject.execute(sqlQuery, values)
    rows = cursorObject.fetchall()
    for row in rows:
        apiId= row[0]
    sqlQuery = "SELECT distinct countActors.title" \
               " FROM (SELECT m2.apiId as id, m2.title as title, count(*) as sharedActors 		FROM" \
               "  Movie as m, Shows as m2, Actors as a, ActorsMovie as am, ActorsShow as am2 		" \
               "WHERE m.apiId=%s AND m.langId=m2.langId  AND am.filmId=m.apiId AND am.actorId=a.actorId" \
               " AND am2.showId=m2.apiId AND am.actorId=am2.actorId 		GROUP BY m2.apiId) as countActors," \
               " 		(SELECT distinct m2.apiId as id, m2.title as title, count(*) as sharedGenres 		" \
               "FROM  Movie as m, Shows as m2, Genre as g, MoviesGenre as mg, ShowGenre as mg2 		" \
               "WHERE m.apiId=%s AND m.langId=m2.langId  AND mg.apiId=m.apiId AND mg.genreId=g.genreId" \
               " AND mg2.apiId=m2.apiId AND mg.genreId=mg2.genreId  		GROUP BY m2.apiId) as" \
               " countGenres, Shows m1 WHERE countActors.sharedActors >= 1 AND countGenres.sharedGenres >= 1" \
               " AND m1.apiId=countActors.id AND m1.apiId=countGenres.id"
    values = (apiId,apiId)
    cursorObject.execute(sqlQuery, values)
    rows = cursorObject.fetchall()
    for row in rows:
        print(row[0], '\n')
    return rows

def similar_Show_To_Movie(connectionObject):
    ##query 1
    title = input("enter title : ")
    cursorObject = connectionObject.cursor()
    sqlQuery = "select Shows.apiId from Movie where Shows.title=%s"
    values = (title)
    cursorObject.execute(sqlQuery, values)
    rows = cursorObject.fetchall()
    for row in rows:
        apiId= row[0]
    sqlQuery ="SELECT distinct countActors.titleFROM (SELECT m2.apiId as id, m2.title as title, " \
              "count(*) as sharedActors 		FROM  Shows as m, Movie as m2, Actors as a," \
              " ActorsShow as am, ActorsMovie as am2 		WHERE m.apiId=%s AND m.langId=m2.langId " \
              "AND am.showId=m.apiId AND am.actorId=a.actorId AND am2.filmId=m2.apiId AND am.actorId=am2.actorId" \
              " GROUP BY m2.apiId) as countActors, 		(SELECT distinct m2.apiId as id, m2.title as title, count(*)" \
              " as sharedGenres 		FROM  Shows as m, Movie as m2, Genre as g, ShowGenre as mg, MoviesGenre as mg2" \
              " 		WHERE m.apiId=%s AND m.langId=m2.langId AND mg.apiId=m.apiId AND mg.genreId=g.genreId AND " \
              "mg2.apiId=m2.apiId AND mg.genreId=mg2.genreId 		GROUP BY m2.apiId) as countGenres, Movie m1 " \
              "WHERE countActors.sharedActors >= 1 AND countGenres.sharedGenres >=1 AND m1.apiId=countActors.id AND m1.apiId=countGenres.id"
    values = (apiId,apiId)
    cursorObject.execute(sqlQuery, values)
    rows = cursorObject.fetchall()
    for row in rows:
        print(row[0], '\n')
    return rows

