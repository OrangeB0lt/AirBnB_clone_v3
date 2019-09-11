#!/usr/bin/python3
''' Users viewer '''

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def getUsers():
    ''' gets all User information used for all users '''
    usersList = []
    for user in storage.all("User").values():
        usersList.append(user.to_dict())
    return jsonify(usersList)


@app_views.route('/users/<string:user_id>', methods=['GET'],
                 strict_slashes=False)
def getUser(user_id):
    ''' gets User information for named user '''
    userselect = storage.get("User", user_id)
    if userselect is None:
        abort(404)
    return jsonify(userselect.to_dict())


@app_views.route('/users/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteUser(user_id):
    ''' deletes named user based on its user_id '''
    userDelete = storage.get("User", user_id)
    if userDelete is None:
        abort(404)
    userDelete.delete()
    storage.save()
    return (jsonify({}))


@app_views.route('/users/', methods=['POST'], strict_slashes=False)
def postUser():
    ''' create a new user '''
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'email' not in request.get_json():
        return make_response(jsonify({'error': 'Missing email'}), 400)
    if 'password' not in request.get_json():
        return make_response(jsonify({'error': 'Missing password'}), 400)
    userPost = User(**request.get_json())
    userPost.save()
    return make_response(jsonify(userPost.to_dict()), 201)


@app_views.route('/users/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
def putUser(user_id):
    ''' updates named user '''
    userUpdate = storage.get("User", user_id)
    if userUpdate is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, value in request.get_json().items():
        if attr not in ['id', 'created_at', 'updated_at', 'email']:
            setattr(userUpdate, attr, value)
    userUpdate.save()
    return jsonify(userUpdate.to_dict())
