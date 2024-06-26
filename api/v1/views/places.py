#!/usr/bin/python3
"""places module"""

from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.user import User
from models.state import State
from models.place import Place
from models.amenity import Amenity
from api.v1.views import app_views
from os import getenv


@app_views.route(
        '/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """Get all places in a city.
    Returns:
        JSON -- List of all places.
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Get a specific place by ID.
    Arguments:
        place_id {str} -- Place ID.
    Returns:
        JSON -- Place data.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route(
        '/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Delete a specific place by ID.
    Arguments:
        place_id {str} -- Place ID.
    Returns:
        JSON -- Empty dictionary with status code 200.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route(
        '/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Create a new place.
    Returns:
        JSON -- New place data.
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")
    user = storage.get(User, request.get_json()['user_id'])
    if not user:
        abort(404)
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    place = Place(city_id=city_id, **request.get_json())
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Update a specific place by ID.
    Arguments:
        place_id {str} -- Place ID.
    Returns:
        JSON -- Updated place data.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    for key, value in request.json.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return (jsonify(place.to_dict()), 200)


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    """Search for places.
    Returns:
        JSON -- List of places.
    """
    if not request.get_json():
        abort(400, description="Not a JSON")
    states = request.json.get('states', [])
    cities = request.json.get('cities', [])
    amenities = request.json.get('amenities', [])
    if not states and not cities and not amenities:
        places = [place.to_dict() for place in storage.all(Place).values()]
    else:
        places = []
        for state_id in states:
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    for place in city.places:
                        places.append(place.to_dict())
        for city_id in cities:
            city = storage.get(City, city_id)
            if city:
                for place in city.places:
                    if place.to_dict() not in places:
                        places.append(place.to_dict())
        if amenities:
            places = [place for place in places if all(
                amenity in place['amenities'] for amenity in amenities)]
    return jsonify(places)
