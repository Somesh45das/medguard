"""
Queue management routes.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import date
from app import db
from app.models.models import Department, Doctor, Patient, QueueEntry
from app.services.queue_manager import QueueManager
from app.services.wait_time_estimator import WaitTimeEstimator
from app.services.priority_scorer import PriorityScorer
from app.services.auth_service import admin_required

queue_bp = Blueprint("queue", __name__)


@queue_bp.route("/")
@admin_required
def view_queue():
    """View queue for all departments or a specific one."""
    # Auto-sync today's appointments to queue
    _auto_sync_appointments()
    
    queue_mgr = QueueManager()
    wait_est = WaitTimeEstimator()
    priority_scorer = PriorityScorer()

    dept_id = request.args.get("department", type=int)
    departments = Department.query.filter_by(is_active=True).all()

    queue_data = []
    stats = {}

    if dept_id:
        # Single department view - get all statuses including completed
        entries = QueueEntry.query.filter(
            QueueEntry.department_id == dept_id,
            QueueEntry.queue_date == date.today()
        ).order_by(
            QueueEntry.status.desc(),  # completed last
            QueueEntry.priority_score.desc(),
            QueueEntry.position.asc()
        ).all()
        
        stats = queue_mgr.get_queue_stats(dept_id)

        for entry in entries:
            wait_info = wait_est.estimate(dept_id, entry.position, entry.doctor_id)
            priority_info = priority_scorer.get_priority_label(entry.priority_score)
            queue_data.append({
                "entry": entry,
                "wait": wait_info,
                "priority": priority_info,
            })
    else:
        # Show all departments
        for dept in departments:
            entries = QueueEntry.query.filter(
                QueueEntry.department_id == dept.id,
                QueueEntry.queue_date == date.today(),
                QueueEntry.status.in_(['waiting', 'called', 'in_progress'])
            ).order_by(
                QueueEntry.priority_score.desc(),
                QueueEntry.position.asc()
            ).all()
            
            dept_stats = queue_mgr.get_queue_stats(dept.id)
            dept_queue = []
            for entry in entries:
                wait_info = wait_est.estimate(dept.id, entry.position, entry.doctor_id)
                priority_info = priority_scorer.get_priority_label(entry.priority_score)
                dept_queue.append({
                    "entry": entry,
                    "wait": wait_info,
                    "priority": priority_info,
                })
            if dept_queue:
                queue_data.append({
                    "department": dept,
                    "queue": dept_queue,
                    "stats": dept_stats,
                })

        stats = queue_mgr.get_queue_stats()

    return render_template(
        "queue.html",
        queue_data=queue_data,
        departments=departments,
        stats=stats,
        selected_dept=dept_id,
        is_single_dept=dept_id is not None,
    )


def _auto_sync_appointments():
    """Automatically sync today's appointments to queue."""
    from app.models.models import Appointment
    
    today = date.today()
    queue_mgr = QueueManager()
    
    # Get today's appointments not yet in queue
    appointments = Appointment.query.filter(
        Appointment.appointment_date == today,
        Appointment.status.in_(['scheduled', 'confirmed'])
    ).all()
    
    for appt in appointments:
        # Check if already in queue
        existing = QueueEntry.query.filter_by(
            appointment_id=appt.id,
            queue_date=today
        ).first()
        
        if not existing:
            try:
                queue_mgr.add_to_queue(
                    patient_id=appt.patient_id,
                    department_id=appt.department_id,
                    doctor_id=appt.doctor_id,
                    appointment_id=appt.id,
                    symptoms=appt.symptoms
                )
                appt.status = 'waiting'
            except:
                pass  # Silently fail to avoid breaking the page
    
    db.session.commit()


@queue_bp.route("/add", methods=["POST"])
@admin_required
def add_to_queue():
    """Add a walk-in patient to queue."""
    queue_mgr = QueueManager()

    patient_name = request.form.get("patient_name", "").strip()
    patient_age = int(request.form.get("patient_age", 30))
    patient_gender = request.form.get("patient_gender", "Other")
    department_id = int(request.form.get("department_id"))
    doctor_id = request.form.get("doctor_id")
    symptoms = request.form.get("symptoms", "")
    is_emergency = request.form.get("is_emergency") == "on"

    # Create patient record
    pcount = Patient.query.count()
    patient = Patient(
        patient_id=f"W-{date.today().strftime('%Y%m%d')}-{pcount + 1:03d}",
        name=patient_name,
        age=patient_age,
        gender=patient_gender,
        is_emergency=is_emergency,
    )
    db.session.add(patient)
    db.session.flush()

    entry = queue_mgr.add_to_queue(
        patient_id=patient.id,
        department_id=department_id,
        doctor_id=int(doctor_id) if doctor_id else None,
        symptoms=symptoms,
    )

    flash(
        f"Token {entry.token_number} issued! Position: {entry.position}, "
        f"Est. wait: {entry.estimated_wait_min} min",
        "success",
    )
    return redirect(url_for("queue.view_queue", department=department_id))


@queue_bp.route("/call-next/<int:dept_id>", methods=["POST"])
@admin_required
def call_next(dept_id):
    """Call the next patient."""
    queue_mgr = QueueManager()
    doctor_id = request.form.get("doctor_id", type=int)
    entry = queue_mgr.call_next(dept_id, doctor_id)
    if entry:
        flash(f"Calling {entry.patient.name} – Token {entry.token_number}", "info")
    else:
        flash("No patients in queue.", "warning")
    return redirect(url_for("queue.view_queue", department=dept_id))


@queue_bp.route("/start/<int:queue_id>", methods=["POST"])
@admin_required
def start_consultation(queue_id):
    """Start consultation."""
    queue_mgr = QueueManager()
    entry = queue_mgr.start_consultation(queue_id)
    if entry:
        flash(f"Consultation started for {entry.patient.name}", "success")
    return redirect(url_for("queue.view_queue", department=entry.department_id if entry else ""))


@queue_bp.route("/complete/<int:queue_id>", methods=["POST"])
@admin_required
def complete_consultation(queue_id):
    """Complete consultation."""
    queue_mgr = QueueManager()
    entry = queue_mgr.complete_consultation(queue_id)
    if entry:
        flash(f"Consultation completed for {entry.patient.name}", "success")
        
        # Send follow-up SMS after completion
        if entry.appointment_id:
            from app.services.notification_manager import NotificationManager
            notif_mgr = NotificationManager()
            notif_mgr.send_followup_after_completion(entry.appointment_id)
    
    return redirect(url_for("queue.view_queue", department=entry.department_id if entry else ""))


@queue_bp.route("/skip/<int:queue_id>", methods=["POST"])
@admin_required
def skip_patient(queue_id):
    """Skip / no-show a patient."""
    queue_mgr = QueueManager()
    entry = queue_mgr.skip_patient(queue_id)
    if entry:
        flash(f"Patient {entry.patient.name} marked as skipped.", "warning")
    return redirect(url_for("queue.view_queue", department=entry.department_id if entry else ""))


@queue_bp.route("/sync-appointments")
@admin_required
def sync_appointments():
    """Manually sync today's appointments to queue."""
    from app.models.models import Appointment
    
    today = date.today()
    queue_mgr = QueueManager()
    
    # Get today's appointments not yet in queue
    appointments = Appointment.query.filter(
        Appointment.appointment_date == today,
        Appointment.status.in_(['scheduled', 'confirmed'])
    ).all()
    
    synced = 0
    for appt in appointments:
        # Check if already in queue
        existing = QueueEntry.query.filter_by(
            appointment_id=appt.id,
            queue_date=today
        ).first()
        
        if not existing:
            try:
                queue_mgr.add_to_queue(
                    patient_id=appt.patient_id,
                    department_id=appt.department_id,
                    doctor_id=appt.doctor_id,
                    appointment_id=appt.id,
                    symptoms=appt.symptoms
                )
                appt.status = 'waiting'
                synced += 1
            except Exception as e:
                flash(f"Error syncing {appt.patient.name}: {str(e)}", "danger")
    
    db.session.commit()
    
    if synced > 0:
        flash(f"✅ Synced {synced} appointment(s) to queue", "success")
    else:
        flash("All appointments are already in queue", "info")
    
    return redirect(url_for("queue.view_queue"))


@queue_bp.route("/patient/<int:patient_id>")
@admin_required
def patient_details(patient_id):
    """View detailed patient information."""
    from app.models.models import Appointment
    
    # Get patient
    patient = Patient.query.get_or_404(patient_id)
    
    # Get current queue entry (today's visit)
    today = date.today()
    current_queue = QueueEntry.query.filter_by(
        patient_id=patient_id,
        queue_date=today
    ).first()
    
    # Get priority info if in queue
    priority = None
    if current_queue:
        priority_scorer = PriorityScorer()
        priority = priority_scorer.get_priority_label(current_queue.priority_score)
    
    # Get appointment history (all appointments, ordered by date desc)
    appointments = Appointment.query.filter_by(
        patient_id=patient_id
    ).order_by(
        Appointment.appointment_date.desc(),
        Appointment.appointment_time.desc()
    ).all()
    
    return render_template(
        "patient_details.html",
        patient=patient,
        current_queue=current_queue,
        priority=priority,
        appointments=appointments
    )

