"""
Notification service for alerts and messages.
"""
from datetime import datetime
from app import db
from app.models.models import Notification


class NotificationService:
    """Manages system notifications and alerts."""

    @staticmethod
    def create(
        title: str,
        message: str,
        notif_type: str = "info",
        target: str = "all",
        target_id: int = None,
    ) -> Notification:
        """Create a new notification."""
        notif = Notification(
            title=title,
            message=message,
            type=notif_type,
            target=target,
            target_id=target_id,
        )
        db.session.add(notif)
        db.session.commit()
        return notif

    @staticmethod
    def get_recent(limit: int = 20) -> list:
        """Get recent notifications."""
        return (
            Notification.query.order_by(Notification.created_at.desc())
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_unread_count() -> int:
        return Notification.query.filter_by(is_read=False).count()

    @staticmethod
    def mark_read(notif_id: int):
        n = Notification.query.get(notif_id)
        if n:
            n.is_read = True
            db.session.commit()

    @staticmethod
    def mark_all_read():
        Notification.query.filter_by(is_read=False).update({"is_read": True})
        db.session.commit()

    @staticmethod
    def alert_high_crowd(department_name: str, level: str):
        """Generate alert when crowd is high."""
        if level in ("high", "critical"):
            NotificationService.create(
                title=f"⚠️ {level.upper()} Crowd Alert – {department_name}",
                message=(
                    f"The {department_name} department is experiencing "
                    f"{level} crowd levels. Consider redistributing patients."
                ),
                notif_type="warning" if level == "high" else "critical",
                target="department",
            )

    @staticmethod
    def alert_long_wait(patient_name: str, wait_minutes: int):
        """Alert when a patient has been waiting too long."""
        if wait_minutes > 45:
            NotificationService.create(
                title=f"⏰ Long Wait Alert – {patient_name}",
                message=f"Patient has been waiting for {wait_minutes} minutes.",
                notif_type="warning",
            )
