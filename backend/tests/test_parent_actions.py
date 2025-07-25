# Backend/tests/test_parent_actions.py

from models import db, User, Parent, Child
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token
from app import app # Import the app instance

def test_add_child_success(client):
    """Test a parent successfully adding a child."""
    # Use the app context to ensure all operations happen in the same scope
    with app.app_context():
        # Setup: Create parent user
        hashed_pw = generate_password_hash("pw")
        user = User(username="parent1", password=hashed_pw, role="parent", email="p1@test.com")
        db.session.add(user)
        db.session.commit()
        parent = Parent(id=user.id, name="Parent One")
        db.session.add(parent)
        db.session.commit()

        # Create the token within the same app context
        token = create_access_token(identity=str(user.id), additional_claims={'role': 'parent'})
        headers = {'Authorization': f'Bearer {token}'}

    # The actual test is performed using the created token.
    # The client handles the application context for the request.
    res = client.post('/add-child', headers=headers, json={
        "username": "child1",
        "password": "childpw",
        "name": "Child One",
        "age": 10,
        "gender": "female"
    })
    
    assert res.status_code == 201
    assert res.get_json()['message'] == 'Child added successfully'

def test_get_all_children(client):
    """Test fetching all children associated with a parent."""
    with app.app_context():
        # Setup: Create parent and children
        parent_user = User(username="parent2", password=generate_password_hash("pw"), role="parent", email="p2@test.com")
        db.session.add(parent_user)
        db.session.commit()
        parent = Parent(id=parent_user.id, name="Parent Two")
        db.session.add(parent)
        db.session.commit()

        child1_user = User(username="child_a", password=generate_password_hash("cpw"), role="child", email="p2@test.com")
        db.session.add(child1_user)
        db.session.commit()
        child1 = Child(id=child1_user.id, name="Child A", age=8, gender="male", parent_id=parent.id)
        db.session.add(child1)
        db.session.commit()

        # Create the token within the context
        token = create_access_token(identity=str(parent_user.id), additional_claims={'role': 'parent'})
        headers = {'Authorization': f'Bearer {token}'}

    # The actual test
    res = client.get('/parent/children', headers=headers)
    
    assert res.status_code == 200
    children = res.get_json()['children']
    assert len(children) == 1
    assert children[0]['name'] == 'Child A'