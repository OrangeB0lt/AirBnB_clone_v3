#!/usr/bin/python3
''' Places viewer '''

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/places/<string:place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def getPAmenities(place_id):
    ''' gets all Amenity information used for all places '''
    if storage.get('Place', place_id) is None:
        abort(404)
    amenitiesList = []
    place = storage.get('Place', place_id)
    for amenity in place.amenities:
        amenitiesList.append(amenity.to_dict())

    return (jsonify(amenitiesList))


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def deletePAmenity(place_id, amenity_id):
    ''' deletes named amenity based on its place_id and amenityid '''
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    for amenity in place.amenities:
        if amenity.id == amenity_id:
            amenity.delete()
            storage.save()
            return (jsonify({}), 200)
    abort(404)


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['POST'],
                 strict_slashes=False)
def linkAmenity(place_id, amenity_id):
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    the_amenity = storage.get("Amenity", amenity_id)
    if the_amenity is None:
        abort(404)
    for amenity in place.amenities:
        if amenity.id == amenity_id:
            return (jsonify(amenity.to_dict()), 200)
    place.amenities.append(the_amenity)
    storage.save()
    return (jsonify(the_amenity.to_dict()), 201)
