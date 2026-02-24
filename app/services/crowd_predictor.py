"""
ML-based crowd level prediction service.
Uses historical data to predict OPD crowd levels.
"""
import os
import numpy as np
import joblib
from datetime import datetime, date
from config import Config


class CrowdPredictor:
    """Predicts crowd levels using a trained ML model."""

    CROWD_LEVELS = {0: "low", 1: "medium", 2: "high", 3: "critical"}
    CROWD_COLORS = {
        "low": "#28a745",
        "medium": "#ffc107",
        "high": "#fd7e14",
        "critical": "#dc3545",
    }

    def __init__(self):
        self.model = None
        self.scaler = None
        self._load_model()

    def _load_model(self):
        """Load the trained model and scaler from disk."""
        try:
            if os.path.exists(Config.ML_MODEL_PATH):
                self.model = joblib.load(Config.ML_MODEL_PATH)
                self.scaler = joblib.load(Config.ML_SCALER_PATH)
        except Exception as e:
            print(f"[CrowdPredictor] Model not loaded: {e}")
            self.model = None

    def _build_features(
        self,
        department_id: int,
        target_date: date,
        hour: int,
        is_holiday: bool = False,
        temperature: float = 25.0,
        current_count: int = 0,
    ) -> np.ndarray:
        """Build feature vector for prediction."""
        day_of_week = target_date.weekday()
        month = target_date.month
        is_weekend = 1 if day_of_week >= 5 else 0
        is_monday = 1 if day_of_week == 0 else 0

        # Peak hour indicators
        is_morning_peak = 1 if 9 <= hour <= 11 else 0
        is_afternoon_peak = 1 if 14 <= hour <= 16 else 0

        # Seasonal indicator (flu season: Nov-Feb)
        is_flu_season = 1 if month in [11, 12, 1, 2] else 0

        features = np.array(
            [
                [
                    department_id,
                    hour,
                    day_of_week,
                    month,
                    int(is_holiday),
                    is_weekend,
                    is_monday,
                    is_morning_peak,
                    is_afternoon_peak,
                    is_flu_season,
                    temperature,
                    current_count,
                ]
            ]
        )
        return features

    def predict_crowd_level(
        self,
        department_id: int,
        target_date: date = None,
        hour: int = None,
        is_holiday: bool = False,
        temperature: float = 25.0,
        current_count: int = 0,
    ) -> dict:
        """
        Predict crowd level for a given department, date, and hour.

        Returns dict with level, confidence, color, patient_estimate.
        """
        if target_date is None:
            target_date = date.today()
        if hour is None:
            hour = datetime.now().hour

        features = self._build_features(
            department_id, target_date, hour, is_holiday, temperature, current_count
        )

        # If model is available, use it
        if self.model is not None and self.scaler is not None:
            scaled = self.scaler.transform(features)
            prediction = self.model.predict(scaled)[0]
            probabilities = self.model.predict_proba(scaled)[0]
            confidence = float(max(probabilities)) * 100
        else:
            # Fallback: rule-based prediction
            prediction, confidence = self._rule_based_predict(
                hour, target_date.weekday(), current_count
            )

        level = self.CROWD_LEVELS.get(prediction, "medium")
        patient_estimate = self._estimate_patient_count(level, hour)

        return {
            "level": level,
            "level_code": int(prediction),
            "confidence": round(confidence, 1),
            "color": self.CROWD_COLORS[level],
            "patient_estimate": patient_estimate,
            "hour": hour,
            "date": target_date.isoformat(),
            "department_id": department_id,
        }

    def _rule_based_predict(self, hour: int, day_of_week: int, current_count: int):
        """Fallback rule-based prediction when ML model is unavailable."""
        score = 0

        # Time-based scoring
        if 9 <= hour <= 11:
            score += 3
        elif 14 <= hour <= 16:
            score += 2
        elif 8 <= hour <= 12:
            score += 1

        # Day-based scoring
        if day_of_week == 0:  # Monday
            score += 2
        elif day_of_week in [1, 2]:
            score += 1
        elif day_of_week >= 5:  # Weekend
            score -= 1

        # Current load
        if current_count > 30:
            score += 2
        elif current_count > 15:
            score += 1

        # Map to levels
        if score >= 5:
            return 3, 70.0  # critical
        elif score >= 3:
            return 2, 65.0  # high
        elif score >= 1:
            return 1, 60.0  # medium
        else:
            return 0, 75.0  # low

    def _estimate_patient_count(self, level: str, hour: int) -> int:
        """Estimate patient count based on crowd level."""
        base = {"low": 8, "medium": 20, "high": 35, "critical": 50}
        count = base.get(level, 15)

        # Adjust for hour
        if 9 <= hour <= 11:
            count = int(count * 1.3)
        elif hour < 9 or hour > 17:
            count = int(count * 0.5)

        return count

    def predict_day_timeline(
        self, department_id: int, target_date: date = None
    ) -> list:
        """Predict crowd levels for every hour of OPD operation."""
        if target_date is None:
            target_date = date.today()

        timeline = []
        for hour in range(Config.OPD_START_HOUR, Config.OPD_END_HOUR + 1):
            pred = self.predict_crowd_level(department_id, target_date, hour)
            pred["time_label"] = f"{hour:02d}:00"
            timeline.append(pred)

        return timeline
