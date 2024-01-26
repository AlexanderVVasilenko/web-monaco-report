# tests/test_app.py


import pytest
from peewee import SqliteDatabase

from app import app
from store_data import (
    read_abbreviations_and_create_racers,
    read_and_create_race,
    read_lap_time_and_create_races,
)
from models import Race, Racer, LapTime

# Configure a test database
db = SqliteDatabase(":memory:")

# Override the database used by the models to the test database
Race._meta.database = db
Racer._meta.database = db
LapTime._meta.database = db


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    client = app.test_client()

    with app.app_context():
        db.create_tables([Racer, Race, LapTime])
        yield client
        db.drop_tables([Racer, Race, LapTime])


def test_read_abbreviations_and_create_racers(client):
    read_abbreviations_and_create_racers("inputs/abbreviations.txt")
    assert Racer.select().count() == 20


def test_read_and_create_race(client):
    race_obj = read_and_create_race("inputs/race_data.txt")
    assert race_obj.year == "2018"
    assert race_obj.location == "Monaco"
    assert race_obj.race_name == "Monaco Grand Prix"


def test_read_lap_time_and_create_races(client):
    read_abbreviations_and_create_racers("inputs/abbreviations.txt")
    race_obj = read_and_create_race("inputs/race_data.txt")
    read_lap_time_and_create_races(
        "inputs/start.log", "inputs/end.log", "inputs/abbreviations.txt", race_obj
    )

    assert LapTime.select().count() == 20  # Assuming there are 20 racers in your logs
