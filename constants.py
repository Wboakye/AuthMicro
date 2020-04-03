import os
import config
"""
    APP_SETTINGS: ProductionConfig, StagingConfig, DevelopmentConfig, TestingConfig
"""
APP_SETTINGS = os.environ.get("APP_SETTINGS", 3)
APP_SECRET = os.environ.get("APP_SECRET", 3)
JWT_SECRET = os.environ.get("JWT_SECRET", 3)
DB_USER = os.environ.get("DATABASE_USER", 3)
DB_PASS = os.environ.get("DATABASE_PASS", 3)
DB_HOST = os.environ.get("DB_HOST", 3)
DB_PORT = os.environ.get("DB_PORT", 3)
DB_NAME = os.environ.get("DB_NAME", 3)
DB_STRING = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'
