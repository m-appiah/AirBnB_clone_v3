#!/usr/bin/python3
"""Index"""
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """Retrieves the number of each objects by type"""
    fields = {
        "amenities": "Amenity",
        "cities": "City",
        "places": "Place",
        "reviews": "Review",
        "states": "State",
        "users": "User"
    }
    countDict = {}
    for k, v in fields.items():
        countDict[k] = storage.count(v)
    return jsonify(countDict)
