"""
No-Show Prediction Service.
Uses trained ML model to predict appointment no-show probability.
"""
import os
import joblib
import numpy as np
from datetime import datetime, date


class NoShowPredictor:
    """Predicts probability of patient missing appointment."""
    
    def __init__(self):
        self.model = None
        self.scaler = None
        self.feature_names = None
        self._load_model()
    
    def _load_model(self):
        """Load trained model from disk."""
        try:
            models_dir = os.path.join("app", "ml", "models")
            model_path = os.path.join(models_dir, "noshow_model.pkl")
            scaler_path = os.path.join(models_dir, "noshow_scaler.pkl")
            features_path = os.path.join(models_dir, "noshow_features.pkl")
            
            if os.path.exists(model_path):
                self.model = joblib.load(model_path)
                self.scaler = joblib.load(scaler_path)
                self.feature_names = joblib.load(features_path)
                print(f"[NoShowPredictor] Model loaded successfully")
            else:
                print(f"[NoShowPredictor] Model not found at {model_path}")
                print(f"[NoShowPredictor] Run: python app/ml/train_noshow_model.py")
        except Exception as e:
            print(f"[NoShowPredictor] Error loading model: {e}")
            self.model = None
    
    def predict_no_show(
        self,
        age: int,
        gender: str = "M",
        booking_gap_days: int = 7,
        previous_no_shows: int = 0,
        appointment_count: int = 1,
        sms_received: int = 1,
        scholarship: int = 0,
        hypertension: int = 0,
        diabetes: int = 0,
        alcoholism: int = 0,
        handicap: int = 0,
        day_of_week: int = None,
        month: int = None,
        appointment_date: date = None
    ) -> dict:
        """
        Predict no-show probability for an appointment.
        
        Args:
            age: Patient age
            gender: M/F
            booking_gap_days: Days between booking and appointment
            previous_no_shows: Number of previous no-shows
            appointment_count: Total appointments for this patient
            sms_received: 1 if SMS reminder sent, 0 otherwise
            scholarship: 1 if patient has social welfare, 0 otherwise
            hypertension: 1 if patient has hypertension, 0 otherwise
            diabetes: 1 if patient has diabetes, 0 otherwise
            alcoholism: 1 if patient has alcoholism, 0 otherwise
            handicap: Disability level (0-4)
            day_of_week: 0=Monday, 6=Sunday (auto-calculated if appointment_date provided)
            month: 1-12 (auto-calculated if appointment_date provided)
            appointment_date: Date of appointment (optional)
        
        Returns:
            dict with probability, risk_level, recommendation
        """
        # Fallback if model not loaded
        if self.model is None:
            return self._fallback_prediction(age, booking_gap_days, previous_no_shows)
        
        # Auto-calculate temporal features
        if appointment_date:
            day_of_week = appointment_date.weekday()
            month = appointment_date.month
        else:
            if day_of_week is None:
                day_of_week = datetime.now().weekday()
            if month is None:
                month = datetime.now().month
        
        # Calculate derived features
        is_elderly = 1 if age >= 65 else 0
        is_child = 1 if age <= 12 else 0
        is_same_day = 1 if booking_gap_days == 0 else 0
        is_short_notice = 1 if booking_gap_days <= 3 else 0
        is_weekend = 1 if day_of_week >= 5 else 0
        is_monday = 1 if day_of_week == 0 else 0
        health_risk_score = hypertension + diabetes + alcoholism + handicap
        gender_encoded = 1 if gender.upper() == "M" else 0
        
        # Age group encoding (matches training)
        if age <= 12:
            age_group_encoded = 0  # child
        elif age <= 18:
            age_group_encoded = 1  # teen
        elif age <= 35:
            age_group_encoded = 2  # young_adult
        elif age <= 50:
            age_group_encoded = 3  # adult
        elif age <= 65:
            age_group_encoded = 4  # senior
        else:
            age_group_encoded = 5  # elderly
        
        # Build feature vector (must match training order exactly)
        features = np.array([[
            age,                    # 0
            is_elderly,             # 1
            is_child,               # 2
            scholarship,            # 3
            health_risk_score,      # 4
            previous_no_shows,      # 5
            appointment_count,      # 6
            booking_gap_days,       # 7
            is_same_day,            # 8
            is_short_notice,        # 9
            day_of_week,            # 10
            month,                  # 11
            is_weekend,             # 12
            is_monday,              # 13
            sms_received,           # 14
            hypertension,           # 15
            diabetes,               # 16
            alcoholism,             # 17
            handicap,               # 18
            gender_encoded,         # 19
            age_group_encoded,      # 20
        ]])
        
        # Scale features
        features_scaled = self.scaler.transform(features)
        
        # Predict
        probability = self.model.predict_proba(features_scaled)[0][1]  # Probability of no-show
        
        # Determine risk level
        if probability >= 0.4:
            risk_level = "HIGH"
            risk_color = "#dc3545"
            recommendation = "⚠️ High no-show risk. Send SMS reminder and consider overbooking."
        elif probability >= 0.25:
            risk_level = "MEDIUM"
            risk_color = "#ffc107"
            recommendation = "⚡ Moderate risk. Send SMS reminder 24 hours before."
        else:
            risk_level = "LOW"
            risk_color = "#28a745"
            recommendation = "✅ Low risk. Standard confirmation sufficient."
        
        return {
            "probability": round(probability, 3),
            "percentage": round(probability * 100, 1),
            "risk_level": risk_level,
            "risk_color": risk_color,
            "recommendation": recommendation,
            "show_probability": round(1 - probability, 3),
            "confidence": "ML-based prediction"
        }
    
    def _fallback_prediction(self, age: int, booking_gap_days: int, previous_no_shows: int) -> dict:
        """Simple rule-based prediction when ML model unavailable."""
        score = 0.2  # Base no-show rate
        
        # Age factor
        if 18 <= age <= 35:
            score += 0.05  # Young adults more likely to miss
        elif age >= 65:
            score -= 0.05  # Elderly more reliable
        
        # Booking gap factor
        if booking_gap_days > 30:
            score += 0.10  # Long gap increases no-show
        elif booking_gap_days == 0:
            score -= 0.05  # Same-day less likely to miss
        
        # History factor
        if previous_no_shows > 0:
            score += 0.15 * min(previous_no_shows, 3)  # Cap at 3
        
        # Clamp to [0, 1]
        probability = max(0.0, min(1.0, score))
        
        if probability >= 0.4:
            risk_level = "HIGH"
            risk_color = "#dc3545"
        elif probability >= 0.25:
            risk_level = "MEDIUM"
            risk_color = "#ffc107"
        else:
            risk_level = "LOW"
            risk_color = "#28a745"
        
        return {
            "probability": round(probability, 3),
            "percentage": round(probability * 100, 1),
            "risk_level": risk_level,
            "risk_color": risk_color,
            "recommendation": "Rule-based estimate (ML model not available)",
            "show_probability": round(1 - probability, 3),
            "confidence": "Rule-based fallback"
        }
    
    def predict_batch(self, appointments: list) -> list:
        """
        Predict no-show probability for multiple appointments.
        
        Args:
            appointments: List of dicts with appointment details
        
        Returns:
            List of prediction dicts
        """
        predictions = []
        for appt in appointments:
            pred = self.predict_no_show(**appt)
            pred['appointment_id'] = appt.get('appointment_id')
            predictions.append(pred)
        
        return predictions
    
    def get_overbooking_factor(self, predicted_no_show_rate: float) -> float:
        """
        Calculate overbooking factor based on predicted no-show rate.
        
        Args:
            predicted_no_show_rate: Expected no-show rate (0.0 to 1.0)
        
        Returns:
            Overbooking multiplier (e.g., 1.2 means book 20% more slots)
        """
        if predicted_no_show_rate >= 0.3:
            return 1.3  # High no-show rate: book 30% more
        elif predicted_no_show_rate >= 0.2:
            return 1.2  # Medium no-show rate: book 20% more
        elif predicted_no_show_rate >= 0.1:
            return 1.1  # Low no-show rate: book 10% more
        else:
            return 1.0  # Very low no-show rate: no overbooking
    
    def should_send_reminder(self, no_show_probability: float) -> bool:
        """
        Determine if SMS reminder should be sent based on no-show risk.
        
        Args:
            no_show_probability: Predicted no-show probability (0.0 to 1.0)
        
        Returns:
            True if reminder should be sent
        """
        return no_show_probability >= 0.25  # Send reminder for medium+ risk
    
    def get_model_info(self) -> dict:
        """Get information about the loaded model."""
        if self.model is None:
            return {
                "status": "not_loaded",
                "message": "Model not available. Run training script."
            }
        
        try:
            metadata_path = os.path.join("app", "ml", "models", "noshow_metadata.pkl")
            if os.path.exists(metadata_path):
                metadata = joblib.load(metadata_path)
                return {
                    "status": "loaded",
                    "model_type": metadata.get("model_type"),
                    "n_features": metadata.get("n_features"),
                    "test_accuracy": f"{metadata.get('test_accuracy', 0)*100:.2f}%",
                    "test_auc": f"{metadata.get('test_auc', 0):.4f}",
                    "trained_date": metadata.get("trained_date"),
                    "top_features": [f[0] for f in metadata.get("top_features", [])[:5]]
                }
        except Exception as e:
            return {
                "status": "loaded",
                "message": f"Model loaded but metadata unavailable: {e}"
            }
        
        return {
            "status": "loaded",
            "message": "Model loaded successfully"
        }


# Example usage
if __name__ == "__main__":
    predictor = NoShowPredictor()
    
    # Test prediction
    result = predictor.predict_no_show(
        age=45,
        gender="F",
        booking_gap_days=7,
        previous_no_shows=0,
        sms_received=1,
        scholarship=0,
        hypertension=1,
        diabetes=0
    )
    
    print("\n" + "=" * 60)
    print("   NO-SHOW PREDICTION TEST")
    print("=" * 60)
    print(f"\n   No-Show Probability: {result['percentage']}%")
    print(f"   Risk Level: {result['risk_level']}")
    print(f"   Recommendation: {result['recommendation']}")
    print(f"   Confidence: {result['confidence']}")
    print("\n" + "=" * 60 + "\n")
    
    # Model info
    info = predictor.get_model_info()
    print("   Model Info:")
    for key, value in info.items():
        print(f"      {key}: {value}")
    print("=" * 60 + "\n")
