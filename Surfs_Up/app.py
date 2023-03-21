
import numpy as np
import pandas as pd
import datetime as dt

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################


engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station


# Create our session (link) from Python to the DB
session=Session(engine)


#################################################
# Flask Setup
#################################################


app = Flask(__name__)


#################################################
# Flask Routes
#################################################


@app.route("/")
def Climate_App():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start<br/>"
        f"/api/v1.0/<start>/<end><br/>"
        )






 # Query Precepitation



@app.route("/api/v1.0/precipitation")
def precipitation():
    past_year_prcp = dt.date(2017,8,23)- dt.timedelta(days=365)
    results = session.query(measurement.date, measurement.prcp).filter(measurement.date >=past_year_prcp).\
                order_by(measurement.date).all()
    result_dict = dict(results)
    session.close()
    return jsonify(result_dict)


# Query Stations


@app.route("/api/v1.0/stations")
def stations():
    total_stations = session.query(measurement.station, func.count(measurement.id)).\
            group_by(measurement.station).order_by(func.count(measurement.id).desc()).all()

    stations_dict = dict(total_stations)
    session.close()
    return jsonify(stations_dict)

#Query Tobs


@app.route("/api/v1.0/tobs")
def tobs():
    temp_observations = session.query(measurement.station, measurement.tobs).\
        filter(measurement.date >= '2016-08-23').all()

    tobs_dict = dict(temp_observations)
    session.close()
    return jsonify(tobs_dict)


#Query Start


@app.route("/api/v1.0/<start>")
def start(start):

    # Create session ,code returting error each time without the sessions, or id have to run entire noteboook fir
    session = Session(engine)
    
    # Preform a query to retrieve the minimum, maximum, and average temperature for a specified start date to the end of the dataset
    temps_query = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
            filter(measurement.date >= start).all()
    
    # Close Session                                                  
    session.close()
    return jsonify(start)


@app.route('/api/v1.0/<start>', defaults={'end': None})
@app.route("/api/v1.0/<start>/<end>")
def start_end_temps(start, end):
    
    
    # Create our session to make it easier again
    session = Session(engine)

    # Start and end date max temp and min temp and avg if all info is available
    if end != None:
        temperatures = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
            filter(measurement.date >= start).filter(
            measurement.date <= end).all()
    # limited info
    else:
        temperatures = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
            filter(measurement.date >= start).all()

    session.close()
    
   

     # dictionary for dates 
    dates = []
    for min, max, avg in temperatures:
        dates_dict = {}
        dates_dict["Minimum Temperature"] = min
        dates_dict["Maxium Temperature"] = max
        dates_dict["Average Temperature"] = avg
        dates_dict.append(dates_dict)
        
    return jsonify(dates)


    




    
if __name__ == '__main__':
    app.run(debug=True)










