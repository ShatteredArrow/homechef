from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from wtforms import SelectField, SelectMultipleField
from app import app
from app.models import Tag

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class AddRecipe(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    link = StringField('Link', validators=[DataRequired()])
    ingredients = StringField('Ingredients', validators=[DataRequired()])
    tags = SelectMultipleField('Tag', choices=[], coerce=int)
    submit = SubmitField('Add Recipe')

class AddTag(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Add Tag')

class SelectTag(FlaskForm):
    tags = SelectMultipleField('Tag', choices=[], coerce=int)

