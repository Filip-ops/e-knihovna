from datetime import datetime
from flask import render_template, url_for, flash, redirect, request
from flasklib import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from flasklib.models import User, Author, Title, Wishlist_title, Library_title, Note, Shelf
from flasklib.forms import RegistrationForm, LoginForm
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

admin = Admin(app, index_view=MyAdminIndexView())
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Author, db.session))
admin.add_view(MyModelView(Title, db.session))
admin.add_view(MyModelView(Wishlist_title, db.session))
admin.add_view(MyModelView(Library_title, db.session))
admin.add_view(MyModelView(Note, db.session))
admin.add_view(MyModelView(Shelf, db.session))

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
############################################################################################################################################


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessfull! Check password and mail address', 'Error')
    return render_template('login.html', title='Login', form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully! You can log in now', 'Success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
