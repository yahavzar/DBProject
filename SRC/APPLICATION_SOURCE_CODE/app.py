import json
import pymysql
from flask import Flask, render_template, request

from SRC.APPLICATION_SOURCE_CODE.DB.sql_executor import *

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    res = [{"apiId":"2","title":"yahav"}]
    return render_template('index.html', res=json.dumps(res))
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


@app.route('/movie')
def movie_to_html():
    sqlQuery = "select apiId,title from Movie   "
    res = select(sqlQuery)
    result = [{res['headers'][0]: row[0],
                 res['headers'][1]: row[1]} for row in res['rows']]
    return render_template('movie.html', res=json.dumps(result))






if __name__ == '__main__':
   app.run()
