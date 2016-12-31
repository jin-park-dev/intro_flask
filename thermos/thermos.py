from flask import Flask, render_template, url_for

app = Flask(__name__)

class User:
    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname

    def initals(self):
        return "{}. {}.".format(self.firstname[0], self.lastname[0])

    """Muahahah after learning from Mark Lutz book I'm comfortable doing this and understand!"""
    # def __str__(self):
    #     return "{} {}".format(self.firstname, self.lastname)
    # def __repr__(self):
    #     return "{} {}".format(self.firstname, self.lastname)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title="Title passed from view to template", user=User("Jin", "Park"))

@app.route('/add')
def add():
    return render_template('add.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 400

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug="TRUE")