"""
Management Portal routes - For hospital staff with authentication.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from functools import wraps

management_portal_bp = Blueprint("management_portal", __name__)


def login_required(f):
    """Decorator to require login for management routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_management'):
            flash("Please login to access the management portal.", "warning")
            return redirect(url_for("management_portal.login"))
        return f(*args, **kwargs)
    return decorated_function


@management_portal_bp.route("/")
def home():
    """Management portal landing page."""
    if session.get('is_management'):
        return redirect(url_for("dashboard.index"))
    return render_template("management/login.html")


@management_portal_bp.route("/login", methods=["GET", "POST"])
def login():
    """Management login page."""
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        
        # Simple authentication (in production, use proper auth)
        if username == "admin" and password == "admin123":
            session['is_management'] = True
            session['username'] = username
            flash("Welcome to Management Portal!", "success")
            return redirect(url_for("dashboard.index"))
        else:
            flash("Invalid credentials. Try username: admin, password: admin123", "danger")
    
    return render_template("management/login.html")


@management_portal_bp.route("/logout")
def logout():
    """Logout from management portal."""
    session.pop('is_management', None)
    session.pop('username', None)
    flash("You have been logged out.", "info")
    return redirect(url_for("management_portal.login"))
