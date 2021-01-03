import json
import pymysql
from flask import Flask, render_template, request
import cgi
from SRC.APPLICATION_SOURCE_CODE.DB.sql_executor import *

app = Flask(__name__)


@app.route('/')
def index():

    sqlQuery = "select  m.title , pm.image from Movie m, ( select avg(voteCount) as " \
               "avg from Movie) as avgVoteCount , ( select avg(voteAvg) as avg from Movie)" \
               " as avgVoteavg , ( select avg(popularity) as avg from Movie) as avgPopularity" \
               ",( select avg(revenue) as avg from Movie) as avgrevenue , PosterMovie pm where " \
               "m.voteCount>=avgVoteCount.avg and m.voteAvg>=avgVoteavg.avg and m.popularity>=avgPopularity.avg " \
               "and m.releaseDay between '2020-01-01' and '2021-01-01' and m.revenue>= avgrevenue.avg " \
               "and pm.apiId=m.apiId and pm.image is not null limit 5"
    res = select(sqlQuery)
    result = [{res['headers'][0]: row[0],
                 res['headers'][1]: row[1]} for row in res['rows']]
    image0= result[0]['image']
    image1= result[1]['image']
    image2= result[2]['image']
    image3= result[3]['image']
    image4= result[4]['image']

    return render_template('Front-Page.html',image0=image0,image1=image1,image2=image2,image3=image3,image4=image4)

@app.route('/Credits')
def Credits():
    return render_template('Credits.html')

@app.route('/Actors')
def Actors():
    return render_template('Actors.html')

@app.route('/Foreign-Languages')
def Foreign_Languages():
    return render_template('Foreign-Languages.html')

@app.route('/Search-Movies-or-TV-Shows')
def Search_Movies_or_TV_Shows():
    return render_template('Search-Movies-or-TV-Shows.html')

@app.route('/TV-Show')
def TV_Show():
    return render_template('TV-Show.html')


@app.route('/movie/<apiId>')
def movie(apiId):
    sqlQuery = "select title from Movie where Movie.apiId=%s"
    resTitle = select(sqlQuery,apiId)
    resultTitle = [{resTitle['headers'][0]: row[0]} for row in resTitle['rows']]
    resultTitle=resultTitle[0]['title']
    sqlQuery = "select overview from MovieOverview where MovieOverview.filmId=%s"
    resOverView= select(sqlQuery,apiId)
    resultOverview = [{resOverView['headers'][0]: row[0]} for row in resOverView['rows']]
    resultOverview=resultOverview[0]['overview']
    sqlQuery="select image from PosterMovie where apiId=%s"
    resimage = select(sqlQuery,apiId)
    resultimage = [{resimage['headers'][0]: row[0]} for row in resimage['rows']]
    resultimage=resultimage[0]['image']
    return render_template('Movie.html',resultTitle=resultTitle,resultOverview=resultOverview,resimage=resultimage)


@app.route('/search')
def search_return_html():
    query = request.args.get('query')
    sqlQuery = "select Movie.apiId from Movie where Movie.title=%s"
    res = select(sqlQuery,query)
    apiId=res['rows'][0][0]
    sqlQuery = "select distinct commonMovie.title  from (SELECT m2.apiId as id,m2.title as title, " \
               "count(*) as count FROM Movie as m, Movie as m2, Actors as a, ActorsMovie as am, " \
               "ActorsMovie as am2 WHERE m.apiId=%s AND am.filmId<>am2.filmId AND am.filmId=m.apiId" \
               " AND am.actorId=a.actorId AND am2.filmId=m2.apiId AND am.actorId=am2.actorId AND" \
               " m.langId=m2.langId GROUP BY m2.apiId,m2.title) as commonMovie  , (SELECT distinct m2.apiId " \
               "as id, m2.title as title, count(*) as count FROM Movie as m, Movie as m2, Genre as g" \
               ", MoviesGenre as mg, MoviesGenre as mg2 WHERE m.apiId=%s AND mg.apiId<>mg2.apiId AND " \
               "mg.apiId=m.apiId AND mg.genreId=g.genreId AND mg2.apiId=m2.apiId AND mg.genreId=mg2.genreId " \
               "GROUP BY m2.apiId,m2.title) as commonGenre , Movie m1 where commonMovie.count >4 and commonGenre.count>2" \
               " and m1.apiId=commonMovie.id and m1.apiId=commonGenre.id"
    res = select(sqlQuery, [apiId,apiId])
    str = ""
    for row in res['rows']:
        str = str + " , " + row[0]

    return render_template('searchResults.html',movie=str,query=query,)

@app.route('/specific_movie/<apiId>')
def specific_movie_to_html(apiId):
    sqlQuery = "select apiId,title from Movie where apiId=%s "
    res = select(sqlQuery,apiId)
    movie = res['rows'][0][1]
    return render_template('specific_movie.html', apiId=apiId,movie=movie)


@app.route('/testmoce')
def movie_to_html():
    sqlQuery = "select apiId,title from Movie   "
    res = select(sqlQuery)
    result = [{res['headers'][0]: row[0],
                 res['headers'][1]: row[1]} for row in res['rows']]
    return render_template('testmoce.html', res=json.dumps(result))

@app.route("/Search-Movies-or-TV-Shows",methods=['POST','GET'])
def fun():
   if request.method == 'POST':
       title = request.form['title']
   sqlQuery="select s.title from Shows as s where MATCH(s.title) AGAINST(%s) union select m.title from Movie as m where MATCH(m.title) AGAINST(%s)"
   res=select(sqlQuery,[title,title])
   result=[{res['headers'][0]: row[0] } for row in res['rows']]
   return render_template('Search-Movies-or-TV-Shows.html',res=json.dumps(result))

if __name__ == '__main__':
   app.run()
