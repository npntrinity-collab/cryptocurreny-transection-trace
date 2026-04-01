from flask import Flask, jsonify
from flask_cors import CORS

# 🔹 Import all routes
from routes.auth_routes import auth_bp
from routes.trace_routes import trace_bp
from routes.report_routes import report_bp

def create_app():
    app = Flask(__name__)

    # Enable CORS
    CORS(app)

    # Register all blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(trace_bp)
    app.register_blueprint(report_bp)

    # Health route
    @app.route('/')
    def home():
        return jsonify({
            "message": "Crypto Forensic Backend Running",
            "status": "OK"
        })

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)