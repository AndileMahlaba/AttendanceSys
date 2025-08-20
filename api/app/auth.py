# app/auth.py
from email.mime import text
import uuid
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils.security import generate_token

def register_user(email, password, first_name, last_name, role='student'):
    # Check if user exists
    existing = session.execute(
        text("SELECT id FROM users WHERE email = :email"),
        {"email": email}
    ).fetchone()
    
    if existing:
        return None, "User already exists"
    
    # Hash password
    password_hash = generate_password_hash(password)
    
    # Create user
    user_id = str(uuid.uuid4())
    session.execute(
        text("""
            INSERT INTO users (id, email, password_hash, first_name, last_name, role)
            VALUES (:id, :email, :password_hash, :first_name, :last_name, :role)
        """),
        {
            "id": user_id,
            "email": email,
            "password_hash": password_hash,
            "first_name": first_name,
            "last_name": last_name,
            "role": role
        }
    )
    
    session.commit()
    return user_id, None

def authenticate_user(email, password):
    user = session.execute(
        text("SELECT id, password_hash FROM users WHERE email = :email AND is_active = TRUE"),
        {"email": email}
    ).fetchone()
    
    if not user or not check_password_hash(user.password_hash, password):
        return None, "Invalid credentials"
    
    return user.id, None