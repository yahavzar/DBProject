from flask import Flask

from SRC.APPLICATION_SOURCE_CODE.server.Actors import actors_page
from SRC.APPLICATION_SOURCE_CODE.server.Front_page import home_page
from SRC.APPLICATION_SOURCE_CODE.server.TVshow import tv_page
from SRC.APPLICATION_SOURCE_CODE.server.Foreign_Languages import lang_page
from SRC.APPLICATION_SOURCE_CODE.server.credits import credit_page
from SRC.APPLICATION_SOURCE_CODE.server.search import search_page
from SRC.APPLICATION_SOURCE_CODE.templates.movie import movie_page

app = Flask(__name__)
app.register_blueprint(actors_page)
app.register_blueprint(tv_page)
app.register_blueprint(lang_page)
app.register_blueprint(movie_page)
app.register_blueprint(credit_page)
app.register_blueprint(search_page)
app.register_blueprint(home_page)




if __name__ == '__main__':
   app.run()
   #app.run(host="delta-tomcat-vm.cs.tau.ac.il", port="40494") (for server)

