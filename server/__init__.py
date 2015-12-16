from .config import config, CONFIG_NAME

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

app = Flask(__name__)
app.config.from_object(config[CONFIG_NAME])

db = SQLAlchemy(app)
login_manager = LoginManager(app)

from .views import *

