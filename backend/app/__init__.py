"""Flask application factory."""
import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from app.models import db
from app.blueprints.health import health_bp
from app.blueprints.aseguradoras import aseguradoras_bp
from app.blueprints.auth import auth_bp
from app.blueprints.usuarios import usuarios_bp
from app.blueprints.bienes import bienes_bp
from app.blueprints.polizas import polizas_bp
from app.blueprints.propuestas import propuestas_bp

# Load environment variables from .env file
load_dotenv()


def create_app(config: dict = None):
    """
    Application factory for Flask app.
    
    Args:
        config: Optional configuration dictionary to override defaults
        
    Returns:
        Configured Flask application instance
    """
    app = Flask(__name__)
    
    # Configure CORS - allow requests from frontend
    # In production, restrict origins to specific domains
    CORS(app, 
         origins=[
             'http://localhost:3000', 
             'http://127.0.0.1:3000',
             'http://localhost:5173',  # Vite default port
             'http://127.0.0.1:5173',
             'http://34.56.64.76:3000'
         ],
         methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'],
         allow_headers=['Content-Type', 'Authorization'],
         supports_credentials=True,
         expose_headers=['Content-Type', 'Authorization'])
    
    # Build database URL from environment variables
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        db_host = os.environ.get('DB_HOST', 'localhost')
        db_port = os.environ.get('DB_PORT', '5432')
        db_name = os.environ.get('DB_NAME', 'alfabroker')
        db_user = os.environ.get('DB_USER', 'admin')
        db_password = os.environ.get('DB_PASSWORD', 'admin')
        db_url = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'change-this-in-production')
    app.config['JWT_ACCESS_TOKEN_EXPIRES_MINUTES'] = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES_MINUTES', '30'))
    app.config['JWT_REFRESH_TOKEN_EXPIRES_DAYS'] = int(os.environ.get('JWT_REFRESH_TOKEN_EXPIRES_DAYS', '7'))
    
    # Override with custom config if provided
    if config:
        app.config.update(config)
    
    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(aseguradoras_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(bienes_bp)
    app.register_blueprint(polizas_bp)
    app.register_blueprint(propuestas_bp)
    
    # Global error handlers to ensure proper responses with CORS headers
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": {
                "code": "BAD_REQUEST",
                "message": "Bad request"
            }
        }), 400
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": {
                "code": "NOT_FOUND",
                "message": "Endpoint not found"
            }
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        print(f"Internal error: {error}")
        try:
            db.session.rollback()
        except:
            pass
        return jsonify({
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "Internal server error"
            }
        }), 500
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        print(f"Unhandled exception: {error}")
        import traceback
        traceback.print_exc()
        try:
            db.session.rollback()
        except:
            pass
        return jsonify({
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "Internal server error"
            }
        }), 500
    
    return app
