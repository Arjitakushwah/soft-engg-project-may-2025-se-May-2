from datetime import date, timedelta
from models import db, Child, DailyProgress, BadgeAward, JournalEntry, DailyStory, InfotainmentReadLog

# Badge Milestones
STREAK_BADGE_MILESTONES = [1, 5, 10, 15, 30, 50, 100]
JOURNAL_BADGE_MILESTONES = [1, 5, 10, 20, 50]
STORY_BADGE_MILESTONES = [1, 5, 10, 20, 50]
INFOTAINMENT_BADGE_MILESTONES = [1, 5, 10, 20, 50]

def award_badge(child_id, badge_type, badge_name):
    """Helper to award a badge if not already awarded."""
    already_awarded = BadgeAward.query.filter_by(child_id=child_id, badge_name=badge_name).first()
    if not already_awarded:
        new_badge = BadgeAward(child_id=child_id, badge_type=badge_type, badge_name=badge_name)
        db.session.add(new_badge)

def update_streak(child_id):
    """Update current streak, longest streak, and award streak-related badges."""
    today = date.today()
    child = db.session.get(Child, child_id)
    if not child:
        return
    # Count continuous days with at least 4 tasks completed
    streak = 0
    current_date = today
    while True:
        progress = DailyProgress.query.filter_by(child_id=child_id, date=current_date).first()
        if not progress or progress.total_completed < 4:
            break
        streak += 1
        current_date -= timedelta(days=1)
    child.streak = streak
    if streak > child.longest_streak:
        child.longest_streak = streak
    # Award streak milestone badges
    if streak in STREAK_BADGE_MILESTONES:
        award_badge(child_id, badge_type="streak", badge_name=f"Streak {streak} days")

def evaluate_all_badges(child_id):
    """Main function to update streak and evaluate all types of badges."""
    child = db.session.get(Child, child_id)
    if not child:
        return

    # Update streak and award streak badges
    update_streak(child_id)

    # Journal badges
    total_journals = JournalEntry.query.filter_by(child_id=child_id).count()
    for milestone in JOURNAL_BADGE_MILESTONES:
        if total_journals >= milestone:
            award_badge(child_id, badge_type="journal", badge_name=f"Journal x{milestone}")

    # Story badges
    total_stories = DailyStory.query.filter_by(child_id=child_id, is_done=True).count()
    for milestone in STORY_BADGE_MILESTONES:
        if total_stories >= milestone:
            award_badge(child_id, badge_type="story", badge_name=f"Story x{milestone}")

    # Infotainment badges
    total_info_reads = InfotainmentReadLog.query.filter_by(child_id=child_id, is_done=True).count()
    for milestone in INFOTAINMENT_BADGE_MILESTONES:
        if total_info_reads >= milestone:
            award_badge(child_id, badge_type="infotainment", badge_name=f"Infotainment x{milestone}")

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print("Error while awarding badges:", e)
