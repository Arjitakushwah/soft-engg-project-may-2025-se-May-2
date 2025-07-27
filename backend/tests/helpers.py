from models import db, User, Parent, Child
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token
from app import app
from models import Child, DailyStory, JournalEntry, InfotainmentReadLog, BadgeAward, DailyProgress
from datetime import date, timedelta, datetime


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
    


def create_dummy_journals(client, child_id):
    """
    Creates a set of dummy journal entries for a given child ID for testing search.
    """
    with app.app_context():
        today = date.today()
        yesterday = today - timedelta(days=1)

        entry1 = JournalEntry(child_id=child_id, date=today, text="I had a super happy day at the park!", mood="happy", is_done=True)
        entry2 = JournalEntry(child_id=child_id, date=today, text="I was a bit sad that it rained.", mood="sad", is_done=True)
        entry3 = JournalEntry(child_id=child_id, date=yesterday, text="Yesterday was also a happy day.", mood="happy", is_done=True)
        
        db.session.add_all([entry1, entry2, entry3])
        db.session.commit()

# Add this new function to your helpers.py file


def create_dummy_infotainment_logs(client, child_id):
    """
    Creates a set of dummy infotainment logs for a given child ID for testing search.
    """
    with app.app_context():
        today = date.today()
        yesterday = today - timedelta(days=1)
        now = datetime.now()

        log1 = InfotainmentReadLog(
            child_id=child_id, child_prompt="space", content="Fun facts about space.",
            date=today, time=now.time(), marked_at=now, is_done=False
        )
        log2 = InfotainmentReadLog(
            child_id=child_id, child_prompt="volcanoes", content="All about volcanoes.",
            date=today, time=now.time(), marked_at=now, is_done=True
        )
        log3 = InfotainmentReadLog(
            child_id=child_id, child_prompt="dinosaurs", content="The age of dinosaurs.",
            date=yesterday, time=now.time(), marked_at=now - timedelta(days=1), is_done=True
        )
        
        db.session.add_all([log1, log2, log3])
        db.session.commit()


# Add this new function to your helpers.py file


def create_dummy_daily_progress(client, child_id):
    """
    Creates a set of dummy DailyProgress records for a given child ID for testing.
    """
    with app.app_context():
        today = date.today()
        yesterday = today - timedelta(days=1)
        day_before = today - timedelta(days=2)

        # A day with all 4 tasks completed
        progress1 = DailyProgress(
            child_id=child_id, date=today,
            is_todo_complete=True, is_journal_done=True,
            is_story_done=True, is_infotainment_done=True,
            total_completed=4
        )
        # A day with 2 tasks completed
        progress2 = DailyProgress(
            child_id=child_id, date=yesterday,
            is_todo_complete=True, is_journal_done=True,
            is_story_done=False, is_infotainment_done=False,
            total_completed=2
        )
        # A day with 0 tasks completed (record exists but nothing done)
        progress3 = DailyProgress(
            child_id=child_id, date=day_before,
            is_todo_complete=False, is_journal_done=False,
            is_story_done=False, is_infotainment_done=False,
            total_completed=0
        )
        
        db.session.add_all([progress1, progress2, progress3])
        db.session.commit()



def create_dummy_streak_and_activities(client, child_id):
    """
    Creates a set of dummy activities, badges, and streak data for a given child ID.
    """
    with app.app_context():
        # Update the child's streak info directly
        child = db.session.get(Child, child_id)
        if child:
            child.streak = 5
            child.longest_streak = 10
        
        # Create some completed activities
        story1 = DailyStory(child_id=child_id, date=date.today(), is_done=True, title="s1", theme="t", content="c", question="q", option_a="a", option_b="b", option_c="c", option_d="d", correct_option="a", child_prompt="p")
        story2 = DailyStory(child_id=child_id, date=date.today(), is_done=True, title="s2", theme="t", content="c", question="q", option_a="a", option_b="b", option_c="c", option_d="d", correct_option="a", child_prompt="p")
        journal1 = JournalEntry(child_id=child_id, date=date.today(), text="...", mood="happy", is_done=True)
        
        # Create an incomplete activity (this should not be counted)
        infotainment_incomplete = InfotainmentReadLog(child_id=child_id, date=date.today(), is_done=False, child_prompt="p", content="c")

        # Create some badges
        badge1 = BadgeAward(child_id=child_id, badge_name="Story x1", badge_type="story")
        badge2 = BadgeAward(child_id=child_id, badge_name="Streak 5 days", badge_type="streak")

        db.session.add_all([
            child, story1, story2, journal1, 
            infotainment_incomplete, badge1, badge2
        ])
        db.session.commit()

# Add this new function to your helpers.py file
from models import DailyStory
from datetime import date, timedelta

def create_dummy_stories(client, child_id):
    """
    Creates a set of dummy stories for a given child ID for testing search.
    """
    with app.app_context():
        today = date.today()
        yesterday = today - timedelta(days=1)

        story1 = DailyStory(
            child_id=child_id, date=today, title="The Brave Knight",
            theme="Courage", content="...", question="?", option_a="a", option_b="b",
            option_c="c", option_d="d", correct_option="a", child_prompt="p"
        )
        story2 = DailyStory(
            child_id=child_id, date=today, title="The Silly Dragon",
            theme="Humor", content="...", question="?", option_a="a", option_b="b",
            option_c="c", option_d="d", correct_option="a", child_prompt="p"
        )
        story3 = DailyStory(
            child_id=child_id, date=yesterday, title="A Tale of Courage",
            theme="Courage", content="...", question="?", option_a="a", option_b="b",
            option_c="c", option_d="d", correct_option="a", child_prompt="p"
        )
        
        db.session.add_all([story1, story2, story3])
        db.session.commit()

# Add this new function to your helpers.py file
from models import ToDoItem
from datetime import datetime

def create_todo_item(client, child_id, task_text="An existing task", is_done=False):
    """
    Creates a ToDoItem in the database for a given child and returns the object.
    """
    with app.app_context():
        task = ToDoItem(
            child_id=child_id,
            task=task_text,
            datetime=datetime.now(),
            is_done=is_done
        )
        db.session.add(task)
        db.session.commit()
        return task.id
    
# Add this new function to your helpers.py file
from models import JournalEntry, DailyProgress
from datetime import date, timedelta

def create_dummy_parent_reports_data(client, parent_username="report_parent"):
    """
    Creates a parent, a child, and a history of journal entries and daily progress.
    Returns the parent's token and the child's ID.
    """
    # Use an existing helper to create the basic parent/child structure
    parent_token, child_data = create_parent_with_child(client, parent_username=parent_username)
    child_id = child_data['id']

    with app.app_context():
        today = date.today()
        yesterday = today - timedelta(days=1)
        
        # Create dummy journal entries
        journal1 = JournalEntry(child_id=child_id, date=today, text="Happy day!", mood="happy")
        journal2 = JournalEntry(child_id=child_id, date=today, text="Sad evening.", mood="sad")
        journal3 = JournalEntry(child_id=child_id, date=yesterday, text="Yesterday was fun.", mood="happy")
        
        # Create dummy daily progress records
        progress1 = DailyProgress(
            child_id=child_id, date=today,
            is_journal_done=True, is_story_done=True, total_completed=2
        )
        progress2 = DailyProgress(
            child_id=child_id, date=yesterday,
            is_journal_done=True, is_story_done=True, is_todo_complete=True, is_infotainment_done=True,
            total_completed=4
        )
        
        db.session.add_all([journal1, journal2, journal3, progress1, progress2])
        db.session.commit()
        
        return parent_token, child_id
    

