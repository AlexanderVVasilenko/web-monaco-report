from models import LapTime, Racer


def insert_report(racers: list[LapTime]):
    return [
        {"name": lap_time_obj.racer.name, "team": lap_time_obj.racer.team, "driver_id": lap_time_obj.racer.driver_id,
         "lap_time": lap_time_obj.lap_time} for lap_time_obj in racers]


def get_report_from_db(
        order: str = None) -> list[dict] | None:
    query = LapTime.select()
    report = insert_report(query)
    match order:
        case "asc":
            return sorted(report, key=lambda x: x["lap_time"], reverse=False)
        case "desc":
            return sorted(report, key=lambda x: x["lap_time"], reverse=True)


def get_db_driver_list(order: str = None) -> list[dict] | None:
    query = Racer.select()
    racers = [{"name": racer.name, "team": racer.team, "driver_id": racer.driver_id} for racer in query]
    match order:
        case "asc":
            return sorted(racers, key=lambda x: x["driver_id"], reverse=False)
        case "desc":
            return sorted(racers, key=lambda x: x["driver_id"], reverse=True)


def get_db_driver_data(driver_id: str) -> dict | None:
    for racer in insert_report(LapTime.select()):
        if racer["driver_id"] == driver_id:
            return racer
