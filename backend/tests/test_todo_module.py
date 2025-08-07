from models import db, ToDoItem
from app import app
from tests.helpers import setup_parent_and_child
from unittest.mock import patch
from tests.helpers import create_child_and_get_token
from datetime import datetime, date, timedelta
from tests.helpers import create_todo_item


# --- To-Do Creation Tests (/todo) ---

@patch('api.ist_now')
def test_create_todo_task_success(mock_ist_now, client):
    """
    Test successful creation of a to-do task with a valid future date and time.
    """
    # 1. Mock the current time to a fixed point to make the test predictable.
    now = datetime(2025, 7, 26, 12, 0, 0)
    mock_ist_now.return_value = now
    
    # 2. Get an authenticated child user.
    token, child_id = create_child_and_get_token(client, "todo_user_1")
    headers = {'Authorization': f'Bearer {token}'}
    
    # 3. Define the task details for a future time.
    task_date = (now + timedelta(days=1)).strftime('%Y-%m-%d')
    task_time = "10:30"

    # 4. Make the API call.
    res = client.post('/todo', headers=headers, json={
        "task": "Plan the weekend",
        "date": task_date,
        "time": task_time
    })
    
    # 5. Assert the results.
    assert res.status_code == 201, f"API Error: {res.get_data(as_text=True)}"
    json_data = res.get_json()
    assert json_data['task'] == "Plan the weekend"
    assert json_data['date'] == task_date
    assert json_data['time'] == task_time

def test_create_todo_task_missing_fields(client):
    """
    Test the API's response when 'task' or 'date' fields are missing.
    """
    token, child_id = create_child_and_get_token(client, "todo_user_2")
    headers = {'Authorization': f'Bearer {token}'}
    
    # Test with missing task
    res_no_task = client.post('/todo', headers=headers, json={"date": "2025-08-01"})
    assert res_no_task.status_code == 400
    assert res_no_task.get_json()['error'] == 'Task and date are required'
    
    # Test with missing date
    res_no_date = client.post('/todo', headers=headers, json={"task": "A task with no date"})
    assert res_no_date.status_code == 400
    assert res_no_date.get_json()['error'] == 'Task and date are required'

@patch('api.ist_now')
def test_create_todo_task_in_past(mock_ist_now, client):
    """
    Test that creating a task for a past date/time is not allowed.
    """
    # Set the current time to a fixed point.
    now = datetime(2025, 7, 26, 12, 0, 0)
    mock_ist_now.return_value = now
    
    token, child_id = create_child_and_get_token(client, "todo_user_3")
    headers = {'Authorization': f'Bearer {token}'}
    
    # Define a task for a time that is in the past relative to the mocked "now".
    past_date = (now - timedelta(days=1)).strftime('%Y-%m-%d')

    res = client.post('/todo', headers=headers, json={
        "task": "This task is in the past",
        "date": past_date,
        "time": "11:00"
    })
    
    assert res.status_code == 400
    assert res.get_json()['error'] == 'Cannot create tasks for past dates/times'

def test_create_todo_invalid_formats(client):
    """
    Test the API's validation for incorrect date and time formats.
    """
    token, child_id = create_child_and_get_token(client, "todo_user_4")
    headers = {'Authorization': f'Bearer {token}'}

    # Test with invalid date format
    res_invalid_date = client.post('/todo', headers=headers, json={
        "task": "Invalid date format",
        "date": "26-07-2025" # Should be YYYY-MM-DD
    })
    assert res_invalid_date.status_code == 400
    assert res_invalid_date.get_json()['error'] == 'Invalid date format. Use YYYY-MM-DD'

    # Test with invalid time format
    res_invalid_time = client.post('/todo', headers=headers, json={
        "task": "Invalid time format",
        "date": "2025-07-26",
        "time": "10:30 AM" # Should be HH:MM
    })
    assert res_invalid_time.status_code == 400
    assert "Invalid time values. Hours (0-23) and minutes (0-59)" in res_invalid_time.get_json()['error']


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


# --- To-Do Get and Status Update Tests ---

def test_get_tasks_by_date(client):
    """
    Test fetching all tasks for a specific date.
    """
    token, child_id = create_child_and_get_token(client, "get_user_1")
    headers = {'Authorization': f'Bearer {token}'}
    create_todo_item(client, child_id, "Task for today")
    today_str = date.today().strftime('%Y-%m-%d')

    res = client.get(f'/todo?date={today_str}', headers=headers)
    
    assert res.status_code == 200
    json_data = res.get_json()
    assert len(json_data['tasks']) == 1
    assert json_data['tasks'][0]['task'] == "Task for today"

@patch('api.ist_now')
def test_update_task_status_success(mock_ist_now, client):
    """
    Test successfully marking a task as complete.
    """
    now = datetime(2025, 7, 26, 14, 0, 0)
    mock_ist_now.return_value = now
    
    token, child_id = create_child_and_get_token(client, "status_user_1")
    headers = {'Authorization': f'Bearer {token}'}
    
    # Create a task scheduled for an hour ago relative to "now"
    with app.app_context():
        task_time = now - timedelta(hours=1)
        task = ToDoItem(child_id=child_id, task="Finish this test", datetime=task_time, is_done=False)
        db.session.add(task)
        db.session.commit()
        task_id = task.id

    res = client.put(f'/todo/status/{task_id}', headers=headers)
    
    assert res.status_code == 200
    assert res.get_json()['message'] == 'Task Completed successfully'

# --- To-Do Update Tests (/todo/<id> PUT) ---

def test_update_todo_task_success(client):
    """
    Test successfully updating a task's text and time.
    """
    token, child_id = create_child_and_get_token(client, "update_user_1")
    headers = {'Authorization': f'Bearer {token}'}
    task_id = create_todo_item(client, child_id)

    updated_date = (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d')
    
    res = client.put(f'/todo/{task_id}', headers=headers, json={
        "task": "Updated task text",
        "date": updated_date,
        "time": "15:00"
    })

    assert res.status_code == 200
    json_data = res.get_json()
    assert json_data['task'] == "Updated task text"
    assert json_data['date'] == updated_date
    assert json_data['time'] == "15:00"

def test_update_completed_todo_task_fails(client):
    """
    Test that an already completed task cannot be updated.
    """
    token, child_id = create_child_and_get_token(client, "update_user_2")
    headers = {'Authorization': f'Bearer {token}'}
    task_id = create_todo_item(client, child_id, is_done=True)

    res = client.put(f'/todo/{task_id}', headers=headers, json={"task": "Trying to update"})
    
    assert res.status_code == 403
    assert res.get_json()['error'] == 'Cannot update completed task'

# --- To-Do Deletion Tests (/todo/<id> DELETE) ---

def test_delete_todo_task_success(client):
    """
    Test successfully deleting an incomplete task.
    """
    token, child_id = create_child_and_get_token(client, "delete_user_1")
    headers = {'Authorization': f'Bearer {token}'}
    task_id = create_todo_item(client, child_id)

    res = client.delete(f'/todo/{task_id}', headers=headers)
    
    assert res.status_code == 200
    assert res.get_json()['message'] == 'Task deleted successfully'
    
    with app.app_context():
        deleted_task = db.session.get(ToDoItem, task_id)
        assert deleted_task is None

def test_delete_completed_todo_task_fails(client):
    """
    Test that a completed task cannot be deleted.
    """
    token, child_id = create_child_and_get_token(client, "delete_user_2")
    headers = {'Authorization': f'Bearer {token}'}
    task_id = create_todo_item(client, child_id, is_done=True)

    res = client.delete(f'/todo/{task_id}', headers=headers)
    
    assert res.status_code == 403
    assert res.get_json()['error'] == 'You can not delete completed task'

# --- To-Do Get and Status Update Tests ---

def test_get_tasks_by_date(client):
    """
    Test fetching all tasks for a specific date.
    """
    token, child_id = create_child_and_get_token(client, "get_user_1")
    headers = {'Authorization': f'Bearer {token}'}
    create_todo_item(client, child_id, "Task for today")
    today_str = date.today().strftime('%Y-%m-%d')

    res = client.get(f'/todo?date={today_str}', headers=headers)
    
    assert res.status_code == 200
    json_data = res.get_json()
    assert len(json_data['tasks']) == 1
    assert json_data['tasks'][0]['task'] == "Task for today"

@patch('api.ist_now')
def test_update_task_status_success(mock_ist_now, client):
    """
    Test successfully marking a task as complete.
    """
    now = datetime(2025, 7, 26, 14, 0, 0)
    mock_ist_now.return_value = now
    token, child_id = create_child_and_get_token(client, "status_user_1")
    headers = {'Authorization': f'Bearer {token}'}
    # Create a task scheduled for an hour ago relative to "now"
    with app.app_context():
        task_time = now - timedelta(hours=1)
        task = ToDoItem(child_id=child_id, task="Finish this test", datetime=task_time, is_done=False)
        db.session.add(task)
        db.session.commit()
        task_id = task.id
    res = client.put(f'/todo/status/{task_id}', headers=headers)
    assert res.status_code == 200
    assert res.get_json()['message'] == 'Task Completed successfully'

