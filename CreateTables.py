import pymysql
import RetrieveData


def CreateTables():

    ##shows = RetrieveData.fetch_TV_Show()

    connectionObject = pymysql.connect(host="127.0.0.1", user="DbMysql03", password="DbMysql03", db="DbMysql03",port=3305)
    count=0
    movies = RetrieveData.fetch_movie()
    for movie in movies:
         try:
            # Create a cursor object
            cursorObject = connectionObject.cursor()

            # SQL query string
            # sqlQueryMovie = "INSERT INTO Movie (apiId,title,langId,releaseDay,length,budget," \
            #                 "revenue,collection,imdbId,homePage,status,popularity,voteCount,voteAvg,adult)  \
            #                 "VALUES (%d, %s, %d, %s, %d, %d, %d, %s, %s, %s, %s, %f, %d, %f, %b)"
            # values = (movie.api_id, movie.title, 0, None, movie.runtime, movie.budget, movie.revenue
            #           ,None, movie.imdb_id, movie.homepage, movie.status, movie.popularity, movie.vote_count, movie.vote_avg, movie.adult)

            sqlQueryMovie = "INSERT INTO Movie (apiId,title,langId,releaseDay,length,budget,revenue,collection,imdbId,homePage,status,popularity,voteCount,voteAvg,adult) VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            values = (movie.api_id, movie.title,0,movie.release_date,movie.runtime, movie.budget, movie.revenue,movie.collection,movie.imdb_id, movie.homepage, movie.status, movie.popularity, movie.vote_count, movie.vote_avg, movie.adult)
            # Execute the sqlQuery

            cursorObject.execute(sqlQueryMovie, values)
            connectionObject.commit()
         except Exception as e:
            print("Exeception occured:{}".format(e))
            count+=1
            continue


    print("number of failed is %d",count)


