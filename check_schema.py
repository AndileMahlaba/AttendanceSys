import sqlite3
import os

# Path to your database
db_path = 'database/attendance.db'
print(f"Checking database: {os.path.abspath(db_path)}")
print(f"Database exists: {os.path.exists(db_path)}")

if os.path.exists(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check users table schema
        print("\n=== USERS TABLE SCHEMA ===")
        cursor.execute("PRAGMA table_info(users)")
        users_columns = cursor.fetchall()
        for col in users_columns:
            print(f"Column {col[0]}: {col[1]} ({col[2]}) - Primary Key: {col[5]}")
        
        # Check if id column exists and is primary key
        id_column = [col for col in users_columns if col[1] == 'id']
        if id_column:
            print(f"\nID column details: {id_column[0]}")
            if id_column[0][5] == 1:  # Is primary key
                print("✓ ID column is PRIMARY KEY")
            else:
                print("✗ ID column is NOT primary key")
        else:
            print("✗ ID column does not exist in users table")
        
        # Check what's actually in the users table
        print("\n=== USERS TABLE DATA ===")
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        for user in users:
            print(f"User: {user}")
        
        # Check other tables
        print("\n=== ALL TABLES ===")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        for table in tables:
            print(f"Table: {table[0]}")
        
        conn.close()
        
    except Exception as e:
        print(f"Error checking schema: {e}")
else:
    print("Database file does not exist!")
