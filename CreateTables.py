import pymysql
import RetrieveData


def CreateTables():

    ##shows = RetrieveData.fetch_TV_Show()

    connectionObject = pymysql.connect(host="127.0.0.1", user="DbMysql03", password="DbMysql03", db="DbMysql03",port=3305)

    movies = RetrieveData.fetch_movie()
    for movie in movies:
        # try:
            # Create a cursor object
            cursorObject = connectionObject.cursor()

            # SQL query string
            sqlQueryMovie = "INSERT INTO Movie (apiId,title,langId,releaseDay,length,budget," \
                            "revenue,collection,imdbId,homePage,status,popularity,voteCount,voteAvg,adult) " \
                            "VALUES (%d, %s, %d, %s, %d, %d, %d, %s, %s, %s, %s, %f, %d, %f, %b)"
            values = (movie.api_id, movie.title, 0, None, movie.runtime, movie.budget, movie.revenue
                      ,movie.collection, movie.imdb_id, movie.homepage, movie.status, movie.popularity, movie.vote_count, movie.vote_avg, movie.adult)
            sqlQueryGenre = "INSERT INTO"
            # Execute the sqlQuery

            cursorObject.execute(sqlQueryMovie, values)
            connectionObject.commit()


            # Fetch all the rows

            rows = cursorObject.fetchall()

            for row in rows:
                print(row)

        # except Exception as e:
        #
        #     print("Exeception occured:{}".format(e))


