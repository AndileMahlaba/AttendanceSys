import sqlite3
import os

db_path = 'database/attendance.db'
print(f"Debugging ID issue in: {os.path.abspath(db_path)}")

if os.path.exists(db_path):
    try:
        conn = sqlite3.connect(db_path)
        
        # Method 1: Check with row_factory (like your code)
        print("\n--- Method 1: Using row_factory ---")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', ('admin@attendancesys.com',))
        user = cursor.fetchone()
        if user:
            user_dict = dict(user)
            print(f"User with row_factory: {user_dict}")
            print(f"ID type: {type(user_dict.get('id'))}, ID value: {user_dict.get('id')}")
        
        # Method 2: Check without row_factory
        print("\n--- Method 2: Without row_factory ---")
        conn.row_factory = None
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', ('admin@attendancesys.com',))
        user = cursor.fetchone()
        if user:
            print(f"User without row_factory: {user}")
            print(f"ID type: {type(user[0])}, ID value: {user[0]}")
        
        # Method 3: Check column names
        print("\n--- Method 3: Checking column names ---")
        cursor.execute('PRAGMA table_info(users)')
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        print(f"Column names: {column_names}")
        
        # Check if we're selecting the right column for ID
        if 'id' in column_names:
            id_index = column_names.index('id')
            print(f"ID is at index: {id_index}")
            
            # Get data using column index
            cursor.execute('SELECT * FROM users WHERE email = ?', ('admin@attendancesys.com',))
            user = cursor.fetchone()
            if user:
                print(f"ID from index {id_index}: {user[id_index]} (type: {type(user[id_index])})")
        
        conn.close()
        
    except Exception as e:
        print(f"Error debugging: {e}")
        import traceback
        traceback.print_exc()
else:
    print("Database file does not exist!")
