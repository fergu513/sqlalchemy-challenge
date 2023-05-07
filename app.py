# Import the dependencies.
from flask import Flask, jsonify
import numpy as np 
import datetime as dt 

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#################################################
# Database Setup
#################################################
# Create an engine for the chinook.sqlite database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
meas = Base.classes.measurement
stat = Base.classes.station

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
        f"/api/v1.0/start<start><br/>"
        f"/api/v1.0/start<start>/end<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a precipitation data"""
    # Design a query to retrieve the last 12 months of precipitation data and plot the results. 
    # Starting from the most recent data point in the database. 
    recent_date = dt.date(2017,8,23)
    #   Calculate the date one year from the last date in data set.
    old_date = recent_date - dt.timedelta(days = 365)

    # Perform a query to retrieve the data and precipitation scores
    results = session.query(meas.date,meas.prcp).filter(meas.date>=old_date).all()

    session.close()

    # Convert list of tuples into dict
    #empty list
    all_prcp = []
    #loop through query
    for date, prcp in results:
        #empty dictionary
        prcp_dict = {}
        #fill the dictionary
        prcp_dict[date] = prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Perform a query to retrieve the data and precipitation scores
    results = session.query(stat.station,stat.name).all()

        #empty list
    all_stats = []
    #loop through query
    for station, name in results:
        #empty dictionary
        stat_dict = {}
        #fill the dictionary
        stat_dict[station] = name
        all_stats.append(stat_dict)

    return jsonify(all_stats)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Perform a query to retrieve the data and precipitation scores
    results = session.query(meas.date,meas.tobs).filter_by(station = "USC00519281").all()

        #empty list
    all_tobs = []
    #loop through query
    for date, tobs in results:
        #empty dictionary
        tobs_dict = {}
        #fill the dictionary
        tobs_dict[date] = tobs
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

@app.route("/api/v1.0/start<start>")
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Perform a query to retrieve the data and precipitation scores
    results=session.query(func.min(meas.tobs), func.avg(meas.tobs), func.max(meas.tobs)).\
                filter(meas.date >= start).all()
    session.close()
    #empty dict
    temps = {}
    temps["Min Temp"] = results[0][0]
    temps["Average Temp"] = results[0][1]
    temps["Max Temp"] = results[0][2]

    return jsonify(temps)

@app.route("/api/v1.0/start<start>/end<end>")
def end(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Perform a query to retrieve the data and precipitation scores
    results=session.query(func.min(meas.tobs), func.avg(meas.tobs), func.max(meas.tobs)).\
                filter(meas.date >= start).filter(meas.date <= end).all()
    session.close()
    #empty dict
    temps = {}
    temps["Min Temp"] = results[0][0]
    temps["Average Temp"] = results[0][1]
    temps["Max Temp"] = results[0][2]

    return jsonify(temps)


if __name__ == '__main__':
    app.run(debug=True)