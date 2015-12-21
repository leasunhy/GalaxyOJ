import os

# config the following lines when used in production environment
CONFIG_NAME = 'DEVELOPMENT'
PRODUCTION_DATABASE_URI = ''
PRODUCTION_SECRET_KEY = ''
COMPILER_LIST = {}


basedir = os.path.abspath(os.path.dirname(__file__))

class ConfigBase:
    SECRET_KEY = 'Something you will never know:-)'
    TESTING = False
    CSRF_ENABLED = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    DEFAULT_TIME_LIMIT = 1000  # in milliseconds
    DEFAULT_MEMORY_LIMIT = 65536  # in kibibytes
    COMPILER_NAME_DICT = dict(map(lambda i, x: (x, i), enumerate(COMPILER_LIST)))
    COMPILER_INDEX_DICT = dict(enumerate(COMPILER_LIST))

class DevelopmentConfig(ConfigBase):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "dev.db")
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
}[CONFIG_NAME]

