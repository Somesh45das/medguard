"""
Application configuration.
"""
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "smart-hospital-secret-key-2024")
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL")
        or f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'hospital.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session configuration
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour in seconds
    SESSION_COOKIE_NAME = 'hospital_session'
    
    # Security settings
    WTF_CSRF_ENABLED = False  # TEMPORARY - Disabled for testing
    WTF_CSRF_TIME_LIMIT = None  # CSRF tokens don't expire

    # Hospital settings
    HOSPITAL_NAME = "SmartCare Hospital"
    OPD_START_HOUR = 8       # 8 AM
    OPD_END_HOUR = 20        # 8 PM
    SLOT_DURATION_MIN = 15   # 15-minute slots
    MAX_PATIENTS_PER_SLOT = 5
    EMERGENCY_PRIORITY_BOOST = 50

    # ML Model path
    ML_MODEL_PATH = os.path.join(BASE_DIR, "app", "ml", "crowd_model.pkl")
    ML_SCALER_PATH = os.path.join(BASE_DIR, "app", "ml", "scaler.pkl")

    # Notification settings
    ENABLE_NOTIFICATIONS = True
    HIGH_CROWD_THRESHOLD = 0.75   # 75% capacity = high crowd
    CRITICAL_CROWD_THRESHOLD = 0.90
