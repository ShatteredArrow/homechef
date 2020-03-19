
from app import db, login
from hashlib import md5
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.image import Image


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

recipeTag = db.Table(
    'recipeTag',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    recipes = db.relationship('Recipe',
                            secondary=recipeTag,
                            back_populates='tags')
    def __repr__(self):
        return '{}'.format(self.id)

#Recipes Needs a new column called image hash
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    author = db.Column(db.String(64))
    link = db.Column(db.String(128))
    ingredients = db.Column(db.String(254))
    rating = db.Column(db.Integer,default=0)
    difficulty = db.Column(db.Integer)
    tried_recipe = db.Column(db.Boolean)
    recipe_image = db.Column(db.String(128))
    tags = db.relationship('Tag', 
                            secondary=recipeTag, 
                            back_populates='recipes')

       



    def __repr__(self):
       return '{}'.format(self.id)

    def update_recipe(self,formDict):
        if formDict.get("image_source_link"):
            imageObj=Image(formDict.get("image_source_link"))
            formDict.update(image_source_link=imageObj.imgur_url)
            formDict['recipe_image'] = formDict.pop('image_source_link') 
        for key, value in formDict.items():
            try:
                setattr(self, key, value)
            except AttributeError:
                pass
        tags = Tag.query.filter(Tag.id.in_(formDict.get("tags")))
        self.tags.extend(tags)
        db.session.commit()

    def add_recipe(self,formDict):
        if formDict.get("image_source_link"):
            imageObj=Image(formDict.get("image_source_link"))
            formDict.update(image_source_link=imageObj.imgur_url)
            formDict['recipe_image'] = formDict.pop('image_source_link') 
        for key, value in formDict.items():
            try:
                setattr(self, key, value)
            except AttributeError:
                pass
        tags = Tag.query.filter(Tag.id.in_(formDict.get("tags")))
        self.tags.extend(tags)
        db.session.add(self)
        db.session.commit()

