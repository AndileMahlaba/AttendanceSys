import sqlite3
import os

def check_db_content():
    try:
        # Try multiple possible database paths
        possible_paths = [
            'database/attendance.db',
            '../database/attendance.db',
            os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'database', 'attendance.db')
        ]
        
        for db_path in possible_paths:
            print(f"Trying path: {db_path}")
            if os.path.exists(db_path):
                print(f"Found database at: {db_path}")
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                
                # Check tables
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = cursor.fetchall()
                print("Tables:", [table[0] for table in tables])
                
                # Check users if table exists
                if any('users' in table[0].lower() for table in tables):
                    cursor.execute("SELECT * FROM users")
                    users = cursor.fetchall()
                    print("Users:", users)
                
                conn.close()
                break
        else:
            print("Database not found in any location!")
            
    except Exception as e:
        print(f"Error checking database content: {e}")

if __name__ == "__main__":
    check_db_content()
