from flask import Flask, render_template, request, redirect, url_for
from f1_racing_reports.report import parse_logs, load_abbreviations

app = Flask(__name__)

start_log_file = "src/start.log"
end_log_file = "src/end.log"
abbreviations_file_path = "src/abbreviations.txt"

abbreviations = load_abbreviations(abbreviations_file_path)

top_racers, remaining_racers = parse_logs(start_log_file, end_log_file, abbreviations)


@app.route("/report/", methods=["GET"])
def report():
    order = request.args.get("order", "asc")
    if order == "asc":
        sorted_racers = top_racers + remaining_racers
    elif order == "desc":
        sorted_racers = remaining_racers[::-1] + top_racers[::-1]
    else:
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

    if order == "asc":
        sorted_racers = sorted(abbreviations, key=lambda x: x[1])
    elif order == "desc":
        sorted_racers = sorted(abbreviations, key=lambda x: x[1], reverse=True)
    else:
        return redirect(url_for("drivers"))

    return render_template('driver_list.html', racers=sorted_racers)


app.run(debug=True)
