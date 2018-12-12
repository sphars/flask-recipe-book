from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

recipe_categories = db.Table(
    'recipe_categories',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id')),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    recipes = db.relationship('Recipe', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=True, nullable=False)
    description = db.Column(db.Text)
    ingredients = db.Column(db.Text)
    instructions = db.Column(db.Text)
    timestamp = db.Column(db.Date, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    categories = db.relationship('Category',
        secondary=recipe_categories,
        primaryjoin=(recipe_categories.c.recipe_id == id),
        backref=db.backref('recipes', lazy='dynamic'),
        lazy='dynamic')

    def __repr__(self):
        return '<Recipe {}>'.format(self.title)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(65), unique=True, nullable=False, index=True)

    def __repr__(self):
        return '<Category {}>'.format(self.name)
