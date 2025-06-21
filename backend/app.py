from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity
from config import Config
from models import db, User, Parent, Child
from flask_migrate import Migrate
from utils import jwt_required


# Initialize Flask app
app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config)


# Initialize database
db.init_app(app)
JWTManager(app)
migrate = Migrate(app, db)


@app.route('/')
def home():
    return 'Hello Everyone'
#--------------------------------------------Check Username----------------------------------------------------

@app.route('/check-username', methods=['GET'])
def check_username():
    username = request.args.get('username')
    if not username:
        return jsonify({'error': 'Username is required'}), 400

    exists = User.query.filter_by(username=username).first() is not None
    return jsonify({'available': not exists})

#--------------------------------------------Parent SignUP-------------------------------------------------------
@app.route('/register', methods=['POST'])
def register_parent():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    username = data.get('username')
    if not all([email, password, name, username]):
        return jsonify({'error': 'Email, password, name, and username are required'}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists'}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already taken'}), 400
    try:
        hashed_pw = generate_password_hash(password)
        user = User(email=email, username=username, password=hashed_pw, role='parent')
        db.session.add(user)
        db.session.flush()
        parent = Parent(id=user.id, name=name)
        db.session.add(parent)
        db.session.commit()
        return jsonify({'message': 'Parent registered successfully'}), 201
    except Exception as e:
        db.session.rollback()
        print("Error:", e)
        return jsonify({'error': 'Something went wrong'}), 500

#------------------------------------User Login---------------------------------------------------------
@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"error": "Request content type must be application/json"}), 415

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={"role": user.role}
        )
        if user.role == 'parent':
            dashboard_route = '/parent_dashboard'
        elif user.role == 'child':
            dashboard_route = '/child_dashboard'
        else:
            dashboard_route = '/'

        return jsonify({
            "message": "Login successful",
            "access_token": access_token,
            "role": user.role,
            "redirect_to": dashboard_route
        }), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401

#------------------------------ Add Child-----------------------------------------------------

@app.route('/add-child', methods=['POST'])
@jwt_required(required_role='parent')
def add_child(current_user_id, current_user_role):
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    name = data.get('name')
    age = data.get('age')
    gender = data.get('gender')
    if not all([username, password, name, age]):
        return jsonify({'error': 'All fields (username, password, name, age) are required.'}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already taken'}), 409
    try:
        parent = User.query.get(current_user_id)
        if not parent:
            return jsonify({'error': 'Parent not found'}), 404
        hashed_pw = generate_password_hash(password)
        user = User(
            email=parent.email,
            username=username,
            password=hashed_pw,
            role='child'
        )
        db.session.add(user)
        db.session.flush()
        child = Child(
            id=user.id,
            parent_id=current_user_id,
            name=name,
            age=int(age),
            gender = gender,
            streak=0,
            badges=0
        )
        db.session.add(child)
        db.session.commit()
        return jsonify({'message': 'Child added successfully'}), 201
    except Exception as e:
        db.session.rollback()
        print("Error:", e)
        return jsonify({'error': 'SOmething wrong'}), 500
    
from api import *



if __name__ == '__main__':
    app.run(debug=True)
