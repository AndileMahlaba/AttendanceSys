# app/utils/rate_limiting.py
from flask import jsonify, request
from functools import wraps
from api.app.utils.security import get_client_ip
import redis
import os

# Initialize Redis
redis_client = redis.Redis.from_url(os.getenv('REDIS_URL', 'redis://localhost:6379'))

def rate_limit(requests_per_minute=60):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            ip = get_client_ip()
            key = f"rate_limit:{ip}:{request.path}"
            
            current = redis_client.get(key)
            if current and int(current) > requests_per_minute:
                return jsonify({'error': 'Rate limit exceeded'}), 429
            
            pipe = redis_client.pipeline()
            pipe.incr(key, 1)
            pipe.expire(key, 60)
            pipe.execute()
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator