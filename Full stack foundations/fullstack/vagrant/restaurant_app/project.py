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


@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])



# #ADD JSON API ENDPOINT HERE
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem=menuItem.serialize)
    

@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/menu')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
    return render_template('menu.html', restaurant=restaurant, items = items, restaurant_id = restaurant_id)




@app.route('/restaurant/<int:restaurant_id>/new', methods=['GET','POST'])
def newMenuItem(restaurant_id):
    
    if request.method == 'POST':
        newItem = MenuItem(name = request.form['name'], description = request.form['description'], price = request.form['price'], course = request.form['course'], restaurant_id = restaurant_id)
        session.add(newItem)
        session.commit()
        flash("new menu item created")
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id = restaurant_id)




@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit', methods = ['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    editedItem = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['name']
        if request.form['price']:
            editedItem.price = request.form['price']
        if request.form['course']:
            editedItem.course = request.form['course']
        session.add(editedItem)
        session.commit()
        flash("Menu item edited")
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        
        return render_template('editmenuitem.html', restaurant_id = restaurant_id, menu_id = menu_id, item = editedItem)
    


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete', methods = ['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
    itemToDelete = session.query(MenuItem).filter_by(id = menu_id).one() 
    print(itemToDelete)
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("Menu item deleted")
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template('deletemenuitem.html', item = itemToDelete)



if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = False
    app.run(host = '0.0.0.0', port = 5000)