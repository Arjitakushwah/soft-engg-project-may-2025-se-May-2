import os
from datetime import timedelta

class Config:
    db_url = os.getenv("DATABASE_URL", 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'project.db'))
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv('SEM20257', 'another_secret_key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)

class DevelopmentConfig(Config):
    DEBUG = True
 

