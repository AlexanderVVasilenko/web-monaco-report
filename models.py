from peewee import SqliteDatabase, Model, CharField, ForeignKeyField, FloatField

db = SqliteDatabase("f1_racing.db")


class BaseModel(Model):
    class Meta:
        database = db


class Race(BaseModel):
    race_name = CharField()
    location = CharField()
    year = CharField(null=True)


class Racer(BaseModel):
    name = CharField()
    team = CharField()
    driver_id = CharField(unique=True)


class LapTime(BaseModel):
    race = ForeignKeyField(Race, backref="lap_times")
    racer = ForeignKeyField(Racer, backref="lap_times")
    lap_time = FloatField(null=True)


db.connect()
db.create_tables([Racer, Race, LapTime])


"""
# Create an example race
race_data = {'race_name': 'Monaco Grand Prix', 'location': 'Monte Carlo'}
monaco_race = Race.create(**race_data)

# Create example racers
racer_data1 = {'name': 'Lewis Hamilton', 'team': 'Mercedes', 'driver_id': 'HAM'}
racer_data2 = {'name': 'Max Verstappen', 'team': 'Red Bull Racing', 'driver_id': 'VER'}
racer_data3 = {'name': 'Charles Leclerc', 'team': 'Ferrari', 'driver_id': 'LEC'}

hamilton = Racer.create(**racer_data1)
verstappen = Racer.create(**racer_data2)
leclerc = Racer.create(**racer_data3)

# Create example lap times
lap_time_data1 = {'race': monaco_race, 'racer': hamilton, 'lap_time': 75.23}
lap_time_data2 = {'race': monaco_race, 'racer': verstappen, 'lap_time': 76.45}
lap_time_data3 = {'race': monaco_race, 'racer': leclerc, 'lap_time': 77.12}

LapTime.create(**lap_time_data1)
LapTime.create(**lap_time_data2)
LapTime.create(**lap_time_data3)
"""


db.close()
