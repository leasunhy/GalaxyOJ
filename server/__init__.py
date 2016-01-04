from .config import config

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask_bootstrap import Bootstrap

#For Redis
from rq import Queue
from rq.job import Job
from judge.worker import conn

from judge import judge

app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)

login_manager = LoginManager(app)
from .models.user import AnonymousUser
login_manager.anonymous_user = AnonymousUser
login_manager.login_view = 'auth.user_login'
login_manager.login_message = 'You need to login to access this page.'
login_manager.login_message_category = 'error'

Bootstrap(app)

q = Queue(connection = conn)

from .views import views
for view, prefix in views:
    app.register_blueprint(view, url_prefix=prefix)

# custom jinja2 filters
from .tools import datetime_format
app.jinja_env.filters['dtformat'] = datetime_format

