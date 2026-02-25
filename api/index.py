"""
Vercel serverless function entry point for Flask app.
"""
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Disable ML model loading in serverless environment
os.environ['SKIP_ML_LOADING'] = '1'

# Set minimal config for serverless
os.environ['FLASK_ENV'] = 'production'
os.environ['DATABASE_URL'] = 'sqlite:////tmp/hospital.db'

try:
    from app import create_app
    
    # Create Flask app with minimal config
    app = create_app()
    
    # Initialize database in /tmp (Vercel's writable directory)
    with app.app_context():
        try:
            from app import db
            db.create_all()
            print("✅ Database initialized in /tmp")
        except Exception as db_error:
            print(f"⚠️ Database init warning: {db_error}")
    
    # Vercel handler
    handler = app
    
except Exception as e:
    # Fallback error handler
    from flask import Flask, jsonify
    import traceback
    
    app = Flask(__name__)
    
    @app.route('/')
    def index():
        return jsonify({
            'status': 'error',
            'error': 'Application initialization failed',
            'message': str(e),
            'traceback': traceback.format_exc(),
            'help': 'This is a Flask application. Try accessing /patient or /admin routes.'
        }), 500
    
    @app.route('/health')
    def health():
        return jsonify({
            'status': 'degraded',
            'message': 'App running in fallback mode',
            'error': str(e)
        }), 503
    
    handler = app
