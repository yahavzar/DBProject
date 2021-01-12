
from flask import request, render_template, Blueprint, redirect

from DB import sql_executor
from DB.sql_executor import *

search_page = Blueprint('search', __name__, template_folder='templates')

@search_page.route("/Search-Movies-or-TV-Shows")
def serach_movie_ortv():
    sqlQuery = "select distinct Genre.genreName as title from Genre"
    res=select(sqlQuery)
    result = [k[0] for k in res["rows"]]
    return render_template('Search-Movies-or-TV-Shows.html',genres=result)


@search_page.route("/Search-Movies-or-TV-Shows",methods=['POST','GET'])
def search_full_text():
    sqlQuery = "select distinct Genre.genreName as title from Genre"
    res = select(sqlQuery)
    resultGenre = [k[0] for k in res["rows"]]
    if request.method == 'POST':
       if(request.form.get("title")):
            title = request.form['title']
            sqlQuery="select s.title from Shows as s where MATCH(s.title) AGAINST(%s) union select m.title from Movie as m where MATCH(m.title) AGAINST(%s)"
            try:
                res=select(sqlQuery,[title,title])
                result=[{res['headers'][0]: row[0] } for row in res['rows']]
                return render_template('Search-Movies-or-TV-Shows.html',res=json.dumps(result),genres=resultGenre)
            except sql_executor.NoResultsException:
                return render_template('Search-Movies-or-TV-Shows.html',genres=result)
       elif (request.form.get("dropdown")):
           genere = request.form['dropdown']
           sqlQuery="SELECT Movie.title, Movie.popularity, 'Movie' as Media FROM Movie, Genre, MoviesGenre WHERE " \
                    "Movie.apiId=MoviesGenre.apiId and MoviesGenre.genreId=Genre.genreId and " \
                    "Genre.genreName=%s union SELECT Shows.title, Shows.popularity, 'TvShow' as Media FROM Shows" \
                    ", Genre, ShowGenre WHERE Shows.apiId=ShowGenre.apiId and ShowGenre.genreId=Genre.genreId" \
                    " and Genre.genreName=%s  order by - popularity"
           try:
               res1 = select(sqlQuery, [genere,genere])
               result2 = [{res1['headers'][0]: row[0],res1['headers'][1]: row[1],res1['headers'][2]: row[2]} for row in res1['rows']]
               return render_template('Search-Movies-or-TV-Shows.html', res2=json.dumps(result2), genres=resultGenre)
           except sql_executor.NoResultsException:
               return render_template('Search-Movies-or-TV-Shows.html', genres=resultGenre)


@search_page.route('/search')
def search_return_html():
    try :
        resultTitle = request.args.get('search')
        sqlQuery = "select apiId from Movie where title=%s"
        res = select(sqlQuery,resultTitle)
        resultapi = [{res['headers'][0]: row[0]}  for row in res['rows']]
        apiId = resultapi[0]['apiId']
        return  redirect("movie/"+str(apiId))
    except sql_executor.NoResultsException:
        try:
            resultTitle = request.args.get('search')
            sqlQuery = "select apiId from Shows where title=%s"
            res = select(sqlQuery, resultTitle)
            resultapi = [{res['headers'][0]: row[0]} for row in res['rows']]
            apiId = resultapi[0]['apiId']
            return redirect("tvshow/" + str(apiId))
        except sql_executor.NoResultsException:
            return render_template("Error.html")


