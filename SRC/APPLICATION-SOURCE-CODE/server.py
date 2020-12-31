from flask import Flask, render_template, request

from SRC import Queries

app = Flask(__name__)

@app.route('/search')
def search_return_html():
    query = request.args.get('query')
    Queries.similar_movie()
    # with connector get to your mysql server and query the DB
    # return the answer to number_of_songs var.
    number_of_songs = 8 #should be retrieved from the DB
    return render_template('searchResults.html', count=number_of_songs, query=query)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(port="8888", debug=True)