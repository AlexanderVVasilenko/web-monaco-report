from flask import request
from flask_restful import Resource

from app import api_app
from package_interaction import (
    top_racers,
    remaining_racers,
    reformat_racers_to_dict,
    get_report,
    get_driver_list,
)


class ReportResource(Resource):
    @staticmethod
    def get() -> (dict, int):
        order = request.args.get("order", "asc")
        sorted_racers = get_report(order)
        if not sorted_racers:
            return {"error": "Invalid order parameter"}, 400

        return {"racers": reformat_racers_to_dict(sorted_racers)}, 200


class DriversListResource(Resource):
    @staticmethod
    def get() -> (dict, int):
        order = request.args.get("order", "asc")
        sorted_racers = get_driver_list(order)
        if not sorted_racers:
            return {"error": "Invalid order parameter"}, 400

        return {"racers": sorted_racers}, 200


class DriverResource(Resource):
    @staticmethod
    def get(driver_id: str) -> (dict, int):
        for racer in top_racers + remaining_racers:
            if racer.driver_id == driver_id:
                racer = reformat_racers_to_dict([racer])[0]
                return {"racer": racer}, 200
        return {"error": "Driver not found"}, 404


version = "v1"

api_app.add_resource(ReportResource, f"/api/{version}/report", endpoint="full_report")
api_app.add_resource(
    DriverResource,
    f"/api/{version}/report/drivers/<string:driver_id>",
    endpoint="driver_detail",
)
api_app.add_resource(
    DriversListResource, f"/api/{version}/report/drivers", endpoint="drivers_list"
)
