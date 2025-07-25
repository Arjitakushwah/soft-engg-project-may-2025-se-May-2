# Backend/tests/test_authentication.py

from unittest.mock import patch
from werkzeug.security import generate_password_hash
from models import db, User, Parent

def test_register_parent_success(client):
    """Test successful parent registration."""
    res = client.post('/register', json={
        "email": "parent@example.com",
        "username": "parentuser",
        "password": "password",
        "name": "Parent Name"
    })
    assert res.status_code == 201
    assert res.get_json()['message'] == 'Parent registered successfully'

def test_login_success(client):
    """Test successful login for a parent."""
    hashed_pw = generate_password_hash("password123")
    user = User(username="parentlogin", password=hashed_pw, role="parent", email="login@test.com")
    db.session.add(user)
    db.session.commit()
    parent = Parent(id=user.id, name="Test Parent")
    db.session.add(parent)
    db.session.commit()

    res = client.post('/login', json={"username": "parentlogin", "password": "password123"})
    assert res.status_code == 200
    json_data = res.get_json()
    assert 'access_token' in json_data
    assert json_data['role'] == 'parent'

def test_check_username(client):
    """Test username availability check."""
    user = User(username="existinguser", password="pw", role="parent", email="user@test.com")
    db.session.add(user)
    db.session.commit()

    res_taken = client.get('/check-username?username=existinguser')
    assert res_taken.status_code == 200
    assert not res_taken.get_json()['available']

    res_available = client.get('/check-username?username=newuser')
    assert res_available.status_code == 200
    assert res_available.get_json()['available']

def test_register_parent_missing_fields(client):
    """Test parent registration with missing required fields."""
    res = client.post('/register', json={
        "username": "user1",
        "password": "password",
        "name": "Parent Name"
    })
    assert res.status_code == 400
    assert 'Email, password, name, and username are required' in res.get_json()['error']

def test_login_non_existent_user(client):
    """Test login with a username that does not exist."""
    res = client.post('/login', json={"username": "nouser", "password": "password"})
    assert res.status_code == 401

def test_login_missing_fields(client):
    """Test login with missing username or password."""
    res = client.post('/login', json={"password": "password"})
    assert res.status_code == 400

def test_forgot_username(client):
    """Test the forgot username functionality."""
    res_register = client.post('/register', json={
        "email": "findme@example.com",
        "username": "findableuser",
        "password": "password",
        "name": "Findable Parent"
    })
    assert res_register.status_code == 201

    res_find = client.post('/forgot-username', json={"email": "findme@example.com"})
    assert res_find.status_code == 200
    assert res_find.get_json()['username'] == 'findableuser'

def test_forgot_username_not_found(client):
    """Test forgot username with an email that doesn't exist."""
    res = client.post('/forgot-username', json={"email": "nosuchuser@example.com"})
    assert res.status_code == 404

@patch('app.store_otp')
def test_forgot_password_sends_otp(mock_store_otp, client):
    """Test that the forgot password endpoint calls the OTP service via a client request."""
    mock_store_otp.return_value = True

    # Use the client to make a request to the endpoint
    res = client.post('/forgot-password', json={"email": "test@example.com"})

    # Assert that the mock was called and the response is correct
    mock_store_otp.assert_called_once_with("test@example.com")
    assert res.status_code == 200
    assert res.get_json()['message'] == 'OTP sent to email'

@patch('app.verify_otp')
def test_verify_otp_success(mock_verify_otp, client):
    """Test successful OTP verification via a client request."""
    mock_verify_otp.return_value = (True, "OTP verified successfully.")

    # Use the client to make a request
    res = client.post('/verify-otp', json={"email": "test@example.com", "otp": "123456"})
    
    # Assertions
    mock_verify_otp.assert_called_once_with("test@example.com", "123456")
    assert res.status_code == 200
    assert res.get_json()['success'] is True