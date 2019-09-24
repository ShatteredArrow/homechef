from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, AddRecipe, AddTag, SelectTag
from app.models import Recipe, Tag, recipeTag
from sqlalchemy.orm import sessionmaker
from app import Config
import os
basedir= os.path.abspath(os.path.dirname(__file__))

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'chook'}
    return render_template('index.html', title='Home', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user={}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/recipe_index',  methods=['GET', 'POST'])
def recipe_index():
    categories = [(c.id, c.name) for c in Tag.query.all()]
    form = SelectTag(request.form)
    form.tags.choices = categories
    recipes=[]
    if form.validate():
        tags_id = form.tags.data
        for tag_id in tags_id:
            match=db.session.query(Recipe).filter(Recipe.tags.any(id=tag_id)).all()
            recipes += match
       
    else:
        recipes = Recipe.query.all()



    return render_template('recipe_index.html', title='Recipe Index', form=form, recipes=recipes)

@app.route('/add_tag', methods=['GET', 'POST'])
def add_tag():
    form = AddTag()
    if form.validate_on_submit():
        tag = Tag(
            name=form.name.data,
        )
        db.session.add(tag)
        db.session.commit()
        flash('Successfully added tag: {}'.format(
            form.name.data))
        return redirect(url_for('recipe_index'))
    return render_template('add_tag.html', title='Add Tag', form=form)

@app.route('/recipe/<recipe_id>')
def recipe(recipe_id):
    recipe = Recipe.query.filter_by(id=recipe_id).first_or_404()
    return render_template('recipe.html', title='Recipe', recipes=recipe)

@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    form = AddRecipe()
    if form.validate_on_submit():
        recipe = Recipe(
            title=form.title.data,
            author=form.author.data,
            link=form.link.data,
            ingredients=form.ingredients.data
        )
        #recipe.tags.extend(Tag.query.filter_by(id=tag_id).all())
        db.session.add(recipe)
        db.session.commit()
        flash('Successfully added recipe: {}'.format(
            form.title.data))
        return redirect(url_for('recipe'))
    return render_template('add_recipe.html', title='Add Recipe', form=form)



def select_tag(request, id):
    tag = Tag.query.get(id)
    form = SelectTag(request.POST, obj=tag)
    form.tag_id.choices = [(g.id, g.name) for g in Tag.query.order_by('name')]
