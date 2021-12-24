from flask.globals import request
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
import re
from flask import flash
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class User:
    db = 'third_attempt'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.cars = []

    @classmethod
    def get_all(cls):
        query = 'SELECT * from users;'
        return connectToMySQL(cls.db).query_db(query)

    @classmethod
    def save(cls,data):
        query = 'INSERT INTO users (first_name, last_name, email, password) VALUE (%(first_name)s,%(last_name)s,%(email)s,%(password)s);'
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * from users where email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * from users where id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        user_obj = cls(results[0])
        return user_obj

    @staticmethod
    def validate_user(info):
        is_valid = True
        if len(info['first_name']) < 3:
            flash("First name must be at least 3 characters.", 'register')
        if len(info['last_name']) < 3:
            flash('Last name must be at least 3 characters.', 'register')
        if len(info['password']) < 8:
            flash('Password must be at least 8 characters.', 'register')
        if info['password'] != info['confirm_password']:
            flash('Passwords do not match!', 'register')
            is_valid = False
        if not EMAIL_REGEX.match(info['email']):
            flash("Invalid email address!", 'register')
            is_valid = False
        return is_valid
   