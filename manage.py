from thermos import app, db
from flask_script import Manager, prompt_bool
from thermos.models import User

manager = Manager(app)

@manager.command
def initdb():
    db.create_all() # Creates database with SQLAlchemy magic

    #adding users

    db.session.add(User(username="genie", email="Genie@lamp.com", password="qwerty"))
    db.session.add(User(username="ali", email="G@Broat.com", password="qwerty"))
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
