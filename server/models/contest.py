from werkzeug import generate_password_hash, check_password_hash

from .problem import Problem
from .. import db

contest_problem_rel = db.Table('contest_problem_rel',
        db.Column('contest_id', db.Integer, db.ForeignKey('contest.id')),
        db.Column('problem_id', db.Integer, db.ForeignKey('problem.id'))
)

class Contest(db.Model):
    """Contest model."""

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)

    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

    passcode_hash = db.Column(db.String(128))

    @property
    def passcode(self):
        return "What are you doing?"

    @passcode.setter
    def passcode(self, value):
        if not value:
            self.passcode_hash = None
        else:
            self.passcode_hash = generate_password_hash(value)

    def verify_passcode(self, passcode):
        return self.passcode_hash is None or\
               check_password_hash(self.passcode_hash, passcode)

    # relationships
    problems = db.relationship('Problem', secondary='contest_problem_rel',
                    backref=db.backref('contests', lazy='dynamic'))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Contest %s>' % self.title

