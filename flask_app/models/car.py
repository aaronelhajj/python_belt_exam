from flask.globals import request
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
from flask_app.models import user
bcrypt = Bcrypt(app)
import re
from flask import flash

class Car:
    db = 'third_attempt'
    def __init__(self, data):
        self.id = data['id']
        self.price = data['price']
        self.model = data['model']
        self.make = data['make']
        self.year = data['year']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.seller = None
        self.purchased = False
        self.buyer = None
    
    @classmethod
    def get_all(cls):
        query = 'SELECT * from cars left join users on user_id = users.id left join purchases on purchases.car_id = cars.id;'
        results = connectToMySQL(cls.db).query_db(query)
        all_cars = []
        for car in results:
            this_car = cls(car)
            data = {
                'id': car['users.id']
            }
            this_seller = user.User.get_by_id(data)
            this_car.seller = this_seller
            if car['car_id'] == car['id']:
                this_car.purchased = True
            all_cars.append(this_car)
        return all_cars
        
    @classmethod
    def add_car(cls, data):
        query = 'INSERT into cars (price, model, make, year, description, user_id) VALUE (%(price)s,%(model)s,%(make)s,%(year)s,%(description)s,%(user_id)s);'
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def update_car(cls, data):
        query = 'UPDATE cars SET price = %(price)s, model = %(model)s, make = %(make)s, year = %(year)s, description = %(description)s, user_id = %(user_id)s where id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def get_by_id(cls, data):
        query = 'SELECT * from cars join users on user_id = users.id where cars.id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        car_obj = cls(results[0])
        user_data = {
            'id': results[0]['users.id']
        }
        user_obj = user.User.get_by_id(user_data)
        car_obj.seller = user_obj
        return car_obj

    @classmethod
    def purchase_car(cls, data):
        query = 'INSERT into purchases (car_id, user_id) VALUE (%(car_id)s, %(user_id)s);'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_purchased_cars(cls, data):
        query = 'select * from cars left join purchases on purchases.car_id = cars.id left join users on purchases.user_id = users.id where users.id = %(users_id)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        all_purchases = []
        for purchase in results:
            this_purchase = cls(purchase)
            all_purchases.append(this_purchase)
        return all_purchases

    @classmethod
    def destroy(cls, data):
        query = 'delete from cars where id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query,data)

    @staticmethod
    def validate_info(data):
        is_valid = True
        if data['price'] == '' or int(data['price']) < 1:
            flash('Enter a positive price.', 'car')
            is_valid = False
        if len(data['model']) < 1:
            flash('Please enter a model', 'car')
            is_valid = False
        if len(data['make']) < 1:
            flash('Please enter a Maker', 'car')
            is_valid = False
        if data['year'] == '' or int(data['year']) < 1900:
            flash('Please enter a valid year', 'car')
            is_valid = False
        if len(data['description']) < 1:
            flash('Please enter a valid description', 'car')
            is_valid = False
        return is_valid