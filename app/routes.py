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

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
imageFile = app.config['UPLOAD_FOLDER']








def imageSave(recipeImageData):
    if recipeImageData.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if recipeImageData and allowed_file(recipeImageData.filename):
        filename = secure_filename(str(datetime.now()) + recipeImageData.filename)
        recipeImageData.save(os.path.join(imageFile, filename))
    imageSave.filename=filename
    



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
                categories = [(c.id, c.name) for c in Tag.query.all()]
                TagForm.tags.choices = categories
        if AddForm.validate_on_submit():
            print("submitted add form")
            imageSave(AddForm.recipe_image.data)
            recipe = Recipe(
            title=AddForm.title.data,
            author=AddForm.author.data,
            link=AddForm.link.data,
            ingredients=AddForm.ingredients.data,
            recipe_image=imageSave.filename,
            rating = request.form.get('rating')
            )     
            if not recipe.rating:
                recipe.rating = 0
            tags = Tag.query.filter(Tag.id.in_(AddForm.tags.data))
            recipe.tags.extend(tags)
            db.session.add(recipe)
            db.session.commit()
        if AddTagForm.validate_on_submit():
            add_tag(AddTagForm.name.data)
            AddTagForm.name.data=""
            categories = [(c.id, c.name) for c in Tag.query.all()]
            TagForm.tags.choices = categories
    return render_template('recipe_index.html', title='Recipe Index', form=TagForm, recipes=recipes, addform=AddForm, addTagForm=AddTagForm)

@app.route('/recipe/<recipe_id>',methods=['GET', 'POST'])
def recipe(recipe_id):
    recipe = Recipe.query.filter_by(id=recipe_id).first_or_404()
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
            imageSave(form.recipe_image.data)
            recipe.title = form.title.data
            recipe.author = form.author.data
            recipe.link = form.link.data
            recipe.ingredients = form.ingredients.data
            recipe.rating = request.form.get('rating')
            recipe.recipe_image = imageSave.filename

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
    Recipe.query.filter_by(id=recipe_id).delete()
    db.session.commit()
    return redirect(url_for('recipe_index'))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads/<filename>')
def uploaded_file(filename):
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

@app.route('/modal_add_recipe', methods=['GET', 'POST'])
def modal_add_recipe():
    categories = [(c.id, c.name) for c in Tag.query.all()]
    form = AddRecipe()
    form.tags.choices = categories

    if form.validate_on_submit():
        file = form.recipe_image.data
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(imageFile, filename))
        recipe = Recipe(
            title=form.title.data,
            author=form.author.data,
            link=form.link.data,
            ingredients=form.ingredients.data,
            recipe_image=filename,
            rating = request.form.get('rating')
        )     
        if not recipe.rating:
            recipe.rating = 0
        tags = Tag.query.filter(Tag.id.in_(form.tags.data))
        recipe.tags.extend(tags)
        db.session.add(recipe)
        db.session.commit()
        flash('Successfully added recipe: {}'.format(
            form.title.data))
        return redirect(url_for('recipe_index'))
    return render_template('modal_add_recipe.html', title='Add Recipe', form=form)

