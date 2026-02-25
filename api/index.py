"""
Vercel serverless function entry point for Flask app.
"""
import os
import sys

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Configure for serverless environment
os.environ['SKIP_ML_LOADING'] = '1'
os.environ['FLASK_ENV'] = 'production'

# Use /tmp for database (Vercel's writable directory)
if not os.environ.get('DATABASE_URL'):
    os.environ['DATABASE_URL'] = 'sqlite:////tmp/hospital.db'

try:
    # Import and create Flask app
    from app import create_app, db
    
    app = create_app()
    
    # Initialize database tables
    with app.app_context():
        try:
            db.create_all()
            print("✅ Database initialized")
        except Exception as e:
            print(f"⚠️ Database init: {e}")
    
    # This is what Vercel will use
    app = app
    
except Exception as e:
    # Emergency fallback
    import traceback
    from flask import Flask, jsonify
    
    print(f"❌ App initialization failed: {e}")
    print(traceback.format_exc())
    
    app = Flask(__name__)
    
    @app.route('/')
    @app.route('/<path:path>')
    def fallback(path=''):
        return jsonify({
            'status': 'error',
            'message': 'Application failed to initialize',
            'error': str(e),
            'path': path,
            'help': 'Check Vercel function logs for details'
        }), 500
