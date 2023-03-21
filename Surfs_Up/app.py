import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
#engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)
#print(Base.classes.keys())

#Base.classes.keys()
# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session=Session(engine)


#################################################
# Flask Setup
#################################################


app = Flask(__name__)


#################################################
# Flask Routes
#Start at the homepage.
#List all the available routes.
#################################################

@app.route("/")
def Climate_App():
 
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start<br/>"
        f"/api/v1.0/<start>/<end><br/>"
        )

#########################################################
 # Query Precepitation
#Convert the query results from your precipitation analysis
#(i.e.retrieve only the last 12 months of data) 
#to a dictionary using date as the key and prcp as the value.
#Return the JSON representation of your dictionary.
##########################################################


@app.route("/api/v1.0/precipitation")
def precipitation():
    past_year_prcp = dt.date(2017,8,23)- dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >=past_year_prcp).\
                order_by(Measurement.date).all()
    result_dict = dict(results)
    session.close()
    return jsonify(result_dict)

##########################################################
# Query Stations
# Return a JSON list of stations from the dataset.
###########################################################

@app.route("/api/v1.0/stations")
def stations():
    total_stations = session.query(Measurement.station, func.count(Measurement.id)).\
            group_by(Measurement.station).order_by(func.count(Measurement.id).desc()).all()

    stations_dictionary = dict(total_stations)
    session.close()
    return jsonify(stations_dictionary)
###################################################################
# Query Tobs
# Query the dates and temperature observations of the most-active station for the previous year of data.
# Return a JSON list of temperature observations for the previous year.
########################################################################

@app.route("/api/v1.0/tobs")
def tobs():
    temp_observations = session.query(Measurement.station == 'US00519281', Measurement.tobs).\
        filter(Measurement.date >= '2016-08-23').all()

    tobs_dict = dict(temp_observations)
    session.close()
    return jsonify(tobs_dict)

##############################################################################
#Query Start
# Return a JSON list of the minimum temperature, the average temperature, 
# and the maximum temperature for a specified start or start-end range.
# For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
# For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.

#######################################################################################
@app.route('/api/v1.0/<start>')
@app.route('/api/v1.0/<start>/<end>')

def various_temps_selections(start=None, end=None):
    temps = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    
    if not end:
        results = session.query(*temps).\
        filter(Measurement.date <= start).all()
        temps = list(np.ravel(results))
        session.close()
        return jsonify(temps)
    
    results = session.query(*temps).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    session.close()
    return jsonify(temps)
############################################################################################################

 


    
if __name__ == '__main__':
    app.run(debug=True)

