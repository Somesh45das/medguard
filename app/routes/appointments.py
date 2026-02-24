"""
Appointment management routes.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import date, datetime, time, timedelta
from app import db
from app.models.models import Appointment, Patient, Doctor, Department
from app.services.slot_optimizer import SlotOptimizer
from app.services.notification_service import NotificationService
from app.services.sms_service import SMSService
from app.services.auth_service import admin_required

appointments_bp = Blueprint("appointments", __name__)


@appointments_bp.route("/")
@admin_required
def list_appointments():
    """List today's appointments."""
    filter_date = request.args.get("date", date.today().isoformat())
    filter_dept = request.args.get("department", "")
    filter_status = request.args.get("status", "")

    try:
        target_date = date.fromisoformat(filter_date)
    except ValueError:
        target_date = date.today()

    query = Appointment.query.filter(Appointment.appointment_date == target_date)

    if filter_dept:
        query = query.filter(Appointment.department_id == int(filter_dept))
    if filter_status:
        query = query.filter(Appointment.status == filter_status)

    appointments = query.order_by(Appointment.appointment_time.asc()).all()
    departments = Department.query.filter_by(is_active=True).all()

    return render_template(
        "appointments.html",
        appointments=appointments,
        departments=departments,
        filter_date=target_date.isoformat(),
        filter_dept=filter_dept,
        filter_status=filter_status,
    )


@appointments_bp.route("/book", methods=["GET", "POST"])
@admin_required
def book_appointment():
    """Book a new appointment with slot optimization."""
    optimizer = SlotOptimizer()

    if request.method == "POST":
        # Process booking
        patient_name = request.form.get("patient_name", "").strip()
        patient_age = int(request.form.get("patient_age", 30))
        patient_gender = request.form.get("patient_gender", "Other")
        patient_phone = request.form.get("patient_phone", "")
        doctor_id = int(request.form.get("doctor_id"))
        department_id = int(request.form.get("department_id"))
        appt_date = date.fromisoformat(request.form.get("appointment_date"))
        appt_time_str = request.form.get("appointment_time")
        symptoms = request.form.get("symptoms", "")
        is_emergency = request.form.get("is_emergency") == "on"

        # Parse time
        appt_time = datetime.strptime(appt_time_str, "%H:%M").time()
        
        # Check if slot is already booked
        existing = Appointment.query.filter(
            Appointment.doctor_id == doctor_id,
            Appointment.appointment_date == appt_date,
            Appointment.appointment_time == appt_time,
            Appointment.status.in_(["scheduled", "checked_in", "in_progress"]),
        ).first()
        
        if existing:
            flash(
                f"⚠️ Time slot {appt_time_str} is already booked! Please choose another time.",
                "danger"
            )
            return redirect(url_for("appointments.book_appointment", 
                                  doctor_id=doctor_id, 
                                  date=appt_date.isoformat()))

        # Create or find patient
        patient_count = Patient.query.count()
        patient_id_str = f"P-{date.today().strftime('%Y%m%d')}-{patient_count + 1:03d}"

        patient = Patient(
            patient_id=patient_id_str,
            name=patient_name,
            age=patient_age,
            gender=patient_gender,
            phone=patient_phone,
            is_emergency=is_emergency,
        )
        db.session.add(patient)
        db.session.flush()

        end_time = (
            datetime.combine(appt_date, appt_time) + timedelta(minutes=15)
        ).time()

        # Create appointment
        appt_count = Appointment.query.filter(
            Appointment.appointment_date == appt_date
        ).count()
        appt_number = f"APT-{appt_date.strftime('%Y%m%d')}-{appt_count + 1:03d}"

        appointment = Appointment(
            appointment_number=appt_number,
            patient_id=patient.id,
            doctor_id=doctor_id,
            department_id=department_id,
            appointment_date=appt_date,
            appointment_time=appt_time,
            slot_end_time=end_time,
            symptoms=symptoms,
            status="scheduled",
        )
        db.session.add(appointment)
        db.session.commit()

        # Send SMS confirmation if phone number provided
        if patient_phone:
            doctor = Doctor.query.get(doctor_id)
            department = Department.query.get(department_id)
            SMSService.send_appointment_confirmation(patient, appointment, doctor, department)

        NotificationService.create(
            title="📅 New Appointment Booked",
            message=f"{patient_name} booked at {appt_time_str} with Dr. {appointment.doctor.name}",
            notif_type="success",
        )

        flash(
            f"Appointment booked successfully! Number: {appt_number}. SMS sent to {patient_phone if patient_phone else 'N/A'}", "success"
        )
        return redirect(url_for("appointments.list_appointments"))

    # GET – show form with slot suggestions
    departments = Department.query.filter_by(is_active=True).all()
    doctors = Doctor.query.filter_by(is_available=True).all()

    # Pre-calculate slots for first available doctor
    slots = []
    selected_doctor_id = request.args.get("doctor_id")
    selected_date = request.args.get("date")
    
    # Default to tomorrow if no date specified
    if not selected_date:
        selected_date = (date.today() + timedelta(days=1)).isoformat()

    try:
        target_date = date.fromisoformat(selected_date)
    except ValueError:
        target_date = date.today() + timedelta(days=1)

    if selected_doctor_id:
        slots = optimizer.get_available_slots(int(selected_doctor_id), target_date)

    return render_template(
        "book_appointment.html",
        departments=departments,
        doctors=doctors,
        slots=slots,
        selected_doctor_id=selected_doctor_id,
        selected_date=selected_date,
    )


@appointments_bp.route("/<int:appt_id>/cancel", methods=["POST"])
@admin_required
def cancel_appointment(appt_id):
    """Cancel an appointment."""
    appt = Appointment.query.get_or_404(appt_id)
    appt.status = "cancelled"
    db.session.commit()
    flash(f"Appointment {appt.appointment_number} cancelled.", "warning")
    return redirect(url_for("appointments.list_appointments"))


@appointments_bp.route("/<int:appt_id>/checkin", methods=["POST"])
@admin_required
def checkin(appt_id):
    """Check in a patient for their appointment."""
    appt = Appointment.query.get_or_404(appt_id)
    appt.status = "checked_in"
    appt.checked_in_at = datetime.utcnow()
    db.session.commit()
    flash(f"Patient {appt.patient.name} checked in!", "success")
    return redirect(url_for("appointments.list_appointments"))
