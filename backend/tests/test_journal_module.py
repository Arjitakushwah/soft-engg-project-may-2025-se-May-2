from tests.helpers import create_child_and_get_token, create_dummy_journals
from unittest.mock import patch, ANY
from datetime import date

# --- Journal Creation Tests (/journal) ---

@patch('api.classify_emotion')
# def test_create_journal_success(mock_classify_emotion, client):
#     """
#     Test successful creation of a journal entry.
#     """
#     # 1. Mock the mood classification to return a predictable "happy" mood.
#     mock_classify_emotion.return_value = {"emotion": "happy"}
    
#     # 2. Get an authenticated child user.
#     token, child_id = create_child_and_get_token(client, "journal_user_1")
#     headers = {'Authorization': f'Bearer {token}'}
    
#     # 3. Make the API call to create a journal.
#     res = client.post('/journal', headers=headers, json={"text": "Today was a fantastic day!"})
    
#     # 4. Assert the results.
#     assert res.status_code == 200
#     json_data = res.get_json()
#     assert json_data['message'] == 'Journal entry created successfully'
#     assert json_data['mood'] == 'happy'
    
#     # Verify that the classify_emotion function was called correctly.
#     mock_classify_emotion.assert_called_once_with("Today was a fantastic day!", ANY)

def test_create_journal_missing_text(client):
    """
    Test the API's response when the 'text' field is missing from the request.
    """
    token, child_id = create_child_and_get_token(client, "journal_user_2")
    headers = {'Authorization': f'Bearer {token}'}
    
    res = client.post('/journal', headers=headers, json={}) # Send an empty JSON body
    
    assert res.status_code == 400
    assert res.get_json()['error'] == 'Journal text is required'

@patch('api.classify_emotion', side_effect=Exception("LLM is down"))
def test_create_journal_llm_failure(mock_classify_emotion, client):
    """
    Test the API's error handling when the mood classification agent fails.
    """
    token, child_id = create_child_and_get_token(client, "journal_user_3")
    headers = {'Authorization': f'Bearer {token}'}
    
    res = client.post('/journal', headers=headers, json={"text": "This will fail"})
    
    assert res.status_code == 500
    assert res.get_json()['error'] == 'Failed to process journal entry'

# --- Journal Search Tests (/journal/search) ---

# def test_search_journal_by_mood(client):
#     """
#     Test searching for all journal entries with a specific mood.
#     """
#     token, child_id = create_child_and_get_token(client, "search_user_1")
#     headers = {'Authorization': f'Bearer {token}'}
    
    # 1. Use the helper to create dummy journal entries.
    create_dummy_journals(client, child_id)
    
    # 2. Make the API call to search for "happy" entries.
    res = client.get('/journal/search?mood=happy', headers=headers)
    
    # 3. Assert the results. There should be two "happy" entries.
    assert res.status_code == 200
    search_results = res.get_json()['entries']
    assert len(search_results) == 2
    assert all(entry['mood'] == 'happy' for entry in search_results)

def test_search_journal_by_date(client):
    """
    Test searching for all journal entries from a specific date.
    """
    token, child_id = create_child_and_get_token(client, "search_user_2")
    headers = {'Authorization': f'Bearer {token}'}
    today_str = date.today().strftime("%Y-%m-%d")
    
    # 1. Use the helper to create dummy journal entries.
    create_dummy_journals(client, child_id)
    
    # 2. Make the API call to search for today's entries.
    res = client.get(f'/journal/search?date={today_str}', headers=headers)
    
    # 3. Assert the results. There should be two entries for today.
    assert res.status_code == 200
    search_results = res.get_json()['entries']
    assert len(search_results) == 2
    assert search_results[0]['text'] == "I was a bit sad that it rained." # The most recent one

# def test_search_journal_no_results(client):
#     """
#     Test that the search returns an empty list when no journals match the query.
#     """
#     token, child_id = create_child_and_get_token(client, "search_user_3")
#     headers = {'Authorization': f'Bearer {token}'}
    
#     # Make a search call without creating any dummy data
#     res = client.get('/journal/search?mood=excited', headers=headers)
    
#     assert res.status_code == 200
#     search_results = res.get_json()['entries']
#     assert len(search_results) == 0
