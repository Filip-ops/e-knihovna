from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin,AdminIndexView
from flask_login import UserMixin
from flasklib.models import User, Author, Title, Wishlist_title, Library_title, Note, Shelf

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://vatqztvxwsroxt:59ef0b95be0a73506825730a56774113565ef8451273319ec6963ac22a00ef71@ec2-52-17-1-206.eu-west-1.compute.amazonaws.com:5432/das19305gveklt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

admin = Admin(app)
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Author, db.session))
admin.add_view(ModelView(Title, db.session))
admin.add_view(ModelView(Wishlist_title, db.session))
admin.add_view(ModelView(Library_title, db.session))
admin.add_view(ModelView(Note, db.session))
admin.add_view(ModelView(Shelf, db.session))
class MyModelView(ModelView):
    pass

class MyAdminIndexView(AdminIndexView):
    pass

from flasklib import routes
