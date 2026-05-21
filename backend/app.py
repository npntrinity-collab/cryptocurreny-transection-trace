from flask import Flask, jsonify, request
from flask_cors import CORS
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 🔹 Import all routes
from routes.auth_routes import auth_bp
from routes.trace_routes import trace_bp
from routes.report_routes import report_bp
from routes.dashboard_routes import dashboard_bp
from routes.case_routes import case_bp
from routes.risk_routes import risk_bp
from routes.market_routes import market_bp

def create_app():
    app = Flask(__name__) 

    # Enable CORS globally with permissive settings
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Add custom after_request handler to ensure CORS headers on all responses
    @app.after_request
    def add_cors_headers(response):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Max-Age"] = "3600"
        return response

    @app.errorhandler(Exception)
    def handle_exception(error):
        app.logger.error('Unhandled exception: %s', error, exc_info=True)
        response = jsonify({
            'error': 'Internal Server Error',
            'message': str(error)
        })
        response.status_code = 500
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Max-Age"] = "3600"
        return response

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(trace_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(case_bp)
    app.register_blueprint(risk_bp)
    app.register_blueprint(market_bp)

    # Health check
    @app.route('/')
    def home():
        logger.info("Health check endpoint called")
        return jsonify({
            "message": "Crypto Forensic Backend Running",
            "status": "OK"
        })

    # Log all requests
    @app.before_request
    def log_request():
        logger.info(f"📨 {request.method} {request.path} from {request.remote_addr}")

    return app


if __name__ == '__main__':
    app = create_app()
    logger.info("🚀 Starting Backend Server on http://0.0.0.0:5000")
    logger.info("✅ CORS enabled for all /api/* endpoints")
    logger.info("📡 Available at http://localhost:5000")
    # Disable Flask auto-reloader on Windows to avoid WinError 10038 when files change.
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)