from tests.helpers import create_child_and_get_token, create_dummy_infotainment_logs
from unittest.mock import patch, ANY
from datetime import datetime, timedelta, date
from app import app
from models import db, InfotainmentReadLog

# --- Infotainment Generation Tests (/infotainment/generate) ---

@patch('api.generate_news')
def test_generate_infotainment_success(mock_generate_news, client):
    """
    Test successful generation of infotainment content.
    """
    # 1. Mock the LLM agent to return predictable content.
    mock_generate_news.return_value = "## Fun Facts About Space!\n\nSpace is vast and full of wonders."
    
    # 2. Get an authenticated child user.
    token, child_id = create_child_and_get_token(client, "info_user_1")
    headers = {'Authorization': f'Bearer {token}'}
    
    # 3. Make the API call.
    res = client.post('/infotainment/generate', headers=headers, json={"prompt": "space"})
    
    # 4. Assert the results.
    assert res.status_code == 201
    json_data = res.get_json()
    assert json_data['message'] == 'New content generated and stored.'
    assert "Space is vast" in json_data['content']
    
    # Verify the LLM was called correctly.
    mock_generate_news.assert_called_once_with("space", ANY)

def test_generate_infotainment_missing_prompt(client):
    """
    Test the API's response when the 'prompt' is missing.
    """
    token, child_id = create_child_and_get_token(client, "info_user_2")
    headers = {'Authorization': f'Bearer {token}'}
    
    res = client.post('/infotainment/generate', headers=headers, json={})
    
    assert res.status_code == 400
    assert res.get_json()['error'] == 'Prompt is required'

# --- Infotainment Search Tests (/infotainment/search) ---

def test_search_infotainment_by_keyword(client):
    """
    Test searching for infotainment logs by a keyword.
    """
    token, child_id = create_child_and_get_token(client, "search_user_1")
    headers = {'Authorization': f'Bearer {token}'}
    
    # 1. Use the helper to create dummy data.
    create_dummy_infotainment_logs(client, child_id)
    
    # 2. Make the API call to search for "volcanoes".
    res = client.get('/infotainment/search?q=volcanoes', headers=headers)
    
    # 3. Assert the results.
    assert res.status_code == 200
    search_results = res.get_json()['logs']
    assert len(search_results) == 1
    assert search_results[0]['prompt'] == 'volcanoes'

def test_search_infotainment_by_date(client):
    """
    Test searching for infotainment logs by a specific date.
    """
    token, child_id = create_child_and_get_token(client, "search_user_2")
    headers = {'Authorization': f'Bearer {token}'}
    today_str = date.today().strftime("%Y-%m-%d")
    
    create_dummy_infotainment_logs(client, child_id)
    
    res = client.get(f'/infotainment/search?date={today_str}', headers=headers)
    
    assert res.status_code == 200
    search_results = res.get_json()['logs']
    assert len(search_results) == 2 # Should find the two logs created for today

# --- Mark as Read Tests (/infotainment/mark-read/<log_id>) ---

def test_mark_infotainment_read_success(client):
    """
    Test successfully marking an infotainment log as read after the time limit.
    """
    token, child_id = create_child_and_get_token(client, "mark_user_1")
    headers = {'Authorization': f'Bearer {token}'}
    
    # Create a log entry with a timestamp from 5 minutes ago.
    with app.app_context():
        five_minutes_ago = datetime.now() - timedelta(minutes=5)
        log = InfotainmentReadLog(
            child_id=child_id, child_prompt="test", content="...",
            date=five_minutes_ago.date(), time=five_minutes_ago.time(),
            marked_at=five_minutes_ago, is_done=False
        )
        db.session.add(log)
        db.session.commit()
        log_id = log.id

    res = client.put(f'/infotainment/mark-read/{log_id}', headers=headers)
    
    assert res.status_code == 200
    assert res.get_json()['message'] == 'Marked as read successfully'

def test_mark_infotainment_read_fails_if_too_early(client):
    """
    Test that an infotainment log cannot be marked as read before 3 minutes have passed.
    """
    token, child_id = create_child_and_get_token(client, "mark_user_2")
    headers = {'Authorization': f'Bearer {token}'}
    
    # Create a log entry with a timestamp from just 1 minute ago.
    with app.app_context():
        one_minute_ago = datetime.now() - timedelta(minutes=1)
        log = InfotainmentReadLog(
            child_id=child_id, child_prompt="test", content="...",
            date=one_minute_ago.date(), time=one_minute_ago.time(),
            marked_at=one_minute_ago, is_done=False
        )
        db.session.add(log)
        db.session.commit()
        log_id = log.id

    res = client.put(f'/infotainment/mark-read/{log_id}', headers=headers)
    
    assert res.status_code == 403
    assert "You can mark as read after" in res.get_json()['error']
