import pymysql
import json
import traceback




def select(query, args=None):
    cursor = None
    try:
        cursors = __execute(queries=[{'query': query, 'args': args}])
        cursor = cursors[0]
        res = {'headers': [], 'rows': []}
        for row in cursor:
            if len(res['headers']) == 0:
                res['headers'] = list(row.keys())
            res['rows'].append([row[k] for k in res['headers']])
        if len(res['headers']) == 0:
            raise NoResultsException('No results found')
        else:
            return res
    except Exception as e:
        if type(e) == NoResultsException:
            raise e
        raise Exception('Select query failed. Query: {} Error Traceback: {}'.format(query, traceback.format_exc()))
    finally:
        if cursor:
            cursor.close()


def __execute(queries):
    sql_hostname, sql_username, sql_password, sql_main_database, sql_port = get_mysql_config()
    db = pymysql.connect(host=sql_hostname,
                         user=sql_username,
                         passwd=sql_password,
                         db=sql_main_database,
                         port=sql_port)
    cursors = []
    for query in queries:
        cur = db.cursor(pymysql.cursors.DictCursor)
        cur.execute(query=query['query'], args=query.get('args', None))
        db.commit()
        cursors.append(cur)
    return cursors


def get_mysql_config():
    with open("./DB/config/mysql_config.json") as mysql_conf_file:
        mysql_conf = json.load(mysql_conf_file)
        sql_hostname = mysql_conf['sql_hostname']
        sql_username = mysql_conf['sql_username']
        sql_password = mysql_conf['sql_password']
        sql_main_database = mysql_conf['sql_main_database']
        sql_port = mysql_conf['sql_port']
        mysql_conf_file.close()
    return sql_hostname, sql_username, sql_password, sql_main_database, sql_port


# To separate errors 404 and 500 in UI
class NoResultsException(Exception):
    def __init__(self, message):
        self.message = message

