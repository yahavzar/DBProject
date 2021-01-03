import json

import pymysql
from flask import Flask, render_template, request,abort
import cgi

from SRC.APPLICATION_SOURCE_CODE.DB import sql_executor
from SRC.APPLICATION_SOURCE_CODE.DB.sql_executor import *

app = Flask(__name__)


@app.route('/')
@app.route('/movie')
@app.route('/tvshow')
def index():

    sqlQuery = "select  m.apiId , pm.image from Movie m, ( select avg(voteCount) as " \
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
    link0 = result[0]['apiId']
    link1 = result[1]['apiId']
    link2 = result[2]['apiId']
    link3 = result[3]['apiId']
    link4 = result[4]['apiId']

    return render_template('Front-Page.html',image0=image0,image1=image1,image2=image2,image3=image3,image4=image4,link0=link0,link1=link1,link2=link2,link3=link3,link4=link4)



@app.route("/Search-Movies-or-TV-Shows",methods=['POST','GET'])
def search_full_text():
   if request.method == 'POST':
       title = request.form['title']
   sqlQuery="select s.title from Shows as s where MATCH(s.title) AGAINST(%s) union select m.title from Movie as m where MATCH(m.title) AGAINST(%s)"
   res=select(sqlQuery,[title,title])
   result=[{res['headers'][0]: row[0] } for row in res['rows']]
   return render_template('Search-Movies-or-TV-Shows.html',res=json.dumps(result))

@app.route('/tvshow/<apiId>')
def TV_Show(apiId):
    try :
        sqlQuery = "select title from Shows where apiId=%s"
        resTitle = select(sqlQuery,apiId)
        resultTitle = [{resTitle['headers'][0]: row[0]} for row in resTitle['rows']]
        resultTitle=resultTitle[0]['title']
        sqlQuery = "select overview from ShowOverview where ShowOverview.showId=%s"
        resOverView= select(sqlQuery,apiId)
        resultOverview = [{resOverView['headers'][0]: row[0]} for row in resOverView['rows']]
        resultOverview=resultOverview[0]['overview']
        sqlQuery="select image from PosterShow where apiId=%s"
        resimage = select(sqlQuery,apiId)
        resultimage = [{resimage['headers'][0]: row[0]} for row in resimage['rows']]
        resultimage=resultimage[0]['image']
        return render_template('TV-Show.html',resultTitle=resultTitle,resultOverview=resultOverview,resimage=resultimage)
    except sql_executor.NoResultsException:
        abort(404)

@app.route('/movie/<apiId>')
def movie(apiId):
    try :
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
    except sql_executor.NoResultsException:
        abort(404)


@app.route('/search')
def search_return_html():
    try :
        resultTitle = request.args.get('search')
        sqlQuery = "select apiId from Movie where title=%s"
        res = select(sqlQuery,resultTitle)
        resultapi = [{res['headers'][0]: row[0]} for row in res['rows']]
        apiId = resultapi[0]['apiId']
        sqlQuery = "select overview from MovieOverview where MovieOverview.filmId=%s"
        resOverView= select(sqlQuery,apiId)
        resultOverview = [{resOverView['headers'][0]: row[0]} for row in resOverView['rows']]
        resultOverview=resultOverview[0]['overview']
        sqlQuery="select image from PosterMovie where apiId=%s"
        resimage = select(sqlQuery,apiId)
        resultimage = [{resimage['headers'][0]: row[0]} for row in resimage['rows']]
        resultimage=resultimage[0]['image']
        return render_template('Movie.html',resultTitle=resultTitle,resultOverview=resultOverview,resimage=resultimage)
    except sql_executor.NoResultsException:
        try :
            resultTitle = request.args.get('search')
            sqlQuery = "select apiId from Shows where title=%s"
            res = select(sqlQuery, resultTitle)
            resultapi = [{res['headers'][0]: row[0]} for row in res['rows']]
            apiId = resultapi[0]['apiId']
            sqlQuery = "select overview from ShowOverview where ShowOverview.showId=%s"
            resOverView= select(sqlQuery,apiId)
            resultOverview = [{resOverView['headers'][0]: row[0]} for row in resOverView['rows']]
            resultOverview=resultOverview[0]['overview']
            sqlQuery="select image from PosterShow where apiId=%s"
            resimage = select(sqlQuery,apiId)
            resultimage = [{resimage['headers'][0]: row[0]} for row in resimage['rows']]
            resultimage=resultimage[0]['image']
            return render_template('TV-Show.html',resultTitle=resultTitle,resultOverview=resultOverview,resimage=resultimage)
        except sql_executor.NoResultsException:
            abort(404)

@app.route('/Credits')
def Credits():
    return render_template('Credits.html')

@app.route('/Actors')
def Actors():
    return render_template('Actors.html')

@app.route('/Foreign-Languages')
def Foreign_Languages():
    return render_template('Foreign-Languages.html')

@app.route('/testmoce')
def movie_to_html():
    sqlQuery = "select apiId,title from Movie   "
    res = select(sqlQuery)
    result = [{res['headers'][0]: row[0],
                 res['headers'][1]: row[1]} for row in res['rows']]
    return render_template('testmoce.html', res=json.dumps(result))



if __name__ == '__main__':
   app.run()
