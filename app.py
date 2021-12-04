from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from models import User, Author, Title, Wishlist_title, Library_title, Note, Shelf
#from forms import //////////// ADD FORM


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
