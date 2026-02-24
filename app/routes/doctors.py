"""
Doctor management routes.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import date
from app import db
from app.models.models import Doctor, Department, Appointment
from app.services.auth_service import admin_required

doctors_bp = Blueprint("doctors", __name__)


@doctors_bp.route("/")
@admin_required
def list_doctors():
    """List all doctors with availability status."""
    doctors = Doctor.query.order_by(Doctor.department_id, Doctor.name).all()
    departments = Department.query.filter_by(is_active=True).all()

    doctor_data = []
    for doc in doctors:
        today_count = doc.today_patient_count
        availability = doc.availability_percentage
        doctor_data.append({
            "doctor": doc,
            "today_count": today_count,
            "availability": round(availability, 1),
            "status_color": (
                "#28a745" if availability > 50
                else "#ffc107" if availability > 20
                else "#dc3545"
            ),
        })

    return render_template(
        "doctors.html",
        doctor_data=doctor_data,
        departments=departments,
    )


@doctors_bp.route("/toggle/<int:doc_id>", methods=["POST"])
@admin_required
def toggle_availability(doc_id):
    """Toggle doctor availability."""
    doc = Doctor.query.get_or_404(doc_id)
    doc.is_available = not doc.is_available
    db.session.commit()
    status = "available" if doc.is_available else "unavailable"
    flash(f"Dr. {doc.name} is now {status}.", "info")
    return redirect(url_for("doctors.list_doctors"))
