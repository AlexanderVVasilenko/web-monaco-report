from flask import Flask
from flask_restful import Api

from api import ReportResource, DriverResource, DriversListResource

app = Flask(__name__)
api = Api(app)
api.app.config["RESTFUL_JSON"] = {"ensure_ascii": False}

version = "v1"

api.add_resource(ReportResource, f"/api/{version}/report", endpoint="full_report")
api.add_resource(
    DriverResource,
    f"/api/{version}/report/drivers/<string:driver_id>",
    endpoint="driver_detail",
)
api.add_resource(
    DriversListResource, f"/api/{version}/report/drivers", endpoint="drivers_list"
)


if __name__ == "__main__":
    app.run(debug=True)
