"""
Vercel serverless function entry point for Flask app.
"""
import os
import sys

# Disable ML model loading in serverless environment
os.environ['SKIP_ML_LOADING'] = '1'

try:
    from wsgi import app
    
    # Vercel expects the app to be named 'app' or be the default export
    handler = app
    
except Exception as e:
    # Fallback error handler
    from flask import Flask, jsonify
    
    app = Flask(__name__)
    
    @app.route('/')
    def index():
        return jsonify({
            'error': 'Application initialization failed',
            'message': str(e),
            'help': 'Check Vercel logs for details'
        }), 500
    
    handler = app
