"""
Train the crowd prediction ML model.
Uses Random Forest classifier on synthetic hospital data.
"""
import os
import sys
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score

# Add parent dirs to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from config import Config
from app.ml.generate_training_data import generate_crowd_data


def train_crowd_model():
    """Train and save the crowd prediction model."""
    print("=" * 60)
    print("   SMART HOSPITAL – Crowd Prediction Model Training")
    print("=" * 60)

    # 1. Generate / load data
    print("\n[1/5] Generating training data...")
    df = generate_crowd_data(num_days=365, num_departments=6)

    # 2. Prepare features
    print("[2/5] Preparing features...")
    feature_columns = [
        "department_id",
        "hour",
        "day_of_week",
        "month",
        "is_holiday",
        "is_weekend",
        "is_monday",
        "is_morning_peak",
        "is_afternoon_peak",
        "is_flu_season",
        "temperature",
        "patient_count",
    ]

    X = df[feature_columns].values
    y = df["crowd_level_code"].values

    print(f"   Features shape: {X.shape}")
    print(f"   Target classes: {np.unique(y)}")

    # 3. Split and scale
    print("[3/5] Splitting and scaling...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # 4. Train model
    print("[4/5] Training Random Forest model...")
    model = RandomForestClassifier(
        n_estimators=150,
        max_depth=20,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X_train_scaled, y_train)

    # 5. Evaluate
    print("[5/5] Evaluating model...\n")
    y_pred = model.predict(X_test_scaled)

    accuracy = accuracy_score(y_test, y_pred)
    print(f"   Accuracy: {accuracy:.4f} ({accuracy * 100:.1f}%)\n")

    level_names = ["low", "medium", "high", "critical"]
    print(classification_report(y_test, y_pred, target_names=level_names))

    # Cross-validation
    cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5)
    print(f"   Cross-validation: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")

    # Feature importance
    print("\n   Feature Importance:")
    importances = model.feature_importances_
    for name, imp in sorted(
        zip(feature_columns, importances), key=lambda x: x[1], reverse=True
    ):
        bar = "█" * int(imp * 50)
        print(f"   {name:25s} {imp:.4f} {bar}")

    # 6. Save model
    os.makedirs(os.path.dirname(Config.ML_MODEL_PATH), exist_ok=True)
    joblib.dump(model, Config.ML_MODEL_PATH)
    joblib.dump(scaler, Config.ML_SCALER_PATH)
    print(f"\n   ✅ Model saved to: {Config.ML_MODEL_PATH}")
    print(f"   ✅ Scaler saved to: {Config.ML_SCALER_PATH}")
    print("=" * 60)

    return model, scaler


if __name__ == "__main__":
    train_crowd_model()
