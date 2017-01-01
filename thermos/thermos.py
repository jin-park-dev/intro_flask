from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for

from logging import DEBUG

app = Flask(__name__)
app.logger.setLevel(DEBUG)

class User:
    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname
    def initals(self):
        return "{}. {}.".format(self.firstname[0], self.lastname[0])

bookmarks = []

def store_bookmark(urlfromAddRoute):
    bookmarks.append(dict(
        url = urlfromAddRoute,
        user = "reindert",
        date = datetime.utcnow()
    ))


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title="Title passed from view to template", user=User("Jin", "Park"))

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == "POST":
        urlInAddRoute = request.form['urlInAddHtml']
        store_bookmark(urlInAddRoute)
        app.logger.debug('stored url: ' + urlInAddRoute)
        app.logger.debug('bookmarks: {}'.format(bookmarks))
        return redirect(url_for('index'))
    return render_template('add.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 400

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug="TRUE")