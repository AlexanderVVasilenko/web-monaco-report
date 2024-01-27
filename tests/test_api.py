import requests

from store_data import (
    read_abbreviations_and_create_racers,
    read_and_create_race,
    read_lap_time_and_create_races,
)

HOST = "http://127.0.0.1:5000"


def test_api_endpoints():
    read_abbreviations_and_create_racers("inputs/abbreviations.txt")
    race_obj = read_and_create_race("inputs/race_data.txt")
    read_lap_time_and_create_races(
        "inputs/start.log", "inputs/end.log", "inputs/abbreviations.txt", race_obj
    )

    response = requests.get(f"{HOST}/api/v1/report")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert "racers" in response.json()

    response = requests.get(f"{HOST}/api/v1/report/drivers")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert "racers" in response.json()

    existing_driver_id = "RAI"  # Replace with an existing driver_id
    response = requests.get(f"{HOST}/api/v1/report/drivers/{existing_driver_id}")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert "racer" in response.json()

    non_existing_driver_id = "R"  # Replace with a non-existing driver_id
    response = requests.get(f"{HOST}/api/v1/report/drivers/{non_existing_driver_id}")
    assert response.status_code == 404
    assert response.headers["Content-Type"] == "application/json"
    assert "error" in response.json()
