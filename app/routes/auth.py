"""
Authentication routes - login, register, logout, password reset.
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from app import db
from app.models.user import User
from app.models.models import Patient
from app.forms import LoginForm, RegistrationForm, ForgotPasswordForm, ResetPasswordForm
from app.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Unified login page for both users and admins."""
    if current_user.is_authenticated:
        # Redirect based on role
        if current_user.is_admin():
            return redirect(url_for('dashboard.index'))
        elif current_user.is_doctor():
            return redirect(url_for('doctor_portal.dashboard'))
        else:
            return redirect(url_for('patient_portal.dashboard'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        email = form.email.data.lower().strip()
        password = form.password.data
        
        # Find user
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            if not user.is_active:
                flash('Your account has been deactivated. Please contact support.', 'danger')
                return redirect(url_for('auth.login'))
            
            # Login user
            login_user(user, remember=form.remember_me.data)
            user.update_last_login()
            
            # Redirect based on role
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            
            if user.is_admin():
                flash(f'Welcome back, {user.name}!', 'success')
                return redirect(url_for('dashboard.index'))
            elif user.is_doctor():
                flash(f'Welcome back, Dr. {user.name}!', 'success')
                return redirect(url_for('doctor_portal.dashboard'))
            else:
                flash(f'Welcome back, {user.name}!', 'success')
                return redirect(url_for('patient_portal.dashboard'))
        else:
            flash('Invalid email or password. Please try again.', 'danger')
    
    return render_template('auth/login.html', form=form)


@auth_bp.route('/simple-login', methods=['GET', 'POST'])
def simple_login():
    """Simple login page for testing."""
    if current_user.is_authenticated:
        # Redirect based on role
        if current_user.is_admin():
            return redirect(url_for('dashboard.index'))
        elif current_user.is_doctor():
            return redirect(url_for('doctor_portal.dashboard'))
        else:
            return redirect(url_for('patient_portal.dashboard'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        email = form.email.data.lower().strip()
        password = form.password.data
        
        # Find user
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            if not user.is_active:
                flash('Your account has been deactivated. Please contact support.', 'danger')
                return redirect(url_for('auth.simple_login'))
            
            # Login user
            login_user(user, remember=form.remember_me.data)
            user.update_last_login()
            
            # Redirect based on role
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            
            if user.is_admin():
                flash(f'Welcome back, {user.name}!', 'success')
                return redirect(url_for('dashboard.index'))
            elif user.is_doctor():
                flash(f'Welcome back, Dr. {user.name}!', 'success')
                return redirect(url_for('doctor_portal.dashboard'))
            else:
                flash(f'Welcome back, {user.name}!', 'success')
                return redirect(url_for('patient_portal.dashboard'))
        else:
            flash('Invalid email or password. Please try again.', 'danger')
    
    return render_template('auth/simple_login.html', form=form)


@auth_bp.route('/help')
def help():
    """Help page with navigation and troubleshooting."""
    return render_template('help.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Patient registration page (users only, not admins)."""
    if current_user.is_authenticated:
        return redirect(url_for('patient_portal.dashboard'))
    
    form = RegistrationForm()
    
    if form.validate_on_submit():
        # Create patient record first
        patient = Patient(
            patient_id=f"P-{Patient.query.count() + 1:06d}",
            name=form.name.data,
            age=0,  # Can be updated later
            gender="Other",  # Can be updated later
            phone=form.phone.data,
        )
        db.session.add(patient)
        db.session.flush()
        
        # Create user account
        user = User(
            name=form.name.data,
            email=form.email.data.lower().strip(),
            phone=form.phone.data,
            role='user',
            patient_id=patient.id
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login with your credentials.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)


@auth_bp.route('/logout')
def logout():
    """Logout current user."""
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Forgot password page."""
    if current_user.is_authenticated:
        return redirect(url_for('patient_portal.dashboard'))
    
    form = ForgotPasswordForm()
    
    if form.validate_on_submit():
        email = form.email.data.lower().strip()
        user = User.query.filter_by(email=email).first()
        
        if user:
            # Generate reset token
            token = AuthService.generate_reset_token(user)
            
            # In production, send email with reset link
            # For now, just show the token (in console)
            reset_url = url_for('auth.reset_password', token=token, _external=True)
            print(f"\n{'='*60}")
            print(f"PASSWORD RESET LINK FOR: {user.email}")
            print(f"{'='*60}")
            print(f"{reset_url}")
            print(f"{'='*60}\n")
            
            flash('Password reset instructions have been sent to your email.', 'info')
        else:
            # Don't reveal if email exists or not (security)
            flash('If that email exists, password reset instructions have been sent.', 'info')
        
        return redirect(url_for('auth.login'))
    
    return render_template('auth/forgot_password.html', form=form)


@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Reset password with token."""
    if current_user.is_authenticated:
        return redirect(url_for('patient_portal.dashboard'))
    
    user = AuthService.verify_reset_token(token)
    if not user:
        flash('Invalid or expired reset link.', 'danger')
        return redirect(url_for('auth.forgot_password'))
    
    form = ResetPasswordForm()
    
    if form.validate_on_submit():
        user.set_password(form.password.data)
        AuthService.mark_token_used(token)
        db.session.commit()
        
        flash('Your password has been reset successfully. Please login.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password.html', form=form, token=token)
