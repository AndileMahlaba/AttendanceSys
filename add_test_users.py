import sqlite3
import os

def add_test_users():
    try:
        # Get the absolute path to the database
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        DATABASE_PATH = os.path.join(BASE_DIR, 'database', 'attendance.db')
        
        print(f"Database path: {DATABASE_PATH}")
        print(f"Database exists: {os.path.exists(DATABASE_PATH)}")
        
        if not os.path.exists(DATABASE_PATH):
            print("Creating database directory...")
            os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
        
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Create users table if it doesn't exist
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'student',
            is_active INTEGER NOT NULL DEFAULT 1,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Add admin user
        cursor.execute(
            "INSERT OR REPLACE INTO users (email, password_hash, first_name, last_name, role, is_active) VALUES (?, ?, ?, ?, ?, ?)",
            ('admin@attendancesys.com', 'admin123', 'Admin', 'User', 'admin', 1)
        )
        
        # Add student user
        cursor.execute(
            "INSERT OR REPLACE INTO users (email, password_hash, first_name, last_name, role, is_active) VALUES (?, ?, ?, ?, ?, ?)",
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
        print("Test users added successfully!")
        
    except Exception as e:
        print(f"Error adding test users: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    add_test_users()
