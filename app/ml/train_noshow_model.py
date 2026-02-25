"""
Train No-Show Prediction Model.
Uses processed Medical Appointment No-Show dataset.

Model: Random Forest Classifier
Target: Predict if patient will miss appointment (0=show, 1=no-show)
"""
import os
import sys
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import (
    classification_report, 
    accuracy_score, 
    roc_auc_score,
    confusion_matrix,
    precision_recall_fscore_support
)
import warnings
warnings.filterwarnings('ignore')

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from config import Config


def load_processed_data(filepath="data/processed/no_show_processed.csv"):
    """Load the preprocessed no-show dataset."""
    print(f"Loading processed data from: {filepath}")
    
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        print("\n📥 Please run preprocessing first:")
        print("   python app/ml/preprocess_noshow.py")
        return None
    
    df = pd.read_csv(filepath)
    print(f"✅ Loaded {len(df):,} records")
    
    return df


def prepare_features(df):
    """Prepare features for ML training."""
    print("\n[1/5] Preparing features...")
    
    # Select feature columns
    feature_columns = [
        # Patient demographics
        'Age', 'is_elderly', 'is_child',
        'Scholarship', 'health_risk_score',
        
        # Patient history
        'previous_no_shows', 'appointment_count',
        
        # Appointment characteristics
        'booking_gap_days', 'is_same_day', 'is_short_notice',
        'day_of_week', 'month', 'is_weekend', 'is_monday',
        'SMS_received',
        
        # Medical conditions
        'Hipertension', 'Diabetes', 'Alcoholism', 'Handcap',
    ]
    
    # Encode categorical variables
    le_gender = LabelEncoder()
    df['Gender_encoded'] = le_gender.fit_transform(df['Gender'])
    feature_columns.append('Gender_encoded')
    
    # Handle age_group if present
    if 'age_group' in df.columns:
        le_age_group = LabelEncoder()
        df['age_group_encoded'] = le_age_group.fit_transform(df['age_group'].astype(str))
        feature_columns.append('age_group_encoded')
    
    X = df[feature_columns].values
    y = df['no_show'].values
    
    print(f"   Features: {len(feature_columns)}")
    print(f"   Samples: {len(X):,}")
    print(f"   No-show rate: {y.mean()*100:.2f}%")
    
    return X, y, feature_columns


def train_model(X_train, y_train, X_test, y_test, feature_names):
    """Train Random Forest classifier."""
    print("\n[2/5] Training Random Forest model...")
    
    # Initialize model
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=15,
        min_samples_split=10,
        min_samples_leaf=5,
        max_features='sqrt',
        random_state=42,
        n_jobs=-1,
        class_weight='balanced'  # Handle imbalanced classes
    )
    
    # Train
    print("   Training in progress...")
    model.fit(X_train, y_train)
    print("   ✅ Training complete")
    
    return model


def evaluate_model(model, X_train, y_train, X_test, y_test, feature_names):
    """Evaluate model performance."""
    print("\n[3/5] Evaluating model...")
    
    # Predictions
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)
    
    # Probabilities for ROC-AUC
    y_train_proba = model.predict_proba(X_train)[:, 1]
    y_test_proba = model.predict_proba(X_test)[:, 1]
    
    # Metrics
    train_acc = accuracy_score(y_train, y_train_pred)
    test_acc = accuracy_score(y_test, y_test_pred)
    train_auc = roc_auc_score(y_train, y_train_proba)
    test_auc = roc_auc_score(y_test, y_test_proba)
    
    print(f"\n   Training Accuracy: {train_acc:.4f} ({train_acc*100:.2f}%)")
    print(f"   Testing Accuracy:  {test_acc:.4f} ({test_acc*100:.2f}%)")
    print(f"   Training ROC-AUC:  {train_auc:.4f}")
    print(f"   Testing ROC-AUC:   {test_auc:.4f}")
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, y_test_pred)
    print(f"\n   Confusion Matrix:")
    print(f"                 Predicted")
    print(f"                 Show  No-Show")
    print(f"   Actual Show    {cm[0,0]:5d}  {cm[0,1]:5d}")
    print(f"   Actual No-Show {cm[1,0]:5d}  {cm[1,1]:5d}")
    
    # Classification Report
    print(f"\n   Classification Report:")
    precision, recall, f1, support = precision_recall_fscore_support(
        y_test, y_test_pred, average=None, labels=[0, 1]
    )
    
    print(f"                 Precision  Recall  F1-Score  Support")
    print(f"   Show (0)       {precision[0]:.4f}    {recall[0]:.4f}  {f1[0]:.4f}    {support[0]:,}")
    print(f"   No-Show (1)    {precision[1]:.4f}    {recall[1]:.4f}  {f1[1]:.4f}    {support[1]:,}")
    
    # Feature Importance
    print(f"\n   Top 10 Most Important Features:")
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1][:10]
    
    for i, idx in enumerate(indices, 1):
        bar = "█" * int(importances[idx] * 50)
        print(f"   {i:2d}. {feature_names[idx]:25s} {importances[idx]:.4f} {bar}")
    
    return {
        'train_accuracy': train_acc,
        'test_accuracy': test_acc,
        'train_auc': train_auc,
        'test_auc': test_auc,
        'confusion_matrix': cm,
        'feature_importance': dict(zip(feature_names, importances))
    }


def cross_validate(model, X, y):
    """Perform cross-validation."""
    print("\n[4/5] Performing 5-fold cross-validation...")
    
    cv_scores = cross_val_score(model, X, y, cv=5, scoring='accuracy', n_jobs=-1)
    cv_auc = cross_val_score(model, X, y, cv=5, scoring='roc_auc', n_jobs=-1)
    
    print(f"   Accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
    print(f"   ROC-AUC:  {cv_auc.mean():.4f} (+/- {cv_auc.std():.4f})")
    print(f"   Fold scores: {[f'{s:.4f}' for s in cv_scores]}")
    
    return cv_scores, cv_auc


def save_model(model, scaler, feature_names, metrics):
    """Save trained model and metadata."""
    print("\n[5/5] Saving model...")
    
    # Create models directory
    models_dir = os.path.join("app", "ml", "models")
    os.makedirs(models_dir, exist_ok=True)
    
    # Save model
    model_path = os.path.join(models_dir, "noshow_model.pkl")
    joblib.dump(model, model_path)
    print(f"   ✅ Model saved to: {model_path}")
    
    # Save scaler
    scaler_path = os.path.join(models_dir, "noshow_scaler.pkl")
    joblib.dump(scaler, scaler_path)
    print(f"   ✅ Scaler saved to: {scaler_path}")
    
    # Save feature names
    features_path = os.path.join(models_dir, "noshow_features.pkl")
    joblib.dump(feature_names, features_path)
    print(f"   ✅ Features saved to: {features_path}")
    
    # Save metadata
    metadata = {
        'model_type': 'RandomForestClassifier',
        'n_features': len(feature_names),
        'feature_names': feature_names,
        'train_accuracy': metrics['train_accuracy'],
        'test_accuracy': metrics['test_accuracy'],
        'train_auc': metrics['train_auc'],
        'test_auc': metrics['test_auc'],
        'trained_date': pd.Timestamp.now().isoformat(),
        'top_features': sorted(
            metrics['feature_importance'].items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:10]
    }
    
    metadata_path = os.path.join(models_dir, "noshow_metadata.pkl")
    joblib.dump(metadata, metadata_path)
    print(f"   ✅ Metadata saved to: {metadata_path}")
    
    return model_path


def generate_model_card(metrics, output_path="app/ml/models/NOSHOW_MODEL_CARD.md"):
    """Generate model card documentation."""
    print("\n[BONUS] Generating model card...")
    
    with open(output_path, 'w') as f:
        f.write("# No-Show Prediction Model Card\n\n")
        f.write("## Model Overview\n\n")
        f.write("**Model Type:** Random Forest Classifier  \n")
        f.write("**Purpose:** Predict patient no-show probability for appointment optimization  \n")
        f.write("**Training Date:** " + pd.Timestamp.now().strftime("%Y-%m-%d") + "  \n\n")
        
        f.write("## Performance Metrics\n\n")
        f.write(f"- **Test Accuracy:** {metrics['test_accuracy']*100:.2f}%\n")
        f.write(f"- **Test ROC-AUC:** {metrics['test_auc']:.4f}\n")
        f.write(f"- **Training Accuracy:** {metrics['train_accuracy']*100:.2f}%\n")
        f.write(f"- **Training ROC-AUC:** {metrics['train_auc']:.4f}\n\n")
        
        f.write("## Confusion Matrix\n\n")
        cm = metrics['confusion_matrix']
        f.write("```\n")
        f.write("                 Predicted\n")
        f.write("                 Show  No-Show\n")
        f.write(f"Actual Show      {cm[0,0]:5d}  {cm[0,1]:5d}\n")
        f.write(f"Actual No-Show   {cm[1,0]:5d}  {cm[1,1]:5d}\n")
        f.write("```\n\n")
        
        f.write("## Top 10 Important Features\n\n")
        sorted_features = sorted(
            metrics['feature_importance'].items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:10]
        
        for i, (feature, importance) in enumerate(sorted_features, 1):
            f.write(f"{i}. **{feature}**: {importance:.4f}\n")
        
        f.write("\n## Dataset\n\n")
        f.write("**Source:** Medical Appointment No Shows (Kaggle)  \n")
        f.write("**Records:** 110,527 appointments  \n")
        f.write("**Location:** Brazil  \n")
        f.write("**Time Period:** April-June 2016  \n\n")
        
        f.write("## Usage\n\n")
        f.write("```python\n")
        f.write("from app.services.noshow_predictor import NoShowPredictor\n\n")
        f.write("predictor = NoShowPredictor()\n")
        f.write("probability = predictor.predict_no_show(\n")
        f.write("    age=45,\n")
        f.write("    booking_gap_days=7,\n")
        f.write("    previous_no_shows=0,\n")
        f.write("    sms_received=1,\n")
        f.write("    # ... other features\n")
        f.write(")\n")
        f.write("print(f'No-show probability: {probability:.2%}')\n")
        f.write("```\n\n")
        
        f.write("## Integration\n\n")
        f.write("This model is integrated into:\n")
        f.write("- `SlotOptimizer`: Adjusts overbooking strategy\n")
        f.write("- `AppointmentManager`: Flags high-risk appointments\n")
        f.write("- `SMSService`: Prioritizes reminder sending\n\n")
        
        f.write("## Limitations\n\n")
        f.write("- Trained on Brazilian hospital data (may not generalize to other regions)\n")
        f.write("- Does not account for real-time factors (traffic, weather on appointment day)\n")
        f.write("- Requires patient history for best accuracy\n\n")
        
        f.write("## Future Improvements\n\n")
        f.write("- Add real-time weather data\n")
        f.write("- Include transportation distance\n")
        f.write("- Implement online learning for continuous improvement\n")
        f.write("- Add explainability (SHAP values)\n")
    
    print(f"   ✅ Model card saved to: {output_path}")


def main():
    """Main training pipeline."""
    print("\n" + "=" * 70)
    print("   NO-SHOW PREDICTION MODEL TRAINING")
    print("=" * 70 + "\n")
    
    # Load data
    df = load_processed_data()
    if df is None:
        return
    
    # Prepare features
    X, y, feature_names = prepare_features(df)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\n   Train set: {len(X_train):,} samples")
    print(f"   Test set:  {len(X_test):,} samples")
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train model
    model = train_model(X_train_scaled, y_train, X_test_scaled, y_test, feature_names)
    
    # Evaluate
    metrics = evaluate_model(
        model, X_train_scaled, y_train, X_test_scaled, y_test, feature_names
    )
    
    # Cross-validate
    cv_scores, cv_auc = cross_validate(model, X_train_scaled, y_train)
    
    # Save model
    model_path = save_model(model, scaler, feature_names, metrics)
    
    # Generate model card
    generate_model_card(metrics)
    
    print("\n" + "=" * 70)
    print("   ✅ TRAINING COMPLETE!")
    print("=" * 70)
    print(f"\n   Model Accuracy: {metrics['test_accuracy']*100:.2f}%")
    print(f"   ROC-AUC Score: {metrics['test_auc']:.4f}")
    print(f"   Model saved to: {model_path}")
    print("\nNext steps:")
    print("  1. Review: app/ml/models/NOSHOW_MODEL_CARD.md")
    print("  2. Integrate: Update SlotOptimizer to use no-show predictions")
    print("  3. Test: python -c 'from app.services.noshow_predictor import NoShowPredictor; p = NoShowPredictor(); print(p.predict_no_show(age=45, booking_gap_days=7))'")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
