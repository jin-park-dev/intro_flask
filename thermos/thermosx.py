from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash

from logging import DEBUG
from thermos.forms import BookmarkForm


app = Flask(__name__)
app.logger.setLevel(DEBUG)

class User:
    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname
    def initals(self):
        return "{}. {}.".format(self.firstname[0], self.lastname[0])

bookmarks = []
app.config['SECRET_KEY'] = b"2\xcf\xcc\xd1M'\xe9_a9u\x1c\xf65\xfa\x10/Ac\xf0\xc6\xc4q\x99"


def store_bookmark(url, description):
    bookmarks.append(dict(
        url = url,
        description = description,
        user = "reindert",
        date = datetime.utcnow()
    ))

#Book mark sorted by date
def new_bookmarks(num):
    return sorted(bookmarks, key=lambda bm: bm['date'], reverse=True)[:num]


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title="Title passed from view to template", user=User("Jin", "Park"), new_bookmarks=new_bookmarks(5))

@app.route('/add', methods=['GET', 'POST'])
def add():
    form = BookmarkForm()
    if form.validate_on_submit(): #Checks http method and validate. If GET or ERROR, skips the code
        # checking validity of data.
        url = form.url.data
        description = form.description.data
        store_bookmark(url, description)
        # for showing message. keep it in flash and show flash else where.
        flash("Stored bookmark '{}'".format(description))
        # for debugging
        app.logger.debug('stored url: ' + url)
        app.logger.debug('stored description: ' + description)
        app.logger.debug('bookmarks: {}'.format(bookmarks))

        return redirect(url_for('index'))
    return render_template('add.html', form = form)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 400

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug="TRUE")