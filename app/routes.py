'''recipe Saver'''
import os
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from sqlalchemy.orm import sessionmaker
from app import app, db
from app.forms import LoginForm, AddRecipe, TagList, UpdateRecipe, AddTag
from app.models import Recipe, Tag, recipeTag
from app import Config
from werkzeug.utils import secure_filename
from flask import send_from_directory
from app.image import Image

'''
#Not Used
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
        flash('Login requested for user={}, remember_me={}'.format(form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)
'''

@app.route('/')
@app.route('/recipe_index', methods=['GET', 'POST'])
def recipe_index():
    """Return URL for recipe_index.html"""
    categories = [(c.id, c.name) for c in Tag.query.all()]
    recipeForm = AddRecipe()
    recipeForm.tags.choices = categories

    tagForm = AddTag()
    
    TagForm = TagList()  
    #TagForm.tags.choices = categories
    
    recipes = Recipe.query.all()
    if TagForm.validate_on_submit():
        if TagForm.search.data:
            print("TagForm submitted")
            tags_id = TagForm.tags.data
            recipes = []
            for tag_id in tags_id:
                match = db.session.query(Recipe).filter(Recipe.tags.any(id=tag_id)).all()
                recipes += match
        if TagForm.delete.data:
            tags_id = TagForm.tags.data
            for tag_id in tags_id:
                Tag.query.filter_by(id=tag_id).delete()
            db.session.commit() 
            return redirect(url_for('recipe_index'))
    if AddForm.validate_on_submit():
        recipe = Recipe()
        recipe.add_recipe(AddForm.data)
        #add_new_recipe(AddForm)
        return redirect(url_for('recipe_index'))
    if AddTagForm.validate_on_submit():
        add_tag(AddTagForm.name.data)
        return redirect(url_for('recipe_index'))
    else:
        print("Nothing")


    return render_template('recipe_index.html', title='Recipe Index', form=TagForm, recipes=recipes, recipeForm=recipeForm, tagForm=tagForm)

@app.route('/recipe/<recipe_id>',methods=['GET', 'POST'])
def recipe(recipe_id):
    recipe = Recipe.query.filter_by(id=recipe_id).first_or_404()
    recipe.ingredients = recipe.ingredients.split('\n')
    return render_template('recipe.html', title='Recipe', recipe=recipe, recipe_image=recipe.recipe_image)

@app.route('/<recipe_id>/update_recipe', methods=['GET', 'POST'])
def update_recipe(recipe_id):
    #categories = [(c.id, c.name) for c in Tag.query.all()]
    recipe = Recipe.query.filter_by(id=recipe_id).first_or_404()
    recipeForm = UpdateRecipe(obj=recipe)
    tagForm = AddTag()

    #form.tags.choices = categories
    if recipeForm.validate_on_submit():
        # If new image added, then update. Otherwise keep old image
        recipe.update_recipe(recipeForm.data)
        return redirect(url_for('recipe', recipe_id=recipe_id))
    elif tagForm.validate_on_submit():
        add_tag(tagForm.name.data)
        return redirect(url_for('update_recipe'))
    return render_template('edit_recipe.html', title='Update Recipe', recipeForm=recipeForm, recipes=recipe, tagForm=tagForm)


#Delete recipe needs fixing
@app.route('/<recipe_id>/delete_recipe', methods=['GET', 'POST'])
def delete_recipe(recipe_id):
    #Delete the image assosciated with the recipe 1st
    image = os.path.join(app.config['UPLOAD_FOLDER'], Recipe.query.filter_by(id=recipe_id).first_or_404().recipe_image)
    if os.path.exists(image):
        os.remove(image)
    #Then delete the recipe item from the database
    Recipe.query.filter_by(id=recipe_id).delete()
    db.session.commit()
    return redirect(url_for('recipe_index'))


'''
#Not used
#Create Links to the recipe Image file path or imgurl
@app.route('/uploads/<link>')
def uploaded_file(link):
    img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    if not os.path.exists(img_path):
        return send_from_directory(app.config['UPLOAD_FOLDER'], 'image-placeholder.png')
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

'''


def add_tag(tag_name):
    tag_name = tag_name.lower();
    if Tag.query.filter_by(name=tag_name).first():
        flash('Tag "{}" already exists'.format(
            tag_name))
    else:
        tag = Tag(
            name=tag_name,
        )
        db.session.add(tag)
        db.session.commit()
        flash('Successfully added tag: {}'.format(
            tag_name))

