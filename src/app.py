from flask import Flask
from flask_restful import Api
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)


def create_api_app():
    api_app = Api(app, default_mediatype="application/xml")
    api_app.app.config["RESTFUL_JSON"] = {"ensure_ascii": False}
    return api_app


import api
from web import *

if __name__ == "__main__":
    app.run(debug=True)
