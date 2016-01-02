from flask.ext.login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .. import db
from .. import login_manager


class User(UserMixin, db.Model):
    """User model."""

    id = db.Column(db.Integer, primary_key=True)
    privilege_level = db.Column(db.Integer, nullable=False, default=0)

    login_name = db.Column(db.String(32), nullable=False, unique=True)
    email = db.Column(db.String(64), nullable=False, unique=True)

    nickname = db.Column(db.String(32))
    signature = db.Column(db.String(128))
    real_name = db.Column(db.String(32))
    note = db.Column(db.String(256))

    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        return "NO PASSWORDS WILL BE REVEALED."

    @password.setter
    def password(self, value):
        if bool(value) == False: return
        self.password_hash = generate_password_hash(value)

    @property
    def display_name(self):
        return self.nickname or self.login_name

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self):
        return self.privilege_level > 0

    def __repr__(self):
        return '<User %s>' % self.login_name

    # relationships
    submissions = db.relationship('Submission', backref='owner', lazy='dynamic')
    owned_contests = db.relationship('Contest', backref='owner', lazy='dynamic')
    posts = db.relationship('Post', backref='owner', lazy='dynamic')
    comments = db.relationship('Comment', backref='owner', lazy='dynamic')


class AnonymousUser(AnonymousUserMixin):
    @property
    def is_admin(self):
        return False


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


