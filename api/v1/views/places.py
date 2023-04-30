#!/usr/bin/python3
"""
View for Place objects that handles all default RESTFul API actions.
"""
from api.v1.views import app_views
from flask import (jsonify, abort, make_response, request)
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET', 'POST'], strict_slashes=False)
def places_id(city_id):
    """Retrieves the list of all Place objects on GET.
    Creates a Place on POST.
    """
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        all_places = storage.all(Place)
        city_places = [obj.to_dict() for obj in all_places.values()
                       if obj.city_id == city_id]
        return jsonify(city_places)

    if request.method == 'POST':
        place_data = request.get_json()
        if place_data is None:
            abort(400, "Not a JSON")
        if place_data.get('user_id') is None:
            abort(400, "Missing user_id")
        user_obj = storage.get(User, place_data.get('user_id'))
        if not user_obj:
            abort(404, 'Not found')
        if place_data.get('name') is None:
            abort(400, 'Missing name')
        new_place = Place(**place_data)
        new_place.city_id = city_id
        new_place.save()
        return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def place_id(place_id):
    """Retrieves a Place object on GET request.
    Deletes a Place object on POST request.
    Updates a Place object
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(place.to_dict())

    if request.method == 'DELETE':
        place.delete()
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        place_data = request.get_json()
        if place_data is None:
            abort(400, "Not a JSON")
        for key, value in place_data.items():
            if key not in ['id', 'user_id',
                           'city_id', 'created_at', 'updated_at']:
                setattr(place, key, value)
        storage.save()
        return jsonify(place.to_dict()), 200
