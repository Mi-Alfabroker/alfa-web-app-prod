"""Health check endpoints for API and database connectivity."""
from flask import Blueprint, jsonify
from sqlalchemy import text
from app.models import db

health_bp = Blueprint('health', __name__)


@health_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify the API is running.
    
    Returns:
        JSON with API status
    """
    return jsonify({
        'status': 'healthy',
        'service': 'api',
        'message': 'Alfa-Broker API is up and running'
    }), 200


@health_bp.route('/health/db', methods=['GET'])
def database_health_check():
    """
    Health check endpoint to verify database connectivity.
    
    Returns:
        JSON with database connection status and details
    """
    try:
        # Execute a simple query to test the connection
        result = db.session.execute(text('SELECT 1 as status, version() as version'))
        row = result.fetchone()
        
        # Get connection info
        db_url = str(db.engine.url)
        # Mask password in URL for security
        masked_url = db_url.replace(db.engine.url.password or '', '***')
        
        return jsonify({
            'status': 'healthy',
            'service': 'database',
            'message': 'Database connection successful',
            'details': {
                'connected': True,
                'database_url': masked_url,
                'postgres_version': row.version if row else 'unknown'
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'service': 'database',
            'message': 'Database connection failed',
            'details': {
                'connected': False,
                'error': str(e)
            }
        }), 503


@health_bp.route('/health/full', methods=['GET'])
def full_health_check():
    """
    Complete health check for all services.
    
    Returns:
        JSON with status of all services (API + Database)
    """
    services = {
        'api': {'status': 'healthy', 'message': 'API is running'}
    }
    overall_status = 'healthy'
    http_status = 200
    
    # Check database
    try:
        result = db.session.execute(text('SELECT 1'))
        result.fetchone()
        services['database'] = {
            'status': 'healthy',
            'message': 'Database connected'
        }
    except Exception as e:
        services['database'] = {
            'status': 'unhealthy',
            'message': f'Database error: {str(e)}'
        }
        overall_status = 'degraded'
        http_status = 503
    
    return jsonify({
        'status': overall_status,
        'message': 'Alfa-Broker system health check',
        'services': services
    }), http_status
