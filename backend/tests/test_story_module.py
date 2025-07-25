# Backend/tests/test_story_module.py

from models import db, DailyStory
from app import app
from tests.helpers import create_child_and_get_token
from unittest.mock import patch, ANY
from datetime import date

# --- Story Generation Tests (/generate_story) ---


# --- Story Generation Tests (/generate_story) ---

@patch('api.generate_story')
def test_generate_story_success(mock_generate_story, client):
    """
    Test successful story generation when the LLM provides a valid response.
    """
    mock_generate_story.return_value = {
        'title': 'The Courageous Caterpillar',
        'theme': 'Perseverance',
        'content': 'A story about a caterpillar who never gave up.',
        'quiz': {
            'question': 'What was the caterpillar\'s best quality?',
            'options': ['Speed', 'Strength', 'Perseverance', 'Color'],
            'answer': 'Perseverance'
        }
    }
    
    token, child_id = create_child_and_get_token(client, "story_user_1")
    headers = {'Authorization': f'Bearer {token}'}
    
    res = client.post('/generate_story', headers=headers, json={"child_prompt": "A caterpillar's journey"})
    
    assert res.status_code == 201
    story_response = res.get_json()['story']
    assert story_response['title'] == 'The Courageous Caterpillar'
    
def test_generate_story_missing_prompt(client):
    """
    Test the API's response when the child_prompt is missing from the request.
    """
    token, child_id = create_child_and_get_token(client, "story_user_2")
    headers = {'Authorization': f'Bearer {token}'}
    
    res = client.post('/generate_story', headers=headers, json={}) # Empty JSON body
    
    assert res.status_code == 400
    assert res.get_json()['error'] == 'child_prompt is required'

@patch('api.generate_story')
def test_generate_story_llm_fails(mock_generate_story, client):
    """
    Test the API's error handling when the LLM returns invalid data.
    """
    # Simulate the LLM returning a simple string instead of a valid dictionary
    mock_generate_story.return_value = "Sorry, I could not generate a story."
    
    token, child_id = create_child_and_get_token(client, "story_user_3")
    headers = {'Authorization': f'Bearer {token}'}
    
    res = client.post('/generate_story', headers=headers, json={"child_prompt": "an invalid prompt"})
    
    assert res.status_code == 500
    assert res.get_json()['error'] == 'Story generation failed'

@patch('api.generate_story')
def test_generate_story_llm_unable_to_generate(mock_generate_story, client):
    """
    Test the API's error handling when the LLM returns an empty or None response.
    """
    # Simulate the LLM failing to generate content and returning None
    mock_generate_story.return_value = None
    
    token, child_id = create_child_and_get_token(client, "story_user_4")
    headers = {'Authorization': f'Bearer {token}'}
    
    res = client.post('/generate_story', headers=headers, json={"child_prompt": "a very complex prompt"})
    
    assert res.status_code == 500
    assert res.get_json()['error'] == 'Story generation failed'
    
    # Ensure no story was saved to the database on failure
    with app.app_context():
        story_in_db = DailyStory.query.filter_by(child_id=child_id).first()
        assert story_in_db is None

# --- Quiz Submission Tests (/submit_quiz) ---



def test_submit_quiz_correct_answer(client, story_fixture):
    """
   Test the logic for submitting a correct quiz answer using a fixture.
    """
    token, child_id, story = story_fixture
    headers = {'Authorization': f'Bearer {token}'}
# Make the API call with the correct answer
    res = client.post('/submit_quiz', headers=headers, json={
    "story_title": story.title,
 "selected_option": story.correct_option
 })
    assert res.status_code == 200
    assert res.get_json()['message'] == 'Answer submitted successfully'
    with app.app_context():
        updated_story = db.session.get(DailyStory, story.id)
        assert updated_story.is_correct == 'correct'



def test_submit_quiz_wrong_answer(client, story_fixture):
    """
Test the logic for submitting an incorrect quiz answer using a fixture.
 """
    token, child_id, story = story_fixture
    headers = {'Authorization': f'Bearer {token}'}
    res = client.post('/submit_quiz', headers=headers, json={
"story_title": story.title,
"selected_option": "An incorrect answer" # Submit a wrong answer
})
    assert res.status_code == 200
    with app.app_context():
        updated_story = db.session.get(DailyStory, story.id)
        assert updated_story.is_correct == 'wrong'



# --- Story Search Tests (/stories/search) ---



def test_search_story_by_keyword(client, story_fixture):
    """
Test searching for stories by a keyword in the title using a fixture.
 """
    token, child_id, story = story_fixture
    headers = {'Authorization': f'Bearer {token}'}
# Make the API call to search for a keyword from the fixture's story
    res = client.get('/stories/search?q=Mystery', headers=headers)
    assert res.status_code == 200
    search_results = res.get_json()['stories']
    assert len(search_results) == 1
    assert search_results[0]['title'] == "The Mystery of the Missing Sock"



def test_search_story_by_date(client, story_fixture):
    """
    Test searching for stories by a specific date using a fixture.
"""
    token, child_id, story = story_fixture
    headers = {'Authorization': f'Bearer {token}'}
    today_str = date.today().strftime("%Y-%m-%d")
    res = client.get(f'/stories/search?date={today_str}', headers=headers)
    assert res.status_code == 200
    search_results = res.get_json()['stories']
    assert len(search_results) >= 1 # Should find at least the story from the fixture
    assert search_results[0]['title'] == story.title