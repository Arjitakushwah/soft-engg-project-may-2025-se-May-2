from tests.helpers import create_child_and_get_token, create_dummy_daily_progress
from datetime import date, timedelta

def test_calendar_report_correct_colors(client):
    """
    Test that the calendar report returns the correct color codes based on task completion.
    """
    # 1. Setup a child user and create dummy progress data.
    token, child_id = create_child_and_get_token(client, "calendar_user_1")
    headers = {'Authorization': f'Bearer {token}'}
    create_dummy_daily_progress(client, child_id)
    
    today = date.today()
    yesterday = today - timedelta(days=1)
    day_before = today - timedelta(days=2)

    # 2. Make the API call to get the report.
    res = client.get('/calendar-report', headers=headers)
    
    # 3. Assert the results.
    assert res.status_code == 200
    progress_data = res.get_json()['progress']
    
    # Check today (4 tasks done -> darkest green)
    assert progress_data[today.isoformat()]['status'] == "#216e39"
    assert progress_data[today.isoformat()]['not_done'] == []
    
    # Check yesterday (2 tasks done -> light green)
    assert progress_data[yesterday.isoformat()]['status'] == "#c6e48b"
    assert "story" in progress_data[yesterday.isoformat()]['not_done']
    
    # Check the day before (0 tasks done -> almost white)
    assert progress_data[day_before.isoformat()]['status'] == "#f0f0f0"
    assert len(progress_data[day_before.isoformat()]['not_done']) == 4

def test_calendar_report_date_range(client):
    """
    Test the calendar report's date range filtering.
    """
    token, child_id = create_child_and_get_token(client, "calendar_user_2")
    headers = {'Authorization': f'Bearer {token}'}
    create_dummy_daily_progress(client, child_id)
    # Backend/tests/test_calendar_module.py

from tests.helpers import create_child_and_get_token, create_dummy_daily_progress
from datetime import date, timedelta

def test_calendar_report_correct_colors(client):
    """
    Test that the calendar report returns the correct color codes based on task completion.
    """
    # 1. Setup a child user and create dummy progress data.
    token, child_id = create_child_and_get_token(client, "calendar_user_1")
    headers = {'Authorization': f'Bearer {token}'}
    create_dummy_daily_progress(client, child_id)
    
    today = date.today()
    yesterday = today - timedelta(days=1)
    day_before = today - timedelta(days=2)

    # 2. Make the API call to get the report.
    # FIX: Explicitly provide the start and end date to ensure all dummy data is fetched.
    res = client.get(f'/calendar-report?start_date={day_before.isoformat()}&end_date={today.isoformat()}', headers=headers)
    
    # 3. Assert the results.
    assert res.status_code == 200
    progress_data = res.get_json()['progress']
    
    # Check today (4 tasks done -> darkest green)
    assert progress_data[today.isoformat()]['status'] == "#216e39"
    assert progress_data[today.isoformat()]['not_done'] == []
    
    # Check yesterday (2 tasks done -> light green)
    assert progress_data[yesterday.isoformat()]['status'] == "#c6e48b"
    assert "story" in progress_data[yesterday.isoformat()]['not_done']
    
    # Check the day before (0 tasks done -> almost white)
    assert progress_data[day_before.isoformat()]['status'] == "#f0f0f0"
    assert len(progress_data[day_before.isoformat()]['not_done']) == 4

def test_calendar_report_date_range(client):
    """
    Test the calendar report's date range filtering.
    """
    token, child_id = create_child_and_get_token(client, "calendar_user_2")
    headers = {'Authorization': f'Bearer {token}'}
    create_dummy_daily_progress(client, child_id)
    
    yesterday = date.today() - timedelta(days=1)
    yesterday_str = yesterday.strftime("%Y-%m-%d")

    # Search for a specific date range that only includes yesterday
    res = client.get(f'/calendar-report?start_date={yesterday_str}&end_date={yesterday_str}', headers=headers)
    
    assert res.status_code == 200
    progress_data = res.get_json()['progress']
    
    # The result should contain exactly one day's data
    assert len(progress_data) == 1
    assert yesterday_str in progress_data
    assert progress_data[yesterday_str]['status'] == "#c6e48b" # 2 tasks done

def test_calendar_report_no_data(client):
    """
    Test the report's response for a date range with no progress records.
    """
    token, child_id = create_child_and_get_token(client, "calendar_user_3")
    headers = {'Authorization': f'Bearer {token}'}
    
    # Request a date far in the future where no data exists
    future_date = (date.today() + timedelta(days=30)).strftime("%Y-%m-%d")
    
    res = client.get(f'/calendar-report?start_date={future_date}&end_date={future_date}', headers=headers)
    
    assert res.status_code == 200
    progress_data = res.get_json()['progress']
    
    # Check the single day's data (0 tasks done -> almost white)
    assert progress_data[future_date]['status'] == "#f0f0f0"
    assert len(progress_data[future_date]['not_done']) == 4

    yesterday = date.today() - timedelta(days=1)
    yesterday_str = yesterday.strftime("%Y-%m-%d")

    # Search for a specific date range that only includes yesterday
    res = client.get(f'/calendar-report?start_date={yesterday_str}&end_date={yesterday_str}', headers=headers)
    
    assert res.status_code == 200
    progress_data = res.get_json()['progress']
    
    # The result should contain exactly one day's data
    assert len(progress_data) == 1
    assert yesterday_str in progress_data
    assert progress_data[yesterday_str]['status'] == "#c6e48b" # 2 tasks done

def test_calendar_report_no_data(client):
    """
    Test the report's response for a date range with no progress records.
    """
    token, child_id = create_child_and_get_token(client, "calendar_user_3")
    headers = {'Authorization': f'Bearer {token}'}
    
    # Request a date far in the future where no data exists
    future_date = (date.today() + timedelta(days=30)).strftime("%Y-%m-%d")
    
    res = client.get(f'/calendar-report?start_date={future_date}&end_date={future_date}', headers=headers)
    
    assert res.status_code == 200
    progress_data = res.get_json()['progress']
    
    # Check the single day's data (0 tasks done -> almost white)
    assert progress_data[future_date]['status'] == "#f0f0f0"
    assert len(progress_data[future_date]['not_done']) == 4
