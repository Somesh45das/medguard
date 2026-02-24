"""
Wait time estimation service.
Estimates wait times based on queue position, doctor speed, and crowd level.
"""
from datetime import date
from app.models.models import QueueEntry, Doctor, Department


class WaitTimeEstimator:
    """Estimates patient wait times dynamically."""

    def estimate(
        self,
        department_id: int,
        position: int,
        doctor_id: int = None,
    ) -> dict:
        """
        Estimate wait time for a given queue position.

        Returns dict with min, max, and best estimate in minutes.
        """
        # Get doctor's average consultation time
        if doctor_id:
            doctor = Doctor.query.get(doctor_id)
            avg_consult = doctor.avg_consultation_min if doctor else 15
        else:
            dept = Department.query.get(department_id)
            avg_consult = dept.avg_consultation_min if dept else 15

        # Get recent actual wait times for calibration
        today = date.today()
        recent = (
            QueueEntry.query.filter(
                QueueEntry.department_id == department_id,
                QueueEntry.queue_date == today,
                QueueEntry.status == "completed",
                QueueEntry.called_at.isnot(None),
            )
            .order_by(QueueEntry.completed_at.desc())
            .limit(10)
            .all()
        )

        if recent:
            actual_waits = []
            for e in recent:
                if e.called_at and e.entered_at:
                    diff = (e.called_at - e.entered_at).total_seconds() / 60
                    actual_waits.append(diff)
            if actual_waits:
                avg_consult = sum(actual_waits) / len(actual_waits) / max(1, position)
                avg_consult = max(avg_consult, 5)

        best_estimate = int(position * avg_consult)
        min_estimate = int(best_estimate * 0.7)
        max_estimate = int(best_estimate * 1.4)

        return {
            "min_minutes": max(0, min_estimate),
            "max_minutes": max_estimate,
            "best_estimate": max(0, best_estimate),
            "display": self._format_time(best_estimate),
            "position": position,
        }

    def _format_time(self, minutes: int) -> str:
        """Format minutes to human-readable string."""
        if minutes < 1:
            return "< 1 min"
        elif minutes < 60:
            return f"~{minutes} min"
        else:
            hours = minutes // 60
            mins = minutes % 60
            return f"~{hours}h {mins}m"
