# Backend/tests/test_story_module.py

from models import db, DailyStory
from app import app
from tests.helpers import create_child_and_get_token, create_dummy_stories
from unittest.mock import patch, ANY
from datetime import date

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

@patch('api.certify_query')
@patch('api.generate_story')
def test_generate_story_llm_fails(mock_generate_story, mock_certify_query, client):
    """
    Test the API's error handling when the LLM returns invalid data.
    """
    # FIX: Mock the certification step to ensure the test proceeds to the generation step.
    mock_certify_query.return_value = "true"
    
    # Simulate the LLM returning a simple string instead of a valid dictionary
    mock_generate_story.return_value = "Sorry, I could not generate a story."
    
    token, child_id = create_child_and_get_token(client, "story_user_3")
    headers = {'Authorization': f'Bearer {token}'}
    
    res = client.post('/generate_story', headers=headers, json={"child_prompt": "a prompt that will pass certification"})
    
    # Now the test should correctly receive the 500 error from the generation failure
    assert res.status_code == 500
    assert res.get_json()['error'] == 'Story generation failed'

# --- Quiz Submission Tests (/submit_quiz) ---

def test_submit_quiz_correct_answer(client):
    """
    Test the logic for submitting a correct quiz answer.
    """
    token, child_id = create_child_and_get_token(client, "quiz_user_1")
    headers = {'Authorization': f'Bearer {token}'}
    
    with app.app_context():
        story = DailyStory(
            child_id=child_id, date=date.today(), title="The Mystery of the Missing Sock",
            child_prompt="a mystery story", theme="Curiosity", content="...",
            question="Who stole the sock?", option_a="The dog", option_b="The cat",
            option_c="A ghost", option_d="The washing machine", correct_option="The dog"
        )
        db.session.add(story)
        db.session.commit()
        story_title = story.title
        correct_option = story.correct_option

    res = client.post('/submit_quiz', headers=headers, json={
        "story_title": story_title,
        "selected_option": correct_option
    })
    
    assert res.status_code == 200
    assert res.get_json()['message'] == 'Answer submitted successfully'
    
    with app.app_context():
        updated_story = DailyStory.query.filter_by(child_id=child_id).first()
        assert updated_story.is_correct == 'correct'

def test_submit_quiz_wrong_answer(client):
    """
    Test the logic for submitting an incorrect quiz answer.
    """
    token, child_id = create_child_and_get_token(client, "quiz_user_2")
    headers = {'Authorization': f'Bearer {token}'}
    
    with app.app_context():
        story = DailyStory(
            child_id=child_id, date=date.today(), title="The Quest for the Golden Apple",
            child_prompt="a quest", theme="Adventure", content="...",
            question="What was the prize?", option_a="A silver coin", option_b="A golden apple",
            option_c="A magic sword", option_d="A new hat", correct_option="A golden apple"
        )
        db.session.add(story)
        db.session.commit()
        story_title = story.title

    res = client.post('/submit_quiz', headers=headers, json={
        "story_title": story_title,
        "selected_option": "An incorrect answer"
    })
    
    assert res.status_code == 200

    with app.app_context():
        updated_story = DailyStory.query.filter_by(child_id=child_id).first()
        assert updated_story.is_correct == 'not submitted'

# --- Story Search Tests (/stories) ---

def test_search_story_by_title(client):
    """
    Test searching for stories by a keyword in the title.
    """
    token, child_id = create_child_and_get_token(client, "search_user_1")
    headers = {'Authorization': f'Bearer {token}'}
    create_dummy_stories(client, child_id)

    res = client.get('/stories?by=title&query=Knight', headers=headers)

    assert res.status_code == 200
    search_results = res.get_json()['stories']
    assert len(search_results) == 1
    assert search_results[0]['title'] == "The Brave Knight"

def test_search_story_by_date(client):
    """
    Test searching for stories by a specific date.
    """
    token, child_id = create_child_and_get_token(client, "search_user_2")
    headers = {'Authorization': f'Bearer {token}'}
    create_dummy_stories(client, child_id)
    today_str = date.today().strftime("%Y-%m-%d")

    res = client.get(f'/stories?by=date&query={today_str}', headers=headers)

    assert res.status_code == 200
    search_results = res.get_json()['stories']
    assert len(search_results) == 2
