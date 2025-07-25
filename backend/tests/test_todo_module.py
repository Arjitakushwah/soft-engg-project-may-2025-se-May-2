# Backend/tests/test_todo_module.py

from models import db, ToDoItem
from app import app
from tests.helpers import setup_parent_and_child
from unittest.mock import patch
from datetime import date

@patch('api.ist_today')
def test_create_todo_task(mock_ist_today, client):
    """Test a child can successfully create a to-do task."""
    mock_ist_today.return_value = date.today()
    child_id, token = setup_parent_and_child("todo1")
    headers = {'Authorization': f'Bearer {token}'}
    today_str = date.today().strftime('%Y-%m-%d')

    res = client.post('/todo', headers=headers, json={
        "task": "Read a chapter",
        "datetime": today_str
    })
    
    assert res.status_code == 201
    assert res.get_json()['task'] == 'Read a chapter'

def test_update_todo_status(client):
    """Test a child can mark today's to-do task as complete."""
    child_id, token = setup_parent_and_child("todo2")
    headers = {'Authorization': f'Bearer {token}'}
    today = date.today()
    
    with app.app_context():
        task = ToDoItem(child_id=child_id, datetime=today, task="Test this status", is_done=False)
        db.session.add(task)
        db.session.commit()
        task_id = task.id

    res = client.put(f'/todo/status/{task_id}', headers=headers)
    assert res.status_code == 200
    assert res.get_json()['message'] == 'Task Completed successfully'