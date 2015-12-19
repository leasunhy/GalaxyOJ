from flask.ext.login import UserMixin
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

    password_hash = db.Column(db.String(32))

    @property
    def password(self):
        return "NO PASSWORDS WILL BE REVEALED."

    @password.setter
    def password(self, value):
        self.password_hash = generate_password_hash(value)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %s>' % self.login_name


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


