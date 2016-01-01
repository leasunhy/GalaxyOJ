from functools import wraps
from flask import abort
from flask.ext.login import current_user, login_required

from .. import app

ROOT_PRIVILEGE = 10

def root_required():
    return privilege_required(ROOT_PRIVILEGE)

def privilege_required(priv):
    def decorate(func, *args, **kwargs):
        @wraps(func)
        def new_func(*args, **kwargs):
            with app.app_context():
                if not current_user.is_authenticated or\
                        current_user.privilege_level < priv:
                    abort(401)
                return func(*args, **kwargs)
        return new_func
    return decorate

