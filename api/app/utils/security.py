from functools import wraps
from flask import request, jsonify
import datetime
import base64
import json
import jwt

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        return super().default(obj)

SECRET_KEY = "supersecret"

def generate_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_token(token):
    try:
        # Simple token verification for development
        payload_str = base64.b64decode(token.encode()).decode()
        payload = json.loads(payload_str)
        
        # Check if token is expired
        if datetime.datetime.utcnow() > datetime.datetime.fromisoformat(payload['exp'].replace('Z', '+00:00')):
            return None
            
        return payload['sub']
    except:
        return None

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(" ")[1]

        if not token:
            return jsonify({"error": "Token is missing"}), 401

        try:
            # Decode the token using your SECRET_KEY
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            # Extract user_id from the payload and pass it as a keyword argument
            user_id = payload.get('user_id')
            if not user_id:
                return jsonify({"error": "Invalid token payload"}), 401
                
            # Pass user_id as a keyword argument to the decorated function
            kwargs['user_id'] = user_id
            return f(*args, **kwargs)
            
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

    return decorated
