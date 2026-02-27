"""
User authentication models with role-based access control.
"""
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class User(UserMixin, db.Model):
    """User model for authentication and authorization."""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(15), nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="user")  # user, admin, doctor
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    
    # Relationship to patient records
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=True)
    patient = db.relationship("Patient", backref="user_account", uselist=False)
    
    # Relationship to doctor records
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"), nullable=True)
    doctor = db.relationship("Doctor", backref="user_account", uselist=False)

    def __repr__(self):
        return f"<User {self.email} - {self.role}>"

    def set_password(self, password):
        """Hash and set password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify password against hash."""
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        """Check if user has admin role."""
        return self.role == "admin"

    def is_user(self):
        """Check if user has user/patient role."""
        return self.role == "user"
    
    def is_doctor(self):
        """Check if user has doctor role."""
        return self.role == "doctor"

    def update_last_login(self):
        """Update last login timestamp."""
        self.last_login = datetime.utcnow()
        db.session.commit()


class PasswordResetToken(db.Model):
    """Password reset tokens for forgot password functionality."""
    __tablename__ = "password_reset_tokens"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    token = db.Column(db.String(255), unique=True, nullable=False, index=True)
    expires_at = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref="reset_tokens")

    def __repr__(self):
        return f"<PasswordResetToken {self.token[:10]}... for user {self.user_id}>"

    def is_valid(self):
        """Check if token is still valid."""
        return not self.used and datetime.utcnow() < self.expires_at
