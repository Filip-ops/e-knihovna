from datetime import datetime
from flask import render_template, url_for, flash, redirect, request
from flasklib import app, db, bcrypt, admin
from flask_login import login_user, current_user, logout_user, login_required
from flasklib.models import User, Author, Title, Wishlist_title, Library_title, Note, Shelf
from flasklib.forms import RegistrationForm, LoginForm
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import or_

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Author, db.session))
admin.add_view(ModelView(Title, db.session))
admin.add_view(ModelView(Wishlist_title, db.session))
admin.add_view(ModelView(Library_title, db.session))
admin.add_view(ModelView(Note, db.session))
admin.add_view(ModelView(Shelf, db.session))


@app.route("/")
@app.route("/home/", methods=['GET', 'POST'])
def home():
    titles = Library_title.query
    if current_user.is_authenticated:
        return render_template('home.html', titles=titles, user=current_user)
    else:
        return render_template('home.html', titles=titles)
    
@app.route("/search/", methods=['GET', 'POST'])
def search():
    if current_user.is_authenticated:
        titles = Title.query.order_by(Title.name).all()
        if request.method == "POST":
            if request.form.get("button_search") == "Search":
                name_title = request.form.get("search")
                filter_type = request.form.get("search_filter")
                if filter_type == "all":
                    titles = Title.query.join(Author).filter(or_(Title.name.op('~*')(name_title),
                                                                 Author.name.op('~*')(name_title),
                                                                 Title.genre.op('~*')(name_title))).order_by(
                        Title.name).all()
                elif filter_type == "title":
                    titles = Title.query.filter(Title.name.op('~*')(name_title)).order_by(Title.name).all()
                elif filter_type == "author":
                    titles = Title.query.join(Author).filter(Author.name.op('~*')(name_title)).order_by(Title.name).all()
                else:
                    titles = Title.query.filter(Title.genre.op('~*')(name_title)).order_by(Title.name).all()
        return render_template('search.html', titles=titles)
    else:
        return redirect(url_for('home'))


@app.route("/myShelves/", methods=['GET', 'POST'])
def myShelves():
    shelves = Shelf.query.all()
    if request.method == "POST":
        name = request.form.get("name")
        desc = request.form.get("text")
        shelf = Shelf(name=name, desc=desc, user=current_user.id)
        db.session.add(shelf)
        db.session.commit()
        return render_template('my_shelves.html', shelves=shelves)
    else:
        pass
    return render_template('my_shelves.html', shelves=shelves)


@app.route("/myWishlist/", methods=['GET', 'POST'])
def myWishlist():
    return render_template('my_wishlist.html')


@app.route("/search/", methods=['GET', 'POST'])
def search():
    if current_user.is_authenticated:
        titles = Title.query.order_by(Title.name).all()
        if request.method == "POST":
            if request.form.get("button_search") == "Search":
                name_title = request.form.get("search")
                filter_type = request.form.get("search_filter")
                if filter_type == "all":
                    titles = Title.query.join(Author).filter(or_(Title.name.op('~*')(name_title),
                                                                 Author.name.op('~*')(name_title),
                                                                 Title.genre.op('~*')(name_title))).order_by(
                        Title.name).all()
                elif filter_type == "title":
                    titles = Title.query.filter(Title.name.op('~*')(name_title)).order_by(Title.name).all()
                elif filter_type == "author":
                    titles = Title.query.join(Author).filter(Author.name.op('~*')(name_title)).order_by(Title.name).all()
                else:
                    titles = Title.query.filter(Title.genre.op('~*')(name_title)).order_by(Title.name).all()
        return render_template('search.html', titles=titles)
    else:
        return redirect(url_for('home'))


@app.route("/showAuthor/<int:id>/", methods=['GET', 'POST'])
def showAuthor(id):
    author = Author.query.get(id)
    return render_template('author_detail.html', author=author)


@app.route("/showTitle/<int:id>/", methods=['GET', 'POST'])
def showTitle(id):
    title = Title.query.get(id)
    return render_template('title_detail.html', title=title)


@app.route("/showShelf/<int:id>", methods=['GET', 'POST'])
def showShelf(id):
    shelf = Shelf.query.get(id)

    if request.method == "POST":
        if request.form.get("shelf") == "remove":  # if name == value
            shelf.delete()
            db.session.commit()
            return redirect(url_for('myShelves'))

        if request.form.get("remove"):
            title_id = request.form.get("remove")
            # remove title with title_id from this shelf
            shelf = Shelf.query.get(id)

        if request.form.get("shelf") == "edit":
            shelf.name = request.form.get("name")
            shelf.desc = request.form.get("text")
            db.session.commit()

    else:
        pass
    return render_template('shelf_detail.html', shelf=shelf)


############################################################################################################################################

@app.route("/login/", methods=['GET', 'POST'])
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


@app.route("/register/", methods=['GET', 'POST'])
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


@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
