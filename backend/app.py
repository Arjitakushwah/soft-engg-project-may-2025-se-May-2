from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity
from config import Config
from models import db, User, Parent, Child
from flask_migrate import Migrate
from utils import jwt_required
from flask_cors import CORS
from otp import verify_otp, store_otp, verified_emails


# Initialize Flask app
app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config)
CORS(app)

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

        
        dashboard_route = (
            '/parent_dashboard' if user.role == 'parent' else
            '/child_dashboard' if user.role == 'child' else
            '/'
        )

        return jsonify({
            "message": "Login successful",
            "access_token": access_token,
            "role": user.role,
            "redirect_to": dashboard_route
        }), 200
    else:
        return jsonify({"error": "Invalid username, password, or role"}), 401

#------------------------------------Forgot Username-----------------------------------------
@app.route('/forgot-username', methods=['POST'])
def forgot_username():
    data = request.get_json()
    email = data.get('email')
    if not email:
        return jsonify({"status": "error", "message": "Email is required"}), 400
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({
            "status": "success",
            "username": user.username
        }), 200
    else:
        return jsonify({
            "status": "error",
            "message": "User with this email not found"
        }), 404
    
#-------------------------------------Forgot Password----------------------------------------------------------------
@app.route('/forgot-password', methods=['POST'])
def send_otp():
    data = request.get_json()
    email = data.get("email")

    if store_otp(email):
        return jsonify({"message": "OTP sent to email"}), 200
    return jsonify({"error": "Failed to send OTP"}), 500


@app.route('/verify-otp', methods=['POST'])
def verify_otp_route():
    data = request.get_json()
    email = data.get("email")
    otp = data.get("otp")

    success, message = verify_otp(email, otp)
    return jsonify({"success": success, "message": message}), (200 if success else 400)

@app.route('/set-password', methods=['POST'])
def set_new_password():
    data = request.get_json()
    email = data.get('email')
    new_password = data.get('new_password')

    if not email or not new_password:
        return jsonify({'error': 'Email and password required'}), 400

    if email not in verified_emails:
        return jsonify({'error': 'OTP verification required'}), 401

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    hashed_password = generate_password_hash(new_password)
    user.password = hashed_password
    db.session.commit()

    verified_emails.remove(email)

    return jsonify({'message': 'Password reset successfully'}), 200


#------------------------------ Add Child-----------------------------------------------------------------------------

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

#------------------------------------Get Parent Info---------------------------------------------------------
@app.route('/parent_dashboard', methods=['GET'])
@jwt_required(required_role='parent')
def get_parent_info(current_user_id, current_user_role):
    parent = Parent.query.get(current_user_id)
    user = User.query.get(current_user_id)
    if not parent or not user:
        return jsonify({'error': 'Parent not found'}), 404
    return jsonify({'name': parent.name, 'username': user.username})

#------------------------------------Get Child Info---------------------------------------------------------
@app.route('/child_dashboard', methods=['GET'])
@jwt_required(required_role='child')
def get_child_info(current_user_id, current_user_role):
    child = Child.query.get(current_user_id)
    if not child:
        return jsonify({'error': 'Child not found'}), 404

    user = User.query.get(current_user_id)  # get username from User table

    return jsonify({
        'name': child.name,
        'username': user.username,  #
    })



    
from api import *



if __name__ == '__main__':
    app.run(debug=True)
