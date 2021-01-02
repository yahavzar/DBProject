# from sshtunnel import SSHTunnelForwarder # Uncomment this import  to work locally
USE_SSH = False  # False = local, True = production
DEBUG = False  # False = local, True = production
HOST = "0.0.0.0"
PORT = 40444
BASE_URL = HOST + ":" + str(PORT)

