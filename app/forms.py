"""
WTForms for secure form handling with CSRF protection.
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, IntegerField, TextAreaField, TimeField, DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Optional, NumberRange
from app.models.user import User


class LoginForm(FlaskForm):
    """Login form with CSRF protection."""
    email = StringField('Email', validators=[
        DataRequired(message="Email is required")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required")
    ])
    remember_me = BooleanField('Remember Me')


class RegistrationForm(FlaskForm):
    """User registration form (patients only)."""
    name = StringField('Full Name', validators=[
        DataRequired(message="Name is required"),
        Length(min=2, max=150, message="Name must be between 2 and 150 characters")
    ])
    email = StringField('Email', validators=[
        DataRequired(message="Email is required"),
        Email(message="Invalid email address")
    ])
    phone = StringField('Phone Number', validators=[
        DataRequired(message="Phone number is required"),
        Length(min=10, max=15, message="Invalid phone number")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required"),
        Length(min=8, message="Password must be at least 8 characters")
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message="Please confirm your password"),
        EqualTo('password', message="Passwords must match")
    ])

    def validate_email(self, email):
        """Check if email already exists."""
        user = User.query.filter_by(email=email.data.lower()).first()
        if user:
            raise ValidationError('Email already registered. Please use a different email or login.')


class ForgotPasswordForm(FlaskForm):
    """Forgot password form."""
    email = StringField('Email', validators=[
        DataRequired(message="Email is required"),
        Email(message="Invalid email address")
    ])


class ResetPasswordForm(FlaskForm):
    """Reset password form."""
    password = PasswordField('New Password', validators=[
        DataRequired(message="Password is required"),
        Length(min=8, message="Password must be at least 8 characters")
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message="Please confirm your password"),
        EqualTo('password', message="Passwords must match")
    ])


class DoctorForm(FlaskForm):
    """Form for adding/editing doctors (admin only)."""
    name = StringField('Doctor Name', validators=[
        DataRequired(message="Doctor name is required"),
        Length(min=2, max=150)
    ])
    specialization = StringField('Specialization', validators=[
        DataRequired(message="Specialization is required"),
        Length(max=100)
    ])
    department_id = SelectField('Department', coerce=int, validators=[
        DataRequired(message="Department is required")
    ])
    experience_years = IntegerField('Years of Experience', validators=[
        Optional(),
        NumberRange(min=0, max=60)
    ], default=0)
    avg_consultation_min = IntegerField('Avg Consultation Time (minutes)', validators=[
        DataRequired(message="Consultation time is required"),
        NumberRange(min=5, max=120)
    ], default=15)
    max_patients_per_day = IntegerField('Max Patients Per Day', validators=[
        DataRequired(message="Max patients is required"),
        NumberRange(min=1, max=100)
    ], default=40)
    shift_start = TimeField('Shift Start Time', validators=[
        DataRequired(message="Shift start time is required")
    ])
    shift_end = TimeField('Shift End Time', validators=[
        DataRequired(message="Shift end time is required")
    ])
    rating = IntegerField('Rating (1-5)', validators=[
        Optional(),
        NumberRange(min=1, max=5)
    ], default=4)
    is_available = BooleanField('Currently Available', default=True)


class DepartmentForm(FlaskForm):
    """Form for adding/editing departments (admin only)."""
    name = StringField('Department Name', validators=[
        DataRequired(message="Department name is required"),
        Length(min=2, max=100)
    ])
    floor = IntegerField('Floor Number', validators=[
        DataRequired(message="Floor number is required"),
        NumberRange(min=1, max=20)
    ], default=1)
    max_capacity = IntegerField('Max Capacity', validators=[
        DataRequired(message="Max capacity is required"),
        NumberRange(min=10, max=200)
    ], default=50)
    avg_consultation_min = IntegerField('Avg Consultation Time (minutes)', validators=[
        DataRequired(message="Consultation time is required"),
        NumberRange(min=5, max=60)
    ], default=15)
    is_active = BooleanField('Active', default=True)
