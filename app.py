import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement

Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/2013-01-01<br/>"
        f"/api/v1.0/2013-01-01/2014-01-01"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitation data"""
    # Query all precipitation
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_precipitation
    all_precipitation = []
    for date, precipitation in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["precipitation"] = precipitation
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of station data"""
    # Query all stations
    results = session.query(Station.station, Station.name).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_station
    all_station = []
    for station, name in results:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        all_station.append(station_dict)

    return jsonify(all_station)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of temperature data"""

    latest_date = dt.date(2015,10,30)

    last_year = latest_date - dt.timedelta(days=365)

    # Query all temperature
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= last_year).\
                                                            filter(Measurement.date <= latest_date).all()
    session.close()

    # Create a dictionary from the row data and append to a list of all_temperature
    all_temperature = []
    for date, temperature in results:
        temperature_dict = {}
        temperature_dict["date"] = date
        temperature_dict["temperature"] = temperature
        all_temperature.append(temperature_dict)

    return jsonify(all_temperature)

@app.route("/api/v1.0/<start>")
def temperature(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Return a list of temperature data"""

    # Query all stations
    results = session.query(func.max(Measurement.tobs), func.min(Measurement.tobs),func.avg(Measurement.tobs)).\
                                                            filter(Measurement.date >= start).all()
    session.close()

    # Create a dictionary from the row data and append to a list of all_temperature
    all_temperature_analysis = []
    for max_temp, min_temp, avg_temp in results:
        temperature_analysis_dict = {}
        temperature_analysis_dict["max temp"] = max_temp
        temperature_analysis_dict["min_temp"] = min_temp
        temperature_analysis_dict["avg_temp"] = avg_temp
        all_temperature_analysis.append(temperature_analysis_dict)

    return jsonify(all_temperature_analysis)

@app.route("/api/v1.0/<start>/<end>")
def temperature_set(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Return a list of temperature data"""

    # Query all stations
    results = session.query(func.max(Measurement.tobs), func.min(Measurement.tobs),func.avg(Measurement.tobs)).\
                                                            filter(Measurement.date >= start).\
                                                            filter(Measurement.date <= end).all()
    session.close()

    # Create a dictionary from the row data and append to a list of all_temperature
    all_temperature_analysis = []
    for max_temp, min_temp, avg_temp in results:
        temperature_analysis_dict = {}
        temperature_analysis_dict["max temp"] = max_temp
        temperature_analysis_dict["min_temp"] = min_temp
        temperature_analysis_dict["avg_temp"] = avg_temp
        all_temperature_analysis.append(temperature_analysis_dict)

    return jsonify(all_temperature_analysis)

if __name__ == '__main__':
    app.run(debug=True)
