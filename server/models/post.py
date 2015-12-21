from .. import db

class Post(db.Model):
    """Post model."""

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.String(64))

    def __repr__(self):
        return '<Post %s>' % self.title

    # relationships
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tags = db.relationship('PostTag', secondary='post_tag_rel',
            backref=db.backref('posts', lazy='dynamic'))
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    # polymorphic mapper
    __mapper_args__ = {
            'polymorphic_identity': 'post',
            'polymorphic_on': type
    }


class PostTag(db.Model):
    """PostTag model."""

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(32))


post_tag_rel = db.Table('post_tag_rel',
        db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
        db.Column('tag_id', db.Integer, db.ForeignKey('post_tag.id')),
)


class Notification(Post):
    """Notification model."""

    id = db.Column(db.Integer, db.ForeignKey('post.id'), primary_key=True)
    importance = db.Column(db.Integer, nullable=False, default=1)

    __mapper_args__ = { 'polymorphic_identity': 'notification' }


class Solution(Post):
    """Solution model."""

    id = db.Column(db.Integer, db.ForeignKey('post.id'), primary_key=True)
    problem_id = db.Column(db.Integer, db.ForeignKey('problem.id'), nullable=False)

    __mapper_args__ = { 'polymorphic_identity': 'solution' }


