"""
Landing page route - redirects to login page.
"""
from flask import Blueprint, redirect, url_for
from flask_login import current_user

landing_bp = Blueprint("landing", __name__)


@landing_bp.route("/")
def index():
    """Redirect to appropriate dashboard based on authentication."""
    if current_user.is_authenticated:
        if current_user.is_admin():
            return redirect(url_for("dashboard.index"))
        else:
            return redirect(url_for("patient_portal.dashboard"))
    return redirect(url_for("auth.login"))
