import ipaddress
from functools import wraps
from flask import request, jsonify
from jose import jwt, JWTError
from datetime import datetime, timedelta
import os

def generate_token(user_id, expires_in=3600):
    """Generate JWT token"""
    payload = {
        'sub': user_id,
        'exp': datetime.utcnow() + timedelta(seconds=expires_in),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, os.getenv('JWT_SECRET'), algorithm='HS256')

def verify_token(token):
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=['HS256'])
        return payload['sub']
    except JWTError:
        return None

def token_required(f):
    """Decorator to require JWT token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split()[1]
            except IndexError:
                return jsonify({'error': 'Bearer token malformed'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        user_id = verify_token(token)
        if not user_id:
            return jsonify({'error': 'Token is invalid'}), 401
        
        return f(user_id, *args, **kwargs)
    return decorated

def get_client_ip():
    """Get client IP address with proxy support"""
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    return request.remote_addr

def validate_ip(ip_str, allowed_cidrs):
    """Check if IP is in allowed CIDR ranges"""
    try:
        ip = ipaddress.ip_address(ip_str)
        for cidr in allowed_cidrs or []:
            if ip in ipaddress.ip_network(cidr, strict=False):
                return True
        return False
    except ValueError:
        return False