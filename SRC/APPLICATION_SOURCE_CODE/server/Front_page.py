
from flask import Flask, render_template, request, abort, redirect, Blueprint
from random import shuffle
from SRC.APPLICATION_SOURCE_CODE.DB import sql_executor
from SRC.APPLICATION_SOURCE_CODE.DB.sql_executor import *

home_page = Blueprint('home', __name__, template_folder='templates')

@home_page.route('/', methods=['POST','GET'])
@home_page.route('/movie', methods=['POST','GET'])
@home_page.route('/tvshow', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        try:
            movieTitle = request.form['movieTitle']
            if movieTitle != None:
                showApiId = search_similar_show(movieTitle)
                if showApiId == 0:
                    return render_template("Error.html")

                route = "/tvshow/" + str(showApiId)
                return redirect(route, code=302)
        except :
            try:
                showTitle = request.form['showTitle']
                if showTitle != None:
                    movieApiId = search_similar_movie(showTitle)
                    if movieApiId == 0:
                        return render_template("Error.html")
                    route = "/movie/" + str(movieApiId)
                return redirect(route, code=302)
            except :
                return render_template("Error.html")

    sqlQuery = "select  m.apiId , pm.image from Movie m, ( select avg(voteCount) as " \
               "avg from Movie) as avgVoteCount , ( select avg(voteAvg) as avg from Movie)" \
               " as avgVoteavg , ( select avg(popularity) as avg from Movie) as avgPopularity" \
               ",( select avg(revenue) as avg from Movie) as avgrevenue , PosterMovie pm where " \
               "m.voteCount>=avgVoteCount.avg and m.voteAvg>=avgVoteavg.avg and m.popularity>=avgPopularity.avg " \
               "and m.releaseDay between '2020-01-01' and '2021-01-01' and m.revenue>= avgrevenue.avg " \
               "and pm.apiId=m.apiId and pm.image is not null "
    res = select(sqlQuery)
    result = [{res['headers'][0]: row[0],
                 res['headers'][1]: row[1]} for row in res['rows']]
    shuffle(result)
    image0 = result[0]['image']
    image1 = result[1]['image']
    image2 = result[2]['image']
    image3 = result[3]['image']
    image4 = result[4]['image']
    link0 = result[0]['apiId']
    link1 = result[1]['apiId']
    link2 = result[2]['apiId']
    link3 = result[3]['apiId']
    link4 = result[4]['apiId']


    sqlQuery=" select  m.apiId , pm.image from Shows m, ( select avg(voteCount) " \
             "as avg from Shows) as avgVoteCount , ( select avg(voteAvg) as avg from" \
             " Shows)  as avgVoteavg , ( select avg(popularity) as avg from Shows) as " \
             "avgPopularity   , PosterShow pm where m.voteCount>=avgVoteCount.avg" \
             " and m.voteAvg>=avgVoteavg.avg and m.popularity>=avgPopularity.avg           " \
             "      and m.releaseDay between '2020-01-01' and '2021-01-01' and   pm.apiId=m.apiId " \
             "and pm.image is not null"
    resShow = select(sqlQuery)
    result = [{resShow['headers'][0]: row[0],
               resShow['headers'][1]: row[1]} for row in resShow['rows']]
    shuffle(result)
    imageShow0 = result[0]['image']
    imageShow1 = result[1]['image']
    imageShow2 = result[2]['image']
    imageShow3 = result[3]['image']
    imageShow4 = result[4]['image']
    Imagelink0 = result[0]['apiId']
    Imagelink1 = result[1]['apiId']
    Imagelink2 = result[2]['apiId']
    Imagelink3 = result[3]['apiId']
    Imagelink4 = result[4]['apiId']
    return render_template('Front-Page.html',image0=image0,image1=image1,image2=image2,image3=image3,image4=image4,link0=link0,link1=link1,link2=link2,link3=link3,link4=link4,
                           imageShow0=imageShow0,imageShow1=imageShow1,imageShow2=imageShow2,imageShow3=imageShow3,imageShow4=imageShow4,Imagelink0=Imagelink0,Imagelink1=Imagelink1
                           ,Imagelink2=Imagelink2,Imagelink3=Imagelink3,Imagelink4=Imagelink4)
def search_similar_show(title):
    # Get Movie title id
    movieApiId = get_movie_apiId(title)
    if movieApiId == None:
        return 0
    sqlQuery = " select distinct countActors.title" \
               " from (SELECT m2.apiId as id, m2.title as title, count(*) as sharedActors from" \
               " Movie as m, Shows as m2, Actors as a, ActorsMovie as am, ActorsShow as am2" \
               " where m.apiId=%s and m.langId=m2.langId  and am.filmId=m.apiId and am.actorId=a.actorId" \
               " and am2.showId=m2.apiId and am.actorId=am2.actorId group by m2.apiId) as countActors," \
               " (select distinct m2.apiId as id, m2.title as title, count(*) as sharedGenres" \
               " from  Movie as m, Shows as m2, Genre as g, MoviesGenre as mg, ShowGenre as mg2" \
               " WHERE m.apiId=%s and m.langId=m2.langId  and mg.apiId=m.apiId and mg.genreId=g.genreId" \
               " and mg2.apiId=m2.apiId and mg.genreId=mg2.genreId group by m2.apiId) as" \
               " countGenres, Shows m1 where countActors.sharedActors >= 1 and countGenres.sharedGenres >= 1" \
               " and m1.apiId=countActors.id and m1.apiId=countGenres.id"
    res = select(sqlQuery, [movieApiId, movieApiId])
    tvTitle = res['rows'][0][0]
    # Search for similar show id
    showApiId = get_show_apiId(tvTitle)
    if showApiId == None:
        return 0
    return showApiId


def search_similar_movie(title):
    # Get Show title id
    showApiId = get_show_apiId(title)
    if showApiId == None:
        return 0

    sqlQuery = "select distinct countActors.title from (SELECT m2.apiId as id, m2.title as title, " \
               "count(*) as sharedActors from  Shows as m, Movie as m2, Actors as a," \
               " ActorsShow as am, ActorsMovie as am2 where m.apiId=%s and m.langId=m2.langId " \
               "and am.showId=m.apiId AND am.actorId=a.actorId and am2.filmId=m2.apiId and am.actorId=am2.actorId" \
               " group by m2.apiId,m2.title) as countActors, (select distinct m2.apiId as id, m2.title as title, count(*)" \
               " as sharedGenres from  Shows as m, Movie as m2, Genre as g, ShowGenre as mg, MoviesGenre as mg2" \
               " where m.apiId=%s and m.langId=m2.langId and mg.apiId=m.apiId and mg.genreId=g.genreId and " \
               "mg2.apiId=m2.apiId and mg.genreId=mg2.genreId group by  m2.apiId,m2.title) as countGenres, Movie m1 " \
               "where countActors.sharedActors >= 1 and countGenres.sharedGenres >=1 and m1.apiId=countActors.id and m1.apiId=countGenres.id"

    res = select(sqlQuery, [showApiId, showApiId])
    movieTitle = res['rows'][0][0]
    # Search for similar show id
    movieApiId = get_movie_apiId(movieTitle)
    if movieApiId == None:
        return 0
    return movieApiId


def get_movie_apiId(title):
    try:
        sqlQuery = " select m.apiId" \
                   " from Movie m where m.title = %s"
        res = select(sqlQuery, title)
        return res['rows'][0][0]
    except sql_executor.NoResultsException:
        return None

def get_show_apiId(title):
    try:
        sqlQuery = " select s.apiId" \
                   " from Shows s where s.title = %s"
        res = select(sqlQuery, title)
        return res['rows'][0][0]
    except sql_executor.NoResultsException:
        return None