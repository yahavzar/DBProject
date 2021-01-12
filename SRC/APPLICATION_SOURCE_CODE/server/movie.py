from flask import request, render_template, Blueprint

from SRC.APPLICATION_SOURCE_CODE.DB import sql_executor
from SRC.APPLICATION_SOURCE_CODE.DB.sql_executor import select
from random import shuffle

movie_page = Blueprint('movie', __name__, template_folder='templates')


@movie_page.route('/movie/<apiId>')
def movie(apiId):
    try :
        resultTitle, resultimdb, length, collection, webSite, vote=getBasicInfo(apiId)
    except sql_executor.NoResultsException:
        render_template("Error.html")
    try:
        resultOverview=getOverView(apiId)
    except sql_executor.NoResultsException:
        resultOverview=""
    try:
        credit = getCast(apiId)
    except sql_executor.NoResultsException:
        credit=""
    try:
        director = getDirector(apiId)
    except sql_executor.NoResultsException:
        director=""
    try:
        resultimage = getPoster(apiId)
    except sql_executor.NoResultsException:
        resultimage= "../static/noimage.png"
    try :
        movielang = getSpokenLang(apiId)
    except  sql_executor.NoResultsException:
        movielang=""
    imagers1,links1=getSimilarMovie(apiId)
    imagerc1,linkc1= getComputeMovie(apiId)
    if imagerc1=="":
            imagerc1= "../static/noimage.png"
            linkc1=apiId
    else :
            imagerc1= "https://image.tmdb.org/t/p/w500/" +imagerc1
    if imagers1=="":
            imagers1= "../static/noimage.png"
            links1=apiId
    else :
            imagers1= "https://image.tmdb.org/t/p/w500/" +imagers1
    return render_template('Movie.html',resultTitle=resultTitle,resultOverview=resultOverview,resimage=resultimage,resultimdb=resultimdb,length=length,collection=collection,webSite=webSite,vote=vote,director=director,credit=credit,
                               imagers1=imagers1,links1=links1,imagerc1=imagerc1,linkc1=linkc1,movielang=movielang)


def getOverView(apiId):
    sqlQuery = "select overview from MovieOverview where MovieOverview.filmId=%s"
    resOverView = select(sqlQuery, apiId)
    resultOverview = [{resOverView['headers'][0]: row[0]} for row in resOverView['rows']]
    resultOverview = resultOverview[0]['overview']
    return resultOverview


def getPoster(apiId):
    sqlQuery = "select image from PosterMovie where apiId=%s"
    resimage = select(sqlQuery, apiId)
    resultimage = [{resimage['headers'][0]: row[0]} for row in resimage['rows']]
    resultimage = resultimage[0]['image']
    return resultimage


def getDirector(apiId):
    sqlQuery = "select d.directorName from DirectorsMovie dm , Directors d where dm.filmId=%s and d.directorId=dm.directorId"
    MovieDirector = select(sqlQuery, apiId)
    director = [{MovieDirector['headers'][0]: row[0]} for row in MovieDirector['rows']]
    director = director[0]['directorName']
    if director is not None:
        director = "<b>Director</b>: " + director
    else:
        director = ""
    return  director

def getCast(apiId):
    sqlQuery = "select a.actorName from ActorsMovie am , Actors a where filmId=%s and a.actorId=am.actorId"
    MovieActors = select(sqlQuery, apiId)
    result = [{MovieActors['headers'][0]: row[0]} for row in MovieActors['rows']]
    credit = ''
    first = True
    for actor in result:
        if first == False:
            credit = credit + "," + actor['actorName']
        if first == True:
            credit = actor['actorName']
            first = False
    if credit != None:
        credit = "<b>Cast :</b> " + credit
    return  credit

def getSpokenLang(apiId):
    sqlQuery = "select l.LangName from LanguageMovie lm ,Language l where lm.movieId=%s and l.languageId=lm.languageId"
    LanguagesMovie = select(sqlQuery, apiId)
    result = [{LanguagesMovie['headers'][0]: row[0]} for row in LanguagesMovie['rows']]
    first = True;
    for lang in result:
        if first == False:
            movielang = movielang + "," + lang['LangName']
        if first == True:
            movielang = lang['LangName']
            first = False
    if movielang != None:
        movielang = "<b>Spoken Language :</b> " + movielang;
    else:
        movielang=""
    return  movielang

def getSimilarMovie(apiId):
    imagers1 = ""
    links1=""
    try:
        sqlQuery = "select distinct commonMovie.id ,pm.image from (SELECT m2.apiId as" \
                   " id,m2.title as title,  count(*) as count FROM Movie as m, Movie as " \
                   "m2, Actors as a, ActorsMovie as am, ActorsMovie as am2 WHERE m.apiId=%s" \
                   " AND am.filmId<>am2.filmId AND am.filmId=m.apiId  AND am.actorId=a.actorId" \
                   " AND am2.filmId=m2.apiId AND am.actorId=am2.actorId AND  m.langId=m2.langId " \
                   "GROUP BY m2.apiId,m2.title) as commonMovie  , (SELECT distinct m2.apiId as " \
                   "id, m2.title as title, count(*) as count FROM Movie as m, Movie as m2, Genre " \
                   "as g  , MoviesGenre as mg, MoviesGenre as mg2 WHERE m.apiId=%s AND mg.apiId<>mg2.apiId" \
                   " AND  mg.apiId=m.apiId AND mg.genreId=g.genreId AND mg2.apiId=m2.apiId AND" \
                   " mg.genreId=mg2.genreId  GROUP BY m2.apiId,m2.title) as commonGenre , Movie" \
                   " m1,PosterMovie pm where commonMovie.count >3 and commonGenre.count>2    " \
                   "and m1.apiId=commonMovie.id and m1.apiId=commonGenre.id and commonMovie.id= pm.apiId   "
        similarMovie = select(sqlQuery, [apiId, apiId])
        resultS = [{similarMovie['headers'][0]: row[0],
                    similarMovie['headers'][1]: row[1]} for row in similarMovie['rows']]
        shuffle(resultS)
        imagers1 = resultS[0]['image']
        links1 = resultS[0]['id']
        if imagers1 == None:
            imagers1 = ""
    except sql_executor.NoResultsException:
        return imagers1, links1
    return imagers1,links1

def getComputeMovie(apiId):
    imagerc1=""
    linkc1=""
    try :
        sqlQuery ="select distinct m2.apiId ,pm.image from Movie m1,MoviesGenre mg1 , Movie m2,MoviesGenre" \
                  "     mg2 , PosterMovie pm where  m1.apiId=mg1.apiId and (m2.releaseDay between " \
                  "m1.releaseDay - interval 6 month and m1.releaseDay or m2.releaseDay between m1.releaseDay" \
                  "  and m1.releaseDay + interval 6 month  )and m2.apiId=mg2.apiId and mg1.genreId=mg2.genreId" \
                  " and m2.langId= m1.langId and m1.apiId=%s and m1.apiId <>m2.apiId and pm.apiId=m2.apiId "
        commptiveMovie = select(sqlQuery, apiId)
        resultM = [{commptiveMovie['headers'][0]: row[0],
                    commptiveMovie['headers'][1]: row[1]} for row in commptiveMovie['rows']]
        shuffle(resultM)
        imagerc1 = resultM[0]['image']
        linkc1 = resultM[0]['apiId']
        if imagerc1 == None:
            imagerc1 = ""
    except sql_executor.NoResultsException:
        return imagerc1, linkc1
    return imagerc1, linkc1

def getBasicInfo(apiId):
    sqlQuery = "select * from Movie where Movie.apiId=%s"
    resofMovie = select(sqlQuery, apiId)
    resultTitle = [{resofMovie['headers'][1]: row[1]} for row in resofMovie['rows']]
    resultTitle = resultTitle[0]['title']
    imdb = [{resofMovie['headers'][8]: row[8]} for row in resofMovie['rows']]
    if imdb[0]['imdbId']!=None:
        resultimdb = "https://www.imdb.com/title/" + imdb[0]['imdbId']
    else:
        resultimdb=""
    length = [{resofMovie['headers'][4]: row[4]} for row in resofMovie['rows']]
    length = length[0]['length']
    collection = [{resofMovie['headers'][7]: row[7]} for row in resofMovie['rows']]
    collection = collection[0]['collection']
    if collection is not None:
        collection = "<b>Collection</b>: " + collection
    else:
        collection = ""
    webSite = [{resofMovie['headers'][9]: row[9]} for row in resofMovie['rows']]
    webSite = webSite[0]['homePage']
    if webSite != "":
        webSite = "<b>WebSite</b>: " + webSite
    vote = [{resofMovie['headers'][13]: row[13]} for row in resofMovie['rows']]
    vote = vote[0]['voteAvg']
    return resultTitle,resultimdb,length,collection,webSite,vote;