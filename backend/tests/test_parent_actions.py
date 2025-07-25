# Backend/tests/test_parent_actions.py

# Import the new helper function
from tests.helpers import create_parent_with_child, create_parent_and_get_token

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