import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="prod.env")

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(INSTANCE_DIR, 'project.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    
    JWT_SECRET_KEY = os.getenv('SEM20257', 'another_secret_key')

class DevelopmentConfig(Config):
    DEBUG = True 
