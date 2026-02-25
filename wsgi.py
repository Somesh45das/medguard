"""
WSGI entry point for production deployment (Vercel, Gunicorn, etc.)
"""
import os
from app import create_app

# Create the Flask application
app = create_app()

# Initialize database tables
with app.app_context():
    from app import db
    db.create_all()

if __name__ == "__main__":
    app.run()
