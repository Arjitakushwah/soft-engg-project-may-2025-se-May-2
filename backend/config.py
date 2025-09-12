import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from prod.env (explicitly)
env_path = os.path.join(os.path.dirname(__file__), "prod.env")
load_dotenv(env_path)

class Config:
    # Use DATABASE_URL from prod.env
    db_url = os.getenv("DATABASE_URL")
    if db_url and db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv("SEM20257")   # from prod.env
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)

class DevelopmentConfig(Config):
    DEBUG = True
