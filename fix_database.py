import sqlite3
import os

db_path = 'database/attendance.db'
print(f"Fixing database: {os.path.abspath(db_path)}")

if os.path.exists(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create a temporary table to hold the user data
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users_temp (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            first_name TEXT,
            last_name TEXT,
            role TEXT,
            is_active INTEGER DEFAULT 1,
            created_at DATETIME,
            updated_at DATETIME
        )
        ''')
        
        # Copy data from old users table to temp table
        cursor.execute('''
        INSERT INTO users_temp (email, password_hash, first_name, last_name, role, is_active, created_at, updated_at)
        SELECT email, password_hash, first_name, last_name, role, is_active, created_at, updated_at
        FROM users
        ''')
        
        # Drop the old users table
        cursor.execute('DROP TABLE users')
        
        # Rename temp table to users
        cursor.execute('ALTER TABLE users_temp RENAME TO users')
        
        conn.commit()
        conn.close()
        
        print("Database fixed successfully! Users now have proper IDs.")
        
        # Verify the fix
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
        print("\n=== USERS AFTER FIX ===")
        for user in users:
            print(f"User: {user}")
        conn.close()
        
    except Exception as e:
        print(f"Error fixing database: {e}")
        import traceback
        traceback.print_exc()
else:
    print("Database file does not exist!")
