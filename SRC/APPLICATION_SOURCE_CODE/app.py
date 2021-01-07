import json

import pymysql
from flask import Flask, render_template, request, abort, redirect
import cgi

from SRC.APPLICATION_SOURCE_CODE.DB import sql_executor
from SRC.APPLICATION_SOURCE_CODE.DB.sql_executor import *

app = Flask(__name__)


@app.route('/', methods=['POST','GET'])
@app.route('/movie', methods=['POST','GET'])
@app.route('/tvshow', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        try:
            movieTitle = request.form['movieTitle']
            if movieTitle != None:
                print("Movie Title = ", movieTitle)
                showApiId = search_similar_show(movieTitle)
                if showApiId == 0:
                    return redirect("/")
                route = "/tvshow/" + str(showApiId)
                print("route =",route)
                return redirect(route, code=302)
        except:
            showTitle = request.form['showTitle']
            if showTitle != None:
                print("Show Title = ", showTitle)
                movieApiId = search_similar_movie(showTitle)
                if movieApiId == 0:
                    return redirect("/")
                route = "/movie/" + str(movieApiId)
                print("route =", route)
                return redirect(route, code=302)

        # else:
        #     showTitle = request.form['showTitle']
        #     print("Show Title = ", showTitle)


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
             "and pm.image is not null limit 5"
    resShow = select(sqlQuery)
    result = [{resShow['headers'][0]: row[0],
               resShow['headers'][1]: row[1]} for row in resShow['rows']]
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
    print("movieApiId = ", movieApiId)
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
    print(res)
    print(res['rows'][0][0])
    tvTitle = res['rows'][0][0]
    # Search for similar show id
    showApiId = get_show_apiId(tvTitle)
    print("showApiId = ", showApiId)
    if showApiId == None:
        print("WASDASDASD")
        return 0
    return showApiId


def search_similar_movie(title):
    # Get Show title id
    print("seach movieee")
    showApiId = get_show_apiId(title)
    if showApiId == None:
        return 0
    print("movieApiId = ", showApiId)

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
    print(res)
    print(res['rows'][0][0])
    movieTitle = res['rows'][0][0]
    # Search for similar show id
    movieApiId = get_movie_apiId(movieTitle)
    print("movieApiId = ", movieApiId)
    if movieApiId == None:
        print("WASDASDASD")
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
    print("in func title = ", title)
    try:
        sqlQuery = " select s.apiId" \
                   " from Shows s where s.title = %s"
        res = select(sqlQuery, title)
        return res['rows'][0][0]
    except sql_executor.NoResultsException:
        return None
    
@app.route("/Search-Movies-or-TV-Shows")
def serach_movie_ortv():
    return render_template('Search-Movies-or-TV-Shows.html')


@app.route("/Search-Movies-or-TV-Shows",methods=['POST','GET'])
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
        sqlQuery = "select * from Shows where Shows.apiId=%s"
        resofShows = select(sqlQuery,apiId)
        length = [{resofShows['headers'][4]: row[4]} for row in resofShows['rows']]
        length = length[0]['length']
        webSite = [{resofShows['headers'][5]: row[5]} for row in resofShows['rows']]
        webSite = webSite[0]['homePage']
        if webSite != "":
            webSite = "<b>WebSite</b>: " + webSite
        vote = [{resofShows['headers'][9]: row[9]} for row in resofShows['rows']]
        vote = vote[0]['voteAvg']
        seasons = [{resofShows['headers'][10]: row[10]} for row in resofShows['rows']]
        seasons = seasons[0]['seasons']
        sqlQuery = "select p.producerName from ProducersShow ps , Producers p where ps.ShowId=%s and p.producerId=ps.producerId"
        try :
            ShowPrducer = select(sqlQuery, apiId)
            producer = [{ShowPrducer['headers'][0]: row[0]} for row in ShowPrducer['rows']]
            producer = producer[0]['producerName']
            if producer is not None:
                producer = "<b>Producer</b>: " + producer
        except sql_executor.NoResultsException:
                producer = ""
        sqlQuery = "select a.actorName from ActorsShow am , Actors a where ShowId=%s and a.actorId=am.actorId"
        try :
            ShowsActors = select(sqlQuery, apiId)
            result = [{ShowsActors['headers'][0]: row[0]} for row in ShowsActors['rows']]
            credit = ''
            first = True
            for actor in result:
                if first == False:
                    credit = credit + "," + actor['actorName']
                if first == True:
                    credit = actor['actorName']
                    first = False
            if credit != None:
                credit = "<b>Cast :</b> " + credit;
        except sql_executor.NoResultsException:
                credit = ""
        imagerc1 = ""
        linkc1 = ""
        imagers1 = ""
        links1 = ""
    except sql_executor.NoResultsException:
        abort(404)
    try:
        sqlQuery ="select distinct commonShow.id ,pm.image from (SELECT m2.apiId as  id,m2.title as title,  " \
                  "count(*) as count FROM Shows as m, Shows as m2, Actors as a, ActorsShow as am, ActorsShow " \
                  "as am2 WHERE m.apiId=%s AND am.showId<>am2.showId AND am.showId=m.apiId  AND am.actorId=a.actorId " \
                  " AND am2.showId=m2.apiId AND am.actorId=am2.actorId AND  m.langId=m2.langId  GROUP BY m2.apiId,m2.title) " \
                  "as commonShow  , (SELECT distinct m2.apiId as  id, m2.title as title, count(*) as count FROM Shows as m," \
                  " Shows as m2, Genre as g  , ShowGenre as mg, ShowGenre as mg2 WHERE m.apiId=%s AND mg.apiId<>mg2.apiId AND " \
                  " mg.apiId=m.apiId AND mg.genreId=g.genreId AND mg2.apiId=m2.apiId AND  mg.genreId=mg2.genreId  GROUP BY " \
                  "m2.apiId,m2.title) as commonGenre , Shows  m1,PosterShow pm where commonShow.count >=1 and commonGenre.count>=1 " \
                  " and m1.apiId=commonShow.id and m1.apiId=commonGenre.id and commonShow.id= pm.apiId limit 2   "
        similarShow = select(sqlQuery, [apiId, apiId])
        resultS = [{similarShow['headers'][0]: row[0],
                    similarShow['headers'][1]: row[1]} for row in similarShow['rows']]
        imagers1 = resultS[0]['image']
        links1 = resultS[0]['id']
    except sql_executor.NoResultsException:
        pass
    try:
        sqlQuery = "select distinct m2.apiId ,pm.image from Shows m1,ShowGenre mg1 " \
                   ", Shows m2, ShowGenre  mg2 ,PosterShow pm where  m1.apiId=mg1.apiId" \
                   " and m2.releaseDay between m1.releaseDay - interval 6 month and m1.releaseDay " \
                   " and m2.apiId=mg2.apiId and mg1.genreId=mg2.genreId and m2.langId= m1.langId" \
                   " and m1.apiId=%s and m1.apiId <>m2.apiId and pm.apiId=m2.apiId"
        commptiveShow = select(sqlQuery, apiId)
        resultM = [{commptiveShow['headers'][0]: row[0],
                    commptiveShow['headers'][1]: row[1]} for row in commptiveShow['rows']]
        imagerc1 = resultM[0]['image']
        linkc1 = resultM[0]['apiId']
        if imagerc1 == "":
            imagerc1 = "./static/noimage.png"
            linkc1 = apiId
        else:
            imagerc1 = "https://image.tmdb.org/t/p/w500/" + imagerc1
        if imagers1 == "":
            imagers1 = "../static/noimage.png"
            links1 = apiId
        else:
            imagers1 = "https://image.tmdb.org/t/p/w500/" + imagers1

        return render_template('TV-Show.html',resultTitle=resultTitle,resultOverview=resultOverview,resimage=resultimage,length=length,webSite=webSite,vote=vote,seasons=seasons,producer=producer,credit=credit
                               ,imagers1=imagers1,links1=links1,imagerc1=imagerc1,linkc1=linkc1)

    except sql_executor.NoResultsException:
        return render_template('TV-Show.html',resultTitle=resultTitle,resultOverview=resultOverview,resimage=resultimage,length=length,webSite=webSite,vote=vote,seasons=seasons,producer=producer,credit=credit)

@app.route('/movie/<apiId>')
def movie(apiId):
    try :
        sqlQuery = "select * from Movie where Movie.apiId=%s"
        resofMovie = select(sqlQuery,apiId)
        resultTitle = [{resofMovie['headers'][1]: row[1]} for row in resofMovie['rows']]
        resultTitle=resultTitle[0]['title']
        sqlQuery = "select overview from MovieOverview where MovieOverview.filmId=%s"
        resOverView= select(sqlQuery,apiId)
        resultOverview = [{resOverView['headers'][0]: row[0]} for row in resOverView['rows']]
        resultOverview=resultOverview[0]['overview']
        sqlQuery="select image from PosterMovie where apiId=%s"
        resimage = select(sqlQuery,apiId)
        resultimage = [{resimage['headers'][0]: row[0]} for row in resimage['rows']]
        resultimage=resultimage[0]['image']
        imdb = [{resofMovie['headers'][8]: row[8]} for row in resofMovie['rows']]
        resultimdb="https://www.imdb.com/title/"+imdb[0]['imdbId']
        length = [{resofMovie['headers'][4]: row[4]} for row in resofMovie['rows']]
        length=length[0]['length']
        collection = [{resofMovie['headers'][7]: row[7]} for row in resofMovie['rows']]
        collection=collection[0]['collection']
        if collection is not None :
            collection = "<b>Collection</b>: " + collection
        else :
            collection=""
        webSite = [{resofMovie['headers'][9]: row[9]} for row in resofMovie['rows']]
        webSite = webSite[0]['homePage']
        if webSite != "":
            webSite = "<b>WebSite</b>: " + webSite
        vote = [{resofMovie['headers'][13]: row[13]} for row in resofMovie['rows']]
        vote = vote[0]['voteAvg']
        sqlQuery = "select d.directorName from DirectorsMovie dm , Directors d where dm.filmId=%s and d.directorId=dm.directorId"
        MovieDirector= select(sqlQuery,apiId)
        director = [{MovieDirector['headers'][0]: row[0]} for row in MovieDirector['rows']]
        director = director[0]['directorName']
        if director is not None :
            director = "<b>Director</b>: " + director
        else :
            director=""
        sqlQuery = "select a.actorName from ActorsMovie am , Actors a where filmId=%s and a.actorId=am.actorId"
        MovieActors= select(sqlQuery,apiId)
        result = [{MovieActors['headers'][0]: row[0]} for row in MovieActors['rows']]
        credit=''
        first= True
        for actor in result:
            if  first==False:
                credit = credit +"," +actor['actorName']
            if first ==True :
                credit  = actor['actorName']
                first=False
        if credit != None:
            credit = "<b>Cast :</b> "  + credit;
        imagerc1 = ""
        linkc1 = ""
        imagers1 = ""
        links1 = ""
    except sql_executor.NoResultsException:
        abort(404)
    try :
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
                   "and m1.apiId=commonMovie.id and m1.apiId=commonGenre.id and commonMovie.id= pm.apiId limit 2   "
        similarMovie = select(sqlQuery,[ apiId,apiId])
        resultS = [{similarMovie['headers'][0]: row[0],
                   similarMovie['headers'][1]: row[1]} for row in similarMovie['rows']]
        imagers1 = resultS[0]['image']
        links1 = resultS[0]['id']
    except sql_executor.NoResultsException:
        pass
    try:
        sqlQuery = "select distinct m2.apiId ,pm.image from Movie m1,MoviesGenre mg1 , Movie m2, " \
                   "MoviesGenre     mg2 , PosterMovie pm where  m1.apiId=mg1.apiId and m2.releaseDay " \
                   "between m1.releaseDay - interval 6 month and m1.releaseDay  and m2.apiId=mg2.apiId " \
                   "and mg1.genreId=mg2.genreId and m2.langId= m1.langId and m1.apiId=%s and m1.apiId <>m2.apiId and pm.apiId=m2.apiId limit 2"
        commptiveMovie = select(sqlQuery, apiId)
        resultM = [{commptiveMovie['headers'][0]: row[0],
                   commptiveMovie['headers'][1]: row[1]} for row in commptiveMovie['rows']]

        imagerc1 = resultM[0]['image']
        linkc1 = resultM[0]['apiId']
        if imagerc1=="":
            imagerc1= "./static/noimage.png"
            linkc1=apiId
        else :
            imagerc1= "https://image.tmdb.org/t/p/w500/" +imagerc1
        if imagers1=="":
            imagers1= "../static/noimage.png"
            links1=apiId
        else :
            imagers1= "https://image.tmdb.org/t/p/w500/" +imagers1
        return render_template('Movie.html',resultTitle=resultTitle,resultOverview=resultOverview,resimage=resultimage,resultimdb=resultimdb,length=length,collection=collection,webSite=webSite,vote=vote,director=director,credit=credit,
                               imagers1=imagers1,links1=links1,imagerc1=imagerc1,linkc1=linkc1)
    except sql_executor.NoResultsException:
        return render_template('Movie.html',resultTitle=resultTitle,resultOverview=resultOverview,resimage=resultimage,resultimdb=resultimdb,length=length,collection=collection,webSite=webSite,vote=vote,director=director,credit=credit)


@app.route('/search')
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
            abort(404)




@app.route('/Credits')
def Credits():
    sqlQuery = "select directorName from Directors   "
    res = select(sqlQuery)
    result = [{res['headers'][0]: row[0]} for row in res['rows']]
    sqlQuery = "select producerName from Producers   "
    res2 = select(sqlQuery)
    result2 = [{res2['headers'][0]: row[0]} for row in res2['rows']]
    sqlQuery = "select a.actorName,d.directorName, count(*) from Actors a, ActorsMovie am" \
               ",Directors d,DirectorsMovie dm , Movie m where a.actorId= am.actorId and " \
               "d.directorId=dm.directorId and am.filmId=dm.filmId and m.apiId=am.filmId " \
               "and m.voteAvg>5 group by a.actorName,d.directorName Having count(*)>7"
    res3 = select(sqlQuery)
    result3 = [{res3['headers'][0]: row[0], res3['headers'][1]: row[1], res3['headers'][2]: row[2]} for row in
               res3['rows']]
    sqlQuery = "select a.actorName,p.producerName, count(*) from Actors a,  ActorsShow acs" \
               ",Producers p,ProducersShow ps , Shows s where a.actorId= acs.actorId and " \
               " p.producerId=ps.producerId and acs.actorId=ps.showId and s.apiId=ps.showId " \
               "and s.voteAvg>5 group by a.actorName,p.producerName Having count(*)>7"
    res4 = select(sqlQuery)
    result4 = [{res4['headers'][0]: row[0], res4['headers'][1]: row[1], res4['headers'][2]: row[2]} for row in
               res4['rows']]
    return render_template('Credits.html', res=json.dumps(result), res2=json.dumps(result2), res3=json.dumps(result3),
                           res4=json.dumps(result4))

@app.route('/Actors')
def Actors():
    sqlQuery = "select distinct Genre.genreName as title from Genre"
    res=select(sqlQuery)
    result = [k[0] for k in res["rows"]]
    return render_template('Actors.html',genres=result)

@app.route("/Actors",methods=['POST','GET'])
def search_recommended_actors():
    if request.method == 'POST':
        if request.form.get("dropdown"):
            title = request.form['dropdown']
            sqlQuery = "select * from (select a.actorName as title, count(*) as cnt from Actors a, MoviesGenre mg, Movie m , ActorsMovie am , Genre g , (select Genre.genreId as id  from Genre  where genreName=%s) AS temp,  (select g.genreId,g.genreName,avg(voteCount) as avgvotecount  from Movie m , Genre g, MoviesGenre mg  where m.apiId=mg.apiId and g.genreId=mg.genreId  group by g.genreId ) as GenreAvgVoteCount  where  m.apiId=mg.apiId and a.actorId=am.actorId and am.filmId=m.apiId and g.genreName=%s and  temp.id=mg.genreId and  m.voteCount>GenreAvgVoteCount.avgvotecount and m.voteAvg>8 and temp.id= GenreAvgVoteCount.genreId group by a.actorId union select a.actorName as name, count(*) as cnt from Actors a, ShowGenre mg, Shows m , ActorsShow am , Genre g , (select Genre.genreId as id from Genre where genreName=%s) AS temp, (select g.genreId,g.genreName,avg(voteCount) as avgvotecount from Shows m , Genre g, ShowGenre mg where m.apiId=mg.apiId and g.genreId=mg.genreId group by g.genreId ) as GenreAvgVoteCount  where  m.apiId=mg.apiId and a.actorId=am.actorId and am.showId=m.apiId and g.genreName=%s and  temp.id=mg.genreId and  m.voteCount>GenreAvgVoteCount.avgvotecount and m.voteAvg>8 and temp.id= GenreAvgVoteCount.genreId  group by a.actorId) as temp order by -cnt;"
            try:
                res = select(sqlQuery, [title, title, title, title])
                result = [{res['headers'][0]: row[0]} for row in res['rows']]
                sqlQuery = "select distinct Genre.genreName as title from Genre"
                res2 = select(sqlQuery)
                result2 = [k[0] for k in res2["rows"]]
                return render_template('Actors.html', res=result, genres=result2)
            except sql_executor.NoResultsException:
                sqlQuery = "select distinct Genre.genreName as title from Genre"
                res2 = select(sqlQuery)
                result2 = [k[0] for k in res2["rows"]]
                return render_template('Actors.html', genres=result2)
        elif request.form.get("startDate1"): # returns actors who participated in at least 3 movies during the time period
            date = request.form['startDate1'].split(" - ")
            moviesNumber = 3
            tempStart = date[0].split("/")
            tempEnd = date[1].split("/")
            start = tempStart[2]+"-"+tempStart[0]+"-"+tempStart[1]
            end = tempEnd[2] + "-" + tempEnd[0] + "-" + tempEnd[1]

            sqlQuery = "select title from(select a1.actorName as title, count(*) as cnt, a1.actorId as id " \
                       "from Movie m1 , Actors a1 , ActorsMovie am1 " \
                       "where a1.actorId=am1.actorId and m1.apiId=am1.filmId and m1.releaseDay between %s and %s " \
                       "group by a1.actorId " \
                       "having count(*)>%s) as temp " \
                       "group by temp.id " \
                       "order by temp.cnt DESC " \
                       "limit 20"
            try:
                res = select(sqlQuery, [start, end, moviesNumber])
                result = [{res['headers'][0]: row[0]} for row in res['rows']]
                sqlQuery = "select distinct Genre.genreName as title from Genre"
                res2 = select(sqlQuery)
                result2 = [k[0] for k in res2["rows"]]
                return render_template('Actors.html', resKnown=result, genres=result2)
            except sql_executor.NoResultsException:
                sqlQuery = "select distinct Genre.genreName as title from Genre"
                res2 = select(sqlQuery)
                result2 = [k[0] for k in res2["rows"]]
                return render_template('Actors.html', genres=result2)
        elif request.form.get("startDate2"):
            # actors who have at least 3 movies between those dates with a popularity above 100 and a revenue-to-budget ratio of at least 6.5
            date = request.form['startDate2'].split(" - ")
            moviesNumber = 3
            revenueToBudeget = 6.5
            popularity = 100
            tempStart = date[0].split("/")
            tempEnd = date[1].split("/")
            start = tempStart[2]+"-"+tempStart[0]+"-"+tempStart[1]
            end = tempEnd[2] + "-" + tempEnd[0] + "-" + tempEnd[1]

            sqlQuery = "select title from( select title, cnt from(select a1.actorName as title, count(*) " \
                       "as cnt, a1.actorId as id from Movie m1 , Actors a1 , ActorsMovie am1 " \
                       "where a1.actorId=am1.actorId and m1.apiId=am1.filmId and m1.releaseDay " \
                       "between %s and %s and ((m1.budget*%s)<m1.revenue) and (m1.popularity>%s) " \
                       "group by a1.actorId having count(*)>%s) as temp " \
                       "group by temp.id order by temp.cnt DESC limit 20) as temp"
            try:
                res = select(sqlQuery, [start, end, revenueToBudeget, popularity, moviesNumber])
                result = [{res['headers'][0]: row[0]} for row in res['rows']]
                sqlQuery = "select distinct Genre.genreName as title from Genre"
                res2 = select(sqlQuery)
                result2 = [k[0] for k in res2["rows"]]
                return render_template('Actors.html', resSuc=result, genres=result2)
            except sql_executor.NoResultsException:
                sqlQuery = "select distinct Genre.genreName as title from Genre"
                res2 = select(sqlQuery)
                result2 = [k[0] for k in res2["rows"]]
                return render_template('Actors.html', genres=result2)
        elif request.form.get('actorName'):
            actor = request.form['actorName']
            sqlQuery = "select Movie.title from Movie, ActorsMovie, Actors " \
                       "where Actors.actorName = %s and ActorsMovie.actorId=Actors.actorId " \
                       "and ActorsMovie.filmId=Movie.apiId order by Movie.popularity Limit 50"
            try:
                res = select(sqlQuery, [actor])
                result = [{res['headers'][0]: row[0]} for row in res['rows']]
                sqlQuery = "select distinct Genre.genreName as title from Genre"
                res2 = select(sqlQuery)
                result2 = [k[0] for k in res2["rows"]]
                return render_template('Actors.html', resNames=result, genres=result2)
            except sql_executor.NoResultsException:
                sqlQuery = "select distinct Genre.genreName as title from Genre"
                res2 = select(sqlQuery)
                result2 = [k[0] for k in res2["rows"]]
                return render_template('Actors.html', genres=result2)


@app.route('/Foreign-Languages')
def Foreign_Languages():
    sqlQurey = "select distinct Language.languageName as language from Language order by language DESC"
    res = select(sqlQurey)
    result = [row[0] for row in res['rows']]
    return render_template('Foreign-Languages.html', languages=result)

@app.route("/Foreign-Languages",methods=['POST','GET'])
def search_foreign_languages():
    if request.method == 'POST':
        title = request.form['dropdown']

    sqlQueryMovie = "select Movie.title, Movie.popularity from Movie, LanguageMovie, Language where Movie.apiId = LanguageMovie.movieId and Movie.langId = LanguageMovie.languageId and LanguageMovie.languageId = Language.languageId and Language.languageName = %s order by - Movie.popularity"
    sqlQueryShow = "select Shows.title , Shows.popularity from Shows, LanguageShow, Language where Shows.apiId = LanguageShow.showId and Shows.langId = LanguageShow.languageId and LanguageShow.languageId = Language.languageId and Language.languageName = %s order by - Shows.popularity"
    sqlQuery = "select distinct Language.languageName as language from Language order by language"
    resLang = select(sqlQuery)
    languages = [row[0] for row in resLang["rows"]]

    try:
        resMovie = select(sqlQueryMovie, title)
        resultMovie = [{resMovie['headers'][0]: row[0] ,
                        resMovie['headers'][1]: row[1]} for row in resMovie['rows']]
        try:
            resShow = select(sqlQueryShow, title)
            resultShow = [{resShow['headers'][0]: row[0],
                           resShow['headers'][1]: row[1] } for row in resShow['rows']]
            return render_template('Foreign-Languages.html', resMovie=resultMovie, resShow=resultShow, languages=languages)
        except sql_executor.NoResultsException:
            return render_template('Foreign-Languages.html', resMovie=resultMovie, resShow=None, languages=languages)
    except sql_executor.NoResultsException:
        try:
            resShow = select(sqlQueryShow, title)
            resultShow = [{resShow['headers'][0]: row[0],
                           resShow['headers'][1]: row[1] } for row in resShow['rows']]
            return render_template('Foreign-Languages.html', resMovie=None, resShow=resultShow, languages=languages)
        except sql_executor.NoResultsException:
            return render_template('Foreign-Languages.html', languages=languages)


@app.route('/testmoce')
def movie_to_html():
    sqlQuery = "select apiId,title from Movie   "
    res = select(sqlQuery)
    result = [{res['headers'][0]: row[0],
                 res['headers'][1]: row[1]} for row in res['rows']]
    return render_template('testmoce.html', res=json.dumps(result))



if __name__ == '__main__':
   app.run()
   #app.run(host="delta-tomcat-vm.cs.tau.ac.il", port="40494") (for server)

