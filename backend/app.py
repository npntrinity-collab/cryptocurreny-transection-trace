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

def create_app():
    app = Flask(__name__)

    # Enable CORS with specific configuration
    CORS(app, resources={
        r"/api/*": {
            "origins": ["*"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(trace_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(case_bp)
    app.register_blueprint(risk_bp)

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
    app.run(debug=True, host='0.0.0.0', port=5000)