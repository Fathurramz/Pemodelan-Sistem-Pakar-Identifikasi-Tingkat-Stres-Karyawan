from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # type: ignore
from flask_jwt_extended import JWTManager  # type: ignore
from flask_cors import CORS  # type: ignore
from datetime import timedelta

db = SQLAlchemy()
jwt = JWTManager()


def create_app():
    """Factory function untuk membuat Flask app."""

    app = Flask(__name__)

    # Load config
    from app.config import Config
    app.config.from_object(Config)
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(
        seconds=Config.JWT_ACCESS_TOKEN_EXPIRES
    )

    # Init extensions
    db.init_app(app)
    jwt.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register blueprints (routes)
    from app.routes.auth import auth_bp
    from app.routes.questions import questions_bp
    from app.routes.assessments import assessments_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(questions_bp, url_prefix="/api")
    app.register_blueprint(assessments_bp, url_prefix="/api")

    # Auto-create tables saat pertama kali jalan
    with app.app_context():
        from app import models  # noqa: F401
        db.create_all()

    return app
