from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
#from models import //////////// ADD MODELS
#from forms import //////////// ADD FORMS
'''app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ptokoocanzqqkx:fae86dd94df17029ffb5c3f6009c8ffedb6323fb56cc2e21e53cb6e88d29e0bf@ec2-34-241-19-183.eu-west-1.compute.amazonaws.com:5432/d655itnumnt7dq'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info' '''

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

if __name__ == '__main__':
    app.run(debug=True)
