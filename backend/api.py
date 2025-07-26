from datetime import datetime, date, timedelta
from utils import jwt_required
from flask import request, jsonify, send_file
from models import db, ToDoItem, User, DailyStory, JournalEntry, InfotainmentReadLog, Child, DailyProgress, BadgeAward
from app import app
from pytz import timezone
from crewai import LLM
from sqlalchemy import func
from pytz import timezone
from report_pdf import generate_pdf





IST = timezone("Asia/Kolkata")

def ist_now():
    aware_dt = datetime.now(IST).replace(second=0, microsecond=0)
    return aware_dt.replace(tzinfo=None)

def ist_today():
    print("IST Today:", datetime.now(IST).date())
    return datetime.now(IST).date()

app.config['SQLALCHEMY_ECHO'] = True

from agents.story_agent import generate_story
from agents.news_agent import generate_news
from agents.mood_classifier import classify_emotion
from progressor import update_daily_progress
from streak_badges_logic import evaluate_all_badges
from agents.report_agent import analyze_child_data
import os
from dotenv import load_dotenv
load_dotenv("agents/prod.env") 
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

llm = LLM(model='gemini/gemini-2.0-flash', api_key=GOOGLE_API_KEY)  # Replace with your actual LLM API key


#------------------------------------To DO List task creation---------------------------------------------------- 
""" 
API: Create To-Do Task 
This API allows child to create task for specific date 

Role Required: 
- Child 

Request Body (JSON): 
- task (str): Accept the task description from child. 
- date (str): The date for which the task is created in YYYY-MM-DD format. (Required) 
- time (str, optional): The time for the task in HH:MM format. 

Response: 
- 201: Task created successfully. 
- 400: If task or date is missing, the date is in the past, or the format is invalid. 
- 500: Internal server error if task creation fails. 
""" 
#------------------------------------To DO List task creation---------------------------------------------------- 
@app.route('/todo', methods=['POST']) 
@jwt_required(required_role='child')  
def create_todo_task(current_user_id, current_user_role): 
    try: 
        data = request.get_json() 
        if not data: 
            return jsonify({'error': 'No data provided'}), 400 
            
        task_text = data.get('task') 
        date_str = data.get('date')  
        time_str = data.get('time', '00:00')  # Default time if not provided 

        if not task_text or not date_str: 
            return jsonify({'error': 'Task and date are required'}), 400 
            
        # Validate date format 
        try: 
            task_date = datetime.strptime(date_str, '%Y-%m-%d').date() 
        except ValueError: 
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400 

        # Validate time format (accepts both HH:MM and HH:MM:SS) 
        time_parts = time_str.split(':') 
        if len(time_parts) < 2 or len(time_parts) > 3: 
            return jsonify({'error': 'Invalid time format. Use HH:MM or HH:MM:SS'}), 400 
            
        try: 
            hours = int(time_parts[0]) 
            minutes = int(time_parts[1]) 
            if hours < 0 or hours > 23 or minutes < 0 or minutes > 59: 
                raise ValueError 
        except ValueError: 
            return jsonify({'error': 'Invalid time values. Hours (0-23) and minutes (0-59)'}), 400 

        # Combine date and time 
        try: 
            task_datetime = datetime.strptime(f"{date_str} {time_str}", '%Y-%m-%d %H:%M:%S') 
        except ValueError: 
            try: 
                task_datetime = datetime.strptime(f"{date_str} {time_str}", '%Y-%m-%d %H:%M') 
            except ValueError: 
                return jsonify({'error': 'Invalid datetime format'}), 400 

        # Check if datetime is in the past (with 1 minute buffer) 
        if task_datetime < ist_now() - timedelta(minutes=1): 
            return jsonify({'error': 'Cannot create tasks for past dates/times'}), 400 
            
        new_task = ToDoItem( 
            child_id=current_user_id,  
            task=task_text.strip(), 
            datetime=task_datetime, 
            is_done=False 
        ) 
        
        db.session.add(new_task) 
        db.session.commit() 
        
        return jsonify({ 
            'id': new_task.id, 
            'task': new_task.task, 
            'date': new_task.datetime.strftime('%Y-%m-%d'), 
            'time': new_task.datetime.strftime('%H:%M'), 
            'is_done': new_task.is_done 
        }), 201 
        
    except Exception as e: 
        db.session.rollback() 
        print(f"Error creating task: {str(e)}") 
        return jsonify({'error': 'Failed to create task'}), 500 


#-----------------------------------------To Do List Task update---------------------------------------------------------- 
""" 
API: Update To-Do Task 
Child can update the task details which is not completed and also can update 
the date but it must be current or future date. 
Role Required: 

- Child 
Path Parameters: 
- task_id (int): The ID of the task to update. 

Request Body (JSON): 
- task (str, optional): The updated description of task. 
- date (str, optional): The new task date in YYYY-MM-DD format. 
- time (str, optional): The new task time in HH:MM format. 

Restrictions: 
- Already completed task and past date task can not update. 
- The new date must not be past date or before child's account creation date. 

Response: 
- 200: Task updated successfully. 
- 400: If user try to update status or provide invalid date (past date). 
- 403: If user trying to update a completed task. 
- 404: If the task or user is not found. 
- 500: Internal server error if update fails. 
""" 
#-----------------------------------------To Do List Task update---------------------------------------------------------- 
@app.route('/todo/<int:task_id>', methods=['PUT']) 
@jwt_required(required_role='child') 
def update_todo_task(task_id, current_user_id, current_user_role): 
    try: 
        data = request.get_json() 
        task = ToDoItem.query.filter_by(id=task_id, child_id=current_user_id).first() 

        if not task: 
            return jsonify({'error': 'Task not found'}), 404 
        if task.is_done: 
            return jsonify({'error': 'Cannot update completed task'}), 403 

        # Get current date and time from task, or use new data if provided 
        new_date_str = data.get('date', task.datetime.strftime('%Y-%m-%d')) 
        new_time_str = data.get('time', task.datetime.strftime('%H:%M')) 
        
        # Validate date format 
        try: 
            new_date = datetime.strptime(new_date_str, '%Y-%m-%d').date() 
        except ValueError: 
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400 

        # Validate time format 
        time_parts = new_time_str.split(':') 
        if len(time_parts) < 2: 
            return jsonify({'error': 'Invalid time format. Use HH:MM'}), 400 
            
        try: 
            hours = int(time_parts[0]) 
            minutes = int(time_parts[1]) 
            if hours < 0 or hours > 23 or minutes < 0 or minutes > 59: 
                raise ValueError 
        except ValueError: 
            return jsonify({'error': 'Invalid time values. Hours (0-23) and minutes (0-59)'}), 400 

        # Combine to datetime object 
        try: 
            new_datetime = datetime.strptime(f"{new_date_str} {new_time_str}", '%Y-%m-%d %H:%M') 
        except ValueError: 
            return jsonify({'error': 'Invalid datetime format'}), 400 

        # Check if new datetime is in the past (with 1 minute buffer) 
        if new_datetime < ist_now() - timedelta(minutes=1): 
            return jsonify({'error': 'Cannot set task to past date/time'}), 400 

        # Update task properties 
        task.datetime = new_datetime 
        if 'task' in data: 
            task.task = data['task'].strip() 

        db.session.commit() 
        
        return jsonify({ 
            'id': task.id, 
            'task': task.task, 
            'date': task.datetime.strftime('%Y-%m-%d'), 
            'time': task.datetime.strftime('%H:%M'), 
            'is_done': task.is_done 
        }), 200 
        
    except Exception as e: 
        db.session.rollback() 
        print(f"Error updating task: {str(e)}") 
        return jsonify({'error': 'Failed to update task'}), 500 

#---------------------------------------------Delete task------------------------------------------------------------ 
""" 
API: Delete To-Do Task 
This API allow to child delete task which is not completed 

Role Required: 
- Child 

Path Parameters: 
- task_id (int): The ID of the task to delete. 

Restrictions: 
- Child can not delete task which is completed. 

Response: 
- 200: Task deleted successfully. 
- 403: When child trying to delete a completed task. 
- 404: If the task is not found. 
- 500: Internal server error if deletion fails. 
""" 
@app.route('/todo/<int:task_id>', methods=['DELETE']) 
@jwt_required(required_role='child') 
def delete_todo_task(task_id, current_user_id, current_user_role): 
    # find the task details by task_id and child_id 
    task = ToDoItem.query.filter_by(id=task_id, child_id=current_user_id).first() 
    if not task: 
        return jsonify({'error': 'Task not found'}), 404 
    if task.is_done: 
        return jsonify({'error': 'You can not delete completed task'}), 403 
    try: 
        db.session.delete(task) 
        db.session.commit() 
        update_daily_progress(current_user_id, ist_today()) 
        evaluate_all_badges(current_user_id)
        return jsonify({'message': 'Task deleted successfully'}), 200 
    except Exception as e: 
        db.session.rollback() 
        print("Delete Error:", e) 
        return jsonify({'error': 'Failed to delete task'}), 500 

#-----------------------------------------View task at particular date---------------------------------------------------- 
""" 
API: Get To-Do Tasks by Date 
Fetch all task by taking input of specific date or if child not provided date then fetch the current date task. 

Role Required: 
- Child 

Query Parameters: 
- date (str, optional): Date is parameter in YYYY-MM-DD format and, by default current date. 

Response: 
- 200: When function return list of task in jason format. 
- 400: If the provided date format is invalid. 
""" 
@app.route('/todo', methods=['GET']) 
@jwt_required(required_role='child') 
def tasks_by_date(current_user_id, current_user_role): 
    date_select_str = request.args.get('date') 
    try:  
        selected_date = ( 
            datetime.strptime(date_select_str, "%Y-%m-%d").date() 
            if date_select_str else 
            ist_today() 
        ) 
    except ValueError: 
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400 
        
    # Switched to a more robust date-range filter to avoid DB-specific function issues.
    # This creates a full day range from start to end to query against the datetime column.
    start_of_day_utc = datetime.combine(selected_date, datetime.min.time())
    end_of_day_utc = datetime.combine(selected_date, datetime.max.time())

    tasks = ToDoItem.query.filter(
        ToDoItem.child_id == current_user_id,
        ToDoItem.datetime >= start_of_day_utc,
        ToDoItem.datetime <= end_of_day_utc
    ).all()
    
    task_list = [ 
        { 
            'id': task.id, 
            'task': task.task, 
            'is_done': task.is_done, 
            'date': task.datetime.strftime('%Y-%m-%d'),  
            'time': task.datetime.strftime('%H:%M')
        } for task in tasks 
    ] 
    return jsonify({ 
        'date': selected_date.isoformat(), 
        'tasks': task_list 
    }), 200 

#------------------------------------To Do List status update----------------------------------------------------------- 
""" 
API: Update Task Status 
This API allow the child to mark task completed only current date tasks. 

Role Required: 
- Child 

Path Parameters: 
- task_id (int): ID of the task. 

Restrictions: 
- Child can change status or marked completed only today's task. 
- Child can not change the status of completed task. 

Response: 
- 200: When task marked completed successfully. 
- 400: When the task is already marked as completed. 
- 403: When attempting to change the status of a non-today task. 
- 404: If the task is not found. 
- 500: Internal server error if status update fails. 
""" 
@app.route('/todo/status/<int:task_id>', methods=['PUT']) 
@jwt_required(required_role='child') 
def update_task_status(task_id, current_user_id, current_user_role): 
    task = ToDoItem.query.filter_by(id=task_id, child_id=current_user_id).first() 
    if not task: 
        return jsonify({'error': 'Task not found'}), 404 
        
    # FIX: This now compares the full datetime against the current UTC time.
    # This correctly handles timezone differences and prevents completing a task
    # before its scheduled time (e.g., completing a 2 PM task at 10 AM).

    if task.datetime > ist_now() - timedelta(minutes=1):
        return jsonify({'error': "You cannot complete a task before its scheduled time."}), 403
        
    if task.is_done: 
        return jsonify({'error': 'This task has already been completed'}), 400 
        
    task.is_done = True 
    try: 
        db.session.commit() 
        update_daily_progress(current_user_id, ist_today()) 
        evaluate_all_badges(current_user_id) 
        return jsonify({'message': 'Task Completed successfully'}), 200 
    except Exception as e: 
        db.session.rollback() 
        print("Status update error:", e) 
        return jsonify({'error': 'Failed to update task status'}), 500

    
#----------------------------------Story Generator--------------------------------------------------------------------
"""
API: Generate Daily Story
This api is generate the story and quiz based on given child prompt using story_agent function.
Saves the story and updates the child's progress and streak.
Role Required: Child

Request Body (JSON):
- child_prompt (str, required): A prompt or idea from the child to generate the story.

Response:
- 201: When story generated successfully and saved in databse. Return the story and quiz.
- 400: When prompt is missing.
- 500: When story generation failed.
"""


# ------------------ STORY GENERATION ENDPOINT ------------------
@app.route('/generate_story', methods=['POST'])
@jwt_required(required_role='child')
def create_daily_story(current_user_id, current_user_role):
    data = request.get_json()
    child_prompt = data.get('child_prompt')
    if not child_prompt:
        return jsonify({'error': 'child_prompt is required'}), 400

    try:
        # LLM generation logic
        story_data = generate_story(child_prompt, llm)

        if not isinstance(story_data, dict) or "quiz" not in story_data:
            return jsonify({'error': 'Story generation failed', 'details': story_data}), 500

        options = story_data['quiz'].get('options', [])
        if len(options) < 4:
            return jsonify({'error': 'Quiz options are missing or incomplete'}), 500

        new_story = DailyStory(
            child_id=current_user_id,
            date=date.today(),
            child_prompt=child_prompt,
            title=story_data['title'],
            theme=story_data['theme'],
            content=story_data['content'],
            question=story_data['quiz']['question'],
            option_a=options[0],
            option_b=options[1],
            option_c=options[2],
            option_d=options[3],
            correct_option=story_data['quiz']['answer'],
            is_done=False
        )

        db.session.add(new_story)
        db.session.commit()
        update_daily_progress(current_user_id, date.today())
        evaluate_all_badges(current_user_id)

        return jsonify({
            'message': 'Story generated successfully',
            'story': {
                'title': new_story.title,
                'theme': new_story.theme,
                'content': new_story.content,
                'quiz': {
                    'question': new_story.question,
                    'options': [new_story.option_a, new_story.option_b, new_story.option_c, new_story.option_d],
                    'answer': new_story.correct_option
                }
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Unexpected error occurred', 'details': str(e)}), 500


#----------------------------------Search Stories (NEW)----------------------------------------------------------------
"""
API: Search Stories
This api is to retrieve a list of stories for the logged-in child based on a search query.
Search can be performed by title, theme, or date.
Role Required: Child

Request Query Parameters:
- by (str, required): The field to search by ('title', 'theme', 'date').
- query (str, required): The search term. For date, format should be YYYY-MM-DD.

Response:
- 200: Returns a list of stories matching the criteria.
- 400: When required query parameters are missing or date format is invalid.
- 500: For any other unexpected errors.
"""
# ------------------ SEARCH STORIES ENDPOINT ------------------
@app.route('/stories', methods=['GET'])
@jwt_required(required_role='child')
def search_stories(current_user_id, current_user_role):
    search_by = request.args.get('by')
    query_term = request.args.get('query')

    if not search_by or not query_term:
        return jsonify({'error': 'Missing required query parameters: "by" and "query"'}), 400

    base_query = DailyStory.query.filter_by(child_id=current_user_id)
    
    try:
        if search_by == 'title':
            stories = base_query.filter(DailyStory.title.ilike(f"%{query_term}%")).order_by(DailyStory.date.desc()).all()
        elif search_by == 'theme':
            stories = base_query.filter(DailyStory.theme.ilike(f"%{query_term}%")).order_by(DailyStory.date.desc()).all()
        elif search_by == 'date':
            try:
                search_date = datetime.strptime(query_term, '%Y-%m-%d').date()
                stories = base_query.filter_by(date=search_date).all()
            except ValueError:
                return jsonify({'error': 'Invalid date format. Please use YYYY-MM-DD.'}), 400
        else:
            return jsonify({'error': 'Invalid search field. Use "title", "theme", or "date".'}), 400
    except Exception as e:
        return jsonify({'error': 'An error occurred during search', 'details': str(e)}), 500

    results = []
    for story in stories:
        results.append({
            'id': story.id,
            'title': story.title,
            'theme': story.theme,
            'content': story.content,
            'quiz': {
                'question': story.question,
                'options': [story.option_a, story.option_b, story.option_c, story.option_d],
                'answer': story.correct_option
            }
        })

    return jsonify({'stories': results}), 200


# ------------------ SUBMIT QUIZ ENDPOINT ------------------

@app.route('/submit_quiz', methods=['POST'])
@jwt_required(required_role='child')
def submit_quiz(current_user_id, current_user_role):
    data = request.get_json()
    story_title = data.get('story_title')
    selected_option = data.get('selected_option')

    if not story_title or not selected_option:
        return jsonify({'error': 'Missing required data'}), 400

    story = DailyStory.query.filter_by(
        child_id=current_user_id, 
        title=story_title
    ).order_by(DailyStory.date.desc()).first()

    if not story:
        return jsonify({'error': 'Story not found'}), 404

    is_answer_correct = (selected_option == story.correct_option)

    #  This is the main logic block
    if is_answer_correct:
        # If the answer is correct, set is_done = 1 and save.
        story.is_done = 1
        story.is_correct = 'correct'
        story.submitted_option = selected_option
        
        try:
            db.session.commit()
            update_daily_progress(current_user_id, date.today())
            evaluate_all_badges(current_user_id)
            return jsonify({'is_correct': True, 'message': 'Answer submitted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Database error: ' + str(e)}), 500
    else:
        #  If the answer is wrong, we DO NOT change the database.
        # is_done will remain 0.
        return jsonify({'is_correct': False, 'message': 'Incorrect answer.'}), 200
#------------------------------------------Journal---------------------------------------------------------------
"""
API: Create or Update Daily Journal
This API allow the child to write Journal or update the Journal (text + emoji) if already written in current date. 
After writing the journal api call the mood classifier agent to determine the mood of child and save these.

Role Required: Child

Request Body (JSON):
- text (str, required): Journal entry content written by the child.

Response:
- 200: When the journal is successfully created or updated. Return the mood after determine, Journal, time and marked it done.
- 400: When the journal text is missing in the request body.
- 500: When any error occurs during mood classification or database operations.
"""


# Allows multiple journals per day.
# Keeps each mood + time unique.
# Good for tracking a child's emotions throughout the day.

@app.route('/journal', methods=['POST'])
@jwt_required(required_role='child')
def create_journal(current_user_id, current_user_role):
    data = request.get_json()
    text = data.get('text')
    if not text:
        return jsonify({'error': 'Journal text is required'}), 400

    try:
        mood_dict = classify_emotion(text, llm)
        mood = mood_dict.get("emotion", "unknown")
        now_ist = ist_now()
        entry = JournalEntry(
            child_id=current_user_id,
            date=date.today(),
            text=text,
            mood=mood,
            created_at=now_ist,
            is_done=True
        )

        db.session.add(entry)
        db.session.commit()

        # Optionally update streak and progress
        update_daily_progress(current_user_id, date.today())
        evaluate_all_badges(current_user_id)

        return jsonify({
            'message': 'Journal entry created successfully',
            'mood': mood,
            'journal_text': entry.text
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to process journal entry', 'details': str(e)}), 500

#----------------------------------search Journal---------------------------------------------------------------
@app.route('/journal/search', methods=['GET'])
@jwt_required(required_role='child')
def search_journals(current_user_id, current_user_role):
    date_query = request.args.get('date')
    mood_query = request.args.get('mood')

    filters = [JournalEntry.child_id == current_user_id]
    if date_query:
        filters.append(JournalEntry.date == date.fromisoformat(date_query))
    if mood_query:
        filters.append(JournalEntry.mood == mood_query)

    results = JournalEntry.query.filter(*filters).order_by(JournalEntry.created_at.desc()).all()
    

    entries = [{
        'id': entry.id,
        'date': entry.date.isoformat(),
        'created_at': entry.created_at.strftime("%H:%M:%S"),
        'mood': entry.mood,
        'text': entry.text
    } for entry in results]
    print(entries)

    return jsonify({'entries': entries}), 200

#----------------------------------Infotainment---------------------------------------------------------------
"""
API: Generate Infotainment Content
This API call the function of new agent by taking prompt from child in their interest, and prevent to generating again in same day.

Role Required: Child

Request Body (JSON):
- prompt (str, required): A prompt to generate the content or news.

Response:
- 201: When content was generated then return contend and log ID.
- 200: When child already generated content and tried to generate again in same day then return the existing content and log ID.
- 400: If the prompt is missing in the request body.
- 500: If an error occurs during content generation or database operations.
"""

@app.route('/infotainment/generate', methods=['POST'])
@jwt_required(required_role='child')
def generate_infotainment(current_user_id, current_user_role):
    data = request.get_json()
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400

    try:
        #  Generate AI content using agent
        response = generate_news(prompt, llm)

        now = ist_now()

        #  Store the generated content with time
        log = InfotainmentReadLog(
            child_id=current_user_id,
            child_prompt=prompt,
            content=response,
            date=now.date(),
            time=now.time(),
            is_done=False,
            marked_at=now
        )
        db.session.add(log)
        db.session.commit()

        return jsonify({
            'message': 'New content generated and stored.',
            'content': response,
            'log_id': log.id,
            'date': log.date.strftime('%Y-%m-%d'),
            'time': log.time.strftime('%H:%M:%S')
        }), 201

    except Exception as e:
        db.session.rollback()
        print("Infotainment generation error:", e)
        return jsonify({'error': 'Failed to generate content'}), 500
    
#-----------------------------------Search Infotainment---------------------------------------------------------------
@app.route('/infotainment/search', methods=['GET'])
@jwt_required(required_role='child')
def search_infotainment(current_user_id, current_user_role):
    search_query = request.args.get('q', '').strip().lower()
    search_date = request.args.get('date', '').strip()

    logs = InfotainmentReadLog.query.filter_by(child_id=current_user_id)

    # If user searched by date
    if search_date:
        try:
            search_date_obj = datetime.strptime(search_date, '%Y-%m-%d').date()
            logs = logs.filter(InfotainmentReadLog.date == search_date_obj)
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

    logs = logs.order_by(InfotainmentReadLog.date.desc(), InfotainmentReadLog.marked_at.desc()).all()

    result = []
    for log in logs:
        if not search_query or (
            search_query in log.child_prompt.lower() or
            search_query in (log.content or '').lower()
        ):
            result.append({
                'id': log.id,
                'prompt': log.child_prompt,
                'content': log.content,
                'is_done': log.is_done,
                'date': log.date.strftime('%Y-%m-%d'),
                'marked_at': log.marked_at.isoformat() if log.marked_at else None
            })

    return jsonify({'logs': result}), 200



#---------------------------------------Marked completed--------------------------------------------------------
"""
API: Mark Infotainment Content as Read
This API prevent the child to marked as completed before 3 minutes after generating, and help to marked as completed after 3 minute.

Role Required: Child

Path Parameters:
- log_id (int, required): Paramter is only log ID when infotainment generated.

Response:
- 200: When successfully marked.
- 403: when child attempting to mark a different day's content or before the 3-minute waiting period.
- 404: When the content with the specified log ID is not found for the current child.
- 500: When any error occurred during operation.
"""
@app.route('/infotainment/mark-read/<int:log_id>', methods=['PUT'])
@jwt_required(required_role='child')
def mark_infotainment_read(log_id, current_user_id, current_user_role):
    query = InfotainmentReadLog.query.filter_by(id=log_id, child_id=current_user_id).first()
    if not query:
        return jsonify({'error': 'Content not found'}), 404
    now = ist_now()
    if query.date != now.date():
        return jsonify({'error': 'You can mark only today\'s content'}), 403
    marked_at = query.marked_at
    
    if marked_at.tzinfo is None:
        marked_at = IST.localize(marked_at)
        marked_at_naive = marked_at.replace(tzinfo=None)
    
    elapsed = now - marked_at_naive
    if elapsed.total_seconds() < 180:
        print(f"Elapsed time: {elapsed.total_seconds()} seconds")
        return jsonify({'error': f'You can mark as read after {int(180 - elapsed.total_seconds())} seconds'}), 403
    if query.is_done:
        return jsonify({'message': 'Already marked as read'}), 200
    try:
        query.is_done = True
        query.marked_at = now
        db.session.commit()
        update_daily_progress(current_user_id, now.date())
        evaluate_all_badges(current_user_id)
        return jsonify({'message': 'Marked as read successfully'}), 200
    except Exception as e:
        db.session.rollback()
        print("Error:", e)
        return jsonify({'error': 'Failed to mark as read'}), 500
    
#----------------------------------Calendar Report-------------------------------------------------------------
"""
API: Get Calendar Report
This API is update the daily calender with completed task incomplete task.
Each day is color-coded based on the number of completed task.

Role Required: Child

Query Parameters:
- start_date (str, optional): By default child account creation date but child can enter the date manually
- end_date (str, optional): By default current date but child can enter the date.

Response:
- 200: Return the dictionary with complted task and incompleted task.
- 400: when the date format is invalid.
- 404: when the child/user is not found in the system.

Color Legend:
- "darkest green": All 4 tasks completed
- "medium green": 3 tasks completed
- "light green": 2 tasks completed
- "gray": 1 task completed
- "red": 0 tasks completed
"""
@app.route('/calendar-report', methods=['GET'])
@jwt_required(required_role='child')
def calendar_report(current_user_id, current_user_role):
    start_str = request.args.get('start_date')
    end_str = request.args.get('end_date')

    # find the child detail
    child = Child.query.get(current_user_id)
    user = User.query.get(current_user_id)
    if not child or not user:
        return jsonify({'error': 'User not found'}), 404

    try:
        # determine the start date, By default account created date
        start_date = (
            datetime.strptime(start_str, '%Y-%m-%d').date()
            if start_str else user.created_at.date()
        )
        # determine the end date, By default current date 
        end_date = (
            datetime.strptime(end_str, '%Y-%m-%d').date()
            if end_str else date.today()
        )
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

    if start_date > end_date:
        return jsonify({'error': 'Start date cannot be after end date'}), 400
    color_map = {
        4: "#216e39",    # darkest green
        3: "#7bc96f",    # medium green
        2: "#c6e48b",    # light green
        1: "#ebedf0",    # very light gray
        0: "#f0f0f0"     # almost white
    }
    # Fetch all records
    records = DailyProgress.query.filter(
        DailyProgress.child_id == current_user_id,
        DailyProgress.date >= start_date,
        DailyProgress.date <= end_date
    ).all()
    progress_by_date = {p.date: p for p in records}
    result = {}
    current_day = start_date
    while current_day <= end_date:
        record = progress_by_date.get(current_day)
        not_done = []
        # Check tasks are completed or not
        if not record or not record.is_todo_complete:
            not_done.append("todo")
        if not record or not record.is_journal_done:
            not_done.append("journal")
        if not record or not record.is_story_done:
            not_done.append("story")
        if not record or not record.is_infotainment_done:
            not_done.append("infotainment")
        # Count the total number of task completed
        done_count = 4 - len(not_done)
        # Assign the color according to number of task done.
        if done_count == 0:
            color = "#f0f0f0" # almost white
        elif done_count == 1:
            color = "#ebedf0" # very light gray
        elif done_count == 2:
            color = "#c6e48b" # light green
        elif done_count == 3:
            color = "#7bc96f" # medium green
        else:
            color = "#216e39" # darkest green
        result[current_day.isoformat()] = {
            "status": color,
            "not_done": not_done
        }
        current_day = current_day+timedelta(days=1)

    return jsonify({
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "progress": result
    }), 200

# ---------------------------------- Streak, Badges, and Content Stats ---------------------------------------------
"""
API: Get Streak, Badge, and Activity Summary

Role Required: Child

Description:
This API provides the following details for a logged-in child:
- Current streak and longest streak values.
- List of all awarded badges with name, type, and date.
- Total number of stories completed.
- Total number of journals written.
- Total number of infotainment articles read.

Response:
- 200 OK: On success, returns JSON with streaks, badges, and totals.
- 404 Not Found: If child record is missing.
"""


@app.route('/streak-badges', methods=['GET'])
@jwt_required(required_role='child')
def get_streak_info(current_user_id, current_user_role):
    child = Child.query.get(current_user_id)
    if not child:
        return jsonify({'error': 'Child not found'}), 404

    # Fetch all badges
    badge_awards = BadgeAward.query.filter_by(child_id=current_user_id).all()
    badge_list = [
        {
            'name': badge.badge_name,
            'type': badge.badge_type,
            'awarded_at': badge.awarded_at.strftime('%Y-%m-%d')
        }
        for badge in badge_awards
    ]

    # Count completed content
    total_stories_read = DailyStory.query.filter_by(child_id=current_user_id, is_done=True).count()
    total_journals_written = JournalEntry.query.filter_by(child_id=current_user_id, is_done=True).count()
    total_infotainment_read = InfotainmentReadLog.query.filter_by(child_id=current_user_id, is_done=True).count()

    return jsonify({
        'current_streak': child.streak,
        'longest_streak': child.longest_streak,
        'badges_count': len(badge_list),
        'badges': badge_list,
        'total_stories_read': total_stories_read,
        'total_journals_written': total_journals_written,
        'total_infotainment_read': total_infotainment_read
    }), 200

#-------------------------------------Trigger evaluate badges and streak-----------------------------------------


@app.route('/trigger-badges', methods=['POST'])
@jwt_required(required_role='child')
def trigger_badges(current_user_id, current_user_role):
    evaluate_all_badges(current_user_id)
    return jsonify({'message': 'Badges evaluated successfully'}), 200


#-----------------------------------------------Parent APIs--------------------------------------------------------------------


#---------------------------------------------Fetch all child information-----------------------------------------
"""
API: Get All Children for Parent
This API is fetch the child profile added by parent.

Role Required: Parent

Response:
- 200: When returns the child ID, name, age, gender, current streak, and longest streak.
- 404: When no children are found for the parent.
- 500: When an internal error occurs while retrieving the data.
"""
@app.route('/parent/children', methods=['GET'])
@jwt_required(required_role='parent')
def get_all_children(current_user_id, current_user_role):
    try:
        # Fetch all children which is added by parent
        children = Child.query.filter_by(parent_id=current_user_id).all()
        if not children:
            return jsonify({'message': 'No children found'}), 404
        result = []
        for child in children:
            result.append({
                'id': child.id,
                'name': child.name,
                'age': child.age,
                'gender': child.gender,
                'streak': child.streak,
                'longest_streak': child.longest_streak
            })
        return jsonify({'children': result}), 200
    except Exception as e:
        print("Error fetching children:", e)
        return jsonify({'error': 'Failed to fetch children'}), 500
    
#--------------------------------------Get Individual child profile summary-----------------------------------
"""
API: Get Child Profile Summary
This API is fetch the profile summary of specific child.

Role Required: Parent

Path Parameters:
- child_id (int, required): Profile ID of the child.

Response:
- 200: When return the child ID, name, age, gender, current streak, longest streak, and earned badges.
- 404: when child is not found or does not belong to the authenticated parent.
- 500: When internal error occurs during profile retrieval.
"""

@app.route('/parent/child/<int:child_id>/profile', methods=['GET'])
@jwt_required(required_role='parent')
def get_child_profile_summary(child_id, current_user_id, current_user_role):
    try:
        # find the child
        child = Child.query.filter_by(id=child_id, parent_id=current_user_id).first()
        if not child:
            return jsonify({'error': 'Child not found or unauthorized'}), 404
        profile = {
            'id': child.id,
            'name': child.name,
            'age': child.age,
            'gender': child.gender,
            'streak': child.streak,
            'longest_streak': child.longest_streak,
            'badges': child.badges,
        }
        return jsonify({'profile': profile}), 200
    except Exception as e:
        print("Profile summary error:", e)
        return jsonify({'error': 'Failed to fetch child profile'}), 500
    
#----------------------------------------Child Daily Performance report-------------------------------------------
"""
API: Get Child Daily Performance
This API help in fetch the task done by the child on daily basis. Includes details for To-Do, Journal, Story, and Infotainment tasks.

Role Required: Parent

Path Parameters:
- child_id (int, required): The ID of the child whose performance is being requested.

Query Parameters:
- date (str, required): Date is only query parameter

Response:
- 200: Returns the status of each task (completed or not), total completed count, and a message. If no progress is found, all tasks are marked as incomplete.
- 400: If the date is missing.
- 404: If the child is not found.
"""

@app.route('/parent/child/<int:child_id>/performance', methods=['GET'])
@jwt_required(required_role='parent')
def child_daily_performance(child_id, current_user_id, current_user_role):
    date_str = request.args.get('date')
    if not date_str:
        return jsonify({'error': 'Date required in format YYYY-MM-DD'}), 400
    try:
        selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    # finding the child
    child = Child.query.filter_by(id=child_id, parent_id=current_user_id).first()
    if not child:
        return jsonify({'error': 'Child not found'}), 404
    # Fetch daily progress
    progress = DailyProgress.query.filter_by(child_id=child_id, date=selected_date).first()

    if not progress:
        return jsonify({
            'date': selected_date.isoformat(),
            'todo_completed': False,
            'journal_done': False,
            'story_done': False,
            'infotainment_done': False,
            'total_completed': 0,
            'message': 'No tasks attempted on this date'
        }), 200

    result = {
        'date': selected_date.isoformat(),
        'todo_completed': progress.is_todo_complete,
        'journal_done': progress.is_journal_done,
        'story_done': progress.is_story_done,
        'infotainment_done': progress.is_infotainment_done,
        'total_completed': progress.total_completed,
        'message': 'Report fetched successfully'
    }
    return jsonify(result), 200

#--------------------------------------------Child Calender report fetch by parent------------------------------------
"""
API: Get Child Calendar Report
Provides a full calendar-style task completion report for the selected child.

Role Required: Parent

Path Parameters:
- child_id (int, required): The ID of the child.

Response:
- 200: When returns the completed, not complted task with color.
- 404: If the child is not found.
"""

@app.route('/parent/child/<int:child_id>/calendar-report', methods=['GET'])
@jwt_required(required_role='parent')
def child_calendar_report(child_id, current_user_id, current_user_role):
    # Finding the child
    child = Child.query.filter_by(id=child_id, parent_id=current_user_id).first()
    if not child:
        return jsonify({'error': 'Child not found'}), 404

    user = User.query.get(child.id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Determine the start date and end date
    start_date = user.created_at.date()
    end_date = date.today()
    
    # Find the Daily progress report with parameters: child_id, start date and end date
    progress_logs = DailyProgress.query.filter_by(child_id=child_id)\
        .filter(DailyProgress.date >= start_date, DailyProgress.date <= end_date)\
        .order_by(DailyProgress.date).all()
    
    # create a dictionary to store the completed and not completed tasks
    report = {}
    for i in progress_logs:
        completed = []
        not_completed = []
        if i.is_todo_complete:
            completed.append("todo")
        else:
            not_completed.append("todo")
        if i.is_journal_done:
            completed.append("journal")
        else:
            not_completed.append("journal")
        if i.is_story_done:
            completed.append("story")
        else:
            not_completed.append("story")
        if i.is_infotainment_done:
            completed.append("infotainment")
        else:
            not_completed.append("infotainment")

        report[i.date.isoformat()] = {
            "completed": completed,
            "not_completed": not_completed,
            "total_completed": i.total_completed
        }

    return jsonify({
        "child_id": child_id,
        "calendar_range": {
            "start": start_date.isoformat(),
            "end": end_date.isoformat()
        },
        "report": report
    }), 200


#---------------------------------- Child Mood----------------------------------------------------
"""
API: Get Child Journal Entries
Fetch the child mood by limit the entries.

Role Required: Parent

Path Parameters:
- child_id (int, required): The ID of the child.

Query Parameters:
- limit (int, optional) prevent the vomiting API: The maximum number of recent entries to return. If not provided or 0, returns all entries.

Response:
- 200:  When returns a list of journal entries (ID, date, mood).
- 400: If the 'limit' parameter is not a valid integer.
- 404: If the child is not found or unauthorized for the parent.
"""
@app.route('/parent/child/<int:child_id>/journal-entries', methods=['GET'])
@jwt_required(required_role='parent')
def child_journal_entries(child_id, current_user_id, current_user_role):
    child = Child.query.filter_by(id=child_id, parent_id=current_user_id).first()
    if not child:
        return jsonify({'error': 'Child not found'}), 404
    # Set the Limit Parameter
    try:
        limit = int(request.args.get('limit', 0))
    except ValueError:
        return jsonify({'error': 'Limit must be an integer'}), 400
    query = JournalEntry.query.filter_by(child_id=child_id).order_by(JournalEntry.date.desc())
    if limit > 0:
        journals = query.limit(limit).all()
    else:
        journals = query.all()
    journal_list = [
        {
            "id": j.id,
            "date": j.date.isoformat(),
            "mood": j.mood
        } for j in journals
    ]
    return jsonify({
        "child_id": child_id,
        "journal_entries": journal_list
    }), 200

# ---------------------------------------------journal-by-date-----------------------------------------------------------
"""
    Description:
    Retrieves all journal entries written by a specific child on a given date.
    This includes the mood, timestamp, and full content of each journal entry.
    The endpoint ensures the child belongs to the requesting parent.

    Query Parameters:
    - date (str, required): The target date in YYYY-MM-DD format.

    Path Parameters:
    - child_id (int): The ID of the child whose journal entries should be retrieved.

    Authorization:
    - Requires Bearer JWT token with role = parent.

    Responses:
    - 200 OK: Returns a list of journal entries with id, timestamp, mood, and content.
    - 400 Bad Request: If date is missing or in the wrong format.
    - 404 Not Found: If the child does not belong to the parent.

    """
@app.route('/parent/child/<int:child_id>/journal-by-date', methods=['GET'])
@jwt_required(required_role='parent')
def journal_by_date(child_id, current_user_id, current_user_role):
    date_str = request.args.get('date')
    if not date_str:
        return jsonify({'error': 'Date parameter is required'}), 400

    try:
        target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

    # Verify child belongs to parent
    child = Child.query.filter_by(id=child_id, parent_id=current_user_id).first()
    if not child:
        return jsonify({'error': 'Child not found or unauthorized'}), 404

    entries = JournalEntry.query.filter(
        JournalEntry.child_id == child_id,
        JournalEntry.date == target_date
    ).order_by(JournalEntry.date.asc()).all()

    result = []
    for entry in entries:
        result.append({
            "id": entry.id,
            "timestamp": entry.created_at.strftime("%H:%M:%S"),  # Full timestamp
            "mood": entry.mood,
            "content": entry.text
        })

    return jsonify({"journal_entries": result}), 200



#------------------------------------------Child weekly and monthly report------------------------------------
"""
API: Get Child Weekly or Monthly Summary
This is provides the performance summary of child weekly and monthly. Tracks task completion stats across all four activity types.

Role Required: Parent

Path Parameters:
- child_id (int, required): The ID of the child.

Query Parameters:
- range (str, required): Must be either `weekly` or `monthly` to indicate the time window for the summary.

Response:
- 200: Returns summary data including:
    - total_days: Number of days in the selected period.
    - tasks_assigned: Total number of tasks assigned (4 tasks per day).
    - tasks_completed: Total number of completed tasks.
    - todo_completed_days: Days on which To-Do tasks were completed.
    - journal_done_days: Days with Journal entries.
    - story_done_days: Days with Story completed.
    - infotainment_done_days: Days with Infotainment marked as done.
    - dates: List of per-day completion data.

- 400: If an invalid or missing range parameter is provided.
- 404: If the child is not found.
"""

@app.route('/parent/child/<int:child_id>/summary', methods=['GET'])
@jwt_required(required_role='parent')
def child_summary(child_id, current_user_id, current_user_role):
    # Findnig the child
    child = Child.query.filter_by(id=child_id, parent_id=current_user_id).first()
    if not child:
        return jsonify({'error': 'Child not found or unauthorized'}), 404
    range_type = request.args.get('range')
    if range_type not in ['weekly', 'monthly']:
        return jsonify({'error': 'Invalid range. Use range=weekly or range=monthly'}), 400
    today = date.today()
    if range_type == 'weekly':
        start_date = today - timedelta(days=6)
    else:  
        start_date = today.replace(day=1)
        # Filter the daily progress report by start and end date
    progress_entries = DailyProgress.query.filter(
        DailyProgress.child_id == child_id,
        DailyProgress.date >= start_date,
        DailyProgress.date <= today
    ).order_by(DailyProgress.date).all()
    # Determine the total number of days
    total_days = (today - start_date).days + 1
    # Determine the total assigned task
    total_tasks = total_days * 4
    summary = {
        "total_days": total_days,
        "tasks_assigned": total_tasks,
        "tasks_completed": 0,
        "todo_completed_days": 0,
        "journal_done_days": 0,
        "story_done_days": 0,
        "infotainment_done_days": 0,
        "dates": []
    }
    for entry in progress_entries:
        day_data = {
            "date": entry.date.isoformat(),
            "todo_done": entry.is_todo_complete,
            "journal_done": entry.is_journal_done,
            "story_done": entry.is_story_done,
            "infotainment_done": entry.is_infotainment_done
        }
        # Count the number of completed tasks for the current day
        completed_count = sum([
            entry.is_todo_complete,
            entry.is_journal_done,
            entry.is_story_done,
            entry.is_infotainment_done
        ])
        # Add to total tasks completed across the summary period
        summary["tasks_completed"] += completed_count
        # Update count of days on which each individual task was completed
        if entry.is_todo_complete:
            summary["todo_completed_days"] += 1
        if entry.is_journal_done:
            summary["journal_done_days"] += 1
        if entry.is_story_done:
            summary["story_done_days"] += 1
        if entry.is_infotainment_done:
            summary["infotainment_done_days"] += 1
        # Append the day's completion status to the summary's date-wise breakdown
        summary["dates"].append(day_data)
    return jsonify({
        "child_id": child_id,
        "summary_range": range_type,
        "summary": summary
    }), 200

#--------------------------------------- Report Agent API -----------------------------------------------------------
@app.route('/parent/child-analysis', methods=['POST'])
@jwt_required(required_role='parent')
def generate_child_analysis_report(current_user_id, current_user_role):
    try:
        # Get child_id and range from query params
        child_id = request.args.get("child_id", type=int)
        summary_range = request.args.get("summary_range", default="weekly")

        if not child_id:
            return jsonify({'error': 'child_id is required as query parameter'}), 400
        if summary_range not in ['weekly', 'monthly']:
            return jsonify({'error': 'Invalid summary_range. Use weekly or monthly'}), 400

        # Fetch the child summary (replicating logic from child_summary)
        child = Child.query.filter_by(id=child_id, parent_id=current_user_id).first()
        if not child:
            return jsonify({'error': 'Child not found or unauthorized'}), 404

        today = date.today()
        if summary_range == 'weekly':
            start_date = today - timedelta(days=6)
        else:
            start_date = today.replace(day=1)

        progress_entries = DailyProgress.query.filter(
            DailyProgress.child_id == child_id,
            DailyProgress.date >= start_date,
            DailyProgress.date <= today
        ).order_by(DailyProgress.date).all()

        total_days = (today - start_date).days + 1
        total_tasks = total_days * 4

        summary = {
            "total_days": total_days,
            "tasks_assigned": total_tasks,
            "tasks_completed": 0,
            "todo_completed_days": 0,
            "journal_done_days": 0,
            "story_done_days": 0,
            "infotainment_done_days": 0,
            "entries": []
        }

        for entry in progress_entries:
            day_data = {
                "date": entry.date.isoformat(),
                "todo_done": entry.is_todo_complete,
                "journal_done": entry.is_journal_done,
                "story_done": entry.is_story_done,
                "infotainment_done": entry.is_infotainment_done
            }
            completed_count = sum([
                entry.is_todo_complete,
                entry.is_journal_done,
                entry.is_story_done,
                entry.is_infotainment_done
            ])
            summary["tasks_completed"] += completed_count
            if entry.is_todo_complete:
                summary["todo_completed_days"] += 1
            if entry.is_journal_done:
                summary["journal_done_days"] += 1
            if entry.is_story_done:
                summary["story_done_days"] += 1
            if entry.is_infotainment_done:
                summary["infotainment_done_days"] += 1
            summary["entries"].append(day_data)

        # Prepare input for LLM agent
        agent_input = {
            "child_id": child_id,
            "summary_range": summary_range,
            **summary
        }

        markdown_output = analyze_child_data(agent_input, llm)
        pdf_path = generate_pdf(markdown_output)

        if not os.path.exists(pdf_path):
            return jsonify({'error': 'PDF generation failed'}), 500

        return send_file(
            pdf_path,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='child_analysis_report.pdf'
        )
    except Exception as e:
        print("Report Generation Error:", e)
        return jsonify({'error': 'Failed to generate analysis report'}), 500


# ---------------------------infotainment logs for insights------------------------------------------------
@app.route('/parent/child/<int:child_id>/infotainment-logs', methods=['GET'])
@jwt_required(required_role='parent')
def get_infotainment_logs(child_id, current_user_id, current_user_role):
    # Optional query parameters
    date_str = request.args.get('date')  # for daily logs
    week = request.args.get('week')      # for weekly summary

    # Step 1: Validate Child Ownership
    child = Child.query.filter_by(id=child_id, parent_id=current_user_id).first()
    if not child:
        return jsonify({'error': 'Child not found or unauthorized'}), 404

    # Step 2A: If specific date is provided, show daily logs
    if date_str:
        try:
            selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

        logs = InfotainmentReadLog.query.filter_by(child_id=child_id, date=selected_date).all()
        result = [{
            'id': log.id,
            'child_prompt': log.child_prompt,
            'content': log.content,
            'is_done': log.is_done,
            'marked_at': log.marked_at.isoformat(),
            'time': log.time.isoformat(),
            'date': log.date.isoformat()
            
        } for log in logs]

        return jsonify({
            'date': selected_date.isoformat(),
            'total_read': len(result),
            'logs': result
        }), 200

    # Step 2B: If `week=true`, return weekly grouped stats
    if week == 'true':
        today = datetime.utcnow().date()
        week_start = today - timedelta(days=today.weekday())  # Monday
        week_end = week_start + timedelta(days=6)             # Sunday

        weekly_logs = db.session.query(
            InfotainmentReadLog.date,
            func.count(InfotainmentReadLog.id).label('topics_read')
        ).filter(
            InfotainmentReadLog.child_id == child_id,
            InfotainmentReadLog.date >= week_start,
            InfotainmentReadLog.date <= week_end,
            InfotainmentReadLog.is_done == True
        ).group_by(InfotainmentReadLog.date).all()

        # Format response
        result = [{
            'date': log.date.isoformat(),
            'topics_read': log.topics_read
        } for log in weekly_logs]

        return jsonify({
            'week_start': week_start.isoformat(),
            'week_end': week_end.isoformat(),
            'weekly_summary': result
        }), 200

    # Step 2C: If no date or week is given, return last 7 entries
    recent_logs = InfotainmentReadLog.query.filter_by(child_id=child_id)\
                    .order_by(InfotainmentReadLog.date.desc())\
                    .limit(7).all()

    result = [{
        'date': log.date.isoformat(),
        'child_prompt': log.child_prompt,
        'is_done': log.is_done,
        'marked_at': log.marked_at.isoformat()
    } for log in recent_logs]

    return jsonify({
        'recent_logs': result
    }), 200



# ---------------------------Story logs for insights------------------------------------------------
@app.route('/parent/child/<int:child_id>/story-logs', methods=['GET'])
@jwt_required(required_role='parent')
def get_story_logs(child_id, current_user_id, current_user_role):
    # Optional query parameters
    date_str = request.args.get('date')  # for daily logs
    week = request.args.get('week')      # for weekly summary

    # Step 1: Validate Child Ownership
    child = Child.query.filter_by(id=child_id, parent_id=current_user_id).first()
    if not child:
        return jsonify({'error': 'Child not found or unauthorized'}), 404

    # Step 2A: If specific date is provided, show daily logs
    if date_str:
        try:
            selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

        logs = DailyStory.query.filter_by(child_id=child_id, date=selected_date).all()
        result = [{
            'id': log.id,
            'child_prompt': log.child_prompt,
            'title': log.title,
            'theme': log.theme,
            'content': log.content,
            'question': log.question,
            'option_a': log.option_a,
            'option_b': log.option_b,
            'option_c': log.option_c,
            'option_d': log.option_d,
            'correct_option': log.correct_option,
            'submitted_option': log.submitted_option,
            'is_done': log.is_done,
            'date': log.date.isoformat()
        } for log in logs]

        return jsonify({
            'date': selected_date.isoformat(),
            'total_read': len(result),
            'logs': result
        }), 200

    # Step 2B: If `week=true`, return weekly grouped stats
    if week == 'true':
        today = datetime.utcnow().date()
        week_start = today - timedelta(days=today.weekday())  # Monday
        week_end = week_start + timedelta(days=6)             # Sunday

        weekly_logs = db.session.query(
            DailyStory.date,
            func.count(DailyStory.id).label('stories_read')
        ).filter(
            DailyStory.child_id == child_id,
            DailyStory.date >= week_start,
            DailyStory.date <= week_end,
            DailyStory.is_done == True
        ).group_by(DailyStory.date).all()

        result = [{
            'date': log.date.isoformat(),
            'stories_read': log.stories_read
        } for log in weekly_logs]

        return jsonify({
            'week_start': week_start.isoformat(),
            'week_end': week_end.isoformat(),
            'weekly_summary': result
        }), 200

    # Step 2C: If no date or week is given, return last 7 entries
    recent_logs = DailyStory.query.filter_by(child_id=child_id)\
                    .order_by(DailyStory.date.desc())\
                    .limit(7).all()

    result = [{
        'date': log.date.isoformat(),
        'child_prompt': log.child_prompt,
        'title': log.title,
        'theme': log.theme,
        'is_done': log.is_done
    } for log in recent_logs]

    return jsonify({
        'recent_logs': result
    }), 200
