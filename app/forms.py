from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField,RadioField
from wtforms.validators import DataRequired, Regexp
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
    author = StringField('Author',validators=[DataRequired()])
    link = StringField('Link',validators=[DataRequired()])
    ingredients = TextAreaField('Ingredients', render_kw={"rows": 10, "cols": 60}, validators=[DataRequired()])
    rating = RadioField('Rating',choices=[('1',''),('2','2'),('3','3'),('4','4'),('5','5')],id="rating")
    recipe_image = FileField('Image File')
    #recipe_image = FileField('Image File', validators=[FileRequired()])

class AddRecipe(Recipe):
    submit = SubmitField('Add Recipe')

class UpdateRecipe(Recipe):
    submit = SubmitField('Update Recipe')


