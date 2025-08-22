import psycopg2
from psycopg2.extras import RealDictCursor
import datetime

# --- Database connection ---
conn = psycopg2.connect(
    dbname="attendance_db",
    user="postgres",
    password="newpassword",  # replace with your password
    host="localhost"
)
cur = conn.cursor(cursor_factory=RealDictCursor)

print("✅ Connected to database")

# --- List existing users ---
cur.execute("SELECT * FROM users;")
users = cur.fetchall()
print("\nUsers:")
for u in users:
    print(u)

# --- List existing venues ---
cur.execute("SELECT * FROM venues;")
venues = cur.fetchall()
print("\nVenues:")
for v in venues:
    print(v)

# --- Create a test lecture ---
cur.execute("""
INSERT INTO lectures (module_code, title, venue_id, start_time, end_time)
SELECT 'CS999', 'Test Lecture', id, now(), now() + interval '1 hour'
FROM venues LIMIT 1
RETURNING id;
""")
lecture_id = cur.fetchone()['id']
print(f"\n✅ Created test lecture with ID: {lecture_id}")

# --- Log attendance for Test Student (0002) ---
cur.execute("""
INSERT INTO attendance_logs (lecture_id, user_id, status, client_lat, client_lng)
SELECT %s, id, 'on_time', -29.86, 31.03
FROM users
WHERE student_number='0002'
RETURNING id;
""", (lecture_id,))
log_id = cur.fetchone()['id']
print(f"✅ Logged attendance with ID: {log_id}")

# --- Insert dummy face template for Test Student ---
cur.execute("""
INSERT INTO face_templates (user_id, model, embedding)
SELECT id, 'face_model_v1', decode('001122334455', 'hex')
FROM users WHERE student_number='0002'
RETURNING id;
""")
template_id = cur.fetchone()['id']
print(f"✅ Inserted face template with ID: {template_id}")

# --- Display attendance logs ---
cur.execute("SELECT * FROM attendance_logs;")
logs = cur.fetchall()
print("\nAttendance Logs:")
for log in logs:
    print(log)

# --- Display face templates ---
cur.execute("SELECT * FROM face_templates;")
templates = cur.fetchall()
print("\nFace Templates:")
for ft in templates:
    print(ft)

# --- Commit and close ---
conn.commit()
cur.close()
conn.close()
print("\n✅ Test completed successfully!")
