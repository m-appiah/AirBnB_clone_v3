#!/usr/bin/python3
"""users module"""

from flask import abort, jsonify, request
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Get all users.    
    Returns:
        JSON -- List of all users.
    """
    users = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Get a specific user by ID.
    Arguments:
        user_id {str} -- User ID.
    Returns:
        JSON -- User data.
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Delete a specific user by ID.
    Arguments:
        user_id {str} -- User ID.
    Returns:
        JSON -- Empty dictionary with status code 200.
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Create a new user.
    Returns:
        JSON -- New user data.
    """
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'email' not in request.get_json():
        abort(400, description="Missing email")
    if 'password' not in request.get_json():
        abort(400, description="Missing password")
    user = User(**request.get_json())
    user.save()
    return (jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Update a specific user by ID.
    Arguments:
        user_id {str} -- User ID.
    Returns:
        JSON -- Updated user data.
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    for key, value in request.json.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    user.save()
    return (jsonify(user.to_dict()), 200)
