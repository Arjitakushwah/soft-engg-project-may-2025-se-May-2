from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# ---------- User Model ----------

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ---------- Parent Model ----------

class Parent(db.Model):
    __tablename__ = 'parents'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    name = db.Column(db.String, nullable=False)
    children = db.relationship("Child", back_populates="parent")

# ---------- Child Model ----------

class Child(db.Model):
    __tablename__ = 'children'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.Integer, nullable=False)
    streak = db.Column(db.Integer, default=0)
    longest_streak = db.Column(db.Integer, default=0)
    badges = db.Column(db.Integer, default=0)
    parent_id = db.Column(db.Integer, db.ForeignKey('parents.id'), nullable=False)
    parent = db.relationship("Parent", back_populates="children")
    to_do_items = db.relationship("ToDoItem", back_populates="child")
    # story_attempts = db.relationship("StoryAttempt", back_populates="child")
    daily_stories = db.relationship("DailyStory", back_populates="child")
    journal_entries = db.relationship("JournalEntry", back_populates="child")
    infotainment_logs = db.relationship("InfotainmentReadLog", back_populates="child")

# ---------- To-Do Item Model ----------

class ToDoItem(db.Model):
    __tablename__ = 'todo_items'
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('children.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    task = db.Column(db.Text, nullable=False)
    is_done = db.Column(db.Boolean, default=False)
    child = db.relationship("Child", back_populates="to_do_items")

# ---------- Daily Story & Quiz ----------

class DailyStory(db.Model):
    __tablename__ = 'daily_stories'
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('children.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    child_prompt= db.Column(db.Text, nullable=False)
    title = db.Column(db.Text, nullable=False)
    theme = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    question = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.Text, nullable=False)
    option_b = db.Column(db.Text, nullable=False)
    option_c = db.Column(db.Text, nullable=False)
    option_d = db.Column(db.Text, nullable=False)
    correct_option = db.Column(db.Text, nullable=False )
    submitted_option = db.Column(db.Text, nullable=False,default='not submitted')
    is_done = db.Column(db.Boolean, default=False)

    #can be wrong , correct , not submitted
    is_correct = db.Column(db.String, nullable=False , default='not submitted')
    child = db.relationship("Child", back_populates="daily_stories")


class JournalEntry(db.Model):
    __tablename__ = 'journal_entries'
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('children.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    text = db.Column(db.String, nullable=False)
    mood = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_done = db.Column(db.Boolean, default=False)
    child = db.relationship("Child", back_populates="journal_entries")


class InfotainmentReadLog(db.Model):
    __tablename__ = 'infotainment_read_log'
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('children.id'), nullable=False)
    child_prompt = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False, default=datetime.utcnow().time()) 
    is_done = db.Column(db.Boolean, default=False)
    marked_at = db.Column(db.DateTime, default=datetime.utcnow)
    child = db.relationship("Child", back_populates="infotainment_logs")

class DailyProgress(db.Model):
    __tablename__ = 'daily_progress'
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('children.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, index=True)
    is_todo_complete = db.Column(db.Boolean, default=False)
    is_journal_done = db.Column(db.Boolean, default=False)
    is_story_done = db.Column(db.Boolean, default=False)
    is_infotainment_done = db.Column(db.Boolean, default=False)
    total_completed = db.Column(db.Integer, default=0)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    child = db.relationship("Child", backref="daily_progress")

class StreakMilestone(db.Model):
    __tablename__ = 'streak_milestones'
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('children.id'), nullable=False)
    milestone = db.Column(db.Integer, nullable=False)
    awarded_at = db.Column(db.DateTime, default=datetime.utcnow)

    db.UniqueConstraint('child_id', 'milestone')  # Prevent duplicates


