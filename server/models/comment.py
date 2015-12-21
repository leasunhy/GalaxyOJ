from .. import db

class Comment(db.Model):
    """Comment model."""

    id = db.Column(db.Integer, primary_key=True)

    content = db.Column(db.Text)
    create_time = db.Column(db.DateTime)

    # relationships
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Comment %s>' % content

