from flask import Flask, jsonify
from flask_cors import CORS

# 🔹 Import route blueprints
from routes.trace_routes import trace_bp
from routes.report_routes import report_bp


def create_app():
    app = Flask(__name__)

    # 🔹 Enable CORS (important for frontend connection)
    CORS(app)

    # 🔹 Register all routes (Blueprints)
    app.register_blueprint(trace_bp)
    app.register_blueprint(report_bp)

    # 🔹 Health check route
    @app.route('/')
    def home():
        return jsonify({
            "message": "Crypto Trace Backend Running",
            "status": "OK"
        })

    return app


# 🔹 Run app
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)