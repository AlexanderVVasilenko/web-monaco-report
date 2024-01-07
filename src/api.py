from flasgger import swag_from
from flask import request, make_response
from flask_restful import Resource
import xmltodict

from app import api_app
from package_interaction import (
    top_racers,
    remaining_racers,
    reformat_racers_to_dict,
    get_report,
    get_driver_list,
)


def convert_to_xml(data: list | dict) -> str:
    xml_data = xmltodict.unparse({"racers": {"racer": data}}, full_document=False)
    return xml_data


class ReportResource(Resource):
    @swag_from("swagger/report.yml")
    def get(self) -> (dict, int):
        order = request.args.get("order", "asc")
        format_type = request.args.get("format", "json")
        sorted_racers = get_report(order)
        if not sorted_racers:
            return {"error": "Invalid order parameter"}, 400

        if format_type not in ["json", "xml"]:
            return {"error": "Invalid format parameter"}, 406

        if format_type == "json":
            return {"racers": sorted_racers}, 200
        elif format_type == "xml":
            xml_data = convert_to_xml(sorted_racers)
            response = make_response(xml_data, 200, {"Content-Type": "application/xml"})
            return response


class DriversListResource(Resource):
    @swag_from("swagger/drivers_list.yml")
    def get(self) -> (dict, int):
        format_type = request.args.get("format", "json")
        if format_type not in ["json", "xml"]:
            return {"error": "Invalid format parameter"}, 406

        order = request.args.get("order", "asc")
        sorted_racers = get_driver_list(order)
        if not sorted_racers:
            return {"error": "Invalid order parameter"}, 400

        if format_type == "json":
            return {"racers": sorted_racers}, 200
        elif format_type == "xml":
            xml_data = convert_to_xml(sorted_racers)
            response = make_response(xml_data, 200, {"Content-Type": "application/xml"})
            return response


class DriverResource(Resource):
    @swag_from("swagger/driver_details.yml")
    def get(self, driver_id: str) -> (dict, int):
        format_type = request.args.get("format", "json")
        if format_type not in ["json", "xml"]:
            return {"error": "Invalid format parameter"}, 406

        for racer in top_racers + remaining_racers:
            if racer.driver_id == driver_id:
                racer_data = reformat_racers_to_dict([racer])[0]
                if format_type == "json":
                    return {"racer": racer_data}, 200
                elif format_type == "xml":
                    xml_data = convert_to_xml(racer_data)
                    response = make_response(
                        xml_data, 200, {"Content-Type": "application/xml"}
                    )
                    return response
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
