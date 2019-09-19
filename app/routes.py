from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, AddRecipe, AddTag, SelectTag
from app.models import Recipe, Tag


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


@app.route('/recipe_index')
def recipe_index():
    categories = [(c.id, c.name) for c in Tag.query.all()]
    form = SelectTag(request.form)
    form.tag.choices = categories

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

@app.route('/recipe/<tag_id>')
def recipe(tag_id):
    tag = Tag.query.filter_by(id=tag_id).first_or_404()
    return render_template('recipe.html', title='Recipe', recipes=tag.recipes, tag_id=tag.id)

@app.route('/add_recipe/<tag_id>', methods=['GET', 'POST'])
def add_recipe(tag_id):
    form = AddRecipe()
    if form.validate_on_submit():
        recipe = Recipe(
            title=form.title.data,
            author=form.author.data,
            link=form.link.data,
            ingredients=form.ingredients.data
        )
        recipe.tags.extend(Tag.query.filter_by(id=tag_id).all())
        db.session.add(recipe)
        db.session.commit()
        flash('Successfully added recipe: {}'.format(
            form.title.data))
        return redirect(url_for('recipe', tag_id=tag_id))
    return render_template('add_recipe.html', title='Add Recipe', tag_id=tag_id, form=form)



def select_tag(request, id):
    tag = Tag.query.get(id)
    form = SelectTag(request.POST, obj=tag)
    form.tag_id.choices = [(g.id, g.name) for g in Tag.query.order_by('name')]
