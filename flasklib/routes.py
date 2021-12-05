from datetime import datetime
from flask import render_template, url_for, flash, redirect, request
from sqlalchemy.sql.expression import select
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

"""
    :Author: xputal00
    home() fetches user's titles which are then used in view.
    :return: returns home page with fetched data
"""
@app.route("/")
@app.route("/home/", methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        shelf = Shelf.query.filter_by(name='Reading', user=current_user.id).first()
        return render_template('home.html', titles=shelf.library_titles, user=current_user)
    else:
        return render_template('home.html')

"""
    :Author: xputal00
    myLibrary() fetches user's library which are then used in view.
    :return: returns library page with fetched data
"""
@app.route("/myLibrary/", methods=['GET', 'POST'])
def myLibrary():
    if current_user.is_authenticated:
        lib_titles = Library_title.query.filter_by(user=current_user.id)
        titles = [Title.query.get(lib_title.title) for lib_title in lib_titles.all()]
        result = None
        bad_isbn = None
        if request.method == "POST":
            if request.form.get("button_search") == "Search":
                name_title = request.form.get("search")
                filter_type = request.form.get("search_filter")
                if filter_type == "all":
                    titles = lib_titles.join(Title).join(Author).filter(
                        or_(Title.name.op('~*')(name_title),
                            Author.name.op('~*')(name_title),
                            Title.genre.op('~*')(name_title))).order_by(
                        Title.name).all()
                elif filter_type == "title":
                    titles = lib_titles.join(Title).filter(Title.name.op('~*')(name_title)).order_by(Title.name).all()
                elif filter_type == "author":
                    titles = lib_titles.join(Title).join(Author).filter(Author.name.op('~*')(name_title)).order_by(
                        Title.name).all()
                else:
                    titles = lib_titles.join(Title).filter(Title.genre.op('~*')(name_title)).order_by(Title.name).all()
            if request.form.get("button_add") == "Add":
                isbn = request.form.get("isbn")
                title = Title.query.get(isbn)
                if not title:
                    result = False
                    bad_isbn = isbn
                else:
                    lib_title = Library_title(page=0, user=current_user.id, title=title.id)
                    db.session.add(lib_title)
                    db.session.commit()
                    result = True
                    lib_titles = Library_title.query.filter_by(user=current_user.id)
                    titles = [Title.query.get(lib_title.id) for lib_title in lib_titles.all()]
            if request.form.get("remove"):
                title_isbn = request.form.get("remove")
                title = Title.query.filter_by(isbn=title_isbn).first()
                item = Library_title.query.filter_by(title=title.id).first()
                db.session.delete(item)
                db.session.commit()
                lib_titles = Library_title.query.filter_by(user=current_user.id)
                titles = [Title.query.get(lib_title.id) for lib_title in lib_titles.all()]

        return render_template('my_library.html', titles=titles, result=result, bad_isbn=bad_isbn)
    else:
        return redirect(url_for('home'))

"""
    :Author: xdudaj02
    myShelves() fetches user's shelves which are then used in view and can be edited.
    :return: returns shelves page with fetched data
"""
@app.route("/myShelves/", methods=['GET', 'POST'])
def myShelves():
    if current_user.is_authenticated:
        shelf_list = Shelf.query.filter_by(user=current_user.id).all()
        shelves = {}
        for shelf in shelf_list:
            shelves[shelf] = len(shelf.library_titles)
        if request.method == "POST":
            name = request.form.get("name")
            desc = request.form.get("text")
            shelf = Shelf(name=name, desc=desc, user=current_user.id)
            db.session.add(shelf)
            db.session.commit()
            return render_template('my_shelves.html', shelves=shelves)
        else:
            pass
    else:
        return redirect(url_for('home'))
    return render_template('my_shelves.html', shelves=shelves)

"""
    :Author: xdudaj02
    myWishlist() fetches user's titles in wishlist which are then used in view and can be interacted with.
    :return: returns wishlist page with fetched data
"""
@app.route("/myWishlist/", methods=['GET', 'POST'])
def myWishlist():
    if current_user.is_authenticated:
        wl_titles = Wishlist_title.query.filter_by(user=current_user.id)
        titles = [Title.query.get(lib_title.title) for lib_title in wl_titles.all()]
        if request.method == "POST":
            if request.form.get("button_search") == "Search":
                name_title = request.form.get("search")
                filter_type = request.form.get("search_filter")
                if filter_type == "all":
                    titles = wl_titles.join(Title).join(Author).filter(
                        or_(Title.name.op('~*')(name_title),
                            Author.name.op('~*')(name_title),
                            Title.genre.op('~*')(name_title))).order_by(
                        Title.name).all()
                elif filter_type == "title":
                    titles = wl_titles.join(Title).filter(Title.name.op('~*')(name_title)).order_by(Title.name).all()
                elif filter_type == "author":
                    titles = wl_titles.join(Title).join(Author).filter(Author.name.op('~*')(name_title)).order_by(
                        Title.name).all()
                else:
                    titles = wl_titles.join(Title).filter(Title.genre.op('~*')(name_title)).order_by(Title.name).all()
            if request.form.get("remove"):
                title_isbn = request.form.get("remove")
                title = Title.query.filter_by(isbn=title_isbn).first()
                item = Wishlist_title.query.filter_by(title=title.id).first()
                db.session.delete(item)
                db.session.commit()
            if request.form.get("add"):
                title_isbn = request.form.get("add")
                title = Title.query.filter_by(isbn=title_isbn).first()
                item = Wishlist_title.query.filter_by(title=title.id).first()
                lib_title = Library_title(page=0, user=current_user.id, title=title.id)
                db.session.delete(item)
                db.session.add(lib_title)
                db.session.commit()

            lib_titles = Wishlist_title.query.filter_by(user=current_user.id)
            titles = [Title.query.get(lib_title.id) for lib_title in lib_titles.all()]

        return render_template('my_wishlist.html', titles=titles)
    else:
        return redirect(url_for('home'))

"""
    :Author: xdudaj02
    search() fetches titles which are then used in view and can be searched through.
    :return: returns search page with fetched data
"""
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
                    titles = Title.query.join(Author).filter(Author.name.op('~*')(name_title)).order_by(
                        Title.name).all()
                else:
                    titles = Title.query.filter(Title.genre.op('~*')(name_title)).order_by(Title.name).all()
            elif request.form.get("add_lib"):
                title_isbn = request.form.get("add_lib")
                title = Title.query.filter_by(isbn=title_isbn).first()
                lib_title = Library_title(page=0, user=current_user.id, title=title.id)
                db.session.add(lib_title)
                db.session.commit()
                titles = Title.query.order_by(Title.name).all()
            elif request.form.get("add_wl"):
                title_isbn = request.form.get("add_wl")
                title = Title.query.filter_by(isbn=title_isbn).first()
                wl_title = Wishlist_title(user=current_user.id, title=title.id)
                db.session.add(wl_title)
                db.session.commit()
                titles = Title.query.order_by(Title.name).all()
            elif request.form.get("remove_lib"):
                title_isbn = request.form.get("remove_lib")
                title = Title.query.filter_by(isbn=title_isbn).first()
                item = Library_title.query.filter_by(title=title.id).first()
                db.session.delete(item)
                db.session.commit()
            elif request.form.get("remove_wl"):
                title_isbn = request.form.get("remove_wl")
                title = Title.query.filter_by(isbn=title_isbn).first()
                item = Wishlist_title.query.filter_by(title=title.id).first()
                db.session.delete(item)
                db.session.commit()
        title_dict = {}
        for title in titles:
            item = [False, False]
            if len(Library_title.query.join(Title).filter(Title.isbn == title.isbn,
                                                          Library_title.user == current_user.id).all()) > 0:
                item[0] = True
            if len(Wishlist_title.query.join(Title).filter(Title.isbn == title.isbn,
                                                           Wishlist_title.user == current_user.id).all()) > 0:
                item[1] = True
            title_dict[title] = item
        return render_template('search.html', titles=title_dict)
    else:
        return redirect(url_for('home'))

"""
    :Author: xsapak05
    showAuthor() fetches authors which are then used in view.
    :return: returns author page with fetched data
"""
@app.route("/showAuthor/<int:id>/", methods=['GET', 'POST'])
def showAuthor(id):
    author = Author.query.get(id)
    titles = Title.query.filter_by(author_id=id)
    return render_template('author_detail.html', author=author, titles=titles)

"""
    :Author: xsapak05/xdudaj02
    showTitle() fetches user's titles which are then used in view and edits title data in database
    :return: returns title page with fetched data
"""
@app.route("/showTitle/<int:id>/", methods=['GET', 'POST'])
def showTitle(id):
    if current_user.is_authenticated:
        title = Title.query.get(id)
        lib_title = Library_title.query.filter_by(title=id, user=current_user.id).first()
        wl_title = Wishlist_title.query.filter_by(title=id, user=current_user.id).first()
        notes = Note.query.order_by(Note.start_page).all()
        if lib_title:
            shelves = Shelf.query.filter_by(user=current_user.id)
            my_shelves = shelves.filter(Shelf.library_titles.any(id=lib_title.id)).all()
            not_shelves = shelves.filter(~Shelf.library_titles.any(id=lib_title.id)).all()
            reading = False
            for shelf in my_shelves:
                if shelf.name == 'Reading':
                    reading = True
                    break
        else:
            shelves = None
            my_shelves = None
            not_shelves = None
            reading = False

        if request.method == "POST":
            if request.form.get("remove_tag"):  # if name == value
                shelf_id = request.form.get("remove_tag")
                shelf = Shelf.query.get(shelf_id)
                shelf.library_titles.remove(lib_title)
                db.session.commit()

            if request.form.get("tag") == "add":

                for s_id in request.form.getlist("selected"):
                    shelf = Shelf.query.get(s_id)
                    shelf.library_titles.append(lib_title)

                db.session.commit()

            if request.form.get("reading") == "done":
                shelf_reading = Shelf.query.filter_by(name='Reading', user=current_user.id).first()
                shelf_read = Shelf.query.filter_by(name='Read', user=current_user.id).first()
                shelf_reading.library_titles.remove(lib_title)
                shelf_read.library_titles.append(lib_title)
                db.session.commit()

            if request.form.get("library") == "add":
                lib_title = Library_title(page=0, user=current_user.id, title=title.id)
                if wl_title:
                    db.session.delete(wl_title)
                db.session.add(lib_title)
                db.session.commit()

            if request.form.get("library") == "remove":
                db.session.delete(lib_title)
                db.session.commit()
                pass

            if request.form.get("wishlist") == "add":
                wl_title = Wishlist_title(user=current_user.id, title=title.id)
                db.session.add(wl_title)
                db.session.commit()

            if request.form.get("wishlist") == "remove":
                db.session.delete(wl_title)
                db.session.commit()

            if request.form.get("note") == "add":
                name = request.form.get("name")
                start_page = request.form.get("page_start")
                end_page = request.form.get("page_end")
                text = request.form.get("text")
                color = request.form.get("color")
                note = Note(name=name, start_page=start_page, text=text, end_page=end_page, color=color,
                            library_title=lib_title.id)
                db.session.add(note)
                db.session.commit()

            if request.form.get("remove_note"):
                note_id = request.form.get("remove_note")
                note = Note.query.get(note_id)
                db.session.delete(note)
                db.session.commit()

            if request.form.get("edit_note"):
                note_id = request.form.get("edit_note")
                note = Note.query.get(note_id)

                pass

            if request.form.get("page"):
                lib_title.page = request.form.get("page")
                db.session.commit()

            lib_title = Library_title.query.filter_by(title=id, user=current_user.id).first()
            wl_title = Wishlist_title.query.filter_by(title=id, user=current_user.id).first()
            notes = Note.query.order_by(Note.start_page).all()
            if lib_title:
                shelves = Shelf.query.filter_by(user=current_user.id)
                my_shelves = shelves.filter(Shelf.library_titles.any(id=lib_title.id)).all()
                not_shelves = shelves.filter(~Shelf.library_titles.any(id=lib_title.id)).all()
                reading = False
                for shelf in my_shelves:
                    if shelf.name == 'Reading':
                        reading = True
                        break

        else:
            pass
    else:
        return redirect(url_for('login'))

    return render_template('title_detail.html', title=title, shelves=not_shelves, my_shelves=my_shelves, notes=notes,
                           reading=reading, lib_title=lib_title, wl_title=wl_title)

"""
    :Author: xsapak05
    showShelf() fetches user's shelves data which are then used in view.
    :return: returns shelf page with fetched data
"""
@app.route("/showShelf/<int:id>", methods=['GET', 'POST'])
def showShelf(id):
    shelf = Shelf.query.get(id)
    if current_user.is_authenticated:
        if request.method == "POST":
            if request.form.get("shelf") == "remove":  # if name == value
                db.session.delete(shelf)
                db.session.commit()
                return redirect(url_for('myShelves'))

            if request.form.get("remove"):
                title_id = request.form.get("remove")
                # remove title with title_id from this shelf
                title = Library_title.query.get(title_id)
                shelf.library_titles.remove(title)
                db.session.commit()

            if request.form.get("shelf") == "edit":
                shelf.name = request.form.get("name")
                shelf.desc = request.form.get("text")
                db.session.commit()

        else:
            pass
    return render_template('shelf_detail.html', shelf=shelf, titles=shelf.library_titles)

"""
    :Author: xputal00
    login() fetches user's data from db and compares with input.
    :return: returns home page with fetched data when successfull else login page
"""
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

"""
    :Author: xputal00
    register() inserts user's data into db.
    :return: returns login/register page
"""
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
        shelf_owned = Shelf(name='Owned', desc='All the books you own.', user=user.id)
        shelf_read = Shelf(name='Read', desc='All the books you have already read.', user=user.id)
        shelf_reading = Shelf(name='Reading', desc='All the books you are currently reading.', user=user.id)
        db.session.add(shelf_owned)
        db.session.add(shelf_read)
        db.session.add(shelf_reading)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

"""
    :Author: xputal00
    logout()
    :return: returns home page with fetched data
"""
@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
