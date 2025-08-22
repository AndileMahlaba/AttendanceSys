import datetime
from flask import Blueprint, request, jsonify
from ..models import User, Student
from ..utils.security import generate_token, token_required
import json

auth_bp = Blueprint('auth', __name__)

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return super().default(obj)

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        print(f"Login attempt: email={email}, password={password}")

        if not email or not password:
            return jsonify({'error': 'Email and password required'}), 400

        user = User.find_by_email(email)
        print(f"User found: {user}")

        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401

        print(f"Stored hash: {user['password_hash']}, Provided password: {password}")
        
        if not User.verify_password(user['password_hash'], password):
            return jsonify({'error': 'Invalid credentials'}), 401

        if not user['is_active']:
            return jsonify({'error': 'Account is deactivated'}), 401

        # Make sure we cast ID to str or int, not None
        if not user['id']:
            return jsonify({'error': 'User has no ID in DB'}), 500

        token = generate_token(str(user['id']))
        
        return jsonify({
            "id": user["id"],
            "email": user["email"],
            "first_name": user["first_name"],
            "last_name": user["last_name"],
            "role": user["role"],
            "token": token
        }), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        role = data.get('role', 'student')

        if not all([email, password, first_name, last_name]):
            return jsonify({'error': 'All fields are required'}), 400

        if User.find_by_email(email):
            return jsonify({'error': 'User already exists'}), 409

        user_id = User.create(email, password, first_name, last_name, role)
        
        if role == 'student':
            student_id = f"ST{user_id:04d}"
            Student.create(user_id, student_id)

        token = generate_token(str(user_id))
        return jsonify({
            'token': token,
            'message': 'User created successfully'
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/profile', methods=['GET'])
@token_required
def get_profile(user_id):   # token_required should inject user_id
    user = User.find_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    user_data = {
        'id': user['id'],
        'email': user['email'],
        'first_name': user['first_name'],
        'last_name': user['last_name'],
        'role': user['role']
    }
    return jsonify(user_data)
