#!/usr/bin/python3
"""
starts a Flask web application, filters
"""

from flask import Flask, render_template
from models.state import State
from models.amenity import Amenity
from models.user import User
from models.place import Place
from models import storage

app = Flask(__name__)


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    """display a HTML page like 6-index.html from static"""
    states = storage.all(State).values()
    amenities = storage.all(Amenity).values()
    places = storage.all(Place).values()
    users = storage.all(User).values()
    return render_template('10-hbnb_filters.html', states=states,
                           amenities=amenities,
                           places=places,
                           users=users)


@app.teardown_appcontext
def teardown_storage(exception):
    """closes the storage on teardown"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
