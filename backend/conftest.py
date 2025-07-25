# Backend/conftest.py

import pytest
from app import app, db
from models import User, Parent

@pytest.fixture(scope='session')
def test_app():
    """Creates a Flask app instance for the entire test session."""
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "JWT_SECRET_KEY": "test-secret-key",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    })

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture()
def client(test_app):
    """Creates a test client for each test function."""
    return test_app.test_client()

@pytest.fixture(autouse=True)
def db_session(test_app):
    """
    Ensures each test has a clean database session. This fixture is
    automatically used by every test.
    """
    with test_app.app_context():
        yield db.session
        db.session.remove()
        db.reflect()
        db.drop_all()
        db.create_all()