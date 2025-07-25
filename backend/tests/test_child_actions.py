# Backend/tests/test_child_actions.py

from models import db, User, Parent, Child, ToDoItem, DailyStory, InfotainmentReadLog
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token
from app import app
from unittest.mock import patch, ANY
from datetime import date, datetime, timedelta

def setup_parent_and_child(username_prefix="test"):
    """Helper function to create a parent and a child, returning the child's ID and token."""
    with app.app_context():
        parent_user = User(
            username=f"{username_prefix}_parent", password=generate_password_hash("pw"),
            role="parent", email=f"{username_prefix}_parent@test.com"
        )
        db.session.add(parent_user)
        db.session.commit()
        parent = Parent(id=parent_user.id, name="Test Parent")
        db.session.add(parent)
        db.session.commit()

        child_user = User(
            username=f"{username_prefix}_child", password=generate_password_hash("pw"),
            role="child", email=parent_user.email
        )
        db.session.add(child_user)
        db.session.commit()
        child = Child(id=child_user.id, name="Test Child", age=10, gender="female", parent_id=parent.id)
        db.session.add(child)
        db.session.commit()
        
        child_id = child_user.id
        token = create_access_token(identity=str(child_id), additional_claims={'role': 'child'})
        
        return child_id, token

# --- To-Do List Tests ---

@patch('api.ist_today')
def test_create_todo_task(mock_ist_today, client):
    """Test a child can successfully create a to-do task."""
    mock_ist_today.return_value = date.today()
    child_id, token = setup_parent_and_child("todo1")
    headers = {'Authorization': f'Bearer {token}'}
    today_str = date.today().strftime('%Y-%m-%d')

    # FIX: The key in the JSON payload must be "datetime" to match your API's expectation.
    res = client.post('/todo', headers=headers, json={
        "task": "Read a chapter",
        "datetime": today_str
    })
    
    assert res.status_code == 201, f"API Error: {res.get_data(as_text=True)}"
    assert res.get_json()['task'] == 'Read a chapter'

def test_update_todo_status(client):
    """Test a child can mark today's to-do task as complete."""
    child_id, token = setup_parent_and_child("todo2")
    headers = {'Authorization': f'Bearer {token}'}
    today = datetime.utcnow().date() # Use a date object here
    
    with app.app_context():
        # FIX: Use the correct attribute `datetime` to match your ToDoItem model.
        task = ToDoItem(child_id=child_id, datetime=today, task="Test this status", is_done=False)
        db.session.add(task)
        db.session.commit()
        task_id = task.id

    res = client.put(f'/todo/status/{task_id}', headers=headers)
    assert res.status_code == 200, f"API Error: {res.get_data(as_text=True)}"
    assert res.get_json()['message'] == 'Task Completed successfully'

# --- Story Module and Other Tests ---

@patch('api.generate_story')
def test_generate_story(mock_generate_story, client):
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
    res = client.post('/submit_quiz', headers=headers, json={"story_title": "Test Quiz Story", "selected_option": "Yes"})
    assert res.status_code == 200

# --- Infotainment Tests ---

def test_mark_infotainment_read_fails_if_too_early(client):
    """Test that infotainment cannot be marked as read before 3 minutes."""
    child_id, token = setup_parent_and_child("info1")
    headers = {'Authorization': f'Bearer {token}'}
    
    # FIX: Avoid mocking datetime. Instead, manually create the log entry in the database
    # with a timestamp in the past. This is a more stable way to test time logic.
    with app.app_context():
        two_minutes_ago = datetime.utcnow() - timedelta(minutes=2)
        log = InfotainmentReadLog(
            child_id=child_id,
            child_prompt="space",
            content="## Fun Fact!",
            date=two_minutes_ago.date(),
            time=two_minutes_ago.time(),
            marked_at=two_minutes_ago,
            is_done=False
        )
        db.session.add(log)
        db.session.commit()
        log_id = log.id

    res_mark = client.put(f'/infotainment/mark-read/{log_id}', headers=headers)
    
    # The API correctly returns 403 Forbidden. This test verifies that logic.
    assert res_mark.status_code == 403, f"Expected 403 Forbidden, but got {res_mark.status_code}"
    assert "You can mark as read after" in res_mark.get_json()['error']