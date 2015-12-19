import os
from flask.ext.script import Manager, Shell, Command
from flask.ext.migrate import Migrate, MigrateCommand

from server import app, db

manager = Manager(app)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

def make_shell_context():
    return dict(app=app, db=db)

manager.add_command('shell', Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()

