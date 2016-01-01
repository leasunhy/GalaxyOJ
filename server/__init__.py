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
Bootstrap(app)

q = Queue(connection = conn)

from .views import views
for view, prefix in views:
    app.register_blueprint(view, url_prefix=prefix)

# custom jinja2 filters
from .tools import datetime_format
app.jinja_env.filters['dtformat'] = datetime_format

