from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask_wtf.file import FileRequired

from wtforms import SelectField, SelectMultipleField, FileField
from app import app
from app.models import Tag

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
    
class AddTag(FlaskForm):
    name = StringField('Name')
    add = SubmitField('Add Tag')

class SelectTag(FlaskForm):
    search = SubmitField("Search Tag")

class DeleteTag(FlaskForm):
    delete = SubmitField("Delete Tag")

class TagList(AddTag, SelectTag, DeleteTag):
    tags = SelectMultipleField('Tag', choices=[], coerce=int,)

class TagWithAdd(AddTag):
    tags = SelectMultipleField('Tag', choices=[], coerce=int,)
    
class Recipe(TagWithAdd):
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author',validators=[DataRequired()])
    link = StringField('Link',validators=[DataRequired()])
    ingredients = TextAreaField('Ingredients', render_kw={"rows": 10, "cols": 100}, validators=[DataRequired()])
    recipe_image = FileField('Image File')
    #recipe_image = FileField('Image File', validators=[FileRequired()])

class AddRecipe(Recipe):
    submit = SubmitField('Add Recipe')

class UpdateRecipe(Recipe):
    submit = SubmitField('Update Recipe')


