from thermos import app, db
from flask_script import Manager, prompt_bool
from thermos.models import User, Bookmark, Tag # Flask migrate need this to detect and generate code.
from flask_migrate import Migrate, MigrateCommand

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand) # Adds command to DB in command line to do stuff.

@manager.command
def insert_data():
    genie = User(username="genie", email="Genie@lamp.com", password="qwerty")
    ali = User(username="ali", email="G@Broat.com", password="qwerty")

    def add_bookmark(url, description, tags):
        db.session.add(Bookmark(url=url, description=description, user=genie,                  tags=tags))


    for name in ["python", "flask", "webdev", "programming", "training", "news", "orm", "databases", "emacs", "gtd", "django"]:
        db.session.add(Tag(name=name))
    db.session.commit()

    add_bookmark("http://www.pluralsight.com", "Pluralsight. Hardcore developer training.", "training,programming,python,flask,webdev")
    add_bookmark("http://www.python.org", "Python - my favorite language", "python")
    add_bookmark("http://flask.pocoo.org", "Flask: Web development one drop at a time.", "python,flask,webdev")
    add_bookmark("http://www.reddit.com", "Reddit. Frontpage of the internet", "news,coolstuff,fun")
    add_bookmark("http://www.sqlalchemyorg", "Nice ORM framework", "python,orm,databases")

    db.session.add(genie)
    db.session.add(ali)
    db.session.commit()

    print('Initialized the datebase')

@manager.command
def dropdb():
    if prompt_bool(
            "You you sure you want to lose all your data"):
        db.drop_all()
        print("Dropped the database")

if __name__ == '__main__':
    manager.run()
