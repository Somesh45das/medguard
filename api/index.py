"""
Vercel serverless function entry point for Flask app.
"""
from wsgi import app

# Vercel expects the app to be named 'app' or be the default export
# This makes the Flask app available to Vercel's Python runtime
handler = app
