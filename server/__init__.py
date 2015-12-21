from .config import config

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

#For Redis
from rq import Queue
from rq.job import Job
from worker import conn

app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)
login_manager = LoginManager(app)

q = Queue(connection = conn)

from .views import *

