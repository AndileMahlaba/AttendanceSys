import psycopg2
import numpy as np

# --------------------------
# CONFIGURATION
# --------------------------
DB_NAME = "attendance_db"
DB_USER = "postgres"
DB_PASSWORD = "newpassword"
DB_HOST = "localhost"

# --------------------------
# CONNECT TO DATABASE
# --------------------------
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST
)
cur = conn.cursor()

# --------------------------
# RUN SCHEMA.SQL
# --------------------------
with open("schema.sql", "r", encoding="utf-8") as f:
    cur.execute(f.read())
    conn.commit()

# --------------------------
# INSERT SAMPLE DATA
# --------------------------
# Admin user
cur.execute("""
INSERT INTO users (student_number, full_name, email, role)
VALUES (%s, %s, %s, %s)
ON CONFLICT DO NOTHING;
""", ("0001", "Admin User", "admin@example.com", "admin"))

# Test student
cur.execute("""
INSERT INTO users (student_number, full_name, email)
VALUES (%s, %s, %s)
ON CONFLICT DO NOTHING;
""", ("0002", "Test Student", "student@example.com"))

# Venue
cur.execute("""
INSERT INTO venues (name, building, latitude, longitude, radius_m, allowed_cidrs)
VALUES (%s, %s, %s, %s, %s, %s)
ON CONFLICT DO NOTHING;
""", ("Main Lecture Hall", "Building A", -29.86, 31.03, 50, ["0.0.0.0/0"]))

# Lecture (pick first venue)
cur.execute("""
INSERT INTO lectures (module_code, title, venue_id, start_time, end_time)
SELECT %s, %s, id, now() + interval '1 hour', now() + interval '2 hour'
FROM venues LIMIT 1
ON CONFLICT DO NOTHING;
""", ("CS101", "Intro to Programming"))

# Sample face embedding for test student
# Get student user_id
cur.execute("SELECT id FROM users WHERE student_number = %s", ("0002",))
student_id = cur.fetchone()[0]

embedding = np.random.rand(512).astype('float32').tobytes()
cur.execute("""
INSERT INTO face_templates (user_id, model, embedding)
VALUES (%s, %s, %s)
ON CONFLICT DO NOTHING;
""", (student_id, "face_model_v1", embedding))

# Commit and close
conn.commit()
cur.close()
conn.close()

print("Database initialized successfully!")
