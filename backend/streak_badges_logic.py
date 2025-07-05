from datetime import date, timedelta
from models import db, Child, DailyProgress, StreakMilestone

# Set the milestone to award badges.
STREAK_BADGE_MILESTONES = [1, 5, 10, 15, 30, 50, 100]

def update_streak(child_id):
    today = date.today()
    child = db.session.get(Child, child_id)
    if not child:
        return
    # Start counting streak backward
    streak = 0
    current_date = today
    while True:
        progress = DailyProgress.query.filter_by(child_id=child_id, date=current_date).first()
        if not progress or progress.total_completed < 4:
            break
        streak += 1
        current_date -= timedelta(days=1)
    # Updating the streak value
    child.streak = streak
    # Update the longest streak when current streak greater than longest streak
    if streak > getattr(child, 'longest_streak', 0):
        child.longest_streak = streak
    # Badges awarded when specified milestone reached only one time
    if streak in STREAK_BADGE_MILESTONES:
        already_awarded = StreakMilestone.query.filter_by(child_id=child_id, milestone=streak).first()
        if not already_awarded:
            child.badges += 1
            new_milestone = StreakMilestone(child_id=child_id, milestone=streak)
            db.session.add(new_milestone)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print("Streak update error:", e)
