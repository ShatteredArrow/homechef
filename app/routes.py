from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm, AddRecipe

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'chook'}
    recipes = [
        {
            'name': 'Fried Chicken',
            'type': 'Entree'
        },
        {
            'name': 'Green Beans',
            'name': 'Side'
        }
    ]
    return render_template('index.html', title='Home', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user={}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/meal')
def meal():
    meals = [
        {
            'name': 'Fried Chicken',
            'type': 'Entree'
        },
        {
            'name': 'Green Beans',
            'type': 'Side'
        }
    ]
    return render_template('meal.html', title='Meal', meals=meals)

@app.route('/recipe')
def recipe():
    recipes = [
        {
            'title': 'Country Fried Chicken',
            'author': 'Chookiee',
            'link': 'https://www.google.com',
            'ingredients': "1 egg, 1 chicken, bread crumbs",
            'rating': 3,
            'difficulty': 4,
            'tried_recipe': False,
            'meal_id': 0
        },
        {
            'title': 'Vegan Fried Chicken',
            'author': 'Chookiee',
            'link': 'https://www.google.com',
            'ingredients': "greens, bread crumbs, ",
            'rating': 1,
            'difficulty': 5,
            'tried_recipe': True,
            'meal_id': 0
        }
    ]
    return render_template('recipe.html', title='Recipe', recipes=recipes)

@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    form = AddRecipe()
    if form.validate_on_submit():
        flash('Successfully added recipe: {}'.format(
            form.title.data))
        return redirect(url_for('recipe'))
    return render_template('add_recipe.html', title='Add Recipe', form=form)
