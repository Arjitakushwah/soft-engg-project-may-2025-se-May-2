from models import db, ToDoItem, JournalEntry, DailyStory, InfotainmentReadLog, DailyProgress
from sqlalchemy import func

"""
Function: update_daily_progress(child_id, target_date)
Create and update the daily tasks (To-Do, Journal, Story, and Infotainment) status.

Parameters:
- child_id (int): The ID of the child.
- target_date (date): The specific date for which the progress is being evaluated.

Behavior:
- If no existing `DailyProgress` record is found for the child then new one is created.
- Checks:
    - To-Do is marked complete only if all tasks are marked as done.
    - Journal, Story, and Infotainment are marked complete if a corresponding record with `is_done=True` exists for that date.
- Computes `total_completed` task.
- Commits the updated progress to the database.

Used In:
- This is automatically called in To-Do tasks, journals, stories, or infotainment to keep progress tracking consistent.
"""

def update_daily_progress(child_id, target_date):
    progress = DailyProgress.query.filter_by(child_id=child_id, date=target_date).first()
    if not progress:
        progress = DailyProgress(child_id=child_id, date=target_date)
        db.session.add(progress)
    
    todos = ToDoItem.query.filter(ToDoItem.child_id==child_id, func.date(ToDoItem.datetime)==target_date).all()
    # Checking the all Todo tasks completed or not.
    progress.is_todo_complete = all(t.is_done for t in todos) if todos else False
    # Check Journal is done or not
    progress.is_journal_done = JournalEntry.query.filter_by(child_id=child_id, date=target_date, is_done=True).first() is not None
    # Check Daily story is done or not
    progress.is_story_done = DailyStory.query.filter_by(child_id=child_id, date=target_date, is_done=True).first() is not None
    # Check Infotainment is done or not
    progress.is_infotainment_done = InfotainmentReadLog.query.filter_by(child_id=child_id, date=target_date, is_done=True).first() is not None
    # Compute the total completed tasks
    progress.total_completed = sum([
        progress.is_todo_complete,
        progress.is_journal_done,
        progress.is_story_done,
        progress.is_infotainment_done
    ])

    db.session.commit()
