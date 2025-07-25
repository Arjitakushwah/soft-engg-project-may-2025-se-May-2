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
        db.drop_all()

@pytest.fixture()
def client(test_app):
    """Creates a test client for each test function."""
    return test_app.test_client()

@pytest.fixture(autouse=True)
def db_session(test_app):
    """Ensures each test has a clean database session."""
    with test_app.app_context():
        yield db.session
        db.session.remove()
        db.reflect()
        db.drop_all()
        db.create_all()

@pytest.fixture
def parent_token(client):
    """Fixture to get a valid token for a parent user."""
    return create_parent_and_get_token(client)

@pytest.fixture
def child_token_and_id(client):
    """Fixture to get a valid token and ID for a child user."""
    return create_child_and_get_token(client)



@pytest.fixture
def story_fixture(client, child_token_and_id):
    """
    Fixture that creates a child user and a story in the database.
    Yields the child's token, child's ID, and the created story object.
    """
    token, child_id = child_token_and_id
    with app.app_context():
        story = DailyStory(
            child_id=child_id,
            date=date.today(),
            title="The Mystery of the Missing Sock",
            child_prompt="a mystery story",
            theme="Curiosity",
            content="A sock went missing and a brave detective...",
            question="Who stole the sock?",
            option_a="The dog", option_b="The cat",
            option_c="A ghost", option_d="The washing machine",
            correct_option="The dog"
        )
        db.session.add(story)
        db.session.commit()
        yield token, child_id, story