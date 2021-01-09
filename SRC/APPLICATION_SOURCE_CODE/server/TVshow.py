from flask import  render_template, Blueprint

from SRC.APPLICATION_SOURCE_CODE.DB import sql_executor
from SRC.APPLICATION_SOURCE_CODE.DB.sql_executor import select
from random import shuffle

tv_page = Blueprint('tvshow', __name__, template_folder='templates')

@tv_page.route('/tvshow/<apiId>')
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
            sqlQuery = "select l.LangName from LanguageShow lm ,Language l where lm.showId=%s and l.languageId=lm.languageId"
            LanguagesShow = select(sqlQuery, apiId)
            result = [{LanguagesShow['headers'][0]: row[0]} for row in LanguagesShow['rows']]
            first = True;
            showlang=""
            for lang in result:
                if first == False:
                    showlang = showlang + "," + lang['LangName']
                if first == True:
                    showlang = lang['LangName']
                    first = False
            if showlang != None:
                showlang = "<b>Spoken Language :</b> " + showlang;
        except sql_executor.NoResultsException:
                credit = ""
        imagerc1 = ""
        linkc1 = ""
        imagers1 = ""
        links1 = ""
    except sql_executor.NoResultsException:
        render_template("Error.html")
    try:
        sqlQuery ="select distinct commonShow.id ,pm.image from (SELECT m2.apiId as  id,m2.title as title,  " \
                  "count(*) as count FROM Shows as m, Shows as m2, Actors as a, ActorsShow as am, ActorsShow " \
                  "as am2 WHERE m.apiId=%s AND am.showId<>am2.showId AND am.showId=m.apiId  AND am.actorId=a.actorId " \
                  " AND am2.showId=m2.apiId AND am.actorId=am2.actorId AND  m.langId=m2.langId  GROUP BY m2.apiId,m2.title) " \
                  "as commonShow  , (SELECT distinct m2.apiId as  id, m2.title as title, count(*) as count FROM Shows as m," \
                  " Shows as m2, Genre as g  , ShowGenre as mg, ShowGenre as mg2 WHERE m.apiId=%s AND mg.apiId<>mg2.apiId AND " \
                  " mg.apiId=m.apiId AND mg.genreId=g.genreId AND mg2.apiId=m2.apiId AND  mg.genreId=mg2.genreId  GROUP BY " \
                  "m2.apiId,m2.title) as commonGenre , Shows  m1,PosterShow pm where commonShow.count >=1 and commonGenre.count>=1 " \
                  " and m1.apiId=commonShow.id and m1.apiId=commonGenre.id and commonShow.id= pm.apiId    "
        similarShow = select(sqlQuery, [apiId, apiId])
        resultS = [{similarShow['headers'][0]: row[0],
                    similarShow['headers'][1]: row[1]} for row in similarShow['rows']]
        shuffle(resultS)
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
        shuffle(resultM)

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
                               ,imagers1=imagers1,links1=links1,imagerc1=imagerc1,linkc1=linkc1,showlang=showlang)

    except sql_executor.NoResultsException:
        return render_template('TV-Show.html',resultTitle=resultTitle,resultOverview=resultOverview,resimage=resultimage,length=length,webSite=webSite,vote=vote,seasons=seasons,producer=producer,credit=credit,showlang=showlang)