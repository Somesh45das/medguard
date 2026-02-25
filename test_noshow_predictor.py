"""
Test the No-Show Predictor service.
"""
from app.services.noshow_predictor import NoShowPredictor

# Initialize predictor
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
print(f"   Show Probability: {result['show_probability']*100:.1f}%")
print(f"   Risk Level: {result['risk_level']}")
print(f"   Recommendation: {result['recommendation']}")
print(f"   Confidence: {result['confidence']}")

# Test high-risk patient
print("\n" + "=" * 60)
print("   HIGH-RISK PATIENT TEST")
print("=" * 60)

result2 = predictor.predict_no_show(
    age=25,
    gender="M",
    booking_gap_days=45,
    previous_no_shows=2,
    sms_received=0,
    scholarship=1
)

print(f"\n   No-Show Probability: {result2['percentage']}%")
print(f"   Risk Level: {result2['risk_level']}")
print(f"   Recommendation: {result2['recommendation']}")

# Model info
print("\n" + "=" * 60)
print("   MODEL INFORMATION")
print("=" * 60)

info = predictor.get_model_info()
for key, value in info.items():
    print(f"   {key}: {value}")

print("\n" + "=" * 60 + "\n")
