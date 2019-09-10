from app import db, login
from hashlib import md5
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    category = db.Column(db.String(64))

    def __repr__(self):
        return '<Meal {}>'.format(self.name)



class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    author = db.Column(db.String(64))
    link = db.Column(db.String(128))
    ingredients = db.Column(db.String(254))
    rating = db.Column(db.Integer)
    difficulty = db.Column(db.Integer)
    tried_recipe = db.Column(db.Boolean)
    meal_id = db.Column(db.Integer, db.ForeignKey('meal.id'))
    
    def __repr__(self):
        return '<Recipe {}>'.format(self.name)

