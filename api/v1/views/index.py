#!/usr/bin/python3
"""Index"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """Returns the status of the API.
    Returns:
        JSON -- Status of the API.
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """Returns the count of all objects by type.
    Returns:
        JSON -- Dictionary with the count of all objects by type.
    """
    countDict = {}
    fields = {
        "amenities": "Amenity",
        "cities": "City",
        "places": "Place",
        "reviews": "Review",
        "states": "State",
        "users": "User"
    }
    for k, v in fields.items():
        countDict[k] = storage.count(v)
    return jsonify(countDict)
