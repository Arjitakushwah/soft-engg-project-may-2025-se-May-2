# Backend/tests/test_story_module.py

from models import db, DailyStory
from app import app
from tests.helpers import setup_parent_and_child
from unittest.mock import patch, ANY
from datetime import date

@patch('api.generate_story')
def test_generate_story(mock_generate_story, client):
    """Test story generation, mocking the AI agent."""
    mock_generate_story.return_value = {
        'title': 'The Mocking Bird', 'theme': 'Kindness', 'content': 'A tale...',
        'quiz': {'question': '?', 'options': ['A', 'B', 'C', 'D'], 'answer': 'A'}
    }
    child_id, token = setup_parent_and_child("story1")
    headers = {'Authorization': f'Bearer {token}'}
    
    res = client.post('/generate_story', headers=headers, json={"child_prompt": "A kind bird"})
    
    assert res.status_code == 201
    mock_generate_story.assert_called_once_with("A kind bird", ANY)

def test_submit_quiz(client):
    """Test submitting a correct answer to a quiz."""
    child_id, token = setup_parent_and_child("quiz1")
    headers = {'Authorization': f'Bearer {token}'}
    
    with app.app_context():
        story = DailyStory(
            child_id=child_id, date=date.today(), title="Test Quiz Story", child_prompt="p",
            theme="t", content="c", question="q", option_a="Yes", option_b="No",
            option_c="Maybe", option_d="Always", correct_option="Yes"
        )
        db.session.add(story)
        db.session.commit()
        
    res = client.post('/submit_quiz', headers=headers, json={
        "story_title": "Test Quiz Story",
        "selected_option": "Yes"
    })
    
    assert res.status_code == 200