import os

# config the following lines when used in production environment
CONFIG_NAME = 'DEVELOPMENT'
PRODUCTION_DATABASE_URI = ''
PRODUCTION_SECRET_KEY = ''

basedir = os.path.abspath(os.path.dirname(__file__))

class ConfigBase:
    SECRET_KEY = 'Something you will never know:-)'
    TESTING = False
    CSRF_ENABLED = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True


class DevelopmentConfig(ConfigBase):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///dev.db"
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProductionConfig(ConfigBase):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = PRODUCTION_DATABASE_URI
    SQLALCHEMY_RECORD_QUERIES = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = PRODUCTION_SECRET_KEY


config = {
    'DEVELOPMENT': DevelopmentConfig,
    'PRODUCTION': ProductionConfig,
}

