#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"



@app.route("/restaurants", methods = ['GET'])
def restaurants():
    # restaurants = [restaurant.to_dict() for restaurant in Restaurant.query.all()]
    # return restaurants
    restaurants = []
    for  i in Restaurant.query.all():

        restaurant_json = {
            "id": i.id,
            "name": i.name,
            "address": i.address,
        }
        restaurants.append(restaurant_json)
        response = make_response(jsonify(restaurants), 200)

    return response



@app.route('/restaurants/<int:id>', methods = ['GET'])
def get_restaurants_by_id(id):
    # restaurants = [restaurant.to_dict() for restaurant in Restaurant.query.filter_by(id=id).first()]
    # return restaurants
    restaurant = Restaurant.query.filter_by(id=id).first()

    if restaurant is None:
        response = jsonify({"error": f"Restaurant not found"})
        response.status_code = 404
        return response  
    

    restaurant_jsonified = jsonify(restaurant.to_dict())
    return restaurant_jsonified


@app.route('/restaurants/<int:id>', methods = ['DELETE'])
def delete_restaurants(id):
    restaurant = Restaurant.query.filter_by(id=id).first()

    if restaurant is None:
        response = jsonify({"error": "Restaurant not found"})
        response.status_code = 404
        return response

        
    db.session.delete(restaurant)
    db.session.commit()
    # 204 No Content status code 
    return '', 204



@app.route('/pizzas', methods = ['GET'])
def get_pizzas():
    pizzas = []
    for  i in Pizza.query.all():

        pizza_json = {
            "id": i.id,
            "ingredients": i.ingredients,
            "name": i.name,
        }
        pizzas.append(pizza_json)
        response = make_response(jsonify(pizzas), 200)
    return response
    

@app.route('/restaurant_pizzas', methods = ['POST'])
def restaurant_pizzas():
    json_data = request.get_json()

    
    price = json_data.get('price')
    if not (1 <= price <= 30):
        return jsonify({"errors": ["validation errors"]}), 400

    restaurant_pizza = RestaurantPizza(
        price=price,
        pizza_id=json_data.get('pizza_id'),
        restaurant_id=json_data.get('restaurant_id')
    )
    db.session.add(restaurant_pizza)
    db.session.commit()

    restaurant_pizza_dict = restaurant_pizza.to_dict()
    return jsonify(restaurant_pizza_dict), 201




if __name__ == "__main__":
    app.run(port=5555, debug=True)
