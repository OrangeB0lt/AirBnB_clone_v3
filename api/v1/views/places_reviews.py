#!/usr/bin/python3
''' Places viewer '''

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.review import Review


@app_views.route('/places/<string:place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def getReviews(place_id):
    ''' gets all Review information used for all places '''
    if storage.get('Place', place_id) is None:
        abort(404)
    reviewsList = []
    all_review_objs = storage.all(Review)
    for review in all_review_objs.values():
        if review.place_id == place_id:
            reviewsList.append(review.to_dict())
    return jsonify(reviewsList)


@app_views.route('/reviews/<string:review_id>', methods=['GET'],
                 strict_slashes=False)
def getReview(review_id):
    ''' gets Review information for named place '''
    reviewSelect = storage.get("Review", review_id)
    if reviewSelect is None:
        abort(404)
    return jsonify(reviewSelect.to_dict())


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteReview(review_id):
    ''' deletes named review based on its review_id '''
    reviewDelete = storage.get("Review", review_id)
    if reviewDelete is None:
        abort(404)
    reviewDelete.delete()
    storage.save()
    return (jsonify({}))


@app_views.route('/places/<string:place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def postReview(place_id):
    ''' create a new review '''
    if storage.get('Place', place_id) is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in request.get_json():
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    if type(request.get_json()) is dict:
        if storage.get('User', request.get_json()['user_id']) is None:
            abort(404)
    if 'text' not in request.get_json():
        return make_response(jsonify({'error': 'Missing text'}), 400)

    reviewPost = Review(**request.get_json())
    setattr(reviewPost, 'place_id', place_id)
    reviewPost.save()
    return make_response(jsonify(reviewPost.to_dict()), 201)


@app_views.route('/reviews/<string:review_id>', methods=['PUT'],
                 strict_slashes=False)
def putReview(review_id):
    ''' updates named review '''
    reviewUpdate = storage.get("Review", review_id)
    if reviewUpdate is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, value in request.get_json().items():
        if attr not in ['id', 'created_at',
                        'updated_at', 'place_id', 'user_id']:
            setattr(reviewUpdate, attr, value)
    reviewUpdate.save()
    return jsonify(reviewUpdate.to_dict())
