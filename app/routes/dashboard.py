"""
Dashboard routes – main overview page.
"""
from flask import Blueprint, render_template
from datetime import date, datetime
from app.models.models import (
    Department, Doctor, Patient, Appointment, QueueEntry, Notification,
)
from app.services.crowd_predictor import CrowdPredictor
from app.services.queue_manager import QueueManager
from app.services.auth_service import admin_required

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
@admin_required
def index():
    """Main dashboard page."""
    today = date.today()
    now = datetime.now()

    predictor = CrowdPredictor()
    queue_mgr = QueueManager()

    # Department-wise crowd levels
    departments = Department.query.filter_by(is_active=True).all()
    dept_crowds = []
    for dept in departments:
        crowd = predictor.predict_crowd_level(dept.id, today, now.hour)
        stats = queue_mgr.get_queue_stats(dept.id)
        dept_crowds.append({
            "department": dept,
            "crowd": crowd,
            "stats": stats,
        })

    # Overall stats
    total_patients_today = Appointment.query.filter(
        Appointment.appointment_date == today
    ).count()
    total_waiting = QueueEntry.query.filter(
        QueueEntry.queue_date == today,
        QueueEntry.status == "waiting",
    ).count()
    total_completed = QueueEntry.query.filter(
        QueueEntry.queue_date == today,
        QueueEntry.status == "completed",
    ).count()
    active_doctors = Doctor.query.filter_by(is_available=True).count()

    overall_stats = queue_mgr.get_queue_stats()

    # Recent notifications
    notifications = Notification.query.order_by(
        Notification.created_at.desc()
    ).limit(5).all()
    unread_count = Notification.query.filter_by(is_read=False).count()

    return render_template(
        "dashboard.html",
        dept_crowds=dept_crowds,
        total_patients_today=total_patients_today,
        total_waiting=total_waiting,
        total_completed=total_completed,
        active_doctors=active_doctors,
        overall_stats=overall_stats,
        notifications=notifications,
        unread_count=unread_count,
        current_time=now.strftime("%I:%M %p"),
        current_date=today.strftime("%A, %B %d, %Y"),
    )
