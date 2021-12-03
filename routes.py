from datetime import datetime
from flask import render_template, url_for, flash, redirect, request
#import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
#from models import //////////// ADD MODELS
#from forms import //////////// ADD FORMS

@app.route("/")
@app.route("/index")
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