import os
from flask.ext.script import Manager, Shell, Command
from flask.ext.migrate import Migrate, MigrateCommand

from server import app, db
from server.models import *

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

def make_shell_context():
    return dict(app=app, db=db, **model_dict)

manager.add_command('shell', Shell(make_context=make_shell_context))

@manager.command
def add_data():
    # add a mock user
    u = User(login_name='leasunhy', email='leasunhy@example.com')

    # add there problems
    p1 = Problem()
    p1.title = 'A+B'
    p1.problem_desc = 'Given two numbers, calculate their sum.'
    p1.input_desc = 'A single line containing two integers separated by a space.'
    p1.output_desc = 'A single line containing the sum.'
    p1.sample_input = '1 2'
    p1.sample_output = '3'
    p1.source = 'Classical'

    p2 = Problem(title='A-B')
    p3 = Problem(title='A*B')

    # add a contest
    import datetime
    c = Contest(title='Newbie Corner')
    c.start_time = datetime.datetime.now()
    c.end_time = c.start_time + datetime.timedelta(1)
    c.owner = u
    c.problems.append(p2)

    # add a submission
    s = Submission()
    s.owner = u
    s.problem = p1
    s.compiler_id = 1
    s.verdict = 'Accepted'

    # add posts
    po1 = Tutorial(title='Introduction to Dynamic Programming', content='Abandon.')
    po1.create_time = datetime.datetime.now()
    po1.owner = u

    po2 = Notification(title='Air pollution detected.', content='Evacuate. NOW!')
    po2.create_time = datetime.datetime.now()
    po2.owner = u
    po2.importance = 233

    po3 = Solution(title='How to attack A+B?', content='Hand calculate.')
    po3.create_time = datetime.datetime.now()
    po3.owner = u
    po3.problem = p1

    db.session.add_all([u, p1, p2, p3, c, s, po1, po2, po3])
    db.session.commit()


if __name__ == '__main__':
    manager.run()

