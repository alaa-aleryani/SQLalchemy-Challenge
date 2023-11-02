# Import the dependencies.
import pandas as pd
import numpy as np
import datetime as dt

# Import the SQLAlchemy dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Import the flask dependency 
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

# instantiate the flask library
app = Flask(__name__)  

#################################################
# Flask Routes
#################################################
@app.route("/")

def welcome():
    """ List all available api routes. """
    return (
        f"Welcome To Our Climate API Homepage!<br/>"
        f"----------------------------------<br/>"
        f"Available Routes:<br/>"
        f"----------------------------------<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start >>> Note: replace 'start' with a date of your choice in this format: YYYY-MM-DD <br/>"
        f"/api/v1.0/start/end >>> Note: replace 'start' and 'end' with a date of your choice in this format: YYYY-MM-DD<br/>"
    )

# ----------------------------------------------------------------------------------------
# Precipitation Route
@app.route("/api/v1.0/precipitation")

def percipitation():
    # Rain for the last year
    # get the date one year from the latest date
    global prev_year_date
    prev_year_date = dt.date(2017,8,23) - dt.timedelta(days=365)  
 
    # query the date
    percip_query = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year_date).all()
    
    # session.close
    session.close()

    # the data we want
    # using dictionary comprehension
    percip = {date:prcp for date, prcp in percip_query}  
    return jsonify(percip)  
    
# ----------------------------------------------------------------------------------------
# Stations Route
@app.route("/api/v1.0/stations")        

def stations():
        
    # query the data
    station_query = session.query(Station.station).all()

    # session.close
    session.close()

    # The data we want:
    # Convert list of tuples into normal list
    stations_list = list(np.ravel(station_query))
    return jsonify(stations_list)

# ----------------------------------------------------------------------------------------
# Tobs Route
@app.route("/api/v1.0/tobs")           

def tobs():
    # this variable - prev_year_date - was also created in the percipitation function
    # to avoid recreating it we could do global before the first time we created
    # prev_year_date variable in the percipitation func. maybe? But that did not work
    prev_year_date = dt.date(2017,8,23) - dt.timedelta(days=365)  

    # query the data
    temp_obs_data = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year_date).all()

    # session.close
    session.close()
    
    # The data we want:
    # Convert list of tuples into normal list
    temp_obs_data_list = list(np.ravel(temp_obs_data))
    return jsonify(temp_obs_data_list)

# ----------------------------------------------------------------------------------------
# start route
@app.route("/api/v1.0/<start>")
# @app.route("/api/v1.0/<start>/<end>") # if I do one function for both routes 
                                        # I would need to do an if statement.
def start(start= None):
    prev_year_date = dt.date(2017,8,23) - dt.timedelta(days=365)  

    # Query the data
    statistic = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), 
                              func.max(Measurement.tobs)).\
                              filter(Measurement.date >= start).all()

    # Session.close
    session.close()

    # The data we want:
    # Convert into normal list
    statistic_list = list(np.ravel(statistic))
    return jsonify(statistic_list)
# ----------------------------------------------------------------------------------------
# start/end route 
@app.route("/api/v1.0/<start>/<end>")

def start_end(start = None, end = None):
    prev_year_date = dt.date(2017,8,23) - dt.timedelta(days=365)  

    # Query the data
    statistic = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), 
                              func.max(Measurement.tobs)).\
                              filter(Measurement.date >= start).\
                              filter(Measurement.date <= end).all()

    # Session.close
    session.close()

    # The data we want:
    # Convert into normal list
    statistic_list = list(np.ravel(statistic))
    return jsonify(statistic_list)

#########################################################
#  RUN IT
#########################################################
if __name__ == "__main__":
    app.run(debug=True)
