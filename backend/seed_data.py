from app import app
from setup_db import creat_db
from werkzeug.security import generate_password_hash
from datetime import datetime
import pytz

IST = pytz.timezone("Asia/Kolkata")
now_ist = datetime.now(IST)


with app.app_context():
    creat_db()
    from models import db, User, Parent, Child
    # Create a parent user
    parent_user = User(
        email="parent@example.com",
        username="parent1",
        password=generate_password_hash("Parent@123"),  
        role="parent",
        created_at=now_ist
    )
    db.session.add(parent_user)
    db.session.flush() 

    # Parent table entry
    parent = Parent(
        id=parent_user.id,
        name="John Doe"
    )
    db.session.add(parent)

    # Create a child user
    child_user = User(
        email="parent@example.com", 
        username="child1",
        password=generate_password_hash("Child@123"),
        role="child",
        created_at=now_ist
    )
    db.session.add(child_user)
    db.session.flush()

    # Child table entry
    child = Child(
        id=child_user.id,
        name="Alice",
        age=10,
        gender=1, 
        parent_id=parent.id
    )
    db.session.add(child)

    # Commit all changes
    db.session.commit()
    print("Seed data inserted successfully with IST timestamps!")
