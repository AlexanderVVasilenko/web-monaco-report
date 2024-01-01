from flask import Flask, render_template, request, redirect, url_for
from flask_restful import Api, Resource
from f1_racing_reports.report import parse_logs, load_abbreviations

app = Flask(__name__)
api = Api(app)

start_log_file = "src/start.log"
end_log_file = "src/end.log"
abbreviations_file_path = "src/abbreviations.txt"

abbreviations = load_abbreviations(abbreviations_file_path)

top_racers, remaining_racers = parse_logs(start_log_file, end_log_file, abbreviations)


def get_report(order: str = None) -> list | None:
    if order == "asc":
        return top_racers + remaining_racers
    elif order == "desc":
        return remaining_racers[::-1] + top_racers[::-1]


def get_driver_list(order: str = None) -> list | None:
    if order == "asc":
        return sorted(abbreviations, key=lambda x: x[1])
    elif order == "desc":
        return sorted(abbreviations, key=lambda x: x[1], reverse=True)


@app.route("/report/", methods=["GET"])
def report():
    order = request.args.get("order", "asc")
    sorted_racers = get_report(order)
    if not sorted_racers:
        return redirect(url_for("report"))

    return render_template("report.html", racers=sorted_racers)


@app.route("/report/drivers/", methods=["GET"])
def driver_list():
    order = request.args.get("order", "asc")
    driver_id = request.args.get('driver_id')

    if driver_id:
        for racer in top_racers + remaining_racers:
            if racer.driver_id == driver_id:
                return render_template('driver_info.html', racer=racer)

        return "Driver not found", 404

    sorted_racers = get_driver_list(order)
    if not sorted_racers:
        return redirect(url_for("drivers"))

    return render_template('driver_list.html', racers=sorted_racers)


class ReportResource(Resource):
    @staticmethod
    def get(order: str = None) -> (dict, int):
        sorted_racers = get_report(order)
        if not sorted_racers:
            return {"error": "Invalid order parameter"}, 400

        return {"racers": sorted_racers}, 200


class DriverListResource(Resource):
    @staticmethod
    def get(order: str = None, driver_id: str = None) -> (dict, int):

        if driver_id:
            for racer in top_racers + remaining_racers:
                if racer.driver_id == driver_id:
                    return {'racer': racer}

            return {"error": "Driver not found"}, 404

        sorted_racers = get_driver_list(order)
        if not sorted_racers:
            return {"error": "Invalid order parameter"}, 400

        return {"racers": sorted_racers}, 200


api.add_resource(ReportResource, "/api/report")
api.add_resource(DriverListResource, "/api/report/drivers")


if __name__ == '__main__':
    app.run(debug=True)
