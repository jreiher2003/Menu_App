from app import app,db # pragma: no cover
from app.models import Place, Menu # pragma: no cover
from flask import Blueprint, render_template, request, url_for, redirect, flash # pragma: no cover
from flask import session as login_session
from flask_login import current_user, login_required
import us # pragma: no cover 

home_blueprint = Blueprint("home", __name__, template_folder="templates") 

@home_blueprint.route("/") 
@home_blueprint.route("/restaurants")
def show_places(): 
	all_places = Place.query.all()
	return render_template(
		'restaurants.html', 
		all_places=all_places)

@home_blueprint.route("/restaurant/new", methods=["GET", "POST"])
@login_required
def new_place():
	states = us.states.STATES 
	if request.method == "POST":
		new = Place(
			name=request.form["name"],
			address=request.form["address"],
			city=request.form["city"],
			state=request.form["state"],
			zip_=request.form["zip_"],
			website=request.form["website"],
			phone=request.form["phone"],
			owner=request.form["owner"],
			yrs_open=request.form["yrs_open"],
			user_id=login_session['user_id']
			)
		db.session.add(new)
		db.session.commit()
		flash("You just added a new restaurant", "success")
		return redirect(url_for("home.show_places"))
	return render_template("new_restaurant.html", states=states)

@home_blueprint.route("/restaurant/<int:place_id>/edit", methods=["GET", "POST"])
@login_required
def edit_place(place_id):
	edit_rest = Place.query.filter_by(id=place_id).one()
	if request.method == "POST":
		edit_rest.name = request.form["name"]
		edit_rest.address = request.form["address"]
		edit_rest.city = request.form["city"]
		edit_rest.state = request.form["state"]
		edit_rest.zip_ = request.form["zip_"]
		edit_rest.website = request.form["website"]
		edit_rest.phone = request.form["phone"]
		edit_rest.owner = request.form["owner"]
		edit_rest.yrs_open = request.form["yrs_open"]
		edit_rest.last_edit = current_user.id
		db.session.add(edit_rest)
		db.session.commit()
		flash("You just edited this restaurant", "success")
		return redirect(url_for("home.show_places"))
	return render_template(
		"edit_restaurant.html", 
		place_id=place_id, 
		edit_rest=edit_rest
		) 

@home_blueprint.route("/restaurant/<int:place_id>/delete", methods=["GET", "POST"])
@login_required
def delete_place(place_id):
	delete_rest = Place.query.filter_by(id=place_id).one()
	if request.method == "POST":
		db.session.delete(delete_rest)
		db.session.commit()
		flash("You just deleted %s" % delete_rest.name, "danger")
		return redirect(url_for("home.show_places"))
	return render_template(
		"delete_restaurant.html", 
		place_id=place_id, 
		delete_rest=delete_rest
		)
	
@home_blueprint.route("/restaurant/<int:place_id>/menu")
@home_blueprint.route("/restaurant/<int:place_id>")
def show_menu(place_id):
	place = Place.query.filter_by(id = place_id).one()
	menuitems = Menu.query.filter(Menu.place_id == place_id).all()
	return render_template(
		"menu.html", 
		place=place,
		menuitems=menuitems
		)

@home_blueprint.route("/restaurant/<int:place_id>/menu/new", methods=["GET", "POST"])
@login_required
def new_menu_item(place_id):
	if request.method == "POST":
		new_menu = Menu(
			name = request.form["name"],
			course = request.form["course"],
			description = request.form["description"],
			price = request.form["price"],
			place_id = place_id,
			user_id = login_session['user_id'] 
			)
		db.session.add(new_menu)
		db.session.commit()
		flash("Just add a new menu item", "success")
		return redirect(url_for("home.show_menu", place_id=place_id))
	return render_template(
		"new_menu.html", 
		place_id=place_id)

@home_blueprint.route("/restaurant/<int:place_id>/menu/<int:menu_id>/edit", methods=["GET","POST"])
@login_required
def edit_menu_item(place_id,menu_id):
	edit_menu = Menu.query.filter_by(id=menu_id).one()
	if request.method == "POST":
		if request.form["name"]:
			edit_menu.name = request.form["name"]
		if request.form['course']:
			edit_menu.course = request.form["course"]
		if request.form['description']:
			edit_menu.description = request.form["description"]
		if request.form['price']:
			edit_menu.price = request.form["price"]
		edit_menu.last_edit = current_user.id
		db.session.add(edit_menu)
		db.session.commit()
		flash("Just edited menu item")
		return redirect(url_for("home.show_menu", place_id=place_id))
	return render_template("edit_menu.html", 
		place_id=place_id, 
		menu_id=menu_id,
		edit_menu=edit_menu
		)

@home_blueprint.route("/restaurant/<int:place_id>/menu/<int:menu_id>/delete", methods=["GET","POST"])
@login_required
def delete_menu_item(place_id,menu_id):
	delete_menu = Menu.query.filter_by(id=menu_id).one()
	if request.method == "POST":
		db.session.delete(delete_menu)
		db.session.commit()
		flash("You just deleted %s" % delete_menu.name, "danger")
		return redirect(url_for("home.show_menu", place_id=place_id))
	return render_template(
		"delete_menu.html", 
		place_id=place_id, 
		menu_id=menu_id,
		delete_menu=delete_menu
		)

