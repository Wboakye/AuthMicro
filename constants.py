import os
import config
"""
    APP_SETTINGS: ProductionConfig, StagingConfig, DevelopmentConfig, TestingConfig
"""
APP_SETTINGS = os.environ["APP_SETTINGS"]
APP_SECRET = os.environ["APP_SECRET"]
JWT_SECRET = os.environ["JWT_SECRET"]
DB_USER = os.environ["DATABASE_USER"]
DB_PASS = os.environ["DATABASE_PASS"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]
DB_STRING = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'
