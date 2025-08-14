# Backend/tests/test_streaks_and_badges.py

from tests.helpers import create_child_and_get_token, create_dummy_streak_and_activities

def test_get_streak_and_badge_summary(client):
    """
    Test the API endpoint for retrieving a summary of streaks, badges, and activities.
    """
    # 1. Setup a child user and create a history of activities and badges.
    token, child_id = create_child_and_get_token(client, "summary_user_1")
    headers = {'Authorization': f'Bearer {token}'}
    create_dummy_streak_and_activities(client, child_id)
    
    # 2. Make the API call to the /streak-badges endpoint.
    res = client.get('/streak-badges', headers=headers)
    
    # 3. Assert the results to ensure all data is correct.
    assert res.status_code == 200
    summary_data = res.get_json()
    
    # Check streak values
    assert summary_data['current_streak'] == 5
    assert summary_data['longest_streak'] == 10
    
    # Check activity counts (only completed activities should be counted)
    assert summary_data['total_stories_read'] == 2
    assert summary_data['total_journals_written'] == 1
    assert summary_data['total_infotainment_read'] == 0 # The dummy log was incomplete
    
    # Check badge information
    assert summary_data['badges_count'] == 2
    assert len(summary_data['badges']) == 2
    
    # Verify the content of one of the badges
    badge_names = [badge['name'] for badge in summary_data['badges']]
    assert "Story x1" in badge_names
    assert "Streak 5 days" in badge_names

def test_get_streak_summary_for_new_user(client):
    """
    Test the summary for a new user with no activity.
    """
    # 1. Setup a new child user without any additional activity data.
    token, child_id = create_child_and_get_token(client, "new_user_1")
    headers = {'Authorization': f'Bearer {token}'}
    
    # 2. Make the API call.
    res = client.get('/streak-badges', headers=headers)
    
    # 3. Assert that all counts are zero for a new user.
    assert res.status_code == 200
    summary_data = res.get_json()
    
    assert summary_data['current_streak'] == 0
    assert summary_data['longest_streak'] == 0
    assert summary_data['total_stories_read'] == 0
    assert summary_data['total_journals_written'] == 0
    assert summary_data['total_infotainment_read'] == 0
    assert summary_data['badges_count'] == 0
    assert summary_data['badges'] == []
