import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///sqlalchemy-challenge\SurfsUp\Resources\hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

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
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
        f"'start' and 'end' date format is YYYY-MM-DD."
    )


@app.route("/api/v1.0/precipitation")
def precipitation():

    # Calculate the date one year from the last date in data set.
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    sel = [Measurement.date, Measurement.prcp]
    last_year_prcp = session.query(*sel).filter(Measurement.date >= last_year).all()

    session.close()

    # Converts results into dictionary
    prcp_dict = {}
    for item in last_year_prcp:
        prcp_dict[item[0]] = item[1]

    return jsonify(prcp_dict)


@app.route("/api/v1.0/stations")
def stations():

    # Query all stations
    stations = session.query(Station.station).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_stations
    all_stations = list(np.ravel(stations))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():

    most_active_station = 'USC00519281'

    # Calculate the date one year from the last date in data set.
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Perform a query to retrieve temperature observation data
    last_year_tobs = session.query(Measurement.tobs) \
    .filter(Measurement.station == most_active_station) \
    .filter(Measurement.date >= last_year).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_tobs
    all_tobs = list(np.ravel(last_year_tobs))

    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def start(start):

    sel = [func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)]

    start = dt.datetime.strptime(start, "%Y-%m-%d")

    # Perform a query to retrieve temperature observation data
    temperatures = session.query(*sel) \
    .filter(Measurement.date >= start).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_temps
    all_temps = list(np.ravel(temperatures))

    return jsonify(all_temps)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):

    sel = [func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)]

    start = dt.datetime.strptime(start, "%Y-%m-%d")
    end = dt.datetime.strptime(end, "%Y-%m-%d")

    # Perform a query to retrieve temperature observation data
    temperatures = session.query(*sel) \
    .filter(Measurement.date >= start) \
    .filter(Measurement.date <= end).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_temps
    all_temps = list(np.ravel(temperatures))

    return jsonify(all_temps)

if __name__ == '__main__':
    app.run(debug=True)
