from .. import db, app

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

