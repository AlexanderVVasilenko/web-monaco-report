from f1_racing_reports.report import load_abbreviations, parse_logs
from models import Racer, Race, db, LapTime
from package_interaction import get_driver_list


def read_abbreviations_and_create_racers(file_path: str) -> None:
    driver_list = get_driver_list("asc", abbrs=load_abbreviations(file_path))

    for driver in driver_list:
        driver_id = driver["driver_id"]
        existing_racer = Racer.select().where(Racer.driver_id == driver_id).first()

        if not existing_racer:
            Racer.create(**driver)


def read_and_create_race(file_path: str) -> Race:
    with open(file_path, "r") as race_data:
        lines = race_data.readlines()
        year = lines[2].split(": ")[1].strip("\n")
        location = lines[1].split(": ")[1].strip("\n")
        name = lines[0].split(": ")[1].strip("\n")

    race, _ = Race.get_or_create(year=year, location=location, race_name=name)
    return race


def read_lap_time_and_create_races(
    start_log_path: str, end_log_path: str, abbrs_path: str, race: Race
) -> None:
    racers = parse_logs(start_log_path, end_log_path, load_abbreviations(abbrs_path))
    racers = racers[0] + racers[1]

    for racer in racers:
        db_racer = Racer.get(Racer.driver_id == racer.driver_id)
        existing_lap_time = (
            LapTime.select()
            .where((LapTime.race == race) & (LapTime.racer == db_racer))
            .first()
        )

        if not existing_lap_time:
            LapTime.create(race=race, racer=db_racer, lap_time=racer.lap_time)


if __name__ == "__main__":
    db.connect()

    read_abbreviations_and_create_racers("inputs/abbreviations.txt")
    race_obj = read_and_create_race("inputs/race_data.txt")
    read_lap_time_and_create_races(
        "inputs/start.log", "inputs/end.log", "inputs/abbreviations.txt", race_obj
    )

    db.close()
