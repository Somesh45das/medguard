"""
Optimal appointment slot suggestion engine.
Analyzes crowd predictions and doctor availability to recommend the best time slots.
"""
from datetime import date, time, datetime, timedelta
from app import db
from app.models.models import Appointment, Doctor, Department
from app.services.crowd_predictor import CrowdPredictor
from config import Config


class SlotOptimizer:
    """Suggests optimal appointment slots to reduce congestion."""

    def __init__(self):
        self.predictor = CrowdPredictor()

    def get_available_slots(
        self,
        doctor_id: int,
        target_date: date = None,
        slot_duration: int = None,
    ) -> list:
        """
        Get all available slots for a doctor on a given date,
        scored and sorted by optimality.
        """
        if target_date is None:
            target_date = date.today()
        if slot_duration is None:
            slot_duration = Config.SLOT_DURATION_MIN

        doctor = Doctor.query.get(doctor_id)
        if not doctor or not doctor.is_available:
            return []

        # Get booked slots
        booked = Appointment.query.filter(
            Appointment.doctor_id == doctor_id,
            Appointment.appointment_date == target_date,
            Appointment.status.in_(["scheduled", "checked_in", "in_progress"]),
        ).all()

        booked_times = set()
        for apt in booked:
            booked_times.add(apt.appointment_time.strftime("%H:%M"))

        # Generate all possible slots
        all_slots = []
        current = datetime.combine(target_date, doctor.shift_start)
        end = datetime.combine(target_date, doctor.shift_end)

        now = datetime.now()

        while current + timedelta(minutes=slot_duration) <= end:
            slot_time = current.time()
            slot_key = slot_time.strftime("%H:%M")

            # Skip past slots for today (only if more than 30 minutes in the past)
            if target_date == date.today() and current < (now - timedelta(minutes=30)):
                current += timedelta(minutes=slot_duration)
                continue

            is_booked = slot_key in booked_times

            # Get crowd prediction for this hour
            crowd = self.predictor.predict_crowd_level(
                doctor.department_id, target_date, current.hour
            )

            if is_booked:
                # Show booked slots with different styling
                all_slots.append(
                    {
                        "time": slot_time.strftime("%H:%M"),
                        "end_time": (
                            current + timedelta(minutes=slot_duration)
                        ).time().strftime("%H:%M"),
                        "crowd_level": crowd["level"],
                        "crowd_color": "#6c757d",
                        "optimality_score": 0,
                        "optimality_label": "Booked",
                        "optimality_color": "#dc3545",
                        "estimated_wait": 0,
                        "recommendation": "❌ This slot is already booked",
                        "is_booked": True,
                        "is_recommended": False,
                        "rank": 999,
                    }
                )
            else:
                # Calculate optimality score (higher = better for patient)
                optimality = self._calculate_optimality(
                    crowd["level_code"],
                    current.hour,
                    len(booked),
                    doctor.max_patients_per_day,
                )

                all_slots.append(
                    {
                        "time": slot_time.strftime("%H:%M"),
                        "end_time": (
                            current + timedelta(minutes=slot_duration)
                        ).time().strftime("%H:%M"),
                        "crowd_level": crowd["level"],
                        "crowd_color": crowd["color"],
                        "optimality_score": optimality["score"],
                        "optimality_label": optimality["label"],
                        "optimality_color": optimality["color"],
                        "estimated_wait": optimality["estimated_wait"],
                        "recommendation": optimality["recommendation"],
                        "is_booked": False,
                    }
                )

            current += timedelta(minutes=slot_duration)

        # Sort by optimality score (descending = best first), booked slots last
        all_slots.sort(key=lambda x: (x.get("is_booked", False), -x["optimality_score"]))

        # Mark top 3 available as "recommended"
        available_count = 0
        for i, slot in enumerate(all_slots):
            if not slot.get("is_booked", False):
                slot["is_recommended"] = available_count < 3
                slot["rank"] = available_count + 1
                available_count += 1
            else:
                slot["is_recommended"] = False
                slot["rank"] = 999

        return all_slots

    def _calculate_optimality(
        self,
        crowd_code: int,
        hour: int,
        booked_count: int,
        max_patients: int,
    ) -> dict:
        """
        Calculate how optimal a slot is.
        Score range: 0 (worst) to 100 (best).
        """
        score = 100.0

        # Penalize for crowd level
        crowd_penalty = {0: 0, 1: 15, 2: 35, 3: 55}
        score -= crowd_penalty.get(crowd_code, 20)

        # Penalize peak hours
        if 9 <= hour <= 11:
            score -= 15
        elif 14 <= hour <= 16:
            score -= 10

        # Bonus for off-peak
        if hour == 8 or hour >= 17:
            score += 10
        if 12 <= hour <= 13:
            score += 5

        # Load factor
        if max_patients > 0:
            load = booked_count / max_patients
            score -= load * 20

        score = max(0, min(100, score))

        # Estimate wait
        base_wait = {0: 5, 1: 15, 2: 30, 3: 50}
        estimated_wait = base_wait.get(crowd_code, 15)

        # Label
        if score >= 75:
            label, color = "Excellent", "#28a745"
            recommendation = "✅ Highly recommended – minimal wait expected"
        elif score >= 55:
            label, color = "Good", "#17a2b8"
            recommendation = "👍 Good slot – moderate crowd expected"
        elif score >= 35:
            label, color = "Fair", "#ffc107"
            recommendation = "⚠️ Expect some waiting – consider alternatives"
        else:
            label, color = "Busy", "#dc3545"
            recommendation = "🔴 High crowd expected – try a different time"

        return {
            "score": round(score, 1),
            "label": label,
            "color": color,
            "estimated_wait": estimated_wait,
            "recommendation": recommendation,
        }

    def get_best_slots(
        self, doctor_id: int, target_date: date = None, count: int = 5
    ) -> list:
        """Get top N best slots for a doctor."""
        slots = self.get_available_slots(doctor_id, target_date)
        return slots[:count]

    def suggest_alternative_dates(
        self, doctor_id: int, days_ahead: int = 7
    ) -> list:
        """Suggest best dates in the upcoming week."""
        suggestions = []
        today = date.today()

        for i in range(days_ahead):
            target = today + timedelta(days=i)
            slots = self.get_available_slots(doctor_id, target)
            if slots:
                best = slots[0]
                avg_score = sum(s["optimality_score"] for s in slots) / len(slots)
                suggestions.append(
                    {
                        "date": target.isoformat(),
                        "date_display": target.strftime("%A, %b %d"),
                        "available_slots": len(slots),
                        "best_slot_time": best["time"],
                        "best_score": best["optimality_score"],
                        "avg_score": round(avg_score, 1),
                    }
                )

        suggestions.sort(key=lambda x: x["avg_score"], reverse=True)
        return suggestions
