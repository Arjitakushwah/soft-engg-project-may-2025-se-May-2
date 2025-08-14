from app import app
from models import db


def create_db():
    with app.app_context():
        db.create_all()
        print("Tables created successfully.")
