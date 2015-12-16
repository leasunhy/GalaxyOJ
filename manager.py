import os
from server import app, db
from flask.ext.script import Manager, Shell, Command

manager = Manager(app)

def make_shell_context():
    return dict(app=app, db=db)

manager.add_command('shell', Shell(make_context=make_shell_context))

@manager.command
def init():
    with app.app_context():
        print("Dropping all tables...")
        db.drop_all()

        print("Creating all tables...")
        db.create_all()

        print("Init DONE.")

if __name__ == '__main__':
    manager.run()

