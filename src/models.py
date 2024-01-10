from peewee import SqliteDatabase, Model, CharField, ForeignKeyField, FloatField

db = SqliteDatabase("f1_racing.db")


class BaseModel(Model):
    class Meta:
        database = db


class Race(BaseModel):
    race_name = CharField()
    location = CharField()


class Racer(BaseModel):
    name = CharField()
    team = CharField()
    driver_id = CharField(unique=True)


class LapTime(BaseModel):
    race = ForeignKeyField(Race, backref='lap_times')
    racer = ForeignKeyField(Racer, backref='lap_times')
    lap_time = FloatField()


db.connect()
db.create_tables([Racer])

# new_racer = Racer.create(name='Lewis Hamilton', team='Mercedes', lap_time='1:30.000', driver_id='HAM')
