from flask import Blueprint

main = Blueprint('main', __name__)
post = Blueprint('post', __name__)
auth = Blueprint('auth', __name__)
admin = Blueprint('admin', __name__)
oj = Blueprint('oj', __name__)

views = [(main, ''),
         (post, '/post'),
         (auth, '/auth'),
         (admin, '/admin'),
         (oj, '/oj')
]

from . import main_view, post_view, auth_view, admin_view, oj_view

