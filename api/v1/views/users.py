#!/usr/bin/python3
"""
New view for State objects
"""

from flask import abort, jsonify, request, make_response
from models import storage
from api.v1.views import app_views
from models.user import User


@app_views.route('/users', strict_slashes=False)
def get_users():
    """retrieves all user objects"""
    users = storage.all('User').values()
    users_list = []
    for user in users:
        users_list.append(user.to_dict())
    return jsonify(users_list)


@app_views.route('/users/<user_id>', strict_slashes=False)
def get_user_id(user_id):
    """retrieves a user object"""
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route(
        '/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """deletes a user object"""
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({})


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """create a user"""
    response = request.get_json()
    if response is None:
        abort(400, 'Not a JSON')
    if 'name' not in response:
        abort(400, 'Missing name')
    user = User(**response)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """update a user obbject"""
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ('id', 'created_at', 'updated_at'):
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
