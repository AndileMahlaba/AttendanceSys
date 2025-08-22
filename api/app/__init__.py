from flask import Flask, jsonify
from flask_cors import CORS
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
load_dotenv()

# Set default database URL with absolute path
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATABASE_PATH = os.path.join(BASE_DIR, 'database', 'attendance.db')
DATABASE_URL = os.getenv('DATABASE_URL', f'sqlite:///{DATABASE_PATH}')

# Database setup
engine = create_engine(DATABASE_URL)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['JWT_SECRET'] = os.getenv('JWT_SECRET', 'jwt-secret-key')

    # Configure CORS properly with credentials support
    CORS(app, 
         origins=["http://localhost:3000"], 
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         allow_headers=["Content-Type", "Authorization"],
         supports_credentials=True)

    # Register blueprints
    from .routes.auth import auth_bp
    from .routes.attendance import attendance_bp
    from .routes.faces import faces_bp
    from .routes.venues import venues_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(attendance_bp, url_prefix='/api/attendance')
    app.register_blueprint(faces_bp, url_prefix='/api/faces')
    app.register_blueprint(venues_bp, url_prefix='/api/venues')

    # Add root endpoint
    @app.route('/')
    def hello():
        return 'Attendance System API is running!'

    @app.route('/api/health')
    def health_check():
        return {'status': 'healthy', 'message': 'API is working'}

    # Add route to list all endpoints
    @app.route('/api/routes')
    def list_routes():
        routes = []
        for rule in app.url_map.iter_rules():
            if rule.endpoint != 'static':
                routes.append({
                    'endpoint': rule.endpoint,
                    'methods': list(rule.methods),
                    'path': str(rule)
                })
        return jsonify(routes)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app
