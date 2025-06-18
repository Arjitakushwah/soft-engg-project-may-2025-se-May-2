from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from config import Config
from models import db, User, Parent, Child
from flask_migrate import Migrate


# Initialize Flask app
app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config)

# Initialize database
db.init_app(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)

@app.route('/')
def home():
    return 'Hello Everyone'

#--------------------------------------------Parent SignUP----------------------------------------
@app.route('/register', methods=['POST'])
def register_parent():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')

    if not all([email, password, name]):
        return jsonify({'error': 'Email, password, and name are required'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'User already exists'}), 400

    hashed_pw = generate_password_hash(password)
    user = User(email=email, password=hashed_pw, role='parent')
    db.session.add(user)
    db.session.flush()

    parent = Parent(id=user.id, name=name)
    db.session.add(parent)
    db.session.commit()

    return jsonify({'message': 'Parent registered successfully'})

#------------------------------------User Login---------------------------------------------------------
@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"error": "Request content type must be application/json"}), 415
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        identity = {
            "id": user.id,
            "role": user.role
        }

        # Generate access token
        access_token = create_access_token(identity=identity)

        # Return the response based on the role
        return jsonify({
            "message": "Login successful",
            "access_token": access_token,
            "role": user.role
        }), 200
    else:
        return jsonify({"error": "Invalid email or password"}), 401

    
@app.route('/x', methods=['GET'])
@jwt_required()
def x():
    return jsonify(get_jwt_identity())


#------------------------------ Add Child-----------------------------------------------------

@app.route('/add-child', methods=['POST'])
@jwt_required()
def add_child():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    age = data.get('age')

    current_user = get_jwt_identity()

    if current_user['role'] != 'parent':
        return jsonify({'error': 'Only parents can add children'}), 403

    if not all([email, password, name, age]):
        return jsonify({'error': 'All fields are required'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Child already exists'}), 409

    try:
        hashed_pw = generate_password_hash(password)
        user = User(email=email, password=hashed_pw, role='child')
        db.session.add(user)
        db.session.flush()
        child = Child(
            id=user.id,
            parent_id=current_user['id'],
            name=name,
            age=age,
            streak=0,
            badges=0
        )
        db.session.add(child)
        db.session.commit()

        return jsonify({'message': f'Child {name} added successfully.'}), 201

    except Exception as e:
        db.session.rollback()
        print("Error:", e)
        return jsonify({'error': 'Something went wrong. Please check logs.'}), 500




if __name__ == '__main__':
    app.run(debug=True)
