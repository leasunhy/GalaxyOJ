from .. import db, app

class Standing(db.Model):
    """standing model."""

    id = db.Column(db.Integer, primary_key=True)

    contest_id = db.Column(db.Integer, db.ForeignKey('contest.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    problem_id = db.Column(db.Integer, db.ForeignKey('problem.id'))

    penalty = db.Column(db.Integer)
    submissions = db.Column(db.Integer)
    accepted = db.Column(db.Boolean)

    def add_record(self, verdict, _time):
        if self.accepted: return
        if verdict == 'Accepted':
            self.accepted = True
            self.penalty = _time + self.submissions * 20
        else:
            self.submissions += 1

    def __repr__(self):
        return '<Standing %d>' % self.id if self.id else '<New Standing>'

