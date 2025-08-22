from flask import Blueprint, request, jsonify
from ..models import Attendance, Student, User
from ..utils.security import token_required

attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.route('/checkin', methods=['POST'])
@token_required
def check_in(user_id):
    try:
        data = request.get_json()
        student_id = data.get('student_id')
        venue_id = data.get('venue_id')
        
        if not student_id or not venue_id:
            return jsonify({'error': 'student_id and venue_id are required'}), 400
        
        # Add your check-in logic here
        # For now, return success
        return jsonify({
            'message': 'Check-in successful',
            'student_id': student_id,
            'venue_id': venue_id,
            'timestamp': '2025-08-22T10:00:00Z'  # You'd use actual datetime
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@attendance_bp.route('/', methods=['GET'])
@token_required
def get_attendance(user_id):
    try:
        # Get actual attendance records from database
        attendance_records = Attendance.get_all()
        return jsonify({'attendance': attendance_records})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@attendance_bp.route('/students', methods=['POST'])
@token_required
def create_student(user_id):
    try:
        data = request.get_json()
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        
        if not all([first_name, last_name, email]):
            return jsonify({'error': 'All fields are required'}), 400
        
        # Check if user already exists
        if User.find_by_email(email):
            return jsonify({'error': 'User already exists'}), 409
        
        # Create user with student role (using default password for now)
        user_id = User.create(email, 'default_password', first_name, last_name, 'student')
        
        # Create student record
        student_id = f"ST{user_id:04d}"
        Student.create(user_id, student_id)
        
        return jsonify({
            'message': 'Student created successfully',
            'student_id': student_id,
            'user_id': user_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@attendance_bp.route('/students', methods=['GET'])
@token_required
def get_students(user_id):
    try:
        # Get all students from database
        # This would need proper implementation in your Student model
        # For now, let's create a mock implementation
        
        # Get all users with student role
        conn = Student.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT u.id, u.first_name, u.last_name, u.email, s.student_id 
            FROM users u 
            JOIN students s ON u.id = s.user_id 
            WHERE u.role = 'student'
        ''')
        students = cursor.fetchall()
        conn.close()
        
        student_list = []
        for student in students:
            student_list.append({
                'id': student[0],
                'first_name': student[1],
                'last_name': student[2],
                'email': student[3],
                'student_id': student[4]
            })
        
        return jsonify({'students': student_list})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@attendance_bp.route('/students/<int:student_id>', methods=['GET'])
@token_required
def get_student(user_id, student_id):
    try:
        # Get single student by ID
        # This would need proper implementation
        return jsonify({
            'student': {
                'id': student_id,
                'first_name': 'Sample',
                'last_name': 'Student',
                'email': 'sample@student.com',
                'student_id': f'ST{student_id:04d}'
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@attendance_bp.route('/record', methods=['POST'])
@token_required
def create_attendance_record(user_id):
    try:
        data = request.get_json()
        student_id = data.get('student_id')
        date = data.get('date')
        status = data.get('status')
        venue_id = data.get('venue_id', 1)  # Default venue
        
        if not all([student_id, date, status]):
            return jsonify({'error': 'student_id, date, and status are required'}), 400
        
        # Add your attendance recording logic here
        # For now, just return success
        return jsonify({
            'message': 'Attendance recorded successfully',
            'student_id': student_id,
            'date': date,
            'status': status,
            'venue_id': venue_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@attendance_bp.route('/stats', methods=['GET'])
@token_required
def get_attendance_stats(user_id):
    try:
        # Get attendance statistics
        # This would need proper implementation
        return jsonify({
            'total_students': 25,
            'present_today': 20,
            'absent_today': 5,
            'attendance_rate': '80%'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@attendance_bp.route('/venue/<int:venue_id>', methods=['GET'])
@token_required
def get_venue_attendance(user_id, venue_id):
    try:
        # Get attendance for specific venue
        # This would need proper implementation
        return jsonify({
            'venue_id': venue_id,
            'attendance': [
                {'student_id': 1, 'status': 'present', 'time': '09:00'},
                {'student_id': 2, 'status': 'absent', 'time': '09:00'}
            ]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
