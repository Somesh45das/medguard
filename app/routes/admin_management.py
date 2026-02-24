"""
Admin management routes - CRUD operations for doctors and departments.
Requires admin authentication.
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user
from datetime import time
from app import db
from app.models.models import Doctor, Department
from app.forms import DoctorForm, DepartmentForm
from app.services.auth_service import admin_required

admin_mgmt_bp = Blueprint('admin_mgmt', __name__)


# ==================== DOCTOR MANAGEMENT ====================

@admin_mgmt_bp.route('/doctors')
@admin_required
def list_doctors():
    """List all doctors (admin only)."""
    doctors = Doctor.query.order_by(Doctor.department_id, Doctor.name).all()
    return render_template('admin/doctors_list.html', doctors=doctors)


@admin_mgmt_bp.route('/doctors/add', methods=['GET', 'POST'])
@admin_required
def add_doctor():
    """Add new doctor (admin only)."""
    form = DoctorForm()
    
    # Populate department choices
    departments = Department.query.filter_by(is_active=True).all()
    form.department_id.choices = [(d.id, d.name) for d in departments]
    
    if form.validate_on_submit():
        doctor = Doctor(
            name=form.name.data,
            specialization=form.specialization.data,
            department_id=form.department_id.data,
            experience_years=form.experience_years.data,
            avg_consultation_min=form.avg_consultation_min.data,
            max_patients_per_day=form.max_patients_per_day.data,
            shift_start=form.shift_start.data,
            shift_end=form.shift_end.data,
            rating=form.rating.data or 4.0,
            is_available=form.is_available.data
        )
        
        db.session.add(doctor)
        db.session.commit()
        
        flash(f'Doctor {doctor.name} added successfully!', 'success')
        return redirect(url_for('admin_mgmt.list_doctors'))
    
    return render_template('admin/doctor_form.html', form=form, title='Add Doctor')


@admin_mgmt_bp.route('/doctors/edit/<int:doctor_id>', methods=['GET', 'POST'])
@admin_required
def edit_doctor(doctor_id):
    """Edit doctor details (admin only)."""
    doctor = Doctor.query.get_or_404(doctor_id)
    form = DoctorForm(obj=doctor)
    
    # Populate department choices
    departments = Department.query.filter_by(is_active=True).all()
    form.department_id.choices = [(d.id, d.name) for d in departments]
    
    if form.validate_on_submit():
        doctor.name = form.name.data
        doctor.specialization = form.specialization.data
        doctor.department_id = form.department_id.data
        doctor.experience_years = form.experience_years.data
        doctor.avg_consultation_min = form.avg_consultation_min.data
        doctor.max_patients_per_day = form.max_patients_per_day.data
        doctor.shift_start = form.shift_start.data
        doctor.shift_end = form.shift_end.data
        doctor.rating = form.rating.data or doctor.rating
        doctor.is_available = form.is_available.data
        
        db.session.commit()
        
        flash(f'Doctor {doctor.name} updated successfully!', 'success')
        return redirect(url_for('admin_mgmt.list_doctors'))
    
    return render_template('admin/doctor_form.html', form=form, title='Edit Doctor', doctor=doctor)


@admin_mgmt_bp.route('/doctors/delete/<int:doctor_id>', methods=['POST'])
@admin_required
def delete_doctor(doctor_id):
    """Delete doctor (admin only)."""
    doctor = Doctor.query.get_or_404(doctor_id)
    
    # Check if doctor has appointments
    if doctor.appointments.count() > 0:
        flash(f'Cannot delete Dr. {doctor.name}. Doctor has existing appointments.', 'danger')
        return redirect(url_for('admin_mgmt.list_doctors'))
    
    name = doctor.name
    db.session.delete(doctor)
    db.session.commit()
    
    flash(f'Doctor {name} deleted successfully.', 'success')
    return redirect(url_for('admin_mgmt.list_doctors'))


@admin_mgmt_bp.route('/doctors/toggle-availability/<int:doctor_id>', methods=['POST'])
@admin_required
def toggle_doctor_availability(doctor_id):
    """Toggle doctor availability (admin only)."""
    doctor = Doctor.query.get_or_404(doctor_id)
    doctor.is_available = not doctor.is_available
    db.session.commit()
    
    status = "available" if doctor.is_available else "unavailable"
    flash(f'Dr. {doctor.name} is now {status}.', 'info')
    return redirect(url_for('admin_mgmt.list_doctors'))


# ==================== DEPARTMENT MANAGEMENT ====================

@admin_mgmt_bp.route('/departments')
@admin_required
def list_departments():
    """List all departments (admin only)."""
    departments = Department.query.order_by(Department.name).all()
    return render_template('admin/departments_list.html', departments=departments)


@admin_mgmt_bp.route('/departments/add', methods=['GET', 'POST'])
@admin_required
def add_department():
    """Add new department (admin only)."""
    form = DepartmentForm()
    
    if form.validate_on_submit():
        department = Department(
            name=form.name.data,
            floor=form.floor.data,
            max_capacity=form.max_capacity.data,
            avg_consultation_min=form.avg_consultation_min.data,
            is_active=form.is_active.data
        )
        
        db.session.add(department)
        db.session.commit()
        
        flash(f'Department {department.name} added successfully!', 'success')
        return redirect(url_for('admin_mgmt.list_departments'))
    
    return render_template('admin/department_form.html', form=form, title='Add Department')


@admin_mgmt_bp.route('/departments/edit/<int:dept_id>', methods=['GET', 'POST'])
@admin_required
def edit_department(dept_id):
    """Edit department details (admin only)."""
    department = Department.query.get_or_404(dept_id)
    form = DepartmentForm(obj=department)
    
    if form.validate_on_submit():
        department.name = form.name.data
        department.floor = form.floor.data
        department.max_capacity = form.max_capacity.data
        department.avg_consultation_min = form.avg_consultation_min.data
        department.is_active = form.is_active.data
        
        db.session.commit()
        
        flash(f'Department {department.name} updated successfully!', 'success')
        return redirect(url_for('admin_mgmt.list_departments'))
    
    return render_template('admin/department_form.html', form=form, title='Edit Department', department=department)


@admin_mgmt_bp.route('/departments/delete/<int:dept_id>', methods=['POST'])
@admin_required
def delete_department(dept_id):
    """Delete department (admin only)."""
    department = Department.query.get_or_404(dept_id)
    
    # Check if department has doctors
    if department.doctors.count() > 0:
        flash(f'Cannot delete {department.name}. Department has doctors assigned.', 'danger')
        return redirect(url_for('admin_mgmt.list_departments'))
    
    name = department.name
    db.session.delete(department)
    db.session.commit()
    
    flash(f'Department {name} deleted successfully.', 'success')
    return redirect(url_for('admin_mgmt.list_departments'))


@admin_mgmt_bp.route('/departments/toggle-status/<int:dept_id>', methods=['POST'])
@admin_required
def toggle_department_status(dept_id):
    """Toggle department active status (admin only)."""
    department = Department.query.get_or_404(dept_id)
    department.is_active = not department.is_active
    db.session.commit()
    
    status = "active" if department.is_active else "inactive"
    flash(f'{department.name} is now {status}.', 'info')
    return redirect(url_for('admin_mgmt.list_departments'))
