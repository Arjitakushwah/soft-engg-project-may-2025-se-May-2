# Backend/tests/test_google_auth.py

from unittest.mock import patch, MagicMock
from models import db, User, Parent
from app import app

# This is a sample user profile that the mocked Google API will return.
MOCK_GOOGLE_USER_INFO = {
    'email': 'new.google.user@example.com',
    'name': 'Google User'
}

# This will be a mock for the `credentials` object that the Flow library creates.
mock_credentials = MagicMock()
mock_credentials.token = 'fake-google-api-token'

# We patch the functions and classes exactly where they are used in your app.py
@patch('app.requests.get')
@patch('app.Flow.from_client_secrets_file')
@patch('app.send_welcome_email')
def test_google_callback_creates_new_user(mock_send_email, mock_flow_from_secrets, mock_requests_get, client):
    """
    Test that the Google callback creates a new user if they don't exist.
    """
    # --- Setup the Mocks ---

    # 1. Mock the Flow instance and its methods.
    #    When `Flow.from_client_secrets_file` is called, it will return our mock instance.
    mock_flow_instance = MagicMock()
    mock_flow_instance.fetch_token.return_value = None  # This method modifies the instance in place.
    mock_flow_instance.credentials = mock_credentials
    mock_flow_from_secrets.return_value = mock_flow_instance

    # 2. Mock the `requests.get` call that fetches user info.
    mock_response = MagicMock()
    mock_response.ok = True
    mock_response.json.return_value = MOCK_GOOGLE_USER_INFO
    mock_requests_get.return_value = mock_response

    # --- Run the Test ---
    # Make a GET request to your callback URL. The query string is not important
    # because we have mocked the `fetch_token` method.
    res = client.get('/auth/google/callback?code=anyfakecode')

    # --- Assertions ---
    # Check the response from our server
    assert res.status_code == 200
    json_data = res.get_json()
    assert 'access_token' in json_data
    assert json_data['role'] == 'parent'

    # Check that the external APIs were called as expected
    mock_flow_from_secrets.assert_called()
    mock_flow_instance.fetch_token.assert_called()
    mock_requests_get.assert_called_with(
        'https://www.googleapis.com/oauth2/v3/userinfo',
        headers={'Authorization': f'Bearer {mock_credentials.token}'}
    )
    # Check that the welcome email was sent for the new user
    mock_send_email.assert_called_once()

    # Check the database state
    with app.app_context():
        user = User.query.filter_by(email=MOCK_GOOGLE_USER_INFO['email']).first()
        assert user is not None
        assert user.role == 'parent'
        # Check that a corresponding Parent record was also created
        parent = Parent.query.filter_by(id=user.id).first()
        assert parent is not None


@patch('app.requests.get')
@patch('app.Flow.from_client_secrets_file')
@patch('app.send_welcome_email')
def test_google_callback_logs_in_existing_user(mock_send_email, mock_flow_from_secrets, mock_requests_get, client):
    """
    Test that the Google callback logs in an existing user without creating a new one.
    """
    # --- Setup the Database State ---
    with app.app_context():
        # Create the user in the database beforehand
        existing_user = User(email='existing.user@example.com', role='parent')
        db.session.add(existing_user)
        db.session.commit()
        initial_user_count = User.query.count()

    # --- Setup the Mocks ---
    mock_flow_instance = MagicMock()
    mock_flow_instance.fetch_token.return_value = None
    mock_flow_instance.credentials = mock_credentials
    mock_flow_from_secrets.return_value = mock_flow_instance

    mock_response = MagicMock()
    mock_response.ok = True
    # The user info from Google should match the user we created in the DB
    mock_response.json.return_value = {'email': 'existing.user@example.com'}
    mock_requests_get.return_value = mock_response

    # --- Run the Test ---
    res = client.get('/auth/google/callback?code=anyfakecode')

    # --- Assertions ---
    assert res.status_code == 200
    assert 'access_token' in res.get_json()

    # IMPORTANT: Check that no new user was created and no welcome email was sent
    mock_send_email.assert_not_called()
    with app.app_context():
        final_user_count = User.query.count()
        assert final_user_count == initial_user_count