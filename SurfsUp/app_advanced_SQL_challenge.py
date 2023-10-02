# challenge advanced SQL WEEK 10 
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
# import Flask
from flask import Flask, jsonify

# reflect an existing database into a new model
Base = automap_base()
# Database Setup
engine = create_engine("sqlite:///hawaii.sqlite")
# reflect the tables
# Base.prepare(autoload_with=engine)
Base.prepare(engine, reflect=True)

# Save reference to the tables
ref_measurement_tb = Base.classes.measurement
ref_station_tb = Base.classes.station
#Create an app, being sure to pass __name__
app = Flask(__name__)

    # Define what to do when a user hits the index route
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
        )


@app.route("/api/v1.0/precipitation")
def precipitations():

    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    
    # Query all dates
    results = session.query(ref_measurement_tb.date, ref_measurement_tb.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_precipitations
    all_precipitations = []
    for datep, precipitationp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = datep
        precipitation_dict["Precipitation"] = precipitationp
        
        all_precipitations.append(precipitation_dict)

    return jsonify(all_precipitations)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    
    # Query all stations
    results = session.query(ref_station_tb.station).all()

    session.close()

    # Convert list of tuples into normal list
    list_stations = list(np.ravel(results))

    return jsonify(list_stations)


@app.route("/api/v1.0/tobs")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    #The following code get the most active station
    most_active_station = session.query(ref_measurement_tb.station).\
                            group_by(ref_measurement_tb.station).\
                            order_by(func.count(ref_measurement_tb.station).desc()).first()
    most_active_station = most_active_station.station
    
    #the following code get the most recent date of the most active station
    the_most_recent_date = session.query(ref_measurement_tb.date).\
                                    filter(ref_measurement_tb.station == most_active_station).\
                                    order_by(ref_measurement_tb.date.desc()).first()
    the_most_recent_date = the_most_recent_date.date
    #the following code calculated one year early from the most recent date
    split_date = the_most_recent_date.split('-')
    most_recent_year = int(split_date[0])
    year_back_int = most_recent_year - 1
    year_back_str = str(year_back_int)
    date_year_back =f"{year_back_str}-{split_date[1]}-{split_date[2]}"
    
    # Query the dates and temperature observations of the most-active station for the previous year of data.
    data_retrieved = session.query(ref_measurement_tb.date, ref_measurement_tb.tobs).\
        filter((ref_measurement_tb.date >= date_year_back) &\
                (ref_measurement_tb.date <= most_active_station) &\
                (ref_measurement_tb.station == most_active_station )).\
        order_by(ref_measurement_tb.date).all()


    session.close()

    

    return jsonify(data_retrieved)


# @app.route("/api/v1.0/<start>")
# def start():
#     # Create our session (link) from Python to the DB
#     session = Session(engine)

#     
#     session.close()

#     

#     return jsonify(all_names)


# @app.route("/api/v1.0/<start>/<end>")
# def start_end():
#     # Create our session (link) from Python to the DB
#     session = Session(engine)

#     

#     session.close()

#     

#     return jsonify(all_names)



if __name__ == "__main__":
    app.run(debug=True)