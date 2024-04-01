#!/usr/bin/python3
"""amenities"""

from flask import abort, jsonify, request
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Get all amenities.
    Returns:
        JSON -- List of all amenities.
    """
    amenities = [amenity.to_dict() for amenity in storage.all(
        Amenity).values()]
    return jsonify(amenities)


@app_views.route(
        '/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """Get a specific amenity by ID.
    Arguments:
        amenity_id {str} -- Amenity ID.
    Returns:
        JSON -- Amenity data.
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route(
        '/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """Delete a specific amenity by ID.
    Arguments:
        amenity_id {str} -- Amenity ID.
    Returns:
        JSON -- Empty dictionary with status code 200.
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Create a new amenity.
    Returns:
        JSON -- New amenity data.
    """
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    amenity = Amenity(**request.get_json())
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route(
        '/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """Update a specific amenity by ID.
    Arguments:
        amenity_id {str} -- Amenity ID.
    Returns:
        JSON -- Updated amenity data.
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    for key, value in request.json.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()
    return (jsonify(amenity.to_dict()), 200)
