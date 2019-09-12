#!/usr/bin/python3
''' places viewer '''

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<string:city_id>/places', methods=['GET'],
                 strict_slashes=False)
def getPlaces(city_id):
    ''' get place information for all places in a specified city '''
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    places = []
    for place in city.places:
        places.append(place.to_dict())
    return jsonify(places)


@app_views.route('/places/<string:place_id>', methods=['GET'],
                 strict_slashes=False)
def getPlace(place_id):
    ''' get place information for specified place_id '''
    placeSelect = storage.get("Place", place_id)
    if placeSelect is None:
        abort(404)
    return jsonify(placeSelect.to_dict())


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
def deletePlace(place_id):
    ''' deletes a place based on its place_id '''
    placeDelete = storage.get("Place", place_id)
    if placeDelete is None:
        abort(404)
    placeDelete.delete()
    storage.save()
    return (jsonify({}))


@app_views.route('/cities/<string:city_id>/places', methods=['POST'],
                 strict_slashes=False)
def postPlace(city_id):
    ''' create a new place '''
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    kwargs = request.get_json()
    if 'user_id' not in kwargs:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    user = storage.get("User", kwargs['user_id'])
    if user is None:
        abort(404)
    if 'name' not in kwargs:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    kwargs['city_id'] = city_id
    place = Place(**kwargs)
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<string:place_id>', methods=['PUT'],
                 strict_slashes=False)
def putPlace(place_id):
    ''' update a place '''
    placeUpdate = storage.get("Place", place_id)
    if placeUpdate is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, value in request.get_json().items():
        if attr not in ['id', 'user_id', 'city_id', 'created_at',
                        'updated_at']:
            setattr(placeUpdate, attr, value)
    placeUpdate.save()
    return jsonify(placeUpdate.to_dict())

@app_views.route('/places_search', methods=['POST'])
def postPlacesSearch():
    ''' places route to handle http method for request to search places '''
    searches = request.get_json(silent=True)
    if searches is None:
        return make_response(jsonify(error="Not a JSON"), 400)
    places = storage.all('Place').values()
    if 'states' in searches and len(searches['states']) > 0:
        places = [
            place for place in places
            if place.city.state.id in searches['states']
        ]
    if 'cities' in searches and len(searches['cities']) > 0:
        places = [
            place for place in places
            if place.city.id in searches['cities']
        ]
    if 'amenities' in searches and len(searches['amenities']) > 0:
        amenities = set(searches['amenities'])
        places = [
            place for place in places
            if amenities - set(am.id for am in place.amenities) == set()
        ]
    return jsonify([place.to_dict() for place in places])