from datetime import datetime, date
from utils import jwt_required
from flask import request, jsonify
from models import db, ToDoItem, User
from app import app
from pytz import timezone

# Use for return current date and time according to user local timezone
def ist_today():
    return datetime.now(timezone("Asia/Kolkata")).date()


#------------------------------------To DO List task creation----------------------------------------------------
"""
API: Create To-Do Task
This API allows child to create task for specific date

Role Required:
- Child

Request Body (JSON):
- task (str): Accept the task description from child.
- date (str): The date for which the task is created in YYYY-MM-DD format. (Required)

Response:
- 201: Task created successfully.
- 400: If task or date is missing, the date is in the past, or the format is invalid.
- 500: Internal server error if task creation fails.
"""
@app.route('/todo', methods=['POST'])
@jwt_required(required_role='child') 
def create_todo_task(current_user_id, current_user_role):
    data = request.get_json()
    task = data.get('task')
    date_str = data.get('date') 
    if not task or not date_str:
        return jsonify({'error': 'Task and date are required'}), 400
    try:
        #Convert the date from string to date format YYYY-MM-DD
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        today = ist_today()
        # Checking if the selected date is past date.
        if selected_date < today:
            return jsonify({'error': 'Cannot create tasks for past dates'}), 400
        new_task = ToDoItem(
            child_id=current_user_id, 
            date=selected_date,
            task=task,
            is_done=False
        )
        db.session.add(new_task)
        db.session.commit()
        return jsonify({'message': 'Task created successfully'}), 201
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    except Exception as e:
        db.session.rollback()
        print("Error:", e)
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
@app.route('/todo/<int:task_id>', methods=['PUT'])
@jwt_required(required_role='child')
def update_todo_task(task_id, current_user_id, current_user_role):
    data = request.get_json()
    task = ToDoItem.query.filter_by(id=task_id, child_id=current_user_id).first()
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    child_user = User.query.get(current_user_id)
    if not child_user:
        return jsonify({'error': 'User not found'}), 404
    if task.is_done:
        return jsonify({'error': 'You can not update a completed tas'}), 403
    if 'is_done' in data:
        return jsonify({'error': 'You can not change staus of the task'}), 400
    if 'date' in data:
        try:
            # Converting date from string to date format YYYY-MM-DD
            new_date = datetime.strptime(data['date'], "%Y-%m-%d").date()
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        # Checking if the selected date is past date or before of child account creation
        if new_date < child_user.created_at.date() or new_date < ist_today():
            return jsonify({'error': 'Date must be today or future'}), 400
        task.date = new_date
    if 'task' in data:
        task.task = data['task']
    try:
        db.session.commit()
        return jsonify({'message': 'Task updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        print("Update error:", e)
        return jsonify({'error': 'Update failed'}), 500
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
    date_select = request.args.get('date')
    try: 
        # If child provide date then convert str to YYYY-MM-DD format otherwise select the current date
        selected_date = (
            datetime.strptime(date_select, "%Y-%m-%d").date()
            if date_select else
            datetime.today().date()
        )
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    # Find tasks by child_id and selected_date
    tasks = ToDoItem.query.filter_by(child_id=current_user_id, date=selected_date).all()
    task_list = [
        {
            'id': task.id,
            'task': task.task,
            'is_done': task.is_done,
            'date': task.date.isoformat()
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
    today = date.today()
    task = ToDoItem.query.filter_by(id=task_id, child_id=current_user_id).first()
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    if task.date != today:
        return jsonify({'error': 'You can change the status of only today\'s tasks'}), 403
    if task.is_done:
        return jsonify({'error': 'You already completed it'}), 400
    task.is_done = True
    try:
        db.session.commit()
        return jsonify({'message': 'Task Completed successfully'}), 200
    except Exception as e:
        db.session.rollback()
        print("Status update error:", e)
        return jsonify({'error': 'Failed to update task status'}), 500




