import RetrieveData
from flask import Flask
import pymysql

app = Flask(__name__)


@app.route("/")
def test():
    return "hello"


if __name__ == '__main__':
    # RetrieveData.main()
    # cnx = pymysql.connect(user="sakila",password="sakila",host="localhost",database="sakila",port=3305)
    # cur = cnx.cursor()
    # cur.execute("SELECT * FROM actor")
    # for i in range (1,10):
    #     row = cur.fetchone()
    #     print (row[0],row[1])
    connectionObject    = pymysql.connect(host="127.0.0.1",user="DbMysql03", password="DbMysql03",db="DbMysql03",port=3305)

    try:

        # Create a cursor object

        cursorObject = connectionObject.cursor()

        # SQL query string

        sqlQuery = "CREATE TABLE Movie(id int, title varchar(32))"

        # Execute the sqlQuery

        cursorObject.execute(sqlQuery)

        # SQL query string

        sqlQuery = "show tables"

        # Execute the sqlQuery

        cursorObject.execute(sqlQuery)

        # Fetch all the rows

        rows = cursorObject.fetchall()

        for row in rows:
            print(row)

    except Exception as e:

        print("Exeception occured:{}".format(e))

    finally:

        connectionObject.close()
