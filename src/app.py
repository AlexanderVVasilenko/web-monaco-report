from flask import Flask, render_template, request, redirect, url_for

from package_interaction import (
    get_report,
    top_racers,
    remaining_racers,
    get_driver_list,
)

app = Flask(__name__)


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
    driver_id = request.args.get("driver_id")

    if driver_id:
        for racer in top_racers + remaining_racers:
            if racer.driver_id == driver_id:
                return render_template("driver_info.html", racer=racer)

        return "Driver not found", 404

    sorted_racers = get_driver_list(order)
    if not sorted_racers:
        return redirect(url_for("drivers"))

    return render_template("driver_list.html", racers=sorted_racers)


if __name__ == "__main__":
    app.run(debug=True)
