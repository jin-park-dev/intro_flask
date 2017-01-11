import os
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

from logging import DEBUG
from thermos.forms import BookmarkForm

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = b"2\xcf\xcc\xd1M'\xe9_a9u\x1c\xf65\xfa\x10/Ac\xf0\xc6\xc4q\x99"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'thermos.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


app.logger.setLevel(DEBUG)

from thermos.forms import BookmarkForm # My Class based on WTF form
#from thermos.models import Bookmark # My object representation of a bookmark row
import thermos.models

# Fake login
def logged_in_user():
    return thermos.models.User.query.filter_by(username='Genie').first()

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title="Title passed from view to template", new_bookmarks=thermos.models.Bookmark.newest(5))

@app.route('/add', methods=['GET', 'POST'])
def add():
    form = BookmarkForm()
    if form.validate_on_submit(): #Checks http method and validate. If GET or ERROR, skips the code
        # checking validity of data.
        url = form.url.data
        description = form.description.data
        bm = thermos.models.Bookmark(user=logged_in_user(), url=url, description=description) #create bookmark with Bookmark class representing row
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

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 400

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

# After adding fake login session it only work running from manager... I get
    #SQLAlchemy  is already attached to session '1' (this is '2')
# if __name__ == '__main__':
#     app.run(debug="TRUE")