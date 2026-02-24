"""
Patient priority scoring system.
Considers age, emergency status, appointment booking, and symptoms.
"""
from config import Config


class PriorityScorer:
    """Calculates priority score for queue ordering."""

    # Symptom keywords that indicate urgency
    URGENT_SYMPTOMS = {
        "chest pain": 40,
        "breathing difficulty": 40,
        "breathless": 35,
        "unconscious": 50,
        "bleeding": 30,
        "fracture": 25,
        "high fever": 20,
        "seizure": 35,
        "stroke": 45,
        "heart attack": 50,
        "accident": 30,
        "severe pain": 25,
        "allergic reaction": 30,
        "poisoning": 40,
        "burn": 25,
    }

    def calculate_priority(
        self, patient, symptoms: str = "", has_appointment: bool = False
    ) -> float:
        """
        Calculate priority score (0-100). Higher = more urgent.

        Factors:
        - Age (elderly/children get priority)
        - Emergency flag
        - Symptom urgency
        - Appointment status
        """
        score = 0.0

        # 1. Emergency flag
        if patient.is_emergency:
            score += Config.EMERGENCY_PRIORITY_BOOST

        # 2. Age-based priority
        age = patient.age if patient.age else 30
        if age >= 75:
            score += 20
        elif age >= 65:
            score += 15
        elif age >= 55:
            score += 8
        elif age <= 5:
            score += 18
        elif age <= 12:
            score += 10

        # 3. Symptom-based urgency
        if symptoms:
            symptoms_lower = symptoms.lower()
            for keyword, points in self.URGENT_SYMPTOMS.items():
                if keyword in symptoms_lower:
                    score += points
                    break  # Only count highest matching symptom

        # 4. Appointment holder gets slight priority
        if has_appointment:
            score += 5

        return min(100.0, round(score, 1))

    def get_priority_label(self, score: float) -> dict:
        """Get human-readable priority label."""
        if score >= 70:
            return {"label": "CRITICAL", "color": "#dc3545", "icon": "🔴"}
        elif score >= 45:
            return {"label": "HIGH", "color": "#fd7e14", "icon": "🟠"}
        elif score >= 20:
            return {"label": "MEDIUM", "color": "#ffc107", "icon": "🟡"}
        else:
            return {"label": "NORMAL", "color": "#28a745", "icon": "🟢"}
