import pymysql
import RetrieveData


def CreateTables():

    ##shows = RetrieveData.fetch_TV_Show()

    connectionObject = pymysql.connect(host="127.0.0.1", user="DbMysql03", password="DbMysql03", db="DbMysql03",port=3305)

    movies = RetrieveData.fetch_movie()
    for movie in movies:
        try:
            # Create a cursor object
            cursorObject = connectionObject.cursor()

            # SQL query string
            sqlQueryMovie = "INSERT INTO Movie (apiId,title,langId,releaseDay,length,budget," \
                            "revenue,collection,imdbId,homePage,status,popularity,voteCount,voteAvg,adult) " \
                            "VALUES (%d,%) "
            sqlQueryMovie = sqlQueryMovie +
            sqlQueryGenre = "INSERT INTO"
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
