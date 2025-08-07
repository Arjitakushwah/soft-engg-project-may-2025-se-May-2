# Backend/conftest.py
import pytest
from app import app, db
from tests.helpers import create_parent_and_get_token, create_child_and_get_token
from models import DailyStory
from datetime import date

@pytest.fixture(scope='session')
def test_app():
    """Creates a Flask app instance for the entire test session."""
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "JWT_SECRET_KEY": "test-secret-key"
    })
    with app.app_context():
        db.create_all()
        yield app
        # db.drop_all()

@pytest.fixture()
def client(test_app):
    """Creates a test client for each test function."""
    return test_app.test_client()
from sqlalchemy.orm import scoped_session, sessionmaker

@pytest.fixture(autouse=True)
def db_session(test_app):
    """
    Rollback-based session fixture.
    """
    with test_app.app_context():
        connection = db.engine.connect()
        transaction = connection.begin()
        # Create a new session bound to the connection
        session_factory = sessionmaker(bind=connection)
        Session = scoped_session(session_factory)     
        db.session = Session  # Override db.session with the test session
        yield Session  # Provide session to the test
        transaction.rollback()
        Session.remove()
        connection.close()

@pytest.fixture
def parent_token(client):
    """Fixture to get a valid token for a parent user."""
    return create_parent_and_get_token(client)

@pytest.fixture
def child_token_and_id(client):
    """Fixture to get a valid token and ID for a child user."""
    return create_child_and_get_token(client)
