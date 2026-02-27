"""
Doctor portal routes for appointment management.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import current_user
from datetime import date, datetime, timedelta
from sqlalchemy import and_, or_
from app import db
from app.models.models import Doctor, Appointment, Patient, QueueEntry, Department
from app.services.auth_service import doctor_required
from app.services.priority_scorer import PriorityScorer
from app.services.sms_service import SMSService

doctor_portal_bp = Blueprint("doctor_portal", __name__, url_prefix="/doctor")


@doctor_portal_bp.route("/dashboard")
@doctor_required
def dashboard():
    """Doctor dashboard showing today's appointments and statistics."""
    if not current_user.doctor:
        flash("No doctor profile linked to your account.", "danger")
        return redirect(url_for("dashboard.index"))
    
    doctor = current_user.doctor
    today = date.today()
    
    # Get today's appointments (all statuses except cancelled)
    today_appointments = Appointment.query.filter(
        Appointment.doctor_id == doctor.id,
        Appointment.appointment_date == today,
        Appointment.status != "cancelled"
    ).order_by(Appointment.appointment_time).all()
    
    # Statistics
    total_today = len(today_appointments)
    completed = len([a for a in today_appointments if a.status == "completed"])
    in_progress = len([a for a in today_appointments if a.status == "in_progress"])
    scheduled = len([a for a in today_appointments if a.status in ["scheduled", "waiting"]])
    checked_in = len([a for a in today_appointments if a.status == "checked_in"])
    
    # Current queue
    current_queue = QueueEntry.query.filter(
        QueueEntry.doctor_id == doctor.id,
        QueueEntry.queue_date == today,
        QueueEntry.status.in_(["waiting", "called"])
    ).order_by(QueueEntry.priority_score.desc(), QueueEntry.position).all()
    
    # Next patient
    next_patient = current_queue[0] if current_queue else None
    
    # Upcoming appointments (next 7 days)
    upcoming = Appointment.query.filter(
        Appointment.doctor_id == doctor.id,
        Appointment.appointment_date > today,
        Appointment.appointment_date <= today + timedelta(days=7),
        Appointment.status == "scheduled"
    ).order_by(Appointment.appointment_date, Appointment.appointment_time).limit(5).all()
    
    return render_template(
        "doctor/dashboard.html",
        doctor=doctor,
        today_appointments=today_appointments,
        total_today=total_today,
        completed=completed,
        in_progress=in_progress,
        scheduled=scheduled,
        checked_in=checked_in,
        current_queue=current_queue,
        next_patient=next_patient,
        upcoming=upcoming,
        today=today
    )


@doctor_portal_bp.route("/appointments")
@doctor_required
def appointments():
    """View all appointments with filtering."""
    if not current_user.doctor:
        flash("No doctor profile linked to your account.", "danger")
        return redirect(url_for("dashboard.index"))
    
    doctor = current_user.doctor
    
    # Get filter parameters
    status_filter = request.args.get("status", "all")
    date_filter = request.args.get("date", "today")
    
    # Base query
    query = Appointment.query.filter(Appointment.doctor_id == doctor.id)
    
    # Apply date filter
    today = date.today()
    if date_filter == "today":
        query = query.filter(Appointment.appointment_date == today)
    elif date_filter == "week":
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        query = query.filter(
            Appointment.appointment_date >= week_start,
            Appointment.appointment_date <= week_end
        )
    elif date_filter == "month":
        query = query.filter(
            db.extract("year", Appointment.appointment_date) == today.year,
            db.extract("month", Appointment.appointment_date) == today.month
        )
    
    # Apply status filter
    if status_filter != "all":
        query = query.filter(Appointment.status == status_filter)
    
    # Get appointments
    appointments = query.order_by(
        Appointment.appointment_date.desc(),
        Appointment.appointment_time.desc()
    ).all()
    
    # Statistics
    stats = {
        "total": len(appointments),
        "scheduled": len([a for a in appointments if a.status == "scheduled"]),
        "checked_in": len([a for a in appointments if a.status == "checked_in"]),
        "in_progress": len([a for a in appointments if a.status == "in_progress"]),
        "completed": len([a for a in appointments if a.status == "completed"]),
        "cancelled": len([a for a in appointments if a.status == "cancelled"]),
        "no_show": len([a for a in appointments if a.status == "no_show"])
    }
    
    return render_template(
        "doctor/appointments.html",
        doctor=doctor,
        appointments=appointments,
        stats=stats,
        status_filter=status_filter,
        date_filter=date_filter
    )


@doctor_portal_bp.route("/appointment/<int:appointment_id>")
@doctor_required
def appointment_detail(appointment_id):
    """View detailed appointment information."""
    if not current_user.doctor:
        flash("No doctor profile linked to your account.", "danger")
        return redirect(url_for("dashboard.index"))
    
    appointment = Appointment.query.get_or_404(appointment_id)
    
    # Verify this appointment belongs to the logged-in doctor
    if appointment.doctor_id != current_user.doctor.id:
        flash("Access denied. This appointment does not belong to you.", "danger")
        return redirect(url_for("doctor_portal.dashboard"))
    
    # Get patient's appointment history
    patient_history = Appointment.query.filter(
        Appointment.patient_id == appointment.patient_id,
        Appointment.id != appointment.id,
        Appointment.status == "completed"
    ).order_by(Appointment.appointment_date.desc()).limit(5).all()
    
    return render_template(
        "doctor/appointment_detail.html",
        appointment=appointment,
        patient_history=patient_history
    )


@doctor_portal_bp.route("/appointment/<int:appointment_id>/update-status", methods=["POST"])
@doctor_required
def update_appointment_status(appointment_id):
    """Update appointment status."""
    if not current_user.doctor:
        return jsonify({"success": False, "message": "No doctor profile linked"}), 403
    
    appointment = Appointment.query.get_or_404(appointment_id)
    
    # Verify this appointment belongs to the logged-in doctor
    if appointment.doctor_id != current_user.doctor.id:
        return jsonify({"success": False, "message": "Access denied"}), 403
    
    new_status = request.form.get("status")
    notes = request.form.get("notes", "")
    
    if new_status not in ["scheduled", "checked_in", "in_progress", "completed", "cancelled", "no_show"]:
        return jsonify({"success": False, "message": "Invalid status"}), 400
    
    old_status = appointment.status
    appointment.status = new_status
    
    if notes:
        appointment.notes = notes
    
    # Update timestamps
    if new_status == "checked_in" and not appointment.checked_in_at:
        appointment.checked_in_at = datetime.utcnow()
    elif new_status == "completed" and not appointment.completed_at:
        appointment.completed_at = datetime.utcnow()
        
        # Calculate actual wait time
        if appointment.checked_in_at:
            wait_delta = appointment.completed_at - appointment.checked_in_at
            appointment.actual_wait_min = int(wait_delta.total_seconds() / 60)
    
    # Update queue entry if exists
    queue_entry = QueueEntry.query.filter_by(appointment_id=appointment.id).first()
    if queue_entry:
        if new_status == "in_progress":
            queue_entry.status = "in_progress"
            queue_entry.called_at = datetime.utcnow()
        elif new_status == "completed":
            queue_entry.status = "completed"
            queue_entry.completed_at = datetime.utcnow()
    
    db.session.commit()
    
    flash(f"Appointment status updated to {new_status}.", "success")
    return jsonify({"success": True, "message": f"Status updated to {new_status}"})


@doctor_portal_bp.route("/appointment/<int:appointment_id>/add-notes", methods=["POST"])
@doctor_required
def add_appointment_notes(appointment_id):
    """Add or update appointment notes."""
    if not current_user.doctor:
        return jsonify({"success": False, "message": "No doctor profile linked"}), 403
    
    appointment = Appointment.query.get_or_404(appointment_id)
    
    # Verify this appointment belongs to the logged-in doctor
    if appointment.doctor_id != current_user.doctor.id:
        return jsonify({"success": False, "message": "Access denied"}), 403
    
    notes = request.form.get("notes", "")
    appointment.notes = notes
    db.session.commit()
    
    flash("Notes saved successfully.", "success")
    return jsonify({"success": True, "message": "Notes saved"})


@doctor_portal_bp.route("/queue")
@doctor_required
def queue():
    """View current queue for the doctor."""
    if not current_user.doctor:
        flash("No doctor profile linked to your account.", "danger")
        return redirect(url_for("dashboard.index"))
    
    doctor = current_user.doctor
    today = date.today()
    
    # Get current queue
    queue_entries = QueueEntry.query.filter(
        QueueEntry.doctor_id == doctor.id,
        QueueEntry.queue_date == today
    ).order_by(
        QueueEntry.status.desc(),  # in_progress first
        QueueEntry.priority_score.desc(),
        QueueEntry.position
    ).all()
    
    # Separate by status
    in_progress = [q for q in queue_entries if q.status == "in_progress"]
    waiting = [q for q in queue_entries if q.status in ["waiting", "called"]]
    completed = [q for q in queue_entries if q.status == "completed"]
    
    return render_template(
        "doctor/queue.html",
        doctor=doctor,
        in_progress=in_progress,
        waiting=waiting,
        completed=completed,
        total_waiting=len(waiting)
    )


@doctor_portal_bp.route("/queue/<int:queue_id>/call-next", methods=["POST"])
@doctor_required
def call_next_patient(queue_id):
    """Call the next patient from queue."""
    if not current_user.doctor:
        return jsonify({"success": False, "message": "No doctor profile linked"}), 403
    
    queue_entry = QueueEntry.query.get_or_404(queue_id)
    
    # Verify this queue entry belongs to the logged-in doctor
    if queue_entry.doctor_id != current_user.doctor.id:
        return jsonify({"success": False, "message": "Access denied"}), 403
    
    # Update status
    queue_entry.status = "called"
    queue_entry.called_at = datetime.utcnow()
    
    # Update appointment if linked
    if queue_entry.appointment:
        queue_entry.appointment.status = "in_progress"
    
    db.session.commit()
    
    flash(f"Patient {queue_entry.patient.name} has been called.", "success")
    return jsonify({
        "success": True,
        "message": f"Patient {queue_entry.patient.name} called",
        "token": queue_entry.token_number
    })


@doctor_portal_bp.route("/schedule")
@doctor_required
def schedule():
    """View weekly schedule."""
    if not current_user.doctor:
        flash("No doctor profile linked to your account.", "danger")
        return redirect(url_for("dashboard.index"))
    
    doctor = current_user.doctor
    
    # Get week parameter or default to current week
    week_offset = int(request.args.get("week", 0))
    today = date.today()
    week_start = today - timedelta(days=today.weekday()) + timedelta(weeks=week_offset)
    week_end = week_start + timedelta(days=6)
    
    # Get appointments for the week
    appointments = Appointment.query.filter(
        Appointment.doctor_id == doctor.id,
        Appointment.appointment_date >= week_start,
        Appointment.appointment_date <= week_end
    ).order_by(Appointment.appointment_date, Appointment.appointment_time).all()
    
    # Organize by day
    schedule_by_day = {}
    for i in range(7):
        day = week_start + timedelta(days=i)
        schedule_by_day[day] = [a for a in appointments if a.appointment_date == day]
    
    return render_template(
        "doctor/schedule.html",
        doctor=doctor,
        schedule_by_day=schedule_by_day,
        week_start=week_start,
        week_end=week_end,
        week_offset=week_offset
    )


@doctor_portal_bp.route("/profile")
@doctor_required
def profile():
    """View and edit doctor profile."""
    if not current_user.doctor:
        flash("No doctor profile linked to your account.", "danger")
        return redirect(url_for("dashboard.index"))
    
    doctor = current_user.doctor
    
    # Get statistics
    total_appointments = Appointment.query.filter_by(doctor_id=doctor.id).count()
    completed_appointments = Appointment.query.filter_by(
        doctor_id=doctor.id,
        status="completed"
    ).count()
    
    # Calculate average consultation time
    completed_with_time = Appointment.query.filter(
        Appointment.doctor_id == doctor.id,
        Appointment.status == "completed",
        Appointment.actual_wait_min.isnot(None)
    ).all()
    
    avg_consultation = 0
    if completed_with_time:
        avg_consultation = sum(a.actual_wait_min for a in completed_with_time) / len(completed_with_time)
    
    return render_template(
        "doctor/profile.html",
        doctor=doctor,
        total_appointments=total_appointments,
        completed_appointments=completed_appointments,
        avg_consultation=round(avg_consultation, 1)
    )
