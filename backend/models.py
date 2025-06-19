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
    badges = db.Column(db.Integer, default=0)
    parent_id = db.Column(db.Integer, db.ForeignKey('parents.id'), nullable=False)
    parent = db.relationship("Parent", back_populates="children")
    to_do_items = db.relationship("ToDoItem", back_populates="child")
    story_attempts = db.relationship("StoryAttempt", back_populates="child")
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
    date = db.Column(db.Date, nullable=False, unique=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    quiz = db.relationship("QuizQuestion", back_populates="story", uselist=False)

class QuizQuestion(db.Model):
    __tablename__ = 'quiz_questions'
    id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer, db.ForeignKey('daily_stories.id'), nullable=False)
    question = db.Column(db.String, nullable=False)
    option_a = db.Column(db.String, nullable=False)
    option_b = db.Column(db.String, nullable=False)
    option_c = db.Column(db.String, nullable=False)
    option_d = db.Column(db.String, nullable=False)
    correct_option = db.Column(db.String, nullable=False)
    story = db.relationship("DailyStory", back_populates="quiz")

# ---------- Story Attempt Model ----------

class StoryAttempt(db.Model):
    __tablename__ = 'story_attempts'
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('children.id'), nullable=False)
    story_id = db.Column(db.Integer, db.ForeignKey('daily_stories.id'), nullable=False)
    submitted_option = db.Column(db.String, nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    child = db.relationship("Child", back_populates="story_attempts")
    story = db.relationship("DailyStory")

# ---------- Journal Entry Model ----------

class JournalEntry(db.Model):
    __tablename__ = 'journal_entries'
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('children.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    text = db.Column(db.String, nullable=False)
    mood = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    child = db.relationship("Child", back_populates="journal_entries")

# ---------- Infotainment Content Model ----------

class InfotainmentDailyContent(db.Model):
    __tablename__ = 'infotainment_daily_content'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, unique=True)
    content = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ---------- Infotainment Read Log ----------

class InfotainmentReadLog(db.Model):
    __tablename__ = 'infotainment_read_log'
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('children.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    marked_at = db.Column(db.DateTime, default=datetime.utcnow)
    child = db.relationship("Child", back_populates="infotainment_logs")
