"""
Health Risk Scoring System.
Combines multiple factors to calculate comprehensive patient risk score.
Used for intelligent appointment prioritization to reduce waiting times.
"""
from datetime import datetime, date
from app.services.noshow_predictor import NoShowPredictor


class HealthRiskScorer:
    """
    Calculates comprehensive health risk score for patients.
    Higher score = Higher risk = Higher priority = Seen sooner
    
    Factors considered:
    1. Age (elderly and children are vulnerable)
    2. Chronic conditions (diabetes, hypertension, etc.)
    3. Symptom severity (chest pain, breathing difficulty, etc.)
    4. Emergency status
    5. No-show probability (inverse - reliable patients get priority)
    6. Appointment history
    """
    
    # Critical symptoms requiring immediate attention
    CRITICAL_SYMPTOMS = {
        "chest pain": 50,
        "heart attack": 50,
        "stroke": 50,
        "unconscious": 50,
        "not breathing": 50,
        "severe bleeding": 45,
        "head injury": 45,
        "poisoning": 45,
    }
    
    # High-priority symptoms
    HIGH_PRIORITY_SYMPTOMS = {
        "breathing difficulty": 40,
        "breathless": 40,
        "seizure": 40,
        "allergic reaction": 35,
        "high fever": 30,
        "severe pain": 30,
        "fracture": 30,
        "burn": 30,
        "bleeding": 25,
        "vomiting blood": 40,
        "confusion": 35,
    }
    
    # Chronic conditions that increase risk
    CHRONIC_CONDITIONS = {
        "diabetes": 15,
        "hypertension": 12,
        "heart disease": 20,
        "kidney disease": 18,
        "liver disease": 18,
        "cancer": 25,
        "copd": 15,
        "asthma": 12,
        "stroke history": 20,
        "heart attack history": 20,
    }
    
    def __init__(self):
        self.noshow_predictor = NoShowPredictor()
    
    def calculate_health_risk(
        self,
        patient,
        symptoms: str = "",
        medical_history: str = "",
        appointment_date: date = None,
        booking_gap_days: int = 7,
        previous_no_shows: int = 0,
        appointment_count: int = 1,
        has_appointment: bool = False
    ) -> dict:
        """
        Calculate comprehensive health risk score (0-100).
        
        Args:
            patient: Patient object with age, gender, is_emergency
            symptoms: Current symptoms description
            medical_history: Patient's medical history
            appointment_date: Date of appointment
            booking_gap_days: Days between booking and appointment
            previous_no_shows: Number of previous no-shows
            appointment_count: Total appointments for this patient
            has_appointment: Whether patient has pre-booked appointment
        
        Returns:
            dict with risk_score, risk_level, priority_rank, factors breakdown
        """
        risk_score = 0.0
        factors = {}
        
        # 1. AGE RISK (0-25 points)
        age_risk = self._calculate_age_risk(patient.age)
        risk_score += age_risk
        factors['age_risk'] = {
            'score': age_risk,
            'reason': self._get_age_reason(patient.age)
        }
        
        # 2. EMERGENCY STATUS (0-30 points)
        emergency_risk = 30 if patient.is_emergency else 0
        risk_score += emergency_risk
        factors['emergency_risk'] = {
            'score': emergency_risk,
            'reason': '🚨 Emergency case' if patient.is_emergency else 'Non-emergency'
        }
        
        # 3. SYMPTOM SEVERITY (0-50 points)
        symptom_risk = self._calculate_symptom_risk(symptoms)
        risk_score += symptom_risk['score']
        factors['symptom_risk'] = symptom_risk
        
        # 4. CHRONIC CONDITIONS (0-25 points)
        chronic_risk = self._calculate_chronic_risk(medical_history)
        risk_score += chronic_risk['score']
        factors['chronic_risk'] = chronic_risk
        
        # 5. RELIABILITY SCORE (inverse of no-show risk) (-10 to +10 points)
        reliability_risk = self._calculate_reliability_risk(
            patient=patient,
            booking_gap_days=booking_gap_days,
            previous_no_shows=previous_no_shows,
            appointment_count=appointment_count,
            appointment_date=appointment_date
        )
        risk_score += reliability_risk['score']
        factors['reliability_risk'] = reliability_risk
        
        # 6. APPOINTMENT HOLDER BONUS (0-5 points)
        appointment_bonus = 5 if has_appointment else 0
        risk_score += appointment_bonus
        factors['appointment_bonus'] = {
            'score': appointment_bonus,
            'reason': 'Has pre-booked appointment' if has_appointment else 'Walk-in patient'
        }
        
        # Cap score at 100
        risk_score = min(100.0, round(risk_score, 1))
        
        # Determine risk level and priority
        risk_level_info = self._get_risk_level(risk_score)
        
        # Calculate priority rank (for queue ordering)
        priority_rank = self._calculate_priority_rank(risk_score, patient.is_emergency)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            risk_score=risk_score,
            is_emergency=patient.is_emergency,
            symptom_risk=symptom_risk['score'],
            chronic_risk=chronic_risk['score'],
            reliability_risk=reliability_risk
        )
        
        return {
            'risk_score': risk_score,
            'risk_level': risk_level_info['level'],
            'risk_color': risk_level_info['color'],
            'risk_icon': risk_level_info['icon'],
            'priority_rank': priority_rank,
            'factors': factors,
            'recommendations': recommendations,
            'estimated_wait_reduction': self._estimate_wait_reduction(risk_score)
        }
    
    def _calculate_age_risk(self, age: int) -> float:
        """Calculate risk based on age (U-shaped curve)."""
        if age <= 1:
            return 25  # Infants - highest risk
        elif age <= 5:
            return 20  # Young children
        elif age <= 12:
            return 15  # Children
        elif age <= 18:
            return 8   # Teenagers
        elif age <= 50:
            return 0   # Adults - baseline
        elif age <= 60:
            return 5   # Middle-aged
        elif age <= 70:
            return 12  # Senior
        elif age <= 80:
            return 18  # Elderly
        else:
            return 25  # Very elderly - highest risk
    
    def _get_age_reason(self, age: int) -> str:
        """Get human-readable age risk reason."""
        if age <= 1:
            return '👶 Infant - requires immediate attention'
        elif age <= 5:
            return '👧 Young child - vulnerable age group'
        elif age <= 12:
            return '🧒 Child - needs priority care'
        elif age <= 18:
            return '👦 Teenager - moderate priority'
        elif age <= 50:
            return '👤 Adult - standard priority'
        elif age <= 60:
            return '👨 Middle-aged - slight priority'
        elif age <= 70:
            return '👴 Senior - increased priority'
        elif age <= 80:
            return '👵 Elderly - high priority'
        else:
            return '🧓 Very elderly - highest priority'
    
    def _calculate_symptom_risk(self, symptoms: str) -> dict:
        """Calculate risk based on symptom severity."""
        if not symptoms:
            return {'score': 0, 'reason': 'No symptoms reported', 'matched_symptoms': []}
        
        symptoms_lower = symptoms.lower()
        max_score = 0
        matched_symptoms = []
        
        # Check critical symptoms
        for symptom, score in self.CRITICAL_SYMPTOMS.items():
            if symptom in symptoms_lower:
                max_score = max(max_score, score)
                matched_symptoms.append(f"🔴 {symptom.title()} (Critical)")
        
        # Check high-priority symptoms
        for symptom, score in self.HIGH_PRIORITY_SYMPTOMS.items():
            if symptom in symptoms_lower:
                max_score = max(max_score, score)
                matched_symptoms.append(f"🟠 {symptom.title()} (High Priority)")
        
        if max_score >= 45:
            reason = '🚨 CRITICAL symptoms detected - immediate attention required'
        elif max_score >= 30:
            reason = '⚠️ High-priority symptoms - expedited care needed'
        elif max_score >= 15:
            reason = '⚡ Moderate symptoms - standard priority'
        else:
            reason = '✓ Mild symptoms - routine care'
        
        return {
            'score': max_score,
            'reason': reason,
            'matched_symptoms': matched_symptoms[:3]  # Top 3
        }
    
    def _calculate_chronic_risk(self, medical_history: str) -> dict:
        """Calculate risk based on chronic conditions."""
        if not medical_history:
            return {'score': 0, 'reason': 'No chronic conditions', 'conditions': []}
        
        history_lower = medical_history.lower()
        total_score = 0
        conditions = []
        
        for condition, score in self.CHRONIC_CONDITIONS.items():
            if condition in history_lower:
                total_score += score
                conditions.append(f"• {condition.title()}")
        
        # Cap at 25 points
        total_score = min(25, total_score)
        
        if total_score >= 20:
            reason = '⚕️ Multiple chronic conditions - high-risk patient'
        elif total_score >= 10:
            reason = '💊 Chronic condition(s) present - increased priority'
        else:
            reason = '✓ No significant chronic conditions'
        
        return {
            'score': total_score,
            'reason': reason,
            'conditions': conditions[:3]  # Top 3
        }
    
    def _calculate_reliability_risk(
        self,
        patient,
        booking_gap_days: int,
        previous_no_shows: int,
        appointment_count: int,
        appointment_date: date = None
    ) -> dict:
        """
        Calculate reliability score (inverse of no-show risk).
        Reliable patients get slight priority boost.
        Unreliable patients get slight penalty.
        """
        # Get no-show prediction
        noshow_pred = self.noshow_predictor.predict_no_show(
            age=patient.age,
            gender=patient.gender,
            booking_gap_days=booking_gap_days,
            previous_no_shows=previous_no_shows,
            appointment_count=appointment_count,
            appointment_date=appointment_date
        )
        
        no_show_prob = noshow_pred['probability']
        
        # Convert to reliability score
        # High no-show risk = negative points (penalty)
        # Low no-show risk = positive points (bonus)
        if no_show_prob >= 0.5:
            score = -10  # High risk of no-show - penalty
            reason = f"⚠️ High no-show risk ({noshow_pred['percentage']}%) - may need reminder"
        elif no_show_prob >= 0.3:
            score = -5   # Moderate risk
            reason = f"⚡ Moderate no-show risk ({noshow_pred['percentage']}%) - send reminder"
        elif no_show_prob >= 0.15:
            score = 0    # Average reliability
            reason = f"✓ Average reliability ({noshow_pred['percentage']}% no-show risk)"
        else:
            score = 5    # Very reliable - bonus
            reason = f"⭐ Highly reliable patient ({noshow_pred['percentage']}% no-show risk)"
        
        return {
            'score': score,
            'reason': reason,
            'no_show_probability': no_show_prob,
            'no_show_percentage': noshow_pred['percentage'],
            'no_show_risk_level': noshow_pred['risk_level']
        }
    
    def _get_risk_level(self, risk_score: float) -> dict:
        """Determine risk level from score."""
        if risk_score >= 80:
            return {
                'level': 'CRITICAL',
                'color': '#dc3545',
                'icon': '🔴',
                'description': 'Immediate attention required'
            }
        elif risk_score >= 60:
            return {
                'level': 'HIGH',
                'color': '#fd7e14',
                'icon': '🟠',
                'description': 'High priority - expedited care'
            }
        elif risk_score >= 40:
            return {
                'level': 'MODERATE',
                'color': '#ffc107',
                'icon': '🟡',
                'description': 'Moderate priority - standard care'
            }
        elif risk_score >= 20:
            return {
                'level': 'LOW',
                'color': '#17a2b8',
                'icon': '🔵',
                'description': 'Low priority - routine care'
            }
        else:
            return {
                'level': 'MINIMAL',
                'color': '#28a745',
                'icon': '🟢',
                'description': 'Minimal risk - routine care'
            }
    
    def _calculate_priority_rank(self, risk_score: float, is_emergency: bool) -> int:
        """
        Calculate priority rank for queue ordering.
        Lower rank = Higher priority = Seen first
        """
        # Emergency patients always get rank 1-10
        if is_emergency:
            return max(1, int(10 - (risk_score / 10)))
        
        # Non-emergency patients get rank 11-100
        # Invert score so higher risk = lower rank number
        return int(100 - risk_score) + 10
    
    def _generate_recommendations(
        self,
        risk_score: float,
        is_emergency: bool,
        symptom_risk: float,
        chronic_risk: float,
        reliability_risk: dict
    ) -> list:
        """Generate actionable recommendations for staff."""
        recommendations = []
        
        # Emergency handling
        if is_emergency:
            recommendations.append({
                'type': 'critical',
                'icon': '🚨',
                'text': 'EMERGENCY CASE - See immediately, bypass queue'
            })
        
        # Critical symptoms
        if symptom_risk >= 45:
            recommendations.append({
                'type': 'critical',
                'icon': '⚠️',
                'text': 'Critical symptoms detected - prioritize consultation'
            })
        elif symptom_risk >= 30:
            recommendations.append({
                'type': 'warning',
                'icon': '⚡',
                'text': 'High-priority symptoms - expedite appointment'
            })
        
        # Chronic conditions
        if chronic_risk >= 20:
            recommendations.append({
                'type': 'info',
                'icon': '⚕️',
                'text': 'Multiple chronic conditions - review medical history'
            })
        
        # No-show risk
        if reliability_risk['no_show_probability'] >= 0.3:
            recommendations.append({
                'type': 'warning',
                'icon': '📱',
                'text': f"Send SMS reminder - {reliability_risk['no_show_percentage']}% no-show risk"
            })
        
        # High overall risk
        if risk_score >= 80:
            recommendations.append({
                'type': 'critical',
                'icon': '🏥',
                'text': 'High-risk patient - consider immediate triage'
            })
        elif risk_score >= 60:
            recommendations.append({
                'type': 'warning',
                'icon': '⏱️',
                'text': 'Reduce wait time - see within 15 minutes'
            })
        
        # Default if no specific recommendations
        if not recommendations:
            recommendations.append({
                'type': 'success',
                'icon': '✓',
                'text': 'Standard care protocol - routine appointment'
            })
        
        return recommendations
    
    def _estimate_wait_reduction(self, risk_score: float) -> dict:
        """Estimate how much wait time should be reduced based on risk."""
        if risk_score >= 80:
            return {
                'reduction_percentage': 90,
                'target_wait_minutes': 5,
                'message': 'See immediately - minimal wait'
            }
        elif risk_score >= 60:
            return {
                'reduction_percentage': 60,
                'target_wait_minutes': 15,
                'message': 'Expedited care - reduced wait'
            }
        elif risk_score >= 40:
            return {
                'reduction_percentage': 30,
                'target_wait_minutes': 25,
                'message': 'Moderate priority - slight reduction'
            }
        else:
            return {
                'reduction_percentage': 0,
                'target_wait_minutes': 35,
                'message': 'Standard wait time'
            }
    
    def sort_patients_by_risk(self, patients_data: list) -> list:
        """
        Sort list of patients by health risk score (highest first).
        
        Args:
            patients_data: List of dicts with patient info and context
        
        Returns:
            Sorted list with risk scores added
        """
        results = []
        
        for data in patients_data:
            risk_result = self.calculate_health_risk(
                patient=data['patient'],
                symptoms=data.get('symptoms', ''),
                medical_history=data.get('medical_history', ''),
                appointment_date=data.get('appointment_date'),
                booking_gap_days=data.get('booking_gap_days', 7),
                previous_no_shows=data.get('previous_no_shows', 0),
                appointment_count=data.get('appointment_count', 1),
                has_appointment=data.get('has_appointment', False)
            )
            
            results.append({
                **data,
                'risk_assessment': risk_result
            })
        
        # Sort by risk score (descending) and priority rank (ascending)
        results.sort(
            key=lambda x: (-x['risk_assessment']['risk_score'], x['risk_assessment']['priority_rank'])
        )
        
        return results
    
    def get_risk_summary(self, risk_result: dict) -> str:
        """Generate human-readable risk summary."""
        score = risk_result['risk_score']
        level = risk_result['risk_level']
        factors = risk_result['factors']
        
        summary = f"Risk Score: {score}/100 ({level})\n\n"
        summary += "Contributing Factors:\n"
        
        for factor_name, factor_data in factors.items():
            if factor_data['score'] > 0:
                summary += f"  • {factor_data['reason']} (+{factor_data['score']} points)\n"
            elif factor_data['score'] < 0:
                summary += f"  • {factor_data['reason']} ({factor_data['score']} points)\n"
        
        summary += f"\nRecommendations:\n"
        for rec in risk_result['recommendations']:
            summary += f"  {rec['icon']} {rec['text']}\n"
        
        return summary


# Example usage
if __name__ == "__main__":
    from app.models.models import Patient
    
    # Create test patient
    test_patient = Patient(
        patient_id="P-20260225-001",
        name="John Doe",
        age=72,
        gender="M",
        is_emergency=False
    )
    
    scorer = HealthRiskScorer()
    
    # Calculate risk
    result = scorer.calculate_health_risk(
        patient=test_patient,
        symptoms="chest pain and breathing difficulty",
        medical_history="diabetes, hypertension, heart disease",
        booking_gap_days=3,
        previous_no_shows=0,
        appointment_count=5,
        has_appointment=True
    )
    
    print("\n" + "=" * 70)
    print("   HEALTH RISK ASSESSMENT")
    print("=" * 70)
    print(f"\n   Patient: {test_patient.name} (Age: {test_patient.age})")
    print(f"   Risk Score: {result['risk_score']}/100")
    print(f"   Risk Level: {result['risk_icon']} {result['risk_level']}")
    print(f"   Priority Rank: #{result['priority_rank']}")
    print(f"\n   Estimated Wait Reduction: {result['estimated_wait_reduction']['reduction_percentage']}%")
    print(f"   Target Wait Time: {result['estimated_wait_reduction']['target_wait_minutes']} minutes")
    
    print(f"\n   Risk Factors:")
    for factor_name, factor_data in result['factors'].items():
        if factor_data['score'] != 0:
            print(f"      • {factor_data['reason']} ({factor_data['score']:+.1f} points)")
    
    print(f"\n   Recommendations:")
    for rec in result['recommendations']:
        print(f"      {rec['icon']} {rec['text']}")
    
    print("\n" + "=" * 70 + "\n")
