import os
from flask.ext.script import Manager, Shell, Command
from flask.ext.migrate import Migrate, MigrateCommand

from server import app, db
from server.models import User

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

def make_shell_context():
    return dict(app=app, db=db, User=User)

manager.add_command('shell', Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()

