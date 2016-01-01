from flask import Blueprint

main = Blueprint('main', __name__)
post = Blueprint('post', __name__)
auth = Blueprint('auth', __name__)
admin = Blueprint('admin', __name__)
oj = Blueprint('oj', __name__)
judge = Blueprint('judge', __name__)
upload = Blueprint('upload', __name__)

views = [(main, ''),
         (post, '/post'),
         (auth, '/auth'),
         (admin, '/admin'),
         (oj, '/oj'),
         (judge, '/judge'),
         (upload, '/upload'),
]

from . import main_view, post_view, auth_view,\
              admin_view, oj_view, judge_view, upload_view


