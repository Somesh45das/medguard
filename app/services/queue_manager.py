"""
Real-time queue management service.
Handles token generation, queue ordering, and position updates.
"""
from datetime import datetime, date
from app import db
from app.models.models import QueueEntry, Patient, Appointment, Department
from app.services.priority_scorer import PriorityScorer


class QueueManager:
    """Manages the real-time patient queue."""

    def __init__(self):
        self.priority_scorer = PriorityScorer()

    def generate_token(self, department_id: int) -> str:
        """Generate a new token number for today."""
        today = date.today()
        count = QueueEntry.query.filter(
            QueueEntry.department_id == department_id,
            QueueEntry.queue_date == today,
        ).count()

        dept = Department.query.get(department_id)
        prefix = "".join(w[0] for w in dept.name.split()[:2]).upper() if dept else "GN"
        return f"{prefix}-{count + 1:03d}"

    def add_to_queue(
        self,
        patient_id: int,
        department_id: int,
        doctor_id: int = None,
        appointment_id: int = None,
        symptoms: str = "",
    ) -> QueueEntry:
        """Add a patient to the queue with priority scoring."""
        patient = Patient.query.get(patient_id)

        # Calculate priority
        priority = self.priority_scorer.calculate_priority(
            patient=patient,
            symptoms=symptoms,
            has_appointment=appointment_id is not None,
        )

        # Get current queue position
        today = date.today()
        current_queue = (
            QueueEntry.query.filter(
                QueueEntry.department_id == department_id,
                QueueEntry.queue_date == today,
                QueueEntry.status.in_(["waiting", "called"]),
            )
            .order_by(QueueEntry.priority_score.desc(), QueueEntry.entered_at.asc())
            .all()
        )

        # Determine position based on priority
        position = 1
        for entry in current_queue:
            if priority > entry.priority_score:
                break
            position += 1

        token = self.generate_token(department_id)

        queue_entry = QueueEntry(
            token_number=token,
            patient_id=patient_id,
            department_id=department_id,
            doctor_id=doctor_id,
            appointment_id=appointment_id,
            queue_date=today,
            position=position,
            priority_score=priority,
            status="waiting",
            estimated_wait_min=self._estimate_wait(department_id, position),
        )

        db.session.add(queue_entry)

        # Update positions of entries below
        for entry in current_queue[position - 1 :]:
            entry.position += 1

        db.session.commit()
        return queue_entry

    def call_next(self, department_id: int, doctor_id: int = None) -> QueueEntry:
        """Call the next patient in queue."""
        today = date.today()
        query = QueueEntry.query.filter(
            QueueEntry.department_id == department_id,
            QueueEntry.queue_date == today,
            QueueEntry.status == "waiting",
        )
        if doctor_id:
            query = query.filter(
                (QueueEntry.doctor_id == doctor_id) | (QueueEntry.doctor_id.is_(None))
            )

        next_entry = query.order_by(
            QueueEntry.priority_score.desc(), QueueEntry.entered_at.asc()
        ).first()

        if next_entry:
            next_entry.status = "called"
            next_entry.called_at = datetime.utcnow()
            if doctor_id:
                next_entry.doctor_id = doctor_id
            db.session.commit()

        return next_entry

    def start_consultation(self, queue_id: int) -> QueueEntry:
        """Mark patient as in consultation."""
        entry = QueueEntry.query.get(queue_id)
        if entry:
            entry.status = "in_progress"

            # Update appointment if linked
            if entry.appointment_id:
                apt = Appointment.query.get(entry.appointment_id)
                if apt:
                    wait_minutes = 0
                    if entry.called_at and entry.entered_at:
                        wait_minutes = int(
                            (entry.called_at - entry.entered_at).total_seconds() / 60
                        )
                    apt.status = "in_progress"
                    apt.actual_wait_min = wait_minutes

            db.session.commit()
        return entry

    def complete_consultation(self, queue_id: int) -> QueueEntry:
        """Mark patient consultation as complete."""
        entry = QueueEntry.query.get(queue_id)
        if entry:
            entry.status = "completed"
            entry.completed_at = datetime.utcnow()

            if entry.appointment_id:
                apt = Appointment.query.get(entry.appointment_id)
                if apt:
                    apt.status = "completed"
                    apt.completed_at = datetime.utcnow()

            # Re-calculate positions
            self._recalculate_positions(entry.department_id)
            db.session.commit()
        return entry

    def skip_patient(self, queue_id: int) -> QueueEntry:
        """Skip / no-show a patient."""
        entry = QueueEntry.query.get(queue_id)
        if entry:
            entry.status = "skipped"
            self._recalculate_positions(entry.department_id)
            db.session.commit()
        return entry

    def get_department_queue(self, department_id: int) -> list:
        """Get current queue for a department."""
        today = date.today()
        entries = (
            QueueEntry.query.filter(
                QueueEntry.department_id == department_id,
                QueueEntry.queue_date == today,
                QueueEntry.status.in_(["waiting", "called", "in_progress"]),
            )
            .order_by(
                QueueEntry.status.desc(),  # in_progress first
                QueueEntry.priority_score.desc(),
                QueueEntry.entered_at.asc(),
            )
            .all()
        )
        return entries

    def get_queue_stats(self, department_id: int = None) -> dict:
        """Get queue statistics."""
        today = date.today()
        query = QueueEntry.query.filter(QueueEntry.queue_date == today)
        if department_id:
            query = query.filter(QueueEntry.department_id == department_id)

        total = query.count()
        waiting = query.filter(QueueEntry.status == "waiting").count()
        in_progress = query.filter(QueueEntry.status == "in_progress").count()
        completed = query.filter(QueueEntry.status == "completed").count()
        skipped = query.filter(QueueEntry.status == "skipped").count()

        # Average wait time for completed
        completed_entries = query.filter(
            QueueEntry.status == "completed",
            QueueEntry.called_at.isnot(None),
        ).all()

        avg_wait = 0
        if completed_entries:
            waits = []
            for e in completed_entries:
                if e.called_at and e.entered_at:
                    waits.append((e.called_at - e.entered_at).total_seconds() / 60)
            avg_wait = sum(waits) / len(waits) if waits else 0

        return {
            "total_today": total,
            "waiting": waiting,
            "in_progress": in_progress,
            "completed": completed,
            "skipped": skipped,
            "avg_wait_minutes": round(avg_wait, 1),
            "completion_rate": round(completed / total * 100, 1) if total > 0 else 0,
        }

    def _estimate_wait(self, department_id: int, position: int) -> int:
        """Estimate wait time based on position and department avg."""
        dept = Department.query.get(department_id)
        avg_time = dept.avg_consultation_min if dept else 15
        return position * avg_time

    def _recalculate_positions(self, department_id: int):
        """Recalculate queue positions after changes."""
        today = date.today()
        entries = (
            QueueEntry.query.filter(
                QueueEntry.department_id == department_id,
                QueueEntry.queue_date == today,
                QueueEntry.status == "waiting",
            )
            .order_by(QueueEntry.priority_score.desc(), QueueEntry.entered_at.asc())
            .all()
        )
        for i, entry in enumerate(entries, 1):
            entry.position = i
            entry.estimated_wait_min = self._estimate_wait(department_id, i)
