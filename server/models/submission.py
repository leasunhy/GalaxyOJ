from .. import db, app

class Submission(db.Model):
    """Submission model."""

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    problem_id = db.Column(db.Integer, db.ForeignKey('problem.id'))

    filename = db.Column(db.String(128), unique=True)
    compiler_id = db.Column(db.Integer, nullable=False)

    time_usage = db.Column(db.Integer)
    memory_usage = db.Column(db.Integer)
    code_length = db.Column(db.Integer)
    verdict = db.Column(db.Enum('Accepted', 'Wrong Answer', 'Runtime Error',
        'Time Limit Exceeded', 'Memory Limit Exceeded', 'Restrict Function',
        'Output Limit Exceeded', 'Presentation Error', 'Compile Error',
        name='oj_verdict_types'))
    log = db.Column(db.String(1024))

    @property
    def compiler(self):
        return app.config['COMPILER_INDEX_DICT'][self.compiler_id]

    @compiler.setter
    def compiler(self, value):
        self.compiler_id = app.config['COMPILER_NAME_DICT'][value]

    def __repr__(self):
        return '<Submission %d>' % self.id if self.id else '<New Submission>'

