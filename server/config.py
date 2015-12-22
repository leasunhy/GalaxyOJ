import os

basedir = os.path.abspath(os.path.dirname(__file__))

# config the following lines when used in production environment
CONFIG_NAME = os.getenv('CONFIG_NAME', 'DEVELOPMENT')
DATABASE_URI = os.getenv('DATABASE_URI', 'postgresql://localhost/galaxyoj_dev')
SECRET_KEY = os.getenv('SECRET_KEY', 'Something you will never know:-)')
COMPILER_LIST = {}


class ConfigBase:
    SECRET_KEY = SECRET_KEY
    TESTING = False
    CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = DATABASE_URI
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    DEFAULT_TIME_LIMIT = 1000  # in milliseconds
    DEFAULT_MEMORY_LIMIT = 65536  # in kibibytes
    COMPILER_NAME_DICT = dict(map(lambda i, x: (x, i), enumerate(COMPILER_LIST)))
    COMPILER_INDEX_DICT = dict(enumerate(COMPILER_LIST))

class DevelopmentConfig(ConfigBase):
    DEBUG = True
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProductionConfig(ConfigBase):
    DEBUG = False
    SQLALCHEMY_RECORD_QUERIES = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(DevelopmentConfig):
    TESTING = True

config = {
    'DEVELOPMENT': DevelopmentConfig,
    'PRODUCTION': ProductionConfig,
    'TESTING': TestingConfig
}[CONFIG_NAME]

