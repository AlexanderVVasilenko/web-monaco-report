from flasgger import swag_from
from flask import request, make_response
from flask_restful import Resource
import xmltodict


from app import create_api_app
from retrieve_data import get_db_report, get_db_driver_list, get_db_driver_data

api_app = create_api_app()


def convert_to_xml(data: list | dict) -> str:
    xml_data = xmltodict.unparse({"racers": {"racer": data}}, full_document=False)
    return xml_data


class ReportResource(Resource):
    @swag_from("swagger/report.yml")
    def get(self) -> (dict, int):
        order = request.args.get("order", "asc")
        format_type = request.args.get("format", "json")
        sorted_report = get_db_report(order)
        if not sorted_report:
            return {"error": "Invalid order parameter"}, 400

        if format_type not in ["json", "xml"]:
            return {"error": "Invalid format parameter"}, 406

        match format_type:
            case "json":
                return {"racers": sorted_report}, 200
            case "xml":
                xml_data = convert_to_xml(sorted_report)
                response = make_response(
                    xml_data, 200, {"Content-Type": "application/xml"}
                )
                return response


class DriversListResource(Resource):
    @swag_from("swagger/drivers_list.yml")
    def get(self) -> (dict, int):
        format_type = request.args.get("format", "json")
        if format_type not in ["json", "xml"]:
            return {"error": "Invalid format parameter"}, 406

        order = request.args.get("order", "asc")
        sorted_racers = get_db_driver_list(order)
        if not sorted_racers:
            return {"error": "Invalid order parameter"}, 400

        match format_type:
            case "json":
                return {"racers": sorted_racers}, 200
            case "xml":
                xml_data = convert_to_xml(sorted_racers)
                response = make_response(
                    xml_data, 200, {"Content-Type": "application/xml"}
                )
                return response


class DriverResource(Resource):
    @swag_from("swagger/driver_details.yml")
    def get(self, driver_id: str) -> (dict, int):
        format_type = request.args.get("format", "json")
        if format_type not in ["json", "xml"]:
            return {"error": "Invalid format parameter"}, 406

        racer_data = get_db_driver_data(driver_id)
        if racer_data:
            match format_type:
                case "json":
                    return {"racer": racer_data}, 200
                case "xml":
                    xml_data = convert_to_xml(racer_data)
                    return make_response(
                        xml_data, 200, {"Content-Type": "application/xml"}
                    )
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
