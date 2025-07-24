import pytest
from app import app, db
from models import Parent, Child
from werkzeug.security import generate_password_hash

@pytest.fixture(scope="function")
def client():
    """Set up the Flask test client and in-memory database once per test function."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

        # Clean up after all tests
        with app.app_context():
            db.drop_all()
            db.session.remove()


@pytest.fixture
def sample_parent():
    parent = Parent(
        email="sampleparent@example.com",
        username="sampleparent",
        password=generate_password_hash("ParentPass123"),
        name="Sample Parent"
    )
    db.session.add(parent)
    db.session.commit()
    return parent

@pytest.fixture
def sample_child(sample_parent):
    child = Child(
        name="Sample Child",
        parent_id=sample_parent.id
    )
    db.session.add(child)
    db.session.commit()
    return child
