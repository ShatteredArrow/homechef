from flask_wtf import FlaskForm
from wtforms.fields.html5 import URLField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField,RadioField
from wtforms.validators import DataRequired, Regexp
from flask_wtf.file import FileRequired
from wtforms import SelectField, SelectMultipleField, FileField
#from app import app
from app.models import Tag

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
    
class AddTag(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Regexp('^[A-Za-z]+$')])
    submit = SubmitField('Add Tag')

class SelectTag(FlaskForm):
    search = SubmitField("Search Tag")

class DeleteTag(FlaskForm):
    delete = SubmitField("Delete Tag")

class TagList(SelectTag, DeleteTag):
    tags = SelectMultipleField('Tag', choices=[], coerce=int,)

class TagWithAdd(FlaskForm):
    tags = SelectMultipleField('Tag', choices=[], coerce=int,)
    
class Recipe(TagWithAdd):
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author')
    link = StringField('Link')
    ingredients = TextAreaField('Ingredients')
    rating = RadioField('Rating', choices=[('5',''),('4',''),('3',''),('2',''),('1',''),('0','')], id="rating",default='0')
    image_source_link = StringField('URL for Image')
    image_source_file = FileField('Image File')

class AddRecipe(Recipe):
    submit = SubmitField('Add Recipe')

class UpdateRecipe(Recipe):
    submit = SubmitField('Update Recipe')


