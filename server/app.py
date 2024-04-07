# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>')
def get_earthquake(id):
    # Query the database for the earthquake with the provided ID
    earthquake = Earthquake.query.filter_by(id=id).first()

    # If no earthquake found, return a 404 response with an error message
    if not earthquake:
        body = {"message": f"Earthquake {id} not found."}
        status = 404
        return make_response(body,status)

    # If earthquake found, return a JSON response with earthquake attributes
    earthquake_data = {
        "id": earthquake.id,
        "location": earthquake.location,
        "magnitude": earthquake.magnitude,
        "year": earthquake.year
    }
    return make_response (earthquake_data)



@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquakes_by_magnitude(magnitude):
    # Query the database for earthquakes with magnitude greater than or equal to the parameter value
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()

    # Count the number of matching earthquakes
    count = len(earthquakes)

    # Prepare data for JSON response
    earthquake_data = [{
        "id": earthquake.id,
        "location": earthquake.location,
        "magnitude": earthquake.magnitude,
        "year": earthquake.year
    } for earthquake in earthquakes]

    # Prepare JSON response
    response_data = {
        "count": count,
        "quakes": earthquake_data
    }

    return make_response((response_data))





if __name__ == '__main__':
    app.run(port=5555, debug=True)
