from datetime import datetime
from sqlalchemy.orm import backref
from flasklib import db, login_manager
from flask_login import UserMixin
from flask_login import current_user

from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

book_shelf = db.Table('book_shelf',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('library_title_id', db.Integer, db.ForeignKey('library_title.id'), primary_key=True)
)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    wishlist_titles = db.relationship('Wishlist_title', backref='user')
    library_titles = db.relationship('Library_title', backref='user')

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    born = db.Column(db.Integer, nullable=False)
    died = db.Column(db.Integer)

    titles = db.relationship('Title', backref='author')

class Title(db.Model):
    isbn = db.Column(db.String(17), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    release_year = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(25), nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    wishlist_titles = db.relationship('Wishlist_title', backref='title')
    library_titles = db.relationship('Library_title', backref='title')
    notes = db.relationship('Note', backref='title')

class Wishlist_title(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_added = db.Column(DateTime, default=datetime.utcnow)

    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(17), db.ForeignKey('title.isbn'))

class Library_title(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_added = db.Column(DateTime, default=datetime.utcnow)
    page = db.Column(db.Integer, nullable=False)

    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(17), db.ForeignKey('title.isbn'))
    shelfs = db.relationship('Shelf', secondary=book_shelf,back_populates='library_titles')

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    text = db.Column(db.String(1000), nullable=False)
    start_page = db.Column(db.Integer, nullable=False)
    end_page = db.Column(db.Integer, nullable=False)

    title = db.Column(db.String(17), db.ForeignKey('title.isbn'))

class Shelf(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    library_titles = db.Column(db.Integer, db.ForeignKey('library_title.id'))
    library_titles = db.relationship('Library_title', secondary=book_shelf,back_populates='shelfs')

class MyModelView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated:
            return True
        else:
            return False

    def inaccessible_callback(self,name, **kwargs):
        return redirect(url_for('login'))

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated:
            return True
        else:
            return False
'''