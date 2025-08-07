from tests.helpers import create_parent_with_child, create_parent_and_get_token, create_dummy_parent_reports_data
from datetime import date, timedelta

def test_add_child_success(client):
    """Test a parent successfully adding a child using a fixture."""
    # This test uses the other helper, which is fine
    token = create_parent_and_get_token(client)
    headers = {'Authorization': f'Bearer {token}'}

    res = client.post('/add-child', headers=headers, json={
        "username": "new_child", "password": "childpw",
        "name": "New Child", "age": 9, "gender": "male"
    })
    
    assert res.status_code == 201
    assert res.get_json()['message'] == 'Child added successfully'

def test_get_all_children(client):
    """Test fetching all children associated with a parent using a helper."""
    # 1. Setup the state with a single call to the helper
    parent_token, child_data = create_parent_with_child(client, child_name="Child Alpha")
    headers = {'Authorization': f'Bearer {parent_token}'}

    # 2. Run the actual test
    res = client.get('/parent/children', headers=headers)
    
    # 3. Assert the results using the returned dictionary
    assert res.status_code == 200
    children_from_api = res.get_json()['children']
    assert len(children_from_api) == 1
    assert children_from_api[0]['id'] == child_data['id']
    assert children_from_api[0]['name'] == child_data['name']

def test_get_child_profile_summary_success(client):
    """
    Test that a parent can successfully fetch the profile summary of their own child.
    """
    # 1. Setup: Create a parent with a child and get the parent's token and child's data.
    parent_token, child_data = create_parent_with_child(client, child_name="Alex")
    headers = {'Authorization': f'Bearer {parent_token}'}
    child_id = child_data['id']

    # 2. Make the API call to the specific child's profile endpoint.
    res = client.get(f'/parent/child/{child_id}/profile', headers=headers)
    
    # 3. Assert the results.
    assert res.status_code == 200
    profile = res.get_json()['profile']
    
    assert profile['id'] == child_id
    assert profile['name'] == "Alex"
    assert profile['age'] == 8  # As defined in the helper
    assert profile['streak'] == 0 # Default for new child

def test_get_child_profile_unauthorized(client):
    """
    Test that a parent cannot fetch the profile of a child that does not belong to them.
    """
    # 1. Setup: Create two separate parents, each with their own child.
    parent1_token, child1_data = create_parent_with_child(client, parent_username="parent1", child_name="Child One")
    parent2_token, child2_data = create_parent_with_child(client, parent_username="parent2", child_name="Child Two")
    
    # Parent 1 will try to access Child 2's profile.
    headers = {'Authorization': f'Bearer {parent1_token}'}
    child2_id = child2_data['id']

    # 2. Make the API call.
    res = client.get(f'/parent/child/{child2_id}/profile', headers=headers)
    
    # 3. Assert that the request is rejected.
    assert res.status_code == 404
    assert res.get_json()['error'] == 'Child not found or unauthorized'

def test_get_child_profile_not_found(client):
    """
    Test the API's response when a parent requests a child ID that does not exist.
    """
    # 1. Setup: Create a parent user.
    parent_token = create_parent_and_get_token(client)
    headers = {'Authorization': f'Bearer {parent_token}'}
    
    # 2. Make the API call with a non-existent child ID.
    non_existent_child_id = 9999
    res = client.get(f'/parent/child/{non_existent_child_id}/profile', headers=headers)
    
    # 3. Assert that the server responds with a 404 error.
    assert res.status_code == 404
    assert res.get_json()['error'] == 'Child not found or unauthorized'


# Backend/tests/test_parent_reports.py

from tests.helpers import create_parent_with_child, create_dummy_parent_reports_data
from unittest.mock import patch
from datetime import date

# --- Parent-Facing Journal APIs Tests ---

def test_get_child_journal_entries_no_limit(client):
    """
    Test fetching all journal entries for a child when no limit is specified.
    """
    parent_token, child_id = create_dummy_parent_reports_data(client)
    headers = {'Authorization': f'Bearer {parent_token}'}
    
    res = client.get(f'/parent/child/{child_id}/journal-entries', headers=headers)
    
    assert res.status_code == 200
    json_data = res.get_json()
    assert len(json_data['journal_entries']) == 3

def test_get_child_journal_entries_with_limit(client):
    """
    Test that the 'limit' query parameter correctly limits the number of journal entries returned.
    """
    parent_token, child_id = create_dummy_parent_reports_data(client)
    headers = {'Authorization': f'Bearer {parent_token}'}
    
    res = client.get(f'/parent/child/{child_id}/journal-entries?limit=2', headers=headers)
    
    assert res.status_code == 200
    json_data = res.get_json()
    assert len(json_data['journal_entries']) == 2

def test_get_journal_by_date(client):
    """
    Test fetching a child's full journal entries for a specific date.
    """
    parent_token, child_id = create_dummy_parent_reports_data(client)
    headers = {'Authorization': f'Bearer {parent_token}'}
    today_str = date.today().strftime("%Y-%m-%d")
    
    res = client.get(f'/parent/child/{child_id}/journal-by-date?date={today_str}', headers=headers)
    
    assert res.status_code == 200
    json_data = res.get_json()
    assert len(json_data['journal_entries']) == 2
    assert json_data['journal_entries'][0]['content'] == "Happy day!"

# --- Parent-Facing Summary and Report APIs Tests ---

def test_get_weekly_summary(client):
    """
    Test the weekly summary report for a child.
    """
    parent_token, child_id = create_dummy_parent_reports_data(client)
    headers = {'Authorization': f'Bearer {parent_token}'}
    
    res = client.get(f'/parent/child/{child_id}/summary?range=weekly', headers=headers)
    
    assert res.status_code == 200
    summary = res.get_json()['summary']
    
    # Based on the dummy data (2 days of activity in the last week)
    assert summary['journal_done_days'] == 2
    assert summary['story_done_days'] == 2
    assert summary['tasks_completed'] == 6 # 4 from yesterday, 2 from today

def test_get_monthly_summary(client):
    """
    Test the monthly summary report for a child.
    """
    parent_token, child_id = create_dummy_parent_reports_data(client)
    headers = {'Authorization': f'Bearer {parent_token}'}
    
    res = client.get(f'/parent/child/{child_id}/summary?range=monthly', headers=headers)
    
    assert res.status_code == 200
    summary = res.get_json()['summary']
    
    # Assumes the dummy data is the only activity this month
    assert summary['journal_done_days'] == 2
    assert summary['tasks_completed'] == 6

@patch('api.os.path.exists') # FIX: Add this mock
@patch('api.generate_pdf')
@patch('api.analyze_child_data')
def test_generate_child_analysis_report(mock_analyze_child_data, mock_generate_pdf, mock_path_exists, client):
    """
    Test the endpoint that generates a PDF analysis report.
    Mocks the external services to avoid actual PDF generation.
    """
    mock_analyze_child_data.return_value = "## Child Report\n\nThis is a mock report."
    mock_generate_pdf.return_value = "mock_report.pdf"
    mock_path_exists.return_value = True # FIX: Ensure the file "exists"

    parent_token, child_id = create_dummy_parent_reports_data(client)
    headers = {'Authorization': f'Bearer {parent_token}'}

    # Mocking send_file is still a good practice to prevent file system operations
    with patch('api.send_file', return_value="PDF content") as mock_send_file:
        res = client.post(f'/parent/child-analysis?child_id={child_id}&summary_range=weekly', headers=headers)
        
        assert res.status_code == 200
        mock_analyze_child_data.assert_called_once()
        mock_generate_pdf.assert_called_once()
        mock_path_exists.assert_called_once_with("mock_report.pdf")
        mock_send_file.assert_called_once()


# Backend/tests/test_parent_reports.py

from tests.helpers import create_parent_with_child, create_dummy_parent_reports_data
from datetime import date, timedelta

# --- Child Daily Performance Tests (/parent/child/<id>/performance) ---

def test_child_daily_performance_success(client):
    """
    Test fetching the daily performance report for a child on a specific date.
    """
    # 1. Setup: Create a parent and child with a history of daily progress.
    parent_token, child_id = create_dummy_parent_reports_data(client)
    headers = {'Authorization': f'Bearer {parent_token}'}
    today_str = date.today().strftime("%Y-%m-%d")
    
    # 2. Make the API call for today's date.
    res = client.get(f'/parent/child/{child_id}/performance?date={today_str}', headers=headers)
    
    # 3. Assert the results.
    assert res.status_code == 200
    performance_data = res.get_json()
    
    assert performance_data['date'] == today_str
    assert performance_data['total_completed'] == 2 # Based on dummy data
    assert performance_data['journal_done'] is True
    assert performance_data['todo_completed'] is False

def test_child_daily_performance_no_data(client):
    """
    Test the response when fetching performance for a date with no activity.
    """
    parent_token, child_data = create_parent_with_child(client)
    child_id = child_data['id']
    headers = {'Authorization': f'Bearer {parent_token}'}
    future_date_str = (date.today() + timedelta(days=5)).strftime("%Y-%m-%d")
    
    res = client.get(f'/parent/child/{child_id}/performance?date={future_date_str}', headers=headers)
    
    assert res.status_code == 200
    performance_data = res.get_json()
    
    assert performance_data['total_completed'] == 0
    assert performance_data['message'] == 'No tasks attempted on this date'

# --- Child Calendar Report Tests (/parent/child/<id>/calendar-report) ---

def test_child_calendar_report_success(client):
    """
    Test fetching the full calendar report for a child.
    """
    parent_token, child_id = create_dummy_parent_reports_data(client)
    headers = {'Authorization': f'Bearer {parent_token}'}
    today_str = date.today().strftime("%Y-%m-%d")
    
    res = client.get(f'/parent/child/{child_id}/calendar-report', headers=headers)
    
    assert res.status_code == 200
    report_data = res.get_json()['report']
    
    # Check that the report contains data for the day with activity
    assert today_str in report_data
    # Verify the details for that day
    assert report_data[today_str]['total_completed'] == 2
    assert "journal" in report_data[today_str]['completed']
    assert "todo" in report_data[today_str]['not_completed']

def test_child_daily_performance_unauthorized(client):
    """
    Test that a parent cannot access the performance report of a child that is not theirs.
    """
    # Create Parent 1 with their child
    parent1_token, child1_id = create_dummy_parent_reports_data(client, parent_username="parent1")
    
    # Create Parent 2 with a different child
    parent2_token, child2_data = create_parent_with_child(client, parent_username="parent2", child_name="Child Beta")

    # Parent 2 tries to access Child 1's report
    headers = {'Authorization': f'Bearer {parent2_token}'}
    today_str = date.today().strftime("%Y-%m-%d")
    
    res = client.get(f'/parent/child/{child1_id}/performance?date={today_str}', headers=headers)
    
    assert res.status_code == 404
    assert res.get_json()['error'] == 'Child not found'
