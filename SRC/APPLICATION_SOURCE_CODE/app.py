from flask import Flask

from server.Actors import actors_page
from server.Front_page import home_page
from server.TVshow import tv_page
from server.Foreign_Languages import lang_page
from server.credits import credit_page
from server.search import search_page
from server.movie import movie_page

app = Flask(__name__)

app.register_blueprint(actors_page)
app.register_blueprint(tv_page)
app.register_blueprint(lang_page)
app.register_blueprint(movie_page)
app.register_blueprint(credit_page)
app.register_blueprint(search_page)
app.register_blueprint(home_page)



if __name__ == '__main__':
   app.run(host="delta-tomcat-vm.cs.tau.ac.il", port="40494")

