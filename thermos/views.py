from flask import render_template, request, redirect, url_for, flash

from thermos import app, db
from thermos.forms import BookmarkForm # My Class based on WTF form
from thermos.models import User, Bookmark # My object representation of a bookmark ro

from logging import DEBUG
app.logger.setLevel(DEBUG)

import os

# Fake login
def logged_in_user():
    return User.query.filter_by(username='Genie').first()

@app.route('/')
@app.route('/index')
def index():
    print(os.path.abspath(os.path.dirname(__file__)))
    return render_template('index.html', title="Title passed from view to template", new_bookmarks=Bookmark.newest(5))

@app.route('/add', methods=['GET', 'POST'])
def add():
    form = BookmarkForm()
    if form.validate_on_submit(): #Checks http method and validate. If GET or ERROR, skips the code
        # checking validity of data.
        url = form.url.data
        description = form.description.data
        bm = Bookmark(user=logged_in_user(), url=url, description=description) #create bookmark with Bookmark class representing row
        db.session.add(bm) #add to session. Haven't commited yet.
        db.session.commit()
        # for showing message. keep it in flash and show flash else where.
        flash("Stored bookmark '{}'".format(description))
        # for debugging
        app.logger.debug('stored url: ' + url)
        app.logger.debug('stored description: ' + description)
        app.logger.debug('bookmarks: {}'.format(bm))

        return redirect(url_for('index'))
    return render_template('add.html', form = form)

@app.route('/user/<username>')
def user(username):
    print(username)
    user = User.query.filter_by(username=username).first_or_404() #SQLAlchemy magic again!!!url_for
    print(user)
    return render_template('user.html', user=user)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 400

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500