
from flask import request, render_template, Blueprint, redirect

from SRC.APPLICATION_SOURCE_CODE.DB import sql_executor
from SRC.APPLICATION_SOURCE_CODE.DB.sql_executor import *

search_page = Blueprint('search', __name__, template_folder='templates')

@search_page.route("/Search-Movies-or-TV-Shows")
def serach_movie_ortv():
    return render_template('Search-Movies-or-TV-Shows.html')


@search_page.route("/Search-Movies-or-TV-Shows",methods=['POST','GET'])
def search_full_text():
   if request.method == 'POST':
       title = request.form['title']

   sqlQuery="select s.title from Shows as s where MATCH(s.title) AGAINST(%s) union select m.title from Movie as m where MATCH(m.title) AGAINST(%s)"
   try:
    res=select(sqlQuery,[title,title])
    result=[{res['headers'][0]: row[0] } for row in res['rows']]
    return render_template('Search-Movies-or-TV-Shows.html',res=json.dumps(result))
   except sql_executor.NoResultsException:
       return render_template('Search-Movies-or-TV-Shows.html')

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
            render_template("Error.html")



