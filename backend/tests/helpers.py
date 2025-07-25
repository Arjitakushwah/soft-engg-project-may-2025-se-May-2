# Backend/tests/helpers.py

from models import db, User, Parent, Child
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token
from app import app


def setup_parent_and_child(username_prefix="test"):
    """Helper function to create a parent and a child, returning the child's ID and token."""
    with app.app_context():
        # Create Parent
        parent_user = User(
            username=f"{username_prefix}_parent", password=generate_password_hash("pw"),
            role="parent", email=f"{username_prefix}_parent@test.com"
        )
        db.session.add(parent_user)
        db.session.commit()
        parent = Parent(id=parent_user.id, name="Test Parent")
        db.session.add(parent)
        db.session.commit()

        # Create Child
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
    


def create_parent_and_get_token(client, username="test_parent"):
    """
    Creates a parent user in the database and returns a valid auth token.
    """
    with app.app_context():
        hashed_pw = generate_password_hash("password")
        user = User(username=username, password=hashed_pw, role="parent", email=f"{username}@test.com")
        db.session.add(user)
        db.session.commit()
        
        parent = Parent(id=user.id, name="Test Parent")
        db.session.add(parent)
        db.session.commit()

        token = create_access_token(identity=str(user.id), additional_claims={'role': 'parent'})
        return token

def create_child_and_get_token(client, username="test_child"):
    """
    Creates both a parent and a child user, returning the child's auth token and ID.
    """
    with app.app_context():
        # Parent is required for a child to exist
        parent_user = User(
            username="parent_for_child", password=generate_password_hash("pw"),
            role="parent", email="pfc@test.com"
        )
        db.session.add(parent_user)
        db.session.commit()
        parent = Parent(id=parent_user.id, name="Parent For Child")
        db.session.add(parent)
        db.session.commit()

        # Child user
        child_user = User(
            username=username, password=generate_password_hash("pw"),
            role="child", email=parent_user.email
        )
        db.session.add(child_user)
        db.session.commit()
        child = Child(id=child_user.id, name="Test Child", age=10, gender="female", parent_id=parent.id)
        db.session.add(child)
        db.session.commit()
        
        token = create_access_token(identity=str(child_user.id), additional_claims={'role': 'child'})
        return token, child_user.id
    

# Add this new function to your helpers.py file

def create_parent_with_child(client, parent_username="parent_with_child", child_name="Child A"):
    """
    Creates a parent and a child, then returns the PARENT's token and the child's data.
    """
    with app.app_context():
        # 1. Create Parent
        parent_user = User(
            username=parent_username, password=generate_password_hash("pw"),
            role="parent", email=f"{parent_username}@test.com"
        )
        db.session.add(parent_user)
        db.session.commit()
        parent = Parent(id=parent_user.id, name="Test Parent")
        db.session.add(parent)
        db.session.commit()

        # 2. Create Child
        child_user = User(
            username=f"{child_name.lower().replace(' ', '_')}", password=generate_password_hash("pw"),
            role="child", email=parent_user.email
        )
        db.session.add(child_user)
        db.session.commit()
        child = Child(id=child_user.id, name=child_name, age=8, gender="male", parent_id=parent.id)
        db.session.add(child)
        db.session.commit()
        
        # FIX: Capture the necessary data before the session closes
        child_data = {'id': child.id, 'name': child.name}
        
        # 3. Create the PARENT's token
        parent_token = create_access_token(identity=str(parent_user.id), additional_claims={'role': 'parent'})
        
        # Return the primitive data (a dictionary), not the detached SQLAlchemy object
        return parent_token, child_data