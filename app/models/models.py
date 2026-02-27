"""
Database models for the Smart Hospital Queue system.
"""
from datetime import datetime, date, time
from app import db


class Department(db.Model):
    """Hospital departments / OPD sections."""
    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    floor = db.Column(db.Integer, default=1)
    max_capacity = db.Column(db.Integer, default=50)
    avg_consultation_min = db.Column(db.Integer, default=15)
    is_active = db.Column(db.Boolean, default=True)

    # Relationships
    doctors = db.relationship("Doctor", backref="department", lazy="dynamic")
    appointments = db.relationship("Appointment", backref="department", lazy="dynamic")

    def __repr__(self):
        return f"<Department {self.name}>"


class Doctor(db.Model):
    """Doctor profiles."""
    __tablename__ = "doctors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"), nullable=False)
    experience_years = db.Column(db.Integer, default=0)
    avg_consultation_min = db.Column(db.Integer, default=15)
    max_patients_per_day = db.Column(db.Integer, default=40)
    is_available = db.Column(db.Boolean, default=True)
    shift_start = db.Column(db.Time, default=time(8, 0))
    shift_end = db.Column(db.Time, default=time(17, 0))
    rating = db.Column(db.Float, default=4.0)

    # Relationships
    appointments = db.relationship("Appointment", backref="doctor", lazy="dynamic")

    def __repr__(self):
        return f"<Doctor {self.name} - {self.specialization}>"

    @property
    def today_patient_count(self):
        today = date.today()
        return Appointment.query.filter(
            Appointment.doctor_id == self.id,
            Appointment.appointment_date == today,
            Appointment.status.in_(["scheduled", "waiting", "checked_in", "in_progress"]),
        ).count()

    @property
    def availability_percentage(self):
        count = self.today_patient_count
        if self.max_patients_per_day == 0:
            return 0
        return max(0, 100 - (count / self.max_patients_per_day * 100))


class Patient(db.Model):
    """Patient records."""
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.String(20), unique=True, nullable=False)   # e.g. P-20240101-001
    name = db.Column(db.String(150), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(15))
    email = db.Column(db.String(120))
    blood_group = db.Column(db.String(5))
    medical_history = db.Column(db.Text, default="")
    is_emergency = db.Column(db.Boolean, default=False)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    appointments = db.relationship("Appointment", backref="patient", lazy="dynamic")
    queue_entries = db.relationship("QueueEntry", backref="patient", lazy="dynamic")

    def __repr__(self):
        return f"<Patient {self.patient_id} - {self.name}>"


class Appointment(db.Model):
    """Appointment bookings."""
    __tablename__ = "appointments"

    id = db.Column(db.Integer, primary_key=True)
    appointment_number = db.Column(db.String(20), unique=True, nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.Time, nullable=False)
    slot_end_time = db.Column(db.Time, nullable=False)
    status = db.Column(
        db.String(20), default="scheduled"
    )  # scheduled, checked_in, in_progress, completed, cancelled, no_show
    priority_score = db.Column(db.Float, default=0.0)
    estimated_wait_min = db.Column(db.Integer, default=0)
    actual_wait_min = db.Column(db.Integer, nullable=True)
    symptoms = db.Column(db.Text, default="")
    notes = db.Column(db.Text, default="")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    checked_in_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"<Appointment {self.appointment_number} - {self.status}>"


class QueueEntry(db.Model):
    """Real-time queue tracking."""
    __tablename__ = "queue_entries"

    id = db.Column(db.Integer, primary_key=True)
    token_number = db.Column(db.String(10), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"), nullable=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey("appointments.id"), nullable=True)
    queue_date = db.Column(db.Date, default=date.today)
    position = db.Column(db.Integer, nullable=False)
    priority_score = db.Column(db.Float, default=0.0)
    status = db.Column(
        db.String(20), default="waiting"
    )  # waiting, called, in_progress, completed, skipped
    entered_at = db.Column(db.DateTime, default=datetime.utcnow)
    called_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    estimated_wait_min = db.Column(db.Integer, default=0)

    # Relationships
    department = db.relationship("Department", backref="queue_entries")
    doctor = db.relationship("Doctor", backref="queue_entries")
    appointment = db.relationship("Appointment", backref="queue_entry")

    def __repr__(self):
        return f"<QueueEntry {self.token_number} - Position {self.position}>"


class CrowdLog(db.Model):
    """Historical crowd data for ML training."""
    __tablename__ = "crowd_logs"

    id = db.Column(db.Integer, primary_key=True)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"), nullable=False)
    log_date = db.Column(db.Date, nullable=False)
    hour = db.Column(db.Integer, nullable=False)  # 0-23
    day_of_week = db.Column(db.Integer, nullable=False)  # 0=Mon, 6=Sun
    month = db.Column(db.Integer, nullable=False)
    is_holiday = db.Column(db.Boolean, default=False)
    patient_count = db.Column(db.Integer, default=0)
    avg_wait_time = db.Column(db.Float, default=0.0)
    crowd_level = db.Column(
        db.String(10), default="low"
    )  # low, medium, high, critical
    weather = db.Column(db.String(20), default="clear")
    temperature = db.Column(db.Float, default=25.0)

    department = db.relationship("Department", backref="crowd_logs")

    def __repr__(self):
        return f"<CrowdLog {self.log_date} H{self.hour} - {self.crowd_level}>"


class Notification(db.Model):
    """System notifications and alerts."""
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(20), default="info")  # info, warning, critical, success
    target = db.Column(db.String(50), default="all")  # all, department, patient
    target_id = db.Column(db.Integer, nullable=True)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Notification {self.title}>"
