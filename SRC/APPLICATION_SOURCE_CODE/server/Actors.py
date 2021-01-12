from flask import request, render_template, Blueprint

from DB import sql_executor
from DB.sql_executor import select

actors_page = Blueprint('actors', __name__, template_folder='templates')

@actors_page.route('/Actors')
def Actors():
    sqlQuery = "select distinct Genre.genreName as title from Genre"
    res=select(sqlQuery)
    result = [k[0] for k in res["rows"]]
    return render_template('Actors.html',genres=result)


@actors_page.route("/Actors",methods=['POST','GET'])
def search_recommended_actors():
    sqlQuery = "select distinct Genre.genreName as title from Genre"
    res2 = select(sqlQuery)
    result2 = [k[0] for k in res2["rows"]]
    if request.method == 'POST':
        if request.form.get("dropdown"):
            title = request.form['dropdown']
            result = getRecommendedActorsByGenre(title)
            return render_template('Actors.html', res=result, genres=result2)
        elif request.form.get("startDate1"): # returns actors who participated in at least 3 movies during the time period
            date = request.form['startDate1'].split(" - ")
            result4=getKnownActors(date)
            return render_template('Actors.html', resKnown=result4, genres=result2)
        elif request.form.get("startDate2"):
            # actors who have at least 3 movies between those dates with a popularity above 100 and a revenue-to-budget ratio of at least 6.5
            date = request.form['startDate2'].split(" - ")
            result3=getSyccesfulActors(date)
            return render_template('Actors.html', resSuc=result3, genres=result2)
        elif request.form.get('actorName'):
            actor = request.form['actorName']
            result=getMediaByActor(actor)
            return render_template('Actors.html', resNames=result, genres=result2)


def getRecommendedActorsByGenre(title):
    try:
        sqlQuery = "select * from " \
               "(select a.actorName as title, count(*) as cnt " \
               "from Actors a, MoviesGenre mg, Movie m , ActorsMovie am , Genre g , " \
               "(select Genre.genreId as id  from Genre  where genreName=%s) AS temp,  " \
               "(select g.genreId,g.genreName,avg(voteCount) as avgvotecount  from Movie m , Genre g, MoviesGenre mg  " \
               "where m.apiId=mg.apiId and g.genreId=mg.genreId  group by g.genreId ) as GenreAvgVoteCount  " \
               "where  m.apiId=mg.apiId and a.actorId=am.actorId and am.filmId=m.apiId and g.genreName=%s " \
               "and  temp.id=mg.genreId and  m.voteCount>GenreAvgVoteCount.avgvotecount and m.voteAvg>8 " \
               "and temp.id= GenreAvgVoteCount.genreId " \
               "group by a.actorId " \
               "union " \
               "select a.actorName as name, count(*) as cnt " \
               "from Actors a, ShowGenre mg, Shows m , ActorsShow am , Genre g , " \
               "(select Genre.genreId as id from Genre where genreName=%s) AS temp, " \
               "(select g.genreId,g.genreName,avg(voteCount) as avgvotecount from Shows m , Genre g, ShowGenre mg " \
               "where m.apiId=mg.apiId and g.genreId=mg.genreId group by g.genreId ) as GenreAvgVoteCount  " \
               "where  m.apiId=mg.apiId and a.actorId=am.actorId and am.showId=m.apiId and g.genreName=%s " \
               "and  temp.id=mg.genreId and  m.voteCount>GenreAvgVoteCount.avgvotecount and m.voteAvg>8 " \
               "and temp.id= GenreAvgVoteCount.genreId  " \
               "group by a.actorId) as temp " \
               "order by -cnt;"
        res = select(sqlQuery, [title, title, title, title])
        result = [{res['headers'][0]: row[0]} for row in res['rows']]
        return result
    except sql_executor.NoResultsException:
        return []

def getKnownActors(date):
    moviesNumber = 3
    tempStart = date[0].split("/")
    tempEnd = date[1].split("/")
    start = tempStart[2] + "-" + tempStart[0] + "-" + tempStart[1]
    end = tempEnd[2] + "-" + tempEnd[0] + "-" + tempEnd[1]

    sqlQuery = "select title, cnt from (select title,cnt from (select a1.actorName as title, count(*) as cnt, a1.actorId as id from Movie m1 , Actors a1 , ActorsMovie am1 where a1.actorId=am1.actorId and m1.apiId=am1.filmId and m1.releaseDay between %s and %s group by a1.actorId having count(*)>%s) as temp group by temp.id  order by temp.cnt DESC) as temp4 union  (select title,cnt from (select a1.actorName as title, count(*) as cnt, a1.actorId as id from Shows m1 , Actors a1 , ActorsShow am1 where a1.actorId=am1.actorId and m1.apiId=am1.showId and m1.releaseDay between %s and %s group by a1.actorId having count(*)>%s) as temp2 group by temp2.id order by temp2.cnt DESC)"
    try:
        res4 = select(sqlQuery, [start, end, moviesNumber, start, end, moviesNumber])
        result4 = [{res4['headers'][0]: row[0]} for row in res4['rows']]
        return result4
    except sql_executor.NoResultsException:
        return []

def getSyccesfulActors(date):
    moviesNumber2 = 3
    revenueToBudeget = 6.5
    popularity = 100
    tempStart = date[0].split("/")
    tempEnd = date[1].split("/")
    start = tempStart[2] + "-" + tempStart[0] + "-" + tempStart[1]
    end = tempEnd[2] + "-" + tempEnd[0] + "-" + tempEnd[1]

    sqlQuery = "select distinct title from" \
               "(select title from" \
               "( select title, cnt from" \
               "(select a1.actorName as title, count(*) as cnt, a1.actorId as id " \
               "from Movie m1 , Actors a1 , ActorsMovie am1 " \
               "where a1.actorId=am1.actorId and m1.apiId=am1.filmId and m1.releaseDay " \
               "between %s and %s and ((m1.budget*%s)<m1.revenue) and (m1.popularity>%s) " \
               "group by a1.actorId having count(*)>%s) as temp group by temp.id order by temp.cnt DESC) as temp " \
               "union " \
               "select title from" \
               "( select title, cnt from" \
               "(select a1.actorName as title, count(*) as cnt, a1.actorId as id " \
               "from Shows m1 , Actors a1 , ActorsShow am1 " \
               "where a1.actorId=am1.actorId and m1.apiId=am1.showId and m1.releaseDay " \
               "between %s and %s and (m1.popularity>%s) " \
               "group by a1.actorId having count(*)>%s) as temp2 " \
               "group by temp2.id " \
               "order by temp2.cnt DESC) as temp4) as final"
    try:
        res3 = select(sqlQuery,
                      [start, end, revenueToBudeget, popularity, moviesNumber2, start, end, popularity, moviesNumber2])
        result3 = [{res3['headers'][0]: row[0]} for row in res3['rows']]
        return result3
    except sql_executor.NoResultsException:
        return []

def getMediaByActor(actor):
    sqlQuery = "(select distinct Movie.title, 'Movie' as Media from Movie, ActorsMovie, Actors Where Actors.actorName = %s and Movie.apiId = ActorsMovie.filmId and ActorsMovie.actorId = Actors.actorId  order by Movie.popularity) union (select distinct Shows.title, 'Series' as Media from Shows, ActorsShow, Actors Where Actors.actorName = %s and Shows.apiId = ActorsShow.showId and ActorsShow.actorId = Actors.actorId  order by Shows.popularity)"
    try:
        res = select(sqlQuery, [actor, actor])
        result = [{res['headers'][0]: row[0],res['headers'][1]:row[1]} for row in res['rows']]
        return result
    except sql_executor.NoResultsException:
        return []