
from flask import  render_template, Blueprint
import json

from SRC.APPLICATION_SOURCE_CODE.DB.sql_executor import select

credit_page = Blueprint('credit', __name__, template_folder='templates')

@credit_page.route('/Credits')
def Credits():
    sqlQuery="select d.directorName , count(*) from Directors d , DirectorsMovie dm where  d.directorId=dm.directorId group by d.directorId order by -count(*)"
    res = select(sqlQuery)
    result = [{res['headers'][0]: row[0],
               res['headers'][1]: row[1]} for row in res['rows']]
    sqlQuery = "select p.producerName , count(*) from Producers p , ProducersShow ps where  p.producerId=ps.producerId group by p.producerId order by -count(*)"
    res2 = select(sqlQuery)
    result2 =[{res2['headers'][0]: row[0],
               res2['headers'][1]: row[1]} for row in res2['rows']]
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

