"""
Patient Portal routes - User-friendly interface for patients.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import current_user
from datetime import date, datetime, timedelta
from app import db
from app.models.models import Appointment, Patient, Doctor, Department
from app.services.slot_optimizer import SlotOptimizer
from app.services.sms_service import SMSService
from app.services.auth_service import user_required

patient_portal_bp = Blueprint("patient_portal", __name__)


@patient_portal_bp.route("/")
def home():
    """Patient portal home page - public landing."""
    return render_template("patient/home.html")


@patient_portal_bp.route("/dashboard")
@user_required
def dashboard():
    """Patient dashboard - shows user's appointments."""
    if not current_user.patient:
        flash("Please complete your profile to view appointments.", "warning")
        return redirect(url_for("patient_portal.home"))
    
    patient = current_user.patient
    today = date.today()
    
    # Get upcoming appointments
    upcoming = Appointment.query.filter(
        Appointment.patient_id == patient.id,
        Appointment.appointment_date >= today,
        Appointment.status.in_(["scheduled", "checked_in"])
    ).order_by(Appointment.appointment_date, Appointment.appointment_time).all()
    
    # Get past appointments
    past = Appointment.query.filter(
        Appointment.patient_id == patient.id,
        Appointment.appointment_date < today
    ).order_by(Appointment.appointment_date.desc()).limit(5).all()
    
    # Get today's appointments
    today_appts = Appointment.query.filter(
        Appointment.patient_id == patient.id,
        Appointment.appointment_date == today
    ).order_by(Appointment.appointment_time).all()
    
    return render_template(
        "patient/dashboard.html",
        patient=patient,
        upcoming=upcoming,
        past=past,
        today_appts=today_appts
    )


@patient_portal_bp.route("/book", methods=["GET", "POST"])
@user_required
def book():
    """Patient self-booking interface."""
    if request.method == "POST":
        # Use logged-in user's patient record
        if not current_user.patient:
            flash("Please complete your profile first.", "warning")
            return redirect(url_for("patient_portal.dashboard"))
        
        patient = current_user.patient
        
        # Get booking details
        department_id = int(request.form.get("department_id"))
        doctor_id = int(request.form.get("doctor_id"))
        appt_date = date.fromisoformat(request.form.get("appointment_date"))
        appt_time_str = request.form.get("appointment_time")
        symptoms = request.form.get("symptoms", "")
        
        # Parse time
        appt_time = datetime.strptime(appt_time_str, "%H:%M").time()
        
        # Check if slot is available
        existing = Appointment.query.filter(
            Appointment.doctor_id == doctor_id,
            Appointment.appointment_date == appt_date,
            Appointment.appointment_time == appt_time,
            Appointment.status.in_(["scheduled", "checked_in", "in_progress"]),
        ).first()
        
        if existing:
            flash("Sorry, this time slot is no longer available. Please choose another.", "warning")
            return redirect(url_for("patient_portal.book", 
                                  doctor_id=doctor_id, 
                                  date=appt_date.isoformat()))
        
        # Create appointment using logged-in user's patient record
        end_time = (datetime.combine(appt_date, appt_time) + timedelta(minutes=15)).time()
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
        
        # Get doctor and department for SMS
        doctor = Doctor.query.get(doctor_id)
        department = Department.query.get(department_id)
        
        # Send SMS confirmation
        sms_result = SMSService.send_appointment_confirmation(
            patient, appointment, doctor, department
        )
        
        # Store appointment ID in session for confirmation page
        session['last_appointment_id'] = appointment.id
        
        flash("Appointment booked successfully! SMS confirmation sent to your phone.", "success")
        return redirect(url_for("patient_portal.confirmation"))
    
    # GET request - show booking form
    departments = Department.query.filter_by(is_active=True).all()
    doctors = Doctor.query.filter_by(is_available=True).all()
    
    optimizer = SlotOptimizer()
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
        # Filter out booked slots for patient view
        slots = [s for s in slots if not s.get("is_booked", False)]
    
    return render_template(
        "patient/book.html",
        departments=departments,
        doctors=doctors,
        slots=slots,
        selected_doctor_id=selected_doctor_id,
        selected_date=selected_date,
    )


@patient_portal_bp.route("/confirmation")
@user_required
def confirmation():
    """Show appointment confirmation details."""
    appointment_id = session.get('last_appointment_id')
    if not appointment_id:
        flash("No recent appointment found.", "warning")
        return redirect(url_for("patient_portal.home"))
    
    appointment = Appointment.query.get(appointment_id)
    if not appointment:
        flash("Appointment not found.", "danger")
        return redirect(url_for("patient_portal.home"))
    
    return render_template("patient/confirmation.html", appointment=appointment)


@patient_portal_bp.route("/check-status", methods=["GET", "POST"])
def check_status():
    """Check appointment status by phone number."""
    if request.method == "POST":
        phone = request.form.get("phone", "").strip()
        appt_number = request.form.get("appointment_number", "").strip()
        
        if not phone:
            flash("Please provide your phone number.", "warning")
            return redirect(url_for("patient_portal.check_status"))
        
        # Find patient by phone
        patient = Patient.query.filter_by(phone=phone).first()
        if not patient:
            flash("No appointments found for this phone number.", "warning")
            return redirect(url_for("patient_portal.check_status"))
        
        # Get appointments
        query = Appointment.query.filter_by(patient_id=patient.id)
        if appt_number:
            query = query.filter_by(appointment_number=appt_number)
        
        appointments = query.order_by(Appointment.appointment_date.desc()).all()
        
        if not appointments:
            flash("No appointments found.", "warning")
            return redirect(url_for("patient_portal.check_status"))
        
        return render_template("patient/status.html", 
                             patient=patient, 
                             appointments=appointments)
    
    return render_template("patient/check_status.html")
