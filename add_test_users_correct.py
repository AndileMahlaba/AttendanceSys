import sqlite3
import os

def add_test_users():
    try:
        # Use the correct relative path
        db_path = 'database/attendance.db'
        print(f"Using database: {os.path.abspath(db_path)}")
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Clear existing test users to avoid duplicates
        cursor.execute("DELETE FROM users WHERE email IN ('admin@attendancesys.com', 'student@attendancesys.com')")
        
        # Add admin user
        cursor.execute(
            "INSERT INTO users (email, password_hash, first_name, last_name, role, is_active) VALUES (?, ?, ?, ?, ?, ?)",
            ('admin@attendancesys.com', 'admin123', 'Admin', 'User', 'admin', 1)
        )
        
        # Add student user
        cursor.execute(
            "INSERT INTO users (email, password_hash, first_name, last_name, role, is_active) VALUES (?, ?, ?, ?, ?, ?)",
            ('student@attendancesys.com', 'password123', 'John', 'Student', 'student', 1)
        )
        
        conn.commit()
        
        # Verify the users were added
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        print("Users in database:")
        for user in users:
            print(f"  - {user}")
            
        conn.close()
        print("Test users added successfully to correct database!")
        
    except Exception as e:
        print(f"Error adding test users: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    add_test_users()
