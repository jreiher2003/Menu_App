from app import app, db 
from app.models import Place, Menu 
from flask import Blueprint, jsonify 

api_blueprint = Blueprint("api", __name__) 

@api_blueprint.route("/api/")
def api():
    return "this is api page"

@api_blueprint.route("/restaurant/JSON/")
def restaurant_json():
    places = Place.query.all()
    return jsonify(Restaurants=[i.serialize for i in places])

@api_blueprint.route("/restaurant/<int:place_id>/menu/JSON")
def menu_json(place_id):
    menu = Menu.query.filter_by(place_id=place_id).all()
    return jsonify(MenuItems=[i.serialize for i in menu])

@api_blueprint.route("/restaurant/<int:place_id>/menu/<int:menu_id>/JSON")
def single_menu_item(place_id, menu_id):
    menu = Menu.query.filter_by(id=menu_id).all()
    return jsonify(MenuItem=[i.serialize for i in menu])