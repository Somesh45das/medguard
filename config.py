"""
Application configuration.
"""
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "smart-hospital-secret-key-2024")
    
    # Database configuration - supports both PostgreSQL (Vercel) and SQLite (local)
    DATABASE_URL = os.environ.get("DATABASE_URL") or os.environ.get("POSTGRES_URL")
    
    if DATABASE_URL:
        # Fix for Vercel Postgres URL (postgres:// -> postgresql://)
        if DATABASE_URL.startswith("postgres://"):
            DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        # Fallback to SQLite for local development
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'hospital.db')}"
    
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

    # SMS Configuration
    SMS_ENABLED = os.environ.get("SMS_ENABLED", "False").lower() == "true"
    SMS_PROVIDER = os.environ.get("SMS_PROVIDER", "simulation")  # "twilio", "aws_sns", or "simulation"
    
    # Twilio Configuration (if using Twilio)
    TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "")
    TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN", "")
    TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER", "")
    
    # AWS SNS Configuration (if using AWS SNS)
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
    AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
