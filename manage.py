from thermos.thermosx import app, db
from flask_script import Manager, prompt_bool

manager = Manager(app)

@manager.command
def initdb():
    db.create_all()
    print('Initialized the datebase')

@manager.command
def dropdb():
    if prompt_bool(
        "You you sure you want to lose all your data"):
        db.drop_all()
        print("Dropped the database")

if __name__ == '__main__':
    manager.run()

