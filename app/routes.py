'''Recipie Saver'''
import os
from flask import render_template, flash, redirect, url_for, request
from sqlalchemy.orm import sessionmaker
from app import app, db
from app.forms import LoginForm, AddRecipe, AddTag, SelectTag
from app.models import Recipe, Tag, recipeTag
from app import Config


@app.route('/')
@app.route('/index')
def index():
    """Return URL for index.html"""
    user = {'username': 'chook'}
    return render_template('index.html', title='Home', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Return URL for login.html"""
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user={}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/recipe_index', methods=['GET', 'POST'])
def recipe_index():
    """Return URL for recipie_index.html"""
    categories = [(c.id, c.name) for c in Tag.query.all()]
    form = SelectTag(request.form)
    form.tags.choices = categories
    recipes = []
    if form.validate():
        tags_id = form.tags.data
        for tag_id in tags_id:
            match = db.session.query(Recipe).filter(Recipe.tags.any(id=tag_id)).all()
            recipes += match
        return render_template('recipe_index.html', title='Recipe Index', form=form, recipes=recipes)
    
    recipes = Recipe.query.all()
    return render_template('recipe_index.html', title='Recipe Index', form=form, recipes=recipes)

@app.route('/add_tag', methods=['GET', 'POST'])
def add_tag():
    """Return URL for add_tag.html"""
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
    return render_template('recipe.html', title='Recipe', recipe=recipe)

@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    categories = [(c.id, c.name) for c in Tag.query.all()]
    form = AddRecipe()
    form.tags.choices = categories

    if form.validate_on_submit():
        print(type(form.tags.data))
        recipe = Recipe(
            title=form.title.data,
            author=form.author.data,
            link=form.link.data,
            ingredients=form.ingredients.data,
            
        )
        tags = Tag.query.filter(Tag.id.in_(form.tags.data))
        recipe.tags.extend(tags)
        db.session.add(recipe)
        db.session.commit()
        flash('Successfully added recipe: {}'.format(
            form.title.data))
        return redirect(url_for('recipe_index'))
    return render_template('add_recipe.html', title='Add Recipe', form=form)

@app.route('/<recipe_id>/update_recipe', methods=['GET', 'POST'])
def update_recipe(recipe_id):
    
    categories = [(c.id, c.name) for c in Tag.query.all()]
    
    recipe = Recipe.query.filter_by(id=recipe_id).first_or_404()
    
    
    form = AddRecipe(obj=recipe)
    form.tags.choices = categories
    if form.validate_on_submit():
        
        recipe.title=form.title.data,
        recipe.author=form.author.data,
        recipe.link=form.link.data,
        recipe.ingredients=form.ingredients.data
        tags = Tag.query.filter(Tag.id.in_(form.tags.data))
        recipe.tags.extend(tags)
        
        #form.populate_obj(recipe)
        db.session.commit()
        return redirect(url_for('recipe', recipe_id=recipe_id))
    return render_template('edit_recipe.html', title='Update Recipe', form=form,recipes=recipe)




