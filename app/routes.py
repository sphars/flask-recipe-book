from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User, Recipe, Category
from werkzeug.urls import url_parse
import random

@app.route('/')
@app.route('/index')
def index():
    random_recipe = Recipe.query.get(random.randint(1, Recipe.query.count()))
    return render_template('index.html', recipe=random_recipe)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/my-recipes')
@login_required
def my_recipes():
    return render_template('my-recipes.html')

@app.route('/authors')
def authors():
    authors = User.query.order_by(User.first_name.desc()).all()
    return render_template('authors.html', authors=authors)

@app.route('/author/<author_id>')
def author(author_id):
    author = User.query.filter_by(id=author_id).first_or_404()
    return render_template('author.html', author=author)

@app.route('/recipes')
def recipes():
    recipes = Recipe.query.all()
    return render_template('recipes.html', recipes=recipes)

@app.route('/recipe/<recipe_id>')
def recipe(recipe_id):
    recipe = Recipe.query.filter_by(id=recipe_id).first_or_404()
    return render_template('recipe.html', recipe=recipe)

@app.route('/categories')
def categories():
    categories = Category.query.all()
    return render_template('categories.html', categories=categories)

@app.route('/category/<category_id>')
def category(category_id):
    category = Category.query.filter_by(id=category_id).first_or_404()
    return render_template('category.html', category=category)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('my_recipes')
        return redirect(next_page)
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('my_recipes'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, first_name=form.first_name.data, last_name=form.last_name.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering! Please login below.')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)