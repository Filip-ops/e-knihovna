from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from models import User, Author, Title, Wishlist_title, Library_title, Note, Shelf
#from forms import //////////// ADD FORMS
app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://vatqztvxwsroxt:59ef0b95be0a73506825730a56774113565ef8451273319ec6963ac22a00ef71@ec2-52-17-1-206.eu-west-1.compute.amazonaws.com:5432/das19305gveklt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

'''
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info' 
'''


app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/myLibrary")
def myLibrary():
    return render_template('my_library.html')


@app.route("/myShelves")
def myShelves():
    return render_template('my_shelves.html')


@app.route("/myWishlist")
def myWishlist():
    return render_template('my_wishlist.html')

@app.route("/search")
def search():
    return render_template('search.html')

@app.route("/showAuthor")
def showAuthor():
    return render_template('author_detail.html')

@app.route("/showTitle")
def showTitle():
    return render_template('title_detail.html')

@app.route("/showShelf")
def showShelf():
    return render_template('shelf_detail.html')

if __name__ == '__main__':
    app.run(debug=True)
