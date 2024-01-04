from flask import Flask
from flask_restful import Api


app = Flask(__name__)
api_app = Api(app)
api_app.app.config["RESTFUL_JSON"] = {"ensure_ascii": False}


import api
from web import *

if __name__ == "__main__":
    app.run(debug=True)
