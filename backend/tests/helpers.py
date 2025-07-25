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