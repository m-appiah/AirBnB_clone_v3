#!/usr/bin/python3
"""places_reviews module"""

from flask import abort, jsonify, request
from models import storage
from models.place import Place
from models.user import User
from models.review import Review
from api.v1.views import app_views


@app_views.route(
        '/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """Get all reviews in a place.
    Returns:
        JSON -- List of all reviews.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Get a specific review by ID.
    Arguments:
        review_id {str} -- Review ID.
    Returns:
        JSON -- Review data.
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route(
        '/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """Delete a specific review by ID.
    Arguments:
        review_id {str} -- Review ID.
    Returns:
        JSON -- Empty dictionary with status code 200.
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route(
        '/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """Create a new review
    Returns:
        JSON -- New review data.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")
    user = storage.get(User, request.get_json()['user_id'])
    if not user:
        abort(404)
    if 'text' not in request.get_json():
        abort(400, description="Missing text")
    review = Review(place_id=place_id, **request.get_json())
    review.save()
    return (jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Update a specific review by ID.
    Arguments:
        review_id {str} -- Review ID.
    Returns:
        JSON -- Updated review data.
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    for key, value in request.json.items():
        if key not in [
            'id',
            'user_id',
            'place_id',
            'created_at',
            'updated_at'
        ]:
            setattr(review, key, value)
    review.save()
    return (jsonify(review.to_dict()), 200)
