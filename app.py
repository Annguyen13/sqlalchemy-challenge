import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

# Database Setup

engine = create_engine("sqlite:///Resources/hawaii2.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup

app = Flask(__name__)

@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start-YYYY-MM-DD<br/>"
        f"/api/v1.0/start-YYYY-MM-DD/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    
    session = Session(engine)

   # Calculate the date 1 year ago from the last data point in the database

    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    # Perform a query to retrieve the data and precipitation scores
    prcp_data = session.query(Measurement.prcp, Measurement.date).filter(Measurement.date > query_date).order_by(Measurement.date).all()
   

    session.close()

    # Create a dictionary from the row data and append to a list of precipitation and date
    prcp_list = []
    for date, prcp in prcp_data:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = precipitation
        prcp_list.append(prcp_dict)

    return jsonify(prcp_list)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)


    # Query all stations
    station_data = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    station_list = list(np.ravel(station_data))

    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Find the date one year ago
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Choose the station with the highest number of temperature observations.
    session.query(Measurement.station, func.count(Measurement.station).label("count")).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).first()
    
    #Query tempo for the most active station in the previous year
    temp_data = session.query(Measurement.station, Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date > query_date).order_by(Measurement.date).all()
    

    session.close()

    # Create a dictionary for the date and tempo for the most active station
    tobs_list = []
    for station, tobs in temp_data:
        tobs_dict = {}
        tobs_dict["station"] = station
        tobs_dict["date"] = date
        tobs_dict["tobs"] = temparature
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")

def start(start):
 
 # Create our session (link) from Python to the DB
    session = Session(engine)

    start_data = session.query(Measurement.station, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).group_by(Measurement.station).order_by(func.count(Measurement.date)).all()

    session.close()

    return jsonify(start_data)


@app.route("/api/v1.0/<start>/<end>")

def start_end(start, end):
 
 # Create our session (link) from Python to the DB
    session = Session(engine)

    start_end_data = session.query(Measurement.station, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start, Measurement.date < end).group_by(Measurement.station).order_by(func.count(Measurement.date)).all()

    session.close()

    return jsonify(start_end_data)


if __name__ == '__main__':
    app.run(debug=True)