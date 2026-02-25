"""
WSGI entry point for production deployment (Vercel, Gunicorn, etc.)
"""
import os
from app import create_app

# Skip ML model loading in serverless environment
skip_ml = os.environ.get('SKIP_ML_LOADING', '0') == '1'

if not skip_ml:
    # Only load ML in non-serverless environments
    from config import Config
    if os.path.exists(Config.ML_MODEL_PATH):
        print("✅ ML model available")

# Create the Flask application
app = create_app()

# Initialize database tables (only if database is configured)
with app.app_context():
    try:
        from app import db
        db.create_all()
        print("✅ Database tables created/verified")
    except Exception as e:
        print(f"⚠️ Database initialization skipped: {e}")

if __name__ == "__main__":
    app.run()
