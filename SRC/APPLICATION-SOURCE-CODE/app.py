import pymysql

from SRC import RetrieveData
from SRC import Queries
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/search')
def search_return_html():
    connectionObject = pymysql.connect(host="127.0.0.1", user="DbMysql03", password="DbMysql03", db="DbMysql03",
                                       port=3305)
    query = request.args.get('query')
    cursorObject = connectionObject.cursor()
    sqlQuery = "select Movie.apiId from Movie where Movie.title=%s"
    values = (query)
    cursorObject.execute(sqlQuery, values)
    rows = cursorObject.fetchall()
    for row in rows:
        apiId = row[0]
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
    values = (apiId, apiId)
    cursorObject.execute(sqlQuery, values)
    rows = cursorObject.fetchall()
    str = ""
    for row in rows :
        str =str+ " , "+row[0]
    # with connector get to your mysql server and query the DB
    # return the answer to number_of_songs var.
    number_of_songs = 8 #should be retrieved from the DB
    return render_template('searchResults.html', movie=str, query=query)

if __name__ == '__main__':
    #connectionObject = pymysql.connect(host="127.0.0.1", user="DbMysql03", password="DbMysql03", db="DbMysql03",port=3305)
   app.run()