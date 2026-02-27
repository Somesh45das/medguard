"""
Notification management routes for admins.
"""
from flask import Blueprint, request, jsonify, flash, redirect, url_for
from app.services.notification_manager import NotificationManager
from app.services.auth_service import admin_required

notifications_bp = Blueprint("notifications", __name__)


@notifications_bp.route("/check-delays", methods=["POST"])
@admin_required
def check_delays():
    """Manually trigger delay notification check."""
    notif_mgr = NotificationManager()
    department_id = request.form.get("department_id", type=int)
    
    count = notif_mgr.check_and_send_delay_notifications(department_id)
    
    if count > 0:
        flash(f"✅ Sent {count} delay notification(s)", "success")
    else:
        flash("ℹ️ No delays detected", "info")
    
    return redirect(request.referrer or url_for("queue.view_queue"))


@notifications_bp.route("/check-congestion", methods=["POST"])
@admin_required
def check_congestion():
    """Manually trigger congestion alert check."""
    notif_mgr = NotificationManager()
    department_id = request.form.get("department_id", type=int)
    
    count = notif_mgr.check_and_send_congestion_alerts(department_id)
    
    if count > 0:
        flash(f"⚠️ Sent {count} congestion alert(s)", "warning")
    else:
        flash("ℹ️ No high congestion detected", "info")
    
    return redirect(request.referrer or url_for("queue.view_queue"))


@notifications_bp.route("/doctor-unavailable", methods=["POST"])
@admin_required
def notify_doctor_unavailable():
    """Notify patients when doctor becomes unavailable."""
    notif_mgr = NotificationManager()
    
    doctor_id = request.form.get("doctor_id", type=int)
    reason = request.form.get("reason", "emergency")
    alternative_doctor_id = request.form.get("alternative_doctor_id", type=int)
    
    if not doctor_id:
        flash("❌ Doctor ID required", "danger")
        return redirect(request.referrer or url_for("admin.doctors_list"))
    
    count = notif_mgr.notify_doctor_unavailable(
        doctor_id,
        reason,
        alternative_doctor_id=alternative_doctor_id
    )
    
    if count > 0:
        flash(f"📱 Notified {count} patient(s) about doctor unavailability", "info")
    else:
        flash("ℹ️ No appointments to notify", "info")
    
    return redirect(request.referrer or url_for("admin.doctors_list"))


@notifications_bp.route("/check-all", methods=["POST"])
@admin_required
def check_all_notifications():
    """Check all notification conditions and send as needed."""
    notif_mgr = NotificationManager()
    results = notif_mgr.check_all_notifications()
    
    total = results['delay_notifications'] + results['congestion_alerts']
    
    if total > 0:
        flash(f"📱 Sent {total} notification(s): "
              f"{results['delay_notifications']} delays, "
              f"{results['congestion_alerts']} congestion alerts", 
              "success")
    else:
        flash("✅ All systems normal - no notifications needed", "success")
    
    return redirect(request.referrer or url_for("queue.view_queue"))


@notifications_bp.route("/api/check-all", methods=["GET"])
def api_check_all():
    """API endpoint for automated notification checks (can be called by cron job)."""
    notif_mgr = NotificationManager()
    results = notif_mgr.check_all_notifications()
    
    return jsonify({
        "success": True,
        "results": results
    })
