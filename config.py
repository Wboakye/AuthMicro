import os
#from constants import *
basedir = os.path.abspath(os.path.dirname(__file__))

DB_USER = os.environ.get("DATABASE_USER", 3)
DB_PASS = os.environ.get("DATABASE_PASS", 3)
DB_HOST = os.environ.get("DB_HOST", 3)
DB_PORT = os.environ.get("DB_PORT", 3)
DB_NAME = os.environ.get("DB_NAME", 3)
DB_STRING = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'
APP_SECRET = os.environ.get("APP_SECRET", 3)

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = APP_SECRET
    SQLALCHEMY_DATABASE_URI = DB_STRING


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True