
from models import User, Parent


def test_register_success(client):
    response = client.post('/register', json={
        "email": "test@example.com",
        "password": "TestPass123",
        "name": "Test Parent",
        "username": "testuser"
    })
    assert response.status_code == 201
    assert response.get_json()['message'] == "Parent registered successfully"

def test_register_missing_fields(client):
    response = client.post('/register', json={
        "email": "test@example.com",
        "password": "TestPass123"
    })
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_register_duplicate_email(client):
    client.post('/register', json={
        "email": "test@example.com",
        "password": "TestPass123",
        "name": "Parent1",
        "username": "uniqueuser1"
    })
    response = client.post('/register', json={
        "email": "test@example.com",
        "password": "TestPass456",
        "name": "Parent2",
        "username": "uniqueuser2"
    })
    assert response.status_code == 400
    assert response.get_json()['error'] == "Email already exists"

def test_register_duplicate_username(client):
    client.post('/register', json={
        "email": "email1@example.com",
        "password": "TestPass123",
        "name": "Parent1",
        "username": "sameusername"
    })
    response = client.post('/register', json={
        "email": "email2@example.com",
        "password": "TestPass456",
        "name": "Parent2",
        "username": "sameusername"
    })
    assert response.status_code == 400
    assert response.get_json()['error'] == "Username already taken"
