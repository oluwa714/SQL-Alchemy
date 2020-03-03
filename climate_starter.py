import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import os

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Station = Base.classes.station
Measurement = Base.classes.measurement

inspector = inspect(engine)

session = Session(engine)

measurement_df = pd.read_sql_query("SELECT date, prcp FROM measurement WHERE id > (19550 - 365)", con=engine)
date = [dt.datetime.strptime(i, '%Y-%m-%d') for i in measurement_df['date']]
measurement_df['Datetime'] = date
measurement_df.set_index("Datetime")
print(measurement_df.head())

measurement_tobs_df = pd.read_sql_query("SELECT date, tobs FROM measurement WHERE id > (19550 - 365)", con=engine)
date = [dt.datetime.strptime(i, '%Y-%m-%d') for i in measurement_tobs_df['date']]
measurement_tobs_df['Datetime'] = date
measurement_tobs_df.set_index("Datetime")
print(measurement_tobs_df.head())

exact_year = (measurement_df['Datetime'][364] - dt.timedelta(days=365))
print(exact_year)

Description = measurement_df.describe()
print(Description)


unique_station = session.query(Station.station).count()
print(unique_station)

active_station = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
print(active_station)

stats_temp_station = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.station == 'USC00519281').all()
print(stats_temp_station)

# year_of_prcp_s = measurement_df["prcp"]
# plt.hist(year_of_prcp_s)
# plt.title = "Year of Precipitation Records"
# plt.xlabel = "Precipitation"
# plt.ylabel = "Frequency"
# plt.show()


# year_tobs = measurement_tobs_df["tobs"]
# plt.hist(year_tobs, bins = 12)
# plt.title = "Year of Temperature Records"
# plt.xlabel = "Temperature"
# plt.ylabel = "Frequency"
# plt.show()


#Application Start
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hawaii.sqlite"

db = SQLAlchemy(app)


@app.route("/")
def home():
    return " - /Precipitation, -/Stations, - /Temperatures, - /Start, - /End"


@app.route("/Precipitation")
def precip():
    return jsonify(measurement_tobs_df.to_dict())

@app.route("/Stations")
def stations():
    return jsonify(active_station)

@app.route("/Temperature")
def temperature():
    return jsonify(measurement_tobs_df.to_dict())

app.run(debug=True)
