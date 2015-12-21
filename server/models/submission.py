from .. import db, app

class Submission(db.Model):
    """Submission model."""

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    problem_id = db.Column(db.Integer, db.ForeignKey('problem.id'))

    filename = db.Column(db.String(128), nullable=False, unique=True)
    compiler_id = db.Column(db.Integer, nullable=False)

    @property
    def compiler(self):
        return app.config['COMPILER_INDEX_DICT'][self.compiler_id]

    @compiler.setter
    def compiler(self, value):
        self.compiler_id = app.config['COMPILER_NAME_DICT'][value]

    def __repr__(self):
        return '<Submission %s>' % filename

