from .. import db, app

problem_tag_rel = db.Table('problem_tag_rel',
        db.Column('tag_id', db.Integer, db.ForeignKey('problem_tag.id')),
        db.Column('problem_id', db.Integer, db.ForeignKey('problem.id'))
)

class Problem(db.Model):
    """Problem model."""

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(128), nullable=False)
    problem_desc = db.Column(db.Text)
    input_desc = db.Column(db.Text)
    output_desc = db.Column(db.Text)
    sample_input = db.Column(db.Text)
    sample_output = db.Column(db.Text)
    source = db.Column(db.Text)

    visible = db.Column(db.Boolean, nullable=False, default=True)

    test_case_count = db.Column(db.Integer, nullable=False, default=1)
    time_limit = db.Column(db.Integer, nullable=False,
                           default=app.config['DEFAULT_TIME_LIMIT'])
    memory_limit = db.Column(db.Integer, nullable=False,
                             default=app.config['DEFAULT_MEMORY_LIMIT'])

    def __repr__(self):
        return '<Problem: %s>' % self.title

    # relationships
    submissions = db.relationship('Submission', backref='problem', lazy='dynamic')
    tags = db.relationship('ProblemTag', secondary='problem_tag_rel',
            backref=db.backref('problems', lazy='dynamic'))


class ProblemTag(db.Model):
    """ProblemTag model"""

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(32), nullable=False)



