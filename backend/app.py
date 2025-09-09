from flask import Flask, jsonify, request, url_for, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, get_jwt
from config import Config
from models import db, User, Parent, Child
from flask_migrate import Migrate
from utils import jwt_required
from flask_cors import CORS
from send_email import verify_otp, store_otp, verified_emails, send_welcome_email, send_mail_username, send_child_credentials_email, verify_otp_username, verified_usernames, resend_otp, resend_child_otp, store_child_otp
import os
from google_auth_oauthlib.flow import Flow
import requests

# Initialize Flask app
app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config)
CORS(app)

jwt_blacklist = set()
# Initialize database
db.init_app(app)
x=JWTManager(app)
migrate = Migrate(app, db)

@x.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    return jwt_payload["jti"] in jwt_blacklist



@app.route('/')
def home():
    return 'Hello Everyone'
#------------------------------------------------- Google Auth Setup -------------------------------------------------
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
REDIRECT_URI = "http://localhost:5000/auth/google/callback" 

# Required for local development to use HTTP instead of HTTPS
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

@app.route('/auth/google/login')
def login_with_google():
    flow = Flow.from_client_secrets_file(
        'client_secret.json',
        scopes=['https://www.googleapis.com/auth/userinfo.email', 'openid'],
        redirect_uri=url_for('handle_callback', _external=True)
    )
    print("Redirect URI:", url_for('handle_callback', _external=True))
    auth_url, _ = flow.authorization_url(prompt='consent')
    return redirect(auth_url)

@app.route('/auth/google/callback')
def handle_callback():
    flow = Flow.from_client_secrets_file(
        'client_secret.json',
        scopes=['https://www.googleapis.com/auth/userinfo.email', 'openid'],
        redirect_uri=url_for('handle_callback', _external=True)
    )
    flow.fetch_token(authorization_response=request.url)

    credentials = flow.credentials
    response = requests.get(
        'https://www.googleapis.com/oauth2/v3/userinfo',
        headers={'Authorization': f'Bearer {credentials.token}'}
    )
    if not response.ok:
        return jsonify({'error': 'Failed to fetch user info from Google'}), 400
    user_info = response.json()
    email = user_info.get('email')
    if not email:
        return jsonify({'error': 'Unable to fetch email from Google'}), 400
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(email=email, role='parent')
        db.session.add(user)
        db.session.flush()
        parent=Parent(id=user.id)
        db.session.add(parent)
        db.session.commit()
        send_welcome_email(email, user.id)
    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role}
    )
    frontend_callback_url = (
    f"https://soft-engg-project-may-2025-se-may-2-3.onrender.com/auth/google/callback"  # Use your Vue app's address
    f"?token={access_token}&role={user.role}&username={user.username}"
)
    return redirect(frontend_callback_url)

#--------------------------------------------Check Username----------------------------------------------------

@app.route('/check-username', methods=['GET'])
def check_username():
    username = request.args.get('username')
    if not username:
        return jsonify({'error': 'Username is required'}), 400
    exists = User.query.filter_by(username=username).first() is not None
    return jsonify({'available': not exists})

#--------------------------------------------Parent SignUP-------------------------------------------------------
@app.route('/register/send-otp', methods=['POST'])
def register_send_otp():
    data = request.get_json()
    email = data.get("email")
    if not email:
        return jsonify({"error": "Email is required"}), 400
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "Email already registered"}), 409
    if store_otp(email):
        return jsonify({"message": "OTP sent to email"}), 200
    else:
        return jsonify({"error": "Failed to send OTP"}), 500

@app.route('/register/verify-otp', methods=['POST'])
def register_verify_otp():
    data = request.get_json()
    email = data.get("email")
    otp = data.get("otp")
    if not email or not otp:
        return jsonify({"error": "Email and OTP are required"}), 400
    success, message = verify_otp(email, otp)
    if success:
        return jsonify({"message": message}), 200
    else:
        return jsonify({"error": message}), 400

@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")
    if not all([username, name, email, password]):
        return jsonify({"error": "Missing required fields"}), 400
    if email not in verified_emails:
        return jsonify({"error": "OTP verification required"}), 401
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 409
    
    try:
        hashed_password = generate_password_hash(password)
        new_user = User(
        email=email,
        username=username,
        password=hashed_password,
        role="parent")
        db.session.add(new_user)
        db.session.flush()
        parent = Parent(
            id=new_user.id,
            name=name)
        db.session.add(parent)
        db.session.commit()
        verified_emails.remove(email)
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        db.session.rollback()
        print("Error:", e)
        return jsonify({'error': 'SOmething wrong'}), 500


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
            '/parent/home' if user.role == 'parent' else
            '/child/home' if user.role == 'child' else
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
    
@app.route('/auth/google_login')
def google_login():
    return login_with_google()
@app.route('/auth/callback')
def callback():
    return handle_callback()

#------------------------------------Forgot Username-----------------------------------------
@app.route('/forgot-username', methods=['POST'])
def forgot_username():
    data = request.get_json()
    email = data.get('email')
    if not email:
        return jsonify({"status": "error", "message": "Email is required"}), 400
    user = User.query.filter_by(email=email).first()
    if user:
        send_mail_username(email, user.username)    
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
    print(email)

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

#------------------------------------------- Update Parent Profile-------------------------------------------------
# Make sure you have this import for password hashing if it's not already in your file
from werkzeug.security import generate_password_hash

# Your other imports like Flask, jsonify, request, db, models (User, Parent), etc.

@app.route('/parent/update-profile', methods=['PUT'])
@jwt_required(required_role='parent')
def update_parent_profile(current_user_id, current_user_role):
    data = request.json
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    user = User.query.get(current_user_id)
    parent = Parent.query.get(current_user_id)
    if not user or not parent:
        return jsonify({"error": "User not found"}), 404

    # --- Start of updated logic ---

    try:
        # Get potential new data from the request
        name = data.get("name")
        new_username = data.get("username")
        new_password = data.get("password")

        # 1. Handle username update
        if new_username:
            # Check if a username is already set. If yes, it cannot be changed.
            if user.username:
                return jsonify({"error": "Username is already set and cannot be changed."}), 400
            
            # If not set, validate that the new username isn't already taken
            if User.query.filter_by(username=new_username).first():
                return jsonify({"error": "Username is already taken. Please choose another."}), 409 # 409 Conflict
            
            user.username = new_username

        # 2. Handle password update
        if new_password:
            # Check if a password hash already exists. If yes, it cannot be changed here.
            # Assumes your password field is named 'password_hash'. Adjust if it's different (e.g., 'password').
            if user.password: 
                return jsonify({"error": "Password is already set and cannot be changed."}), 400
            
            # Securely hash the new password before storing it
            user.password = generate_password_hash(new_password)

        # 3. Handle name update (this logic remains the same)
        if name is not None:
            parent.name = name

        db.session.commit()
        
        return jsonify({
            "message": "Parent profile updated successfully",
            "parent": {
                "id": parent.id,
                "name": parent.name,
                "username": user.username # Also return the newly set username
            }
        }), 200
    
    # --- End of updated logic ---
    
    except Exception as e:
        db.session.rollback()
        print("Parent Profile Update Error:", e) # Using print for logging in development
        return jsonify({"error": "Failed to update profile"}), 500
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
        send_child_credentials_email(username, password, name, parent.email)
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
        'username': user.username, 
        'age': child.age,
        'gender' :child.gender,
    })

#----------------------------------- Update Child Profile------------------------------------------------
@app.route('/child/profile/update', methods=['PUT'])
@jwt_required(required_role='child')
def update_child_profile(current_user_id, current_user_role):
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Missing JSON body'}), 400
        name = data.get('name')
        age = data.get('age')
        gender = data.get('gender')
        child = Child.query.filter_by(id=current_user_id).first()
        user = User.query.filter_by(id=current_user_id).first()
        if not user:
            return jsonify({'error': 'User record not found'}), 404
        if not child:
            return jsonify({'error': 'Child not found'}), 404
        if name is not None:
            child.name = name
        if age is not None:
            child.age = age
        if gender is not None:
            child.gender = gender
        db.session.commit()
        return jsonify({
            'message': 'Profile updated successfully',
            'child': {
                'id': child.id,
                'name': child.name,
                'age': child.age,
                'gender': child.gender
            }
        }), 200
    except Exception as e:
        print("Profile Update Error:", e)
        return jsonify({'error': 'Failed to update profile'}), 500

@app.route('/parent/child/profile/update', methods=['PUT'])
@jwt_required(required_role='parent')
def parent_update_child_profile(current_user_id, current_user_role):
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Missing JSON body'}), 400
        # Parent must specify which child to update
        child_id = data.get("child_id")  
        if not child_id:
            return jsonify({'error': 'Child ID required'}), 400
        name = data.get('name')
        age = data.get('age')
        gender = data.get('gender')
        child = Child.query.filter_by(id=child_id, parent_id=current_user_id).first()
        if not child:
            return jsonify({'error': 'Child not found or does not belong to parent'}), 404

        if name is not None:
            child.name = name
        if age is not None:
            child.age = age
        if gender is not None:
            child.gender = gender
        db.session.commit()
        return jsonify({
            'message': 'Child profile updated successfully',
            'child': {
                'id': child.id,
                'name': child.name,
                'age': child.age,
                'gender': child.gender
            }
        }), 200
    except Exception as e:
        print("Profile Update Error:", e)
        return jsonify({'error': 'Failed to update profile'}), 500


#-------------------------- Forgot Child Password ---------------------------------------------------------
@app.route('/forgot-password-child', methods=['POST'])
def send_otp_child():
    data = request.get_json()
    username = data.get("username")
    if not username:
        return jsonify({"error": "Username required"}), 400
    sent = store_child_otp(username) 
    if sent:
        return jsonify({
            "message": "OTP sent to registered parent email for child"
        }), 200
    return jsonify({"error": "Failed to send OTP"}), 500

@app.route('/verify-otp-child', methods=['POST'])
def verify_otp_child():
    data = request.get_json()
    username = data.get("username")
    otp = data.get("otp")
    if not username or not otp:
        return jsonify({"error": "Username and OTP required"}), 400
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    success, message = verify_otp_username(username, otp)
    return jsonify({"success": success, "message": message}), (200 if success else 400)

@app.route('/set-password-child', methods=['POST'])
def set_password_child():
    data = request.get_json()
    username = data.get('username')
    new_password = data.get('new_password')
    if not username or not new_password:
        return jsonify({'error': 'Username and password required'}), 400
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    if username not in verified_usernames:
        return jsonify({'error': 'OTP verification required'}), 401
    hashed_password = generate_password_hash(new_password)
    user.password = hashed_password
    db.session.commit()
    verified_usernames.remove(username)
    return jsonify({'message': f"Password reset successfully for child {username}"}), 200

#---------------------------------------------Resend OTP for child and parent -----------------------------
@app.route("/resend-otp", methods=["POST"])
def resend_parent_otp():
    data = request.json
    email = data.get("email")
    if not email:
        return jsonify({"error": "Email is required"}), 400
    if resend_otp(email):
        return jsonify({"message": "OTP resent successfully"}), 200
    return jsonify({"error": "Failed to resend OTP"}), 500

@app.route("/resend-child-otp", methods=["POST"])
def resend_child_otp_route():
    data = request.json
    username = data.get("username")
    if not username:
        return jsonify({"error": "Username is required"}), 400
    if resend_child_otp(username):
        return jsonify({"message": "Child OTP resent successfully"}), 200
    return jsonify({"error": "Failed to resend OTP"}), 500

#--------------------------------------------------Logout---------------------------------------------------
@app.route('/logout', methods=['POST'])
@jwt_required()
def logout(current_user_id, current_user_role):
    try:
        claims = get_jwt()
        jti = claims.get("jti")
        if not jti:
            return jsonify({"error": "Token does not have jti"}), 400

        jwt_blacklist.add(jti)
        return jsonify({"message": "Logout successful"}), 200

    except Exception as e:
        return jsonify({"error": "Logout failed", "details": str(e)}), 500

# import all api here to prevent the cicular import
    
from api import *



if __name__ == '__main__':
    app.run(debug=True)
