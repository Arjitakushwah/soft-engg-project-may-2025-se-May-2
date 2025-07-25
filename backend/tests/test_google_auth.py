# Backend/tests/test_google_auth.py

from unittest.mock import patch, MagicMock
from models import db, User
from app import app

MOCK_GOOGLE_USER_INFO = {
    'email': 'new.google.user@example.com',
    'name': 'Google User'
}

mock_credentials = MagicMock()
mock_credentials.token = 'fake-google-api-token'

@patch('app.requests.get')
@patch('app.Flow.from_client_secrets_file')
@patch('app.send_welcome_email')
def test_google_callback_creates_new_user(mock_send_email, mock_flow_from_secrets, mock_requests_get, client):
    """
    Test that the Google callback creates a new user if they don't exist.
    """
    mock_flow_instance = MagicMock()
    mock_flow_instance.fetch_token.return_value = None
    mock_flow_instance.credentials = mock_credentials
    mock_flow_from_secrets.return_value = mock_flow_instance

    mock_response = MagicMock()
    mock_response.ok = True
    mock_response.json.return_value = MOCK_GOOGLE_USER_INFO
    mock_requests_get.return_value = mock_response

    res = client.get('/auth/google/callback?code=anyfakecode')

    assert res.status_code == 200
    json_data = res.get_json()
    assert 'access_token' in json_data
    assert json_data['role'] == 'parent'

    mock_send_email.assert_called_once()
    with app.app_context():
        user = User.query.filter_by(email=MOCK_GOOGLE_USER_INFO['email']).first()
        assert user is not None

@patch('app.requests.get')
@patch('app.Flow.from_client_secrets_file')
@patch('app.send_welcome_email')
def test_google_callback_logs_in_existing_user(mock_send_email, mock_flow_from_secrets, mock_requests_get, client):
    """
    Test that the Google callback logs in an existing user without creating a new one.
    """
    with app.app_context():
        existing_user = User(email='existing.user@example.com', role='parent')
        db.session.add(existing_user)
        db.session.commit()
        initial_user_count = User.query.count()

    mock_flow_instance = MagicMock()
    mock_flow_instance.fetch_token.return_value = None
    mock_flow_instance.credentials = mock_credentials
    mock_flow_from_secrets.return_value = mock_flow_instance

    mock_response = MagicMock()
    mock_response.ok = True
    mock_response.json.return_value = {'email': 'existing.user@example.com'}
    mock_requests_get.return_value = mock_response

    res = client.get('/auth/google/callback?code=anyfakecode')

    assert res.status_code == 200
    assert 'access_token' in res.get_json()

    mock_send_email.assert_not_called()
    with app.app_context():
        final_user_count = User.query.count()
        assert final_user_count == initial_user_count