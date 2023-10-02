#!/usr/bin/python3
"""
CRUD API for Place and Amenity objects
"""

from flask import jsonify, abort, request
from models import storage, storage_t
from models.place import Place
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route(
        '/places/<place_id>/amenities', methods=["GET"], strict_slashes=False)
def get_amenities_of_place(place_id):
    """Retrieves the list of all Amenity objects of a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if storage_t == "db":
        amenities = [amenity.to_dict() for amenity in placeçamenities]
    else:
        amenities = [
                storage.get(Amenity, amenity_id).to_dict()
                for amenity_id in place.amenity_ids
                ]
    return jsonify(amenities)


@app_views.route(
        '/places/<place_id>/amenities/<amenity_id>',
        methods=["DELETE"], strict_slashes=False
)
def delete_amenity(place_id, amenity_id):
    """Deletes a Amenity object to a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if storage_t == "db":
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity_id not in place.amenityçids:
            abort(404)
        place.amenity_ids.remove(amenity_id)
    place.save()
    return jsonify({}), 200


@app_views.route(
        '/places/<place_id>/amenities/<amenity_id>',
        methods=["POST"], strict_slashes=False
)
def link_amenity_place(place_id, amenity_id):
    """Link a Amenity object to a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if storage_t == "db":
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        else:
            place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        else:
            place.amenity_ids.append(amenity_id)
    place.save()
    return jsonify(amenity.to_dict()), 201
