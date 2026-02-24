"""
Authentication service with JWT token generation and validation.
"""
import jwt
import secrets
from datetime import datetime, timedelta
from functools import wraps
from flask import current_app, request, jsonify, redirect, url_for, flash, session
from flask_login import current_user
from app.models.user import User, PasswordResetToken
from app import db


class AuthService:
    """Handle authentication operations."""

    @staticmethod
    def generate_jwt_token(user_id, role, expires_in=3600):
        """Generate JWT token for API authentication."""
        payload = {
            'user_id': user_id,
            'role': role,
            'exp': datetime.utcnow() + timedelta(seconds=expires_in),
            'iat': datetime.utcnow()
        }
        token = jwt.encode(
            payload,
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )
        return token

    @staticmethod
    def verify_jwt_token(token):
        """Verify and decode JWT token."""
        try:
            payload = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256']
            )
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    @staticmethod
    def generate_reset_token(user):
        """Generate password reset token."""
        token = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(hours=1)
        
        reset_token = PasswordResetToken(
            user_id=user.id,
            token=token,
            expires_at=expires_at
        )
        db.session.add(reset_token)
        db.session.commit()
        
        return token

    @staticmethod
    def verify_reset_token(token):
        """Verify password reset token."""
        reset_token = PasswordResetToken.query.filter_by(token=token).first()
        if reset_token and reset_token.is_valid():
            return reset_token.user
        return None

    @staticmethod
    def mark_token_used(token):
        """Mark reset token as used."""
        reset_token = PasswordResetToken.query.filter_by(token=token).first()
        if reset_token:
            reset_token.used = True
            db.session.commit()


def login_required(f):
    """Decorator to require login for routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please login to access this page.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Decorator to require admin role."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please login to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        
        if not current_user.is_admin():
            flash('Access denied. Admin privileges required.', 'danger')
            return redirect(url_for('patient_portal.home'))
        
        return f(*args, **kwargs)
    return decorated_function


def user_required(f):
    """Decorator to require user/patient role."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please login to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        
        if not current_user.is_user():
            flash('Access denied. This page is for patients only.', 'danger')
            return redirect(url_for('dashboard.index'))
        
        return f(*args, **kwargs)
    return decorated_function


def api_token_required(f):
    """Decorator for API routes requiring JWT token."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        
        # Check for token in Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        # Verify token
        payload = AuthService.verify_jwt_token(token)
        if not payload:
            return jsonify({'error': 'Token is invalid or expired'}), 401
        
        # Get user from database
        user = User.query.get(payload['user_id'])
        if not user or not user.is_active:
            return jsonify({'error': 'User not found or inactive'}), 401
        
        # Add user to request context
        request.current_user = user
        
        return f(*args, **kwargs)
    return decorated_function


def api_admin_required(f):
    """Decorator for API routes requiring admin role."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not hasattr(request, 'current_user'):
            return jsonify({'error': 'Authentication required'}), 401
        
        if not request.current_user.is_admin():
            return jsonify({'error': 'Admin privileges required'}), 403
        
        return f(*args, **kwargs)
    return decorated_function
