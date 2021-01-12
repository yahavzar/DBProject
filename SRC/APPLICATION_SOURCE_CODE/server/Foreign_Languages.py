from flask import request, render_template, Blueprint

from DB import sql_executor
from DB.sql_executor import select

lang_page = Blueprint('lang_page', __name__, template_folder='templates')




@lang_page.route('/Foreign-Languages')
def Foreign_Languages():
    sqlQurey = "select distinct Language.langName as language from Language order by language DESC"
    res = select(sqlQurey)
    result = [row[0] for row in res['rows']]
    return render_template('Foreign-Languages.html', languages=result)


@lang_page.route("/Foreign-Languages",methods=['POST','GET'])
def search_foreign_languages():
    if request.method == 'POST':
        title = request.form['dropdown']

    sqlQueryMovie = "select m.title,m.popularity from Movie m , Language l where  m.langId=l.languageId  and l.LangName= %s order by - m.popularity"
    sqlQueryShow = "select s.title , s.popularity from Shows  s, Language l where  s.langId = l.languageId and l.langName = %s order by - s.popularity"
    sqlQuery = "select distinct Language.langName as language from Language order by language DESC"
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