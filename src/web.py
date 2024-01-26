from flask import request, redirect, url_for, render_template


from app import app
from insert_data import get_db_report, get_db_driver_data, get_db_driver_list


@app.route("/report/", methods=["GET"])
def report():
    order = request.args.get("order", "asc")
    sorted_racers = get_db_report(order)
    if not sorted_racers:
        return redirect(url_for("report"))

    return render_template("report.html", racers=sorted_racers)


@app.route("/report/drivers/", methods=["GET"])
def driver_list():
    order = request.args.get("order", "asc")
    driver_id = request.args.get("driver_id")

    if driver_id:
        racer = get_db_driver_data(driver_id)
        if racer:
            return render_template("driver_info.html", racer=racer)

        return "Driver not found", 404

    sorted_racers = get_db_driver_list(order)
    if not sorted_racers:
        return redirect(url_for("drivers"))

    return render_template("driver_list.html", racers=sorted_racers)
