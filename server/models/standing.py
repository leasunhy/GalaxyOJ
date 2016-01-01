from .. import db, app

class Standing(db.Model):
    """standing model."""

    id = db.Column(db.Integer, primary_key=True)

    contest_id = db.Column(db.Integer, db.ForeignKey('contest.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    problem_id = db.Column(db.Integer, db.ForeignKey('problem.id'))

    actime = db.Column(db.Integer, default=0)
    penalty = db.Column(db.Integer, default=0)
    submissions = db.Column(db.Integer, default=0)

    def add_record(self, verdict, _time):
        if self.actime: return
        if verdict == 'Accepted':
            self.actime = _time.seconds
            self.penalty = self.actime/60 + self.submissions * 20
        else:
            if self.submissions is None:
                self.submissions = 0
            self.submissions += 1

    def __repr__(self):
        return '<Standing %d>' % self.id if self.id else '<New Standing>'

