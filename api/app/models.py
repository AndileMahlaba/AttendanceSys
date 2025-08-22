import sqlite3
import os
import datetime

# Get the absolute path to the database
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATABASE_PATH = os.path.join(BASE_DIR, 'database', 'attendance.db')

def convert_datetime_to_string(obj):
    """Convert datetime objects to ISO format strings"""
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    elif isinstance(obj, dict):
        return {key: convert_datetime_to_string(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_datetime_to_string(item) for item in obj]
    else:
        return obj

class User:
    @staticmethod
    def get_db_connection():
        return sqlite3.connect(DATABASE_PATH)

    @staticmethod
    def find_by_email(email):
        try:
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()
            
            # First, get column names to understand the table structure
            cursor.execute('PRAGMA table_info(users)')
            columns = cursor.fetchall()
            column_names = [col[1] for col in columns]
            
            # Now get the user data
            cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
            user = cursor.fetchone()
            conn.close()
            
            if user:
                # Convert to dictionary using column names
                user_dict = {}
                for i, col_name in enumerate(column_names):
                    user_dict[col_name] = user[i]
                
                print(f"User data: {user_dict}")
                return convert_datetime_to_string(user_dict)
            return None
            
        except Exception as e:
            print(f"Database error in find_by_email: {e}")
            import traceback
            traceback.print_exc()
            return None

    @staticmethod
    def verify_password(stored_hash, password):
        # Simple password check for development
        print(f"Verifying password: stored='{stored_hash}', provided='{password}'")
        return stored_hash == password

    @staticmethod
    def create(email, password, first_name, last_name, role):
        try:
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO users (email, password_hash, first_name, last_name, role) VALUES (?, ?, ?, ?, ?)',
                (email, password, first_name, last_name, role)
            )
            user_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return user_id
        except Exception as e:
            print(f"Database error in create: {e}")
            return None

    @staticmethod
    def find_by_id(user_id):
        try:
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()
            
            # Get column names
            cursor.execute('PRAGMA table_info(users)')
            columns = cursor.fetchall()
            column_names = [col[1] for col in columns]
            
            cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
            user = cursor.fetchone()
            conn.close()
            
            if user:
                # Convert to dictionary using column names
                user_dict = {}
                for i, col_name in enumerate(column_names):
                    user_dict[col_name] = user[i]
                
                return convert_datetime_to_string(user_dict)
            return None
            
        except Exception as e:
            print(f"Database error in find_by_id: {e}")
            return None

class Student:
    @staticmethod
    def get_db_connection():
        return sqlite3.connect(DATABASE_PATH)

    @staticmethod
    def create(user_id, student_id):
        try:
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO students (user_id, student_id) VALUES (?, ?)',
                (user_id, student_id)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Database error in Student.create: {e}")
            return False

    @staticmethod
    def get_all():
        try:
            conn = sqlite3.connect(DATABASE_PATH)
            conn.row_factory = sqlite3.Row
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
                student_dict = dict(student)
                student_list.append(convert_datetime_to_string(student_dict))
            
            return student_list
        except Exception as e:
            print(f"Database error in Student.get_all: {e}")
            return []

class Venue:
    @staticmethod
    def get_all():
        try:
            conn = sqlite3.connect(DATABASE_PATH)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM venues')
            venues = cursor.fetchall()
            conn.close()
            return [convert_datetime_to_string(dict(venue)) for venue in venues]
        except Exception as e:
            print(f"Database error in Venue.get_all: {e}")
            return []

class Attendance:
    @staticmethod
    def get_all():
        try:
            conn = sqlite3.connect(DATABASE_PATH)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('''
                SELECT a.*, u.first_name, u.last_name, s.student_id 
                FROM attendance_records a
                JOIN users u ON a.student_id = u.id
                JOIN students s ON u.id = s.user_id
            ''')
            records = cursor.fetchall()
            conn.close()
            return [convert_datetime_to_string(dict(record)) for record in records]
        except Exception as e:
            print(f"Database error in Attendance.get_all: {e}")
            return []
