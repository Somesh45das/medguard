"""
Flask application factory.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
import os

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()


def create_app(config_class=None):
    """Create and configure the Flask application."""
    app = Flask(__name__)

    if config_class is None:
        from config import Config
        config_class = Config

    app.config.from_object(config_class)

    # Secret key for sessions and CSRF
    app.secret_key = app.config['SECRET_KEY']

    # Ensure instance folder exists
    os.makedirs(os.path.join(app.root_path, "..", "instance"), exist_ok=True)

    # Initialize extensions
    db.init_app(app)
    csrf.init_app(app)
    
    # Initialize Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please login to access this page.'
    login_manager.login_message_category = 'warning'
    
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.query.get(int(user_id))

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.landing import landing_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.appointments import appointments_bp
    from app.routes.queue_routes import queue_bp
    from app.routes.doctors import doctors_bp
    from app.routes.api import api_bp
    from app.routes.patient_portal import patient_portal_bp
    from app.routes.admin_management import admin_mgmt_bp

    # Authentication routes (public)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    
    # Landing page
    app.register_blueprint(landing_bp)
    
    # Patient Portal (requires user login)
    app.register_blueprint(patient_portal_bp, url_prefix="/patient")
    
    # Admin Portal (requires admin login)
    app.register_blueprint(dashboard_bp, url_prefix="/admin")
    app.register_blueprint(appointments_bp, url_prefix="/admin/appointments")
    app.register_blueprint(queue_bp, url_prefix="/admin/queue")
    app.register_blueprint(doctors_bp, url_prefix="/admin/doctors")
    app.register_blueprint(admin_mgmt_bp, url_prefix="/admin/manage")
    
    # API routes
    app.register_blueprint(api_bp, url_prefix="/api")

    # Create database tables
    with app.app_context():
        from app.models import models  # noqa: F401
        from app.models import user  # noqa: F401
        db.create_all()

    return app
