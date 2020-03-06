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
        flash('Login requested for user={}, remember_me={}'.format(form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/recipe_index', methods=['GET', 'POST'])
def recipe_index():
    """Return URL for recipe_index.html"""
    categories = [(c.id, c.name) for c in Tag.query.all()]
    AddForm = AddRecipe()
    AddForm.tags.choices = categories

    AddTagForm = AddTag()
    
    TagForm = TagList(request.form)  
    TagForm.tags.choices = categories
    
    recipes = Recipe.query.all()
    if request.method  == 'POST':
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
            add_new_recipe(AddForm)
            return redirect(url_for('recipe_index'))
        if AddTagForm.validate_on_submit():
            add_tag(AddTagForm.name.data)
            return redirect(url_for('recipe_index'))
        else:
            print("Nothing")


    return render_template('recipe_index.html', title='Recipe Index', form=TagForm, recipes=recipes, addform=AddForm, addTagForm=AddTagForm)

@app.route('/recipe/<recipe_id>',methods=['GET', 'POST'])
def recipe(recipe_id):
    recipe = Recipe.query.filter_by(id=recipe_id).first_or_404()
    recipe.ingredients = recipe.ingredients.split('\n')
    return render_template('recipe.html', title='Recipe', recipe=recipe, recipe_image=recipe.recipe_image)

@app.route('/<recipe_id>/update_recipe', methods=['GET', 'POST'])
def update_recipe(recipe_id):
    categories = [(c.id, c.name) for c in Tag.query.all()]
    recipe = Recipe.query.filter_by(id=recipe_id).first_or_404()
    form = UpdateRecipe(obj=recipe)
    AddTagForm = AddTag()

    form.tags.choices = categories
    if form.validate_on_submit():
        if form.submit.data:
            # If new image added, then update. Otherwise keep old image
            if form.recipe_image.data:
                imageSave(form.recipe_image.data)
                recipe.recipe_image = imageSave.filename
            recipe.title = form.title.data.title()
            recipe.author = form.author.data
            recipe.link = form.link.data
            recipe.ingredients = form.ingredients.data
            recipe.rating = request.form.get('rating')

            if not recipe.rating:
                recipe.rating = 0

            tags = Tag.query.filter(Tag.id.in_(form.tags.data))
            recipe.tags.extend(tags)
            db.session.commit()
            return redirect(url_for('recipe', recipe_id=recipe_id))
    elif AddTagForm.validate_on_submit():
        add_tag(AddTagForm.name.data)
        AddTagForm.name.data=""
        categories = [(c.id, c.name) for c in Tag.query.all()]
        form.tags.choices = categories
    return render_template('edit_recipe.html', title='Update Recipe', form=form, recipes=recipe, addTagForm=AddTagForm)

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


#Create Links to the recipe Image file path or imgurl
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    if not os.path.exists(img_path):
        return send_from_directory(app.config['UPLOAD_FOLDER'], 'image-placeholder.png')
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)




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


def add_new_recipe(AddForm):
    imageObj=Image(AddForm.recipe_image.data)

    
    recipe = Recipe(
        title=AddForm.title.data.title(),
        author=AddForm.author.data,
        link=AddForm.link.data,
        ingredients=AddForm.ingredients.data,
        recipe_image=imageObj.filename,
        rating = AddForm.rating.data
    )     
    if not recipe.rating:
        recipe.rating = 0
    tags = Tag.query.filter(Tag.id.in_(AddForm.tags.data))
    recipe.tags.extend(tags)

    db.session.add(recipe)
    db.session.commit()
