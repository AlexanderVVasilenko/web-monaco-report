from src.models import LapTime, Racer


def insert_report(racers: list[LapTime]) -> list[dict]:
    return [
        {
            "name": lap_time_obj.racer.name,
            "team": lap_time_obj.racer.team,
            "driver_id": lap_time_obj.racer.driver_id,
            "lap_time": lap_time_obj.lap_time,
        }
        for lap_time_obj in racers
    ]


def get_db_report(order: str = None) -> list[dict] | None:
    lap_times = LapTime.select()
    report = insert_report(lap_times)

    if order == "asc":
        return sorted(report, key=lambda x: x["lap_time"], reverse=False)
    elif order == "desc":
        return sorted(report, key=lambda x: x["lap_time"], reverse=True)
    else:
        return None


def get_db_driver_list(order: str = None) -> list[dict] | None:
    racers = Racer.select()
    driver_list = [
        {"name": racer.name, "team": racer.team, "driver_id": racer.driver_id}
        for racer in racers
    ]

    if order == "asc":
        return sorted(driver_list, key=lambda x: x["driver_id"], reverse=False)
    elif order == "desc":
        return sorted(driver_list, key=lambda x: x["driver_id"], reverse=True)
    else:
        return None


def get_db_driver_data(driver_id: str) -> dict | None:
    for racer in insert_report(LapTime.select()):
        if racer["driver_id"] == driver_id:
            return racer
    return None
