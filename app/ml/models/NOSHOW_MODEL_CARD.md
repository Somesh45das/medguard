# No-Show Prediction Model Card

## Model Overview

**Model Type:** Random Forest Classifier  
**Purpose:** Predict patient no-show probability for appointment optimization  
**Training Date:** 2026-02-25  

## Performance Metrics

- **Test Accuracy:** 62.42%
- **Test ROC-AUC:** 0.6206
- **Training Accuracy:** 69.33%
- **Training ROC-AUC:** 0.7617

## Confusion Matrix

```
                 Predicted
                 Show  No-Show
Actual Show       6876   3412
Actual No-Show    1997   2107
```

## Top 10 Important Features

1. **Age**: 0.2498
2. **booking_gap_days**: 0.1935
3. **appointment_count**: 0.0896
4. **previous_no_shows**: 0.0755
5. **day_of_week**: 0.0746
6. **age_group_encoded**: 0.0534
7. **month**: 0.0391
8. **SMS_received**: 0.0379
9. **Gender_encoded**: 0.0339
10. **health_risk_score**: 0.0253

## Dataset

**Source:** Medical Appointment No Shows (Kaggle)  
**Records:** 110,527 appointments  
**Location:** Brazil  
**Time Period:** April-June 2016  

## Usage

```python
from app.services.noshow_predictor import NoShowPredictor

predictor = NoShowPredictor()
probability = predictor.predict_no_show(
    age=45,
    booking_gap_days=7,
    previous_no_shows=0,
    sms_received=1,
    # ... other features
)
print(f'No-show probability: {probability:.2%}')
```

## Integration

This model is integrated into:
- `SlotOptimizer`: Adjusts overbooking strategy
- `AppointmentManager`: Flags high-risk appointments
- `SMSService`: Prioritizes reminder sending

## Limitations

- Trained on Brazilian hospital data (may not generalize to other regions)
- Does not account for real-time factors (traffic, weather on appointment day)
- Requires patient history for best accuracy

## Future Improvements

- Add real-time weather data
- Include transportation distance
- Implement online learning for continuous improvement
- Add explainability (SHAP values)
