"""
    :Author: xputala00
    Global variable initialization
""" 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, AdminIndexView
from flask_login import UserMixin
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://nialcqehxsdpas:cef25d511b7991e99ddc2cf347961c9b567954eef38b554af8df36f36e3d16e4@ec2-63-34-223-144.eu-west-1.compute.amazonaws.com:5432/d4aldh40bv2tcr'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

admin = Admin(app)


class MyModelView(ModelView):
    pass


class MyAdminIndexView(AdminIndexView):
    pass


from flasklib import routes
