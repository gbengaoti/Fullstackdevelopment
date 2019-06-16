# Final project for udacity Full stack foundations
# This project is a restaurant menu app

from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

session_factory = sessionmaker(bind=engine)
session = scoped_session(session_factory)

@app.before_request
def before_request():
    session()

@app.after_request
def close_session(response):
    session.remove()
    return(response)

@app.route('/restaurants/JSON')
def restaurantsJSON():
    # get all restaurants
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurants=[r.serialize for r in restaurants])


@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    # get restaurant by id
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    # get menu item by id
    menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem=menuItem.serialize)

@app.route('/')
@app.route('/restaurants')
def showRestaurants():
    # get restaurants from the database
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants=restaurants)


@app.route('/restaurant/new', methods=['GET','POST'])
def newRestaurant():
    # add new restaurant to table Restaurants
    if request.method == 'POST':
        newRestaurant = Restaurant(name = request.form['name'])
        session.add(newRestaurant)
        session.commit()
        flash("New Restaurant Created")
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newrestaurant.html')


@app.route('/restaurant/<int:restaurant_id>/edit' , methods=['GET','POST'])
def editRestaurant(restaurant_id):
	# get restaurant detail from database using id
    editedRestaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedRestaurant.name = request.form['name']
        session.add(editedRestaurant)
        session.commit()
        flash("Restaurant Successfully Edited")
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('editrestaurant.html', restaurant=editedRestaurant)


@app.route('/restaurant/<int:restaurant_id>/delete' , methods=['GET','POST'])
def deleteRestaurant(restaurant_id):
    # get item from db then delete
    toDeleteRestaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        session.delete(toDeleteRestaurant)
        session.commit()
        flash("Restaurant Successfully Deleted")
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('deleterestaurant.html', restaurant=toDeleteRestaurant)


@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    # get menu for restaurant using id
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    return render_template('menu.html', restaurant=restaurant, items = items, restaurant_id = restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/menu/new' , methods=['GET','POST'])
def newMenuItem(restaurant_id):
    # add new menu item to respective restaurant
    if request.method == 'POST':
        newItem = MenuItem(name = request.form['name'], description = request.form['description'], price = request.form['price'], course = request.form['course'], restaurant_id = restaurant_id)
        session.add(newItem)
        session.commit()
        flash("Menu Item Created")
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit' , methods=['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
    # get item to edit and commit changes if any is made
    editedItem = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']
        if request.form['course']:
            editedItem.course = request.form['course']
        session.add(editedItem)
        session.commit()
        flash("Menu Item Successfully Edited(menu.html)")
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('editmenuitem.html', restaurant_id=restaurant_id, item = editedItem)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete' , methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
    # get item to delete then delete it
    itemToDelete = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("Menu Item Successfully Deleted(restaurants.html)")
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('deletemenuitem.html', restaurant_id=restaurant_id, item = itemToDelete)


if __name__ == '__main__':
    app.secret_key = 'super_secret_keys'
    app.debug = False
    app.run(host = '0.0.0.0', port = 5000)