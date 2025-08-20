from flask import Flask
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

# Database setup
engine = create_engine(os.getenv('DATABASE_URL'))
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['JWT_SECRET'] = os.getenv('JWT_SECRET', 'jwt-secret-key')
    
    CORS(app, origins=os.getenv('ALLOWED_ORIGINS', 'http://localhost:3000').split(','))
    
    # Register blueprints
    from app.routes.attendance import attendance_bp
    from app.routes.faces import faces_bp
    from app.routes.venues import venues_bp
    from app.routes.auth import auth_bp
    
    app.register_blueprint(attendance_bp, url_prefix='/api/attendance')
    app.register_blueprint(faces_bp, url_prefix='/api/faces')
    app.register_blueprint(venues_bp, url_prefix='/api/venues')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()
    
    return app