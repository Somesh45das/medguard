"""
Simplified Vercel entry point.
This file is specifically for Vercel deployment.
"""
import os

# Configure for serverless BEFORE any imports
os.environ['SKIP_ML_LOADING'] = '1'
os.environ['FLASK_ENV'] = 'production'
os.environ['DATABASE_URL'] = 'sqlite:////tmp/hospital.db'

# Now import the app
from app import create_app, db

# Create the Flask application
app = create_app()

# Initialize database
with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print(f"Database init: {e}")

# Vercel will use this 'app' object
if __name__ == "__main__":
    app.run()
