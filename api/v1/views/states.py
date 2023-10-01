#!/usr/bin/python3
"""
New view for State objects
"""

from flask import abort, jsonify, request, make_response
from models import storage
from api.v1.views import app_views
from models.state import State


@app_views.route('/states', methods=["GET"], strict_slashes=False)
def get_states():
    """retrieves all State objects"""
    states = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=["GET"], strict_slashes=False)
def get_state_id(state_id):
    """retrieves a state object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route(
        '/states/<state_id>', methods=["DELETE"], strict_slashes=False)
def delete_state(state_id):
    """deletes a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=["POST"], strict_slashes=False)
def create_state():
    """create a State"""
    response = request.get_json()
    if response is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in response:
        return jsonify({"error": "Missing name"}), 400
    state = State(**response)
    storage.new(state)
    storage.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """update a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    state.save()
    return make_response(jsonify(state.to_dict()), 200)
