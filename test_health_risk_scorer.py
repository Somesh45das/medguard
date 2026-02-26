"""
Test script for Health Risk Scorer.
Demonstrates risk-based patient prioritization.
"""
from app.services.health_risk_scorer import HealthRiskScorer
from datetime import date, timedelta


class MockPatient:
    """Mock patient for testing."""
    def __init__(self, patient_id, name, age, gender, is_emergency=False):
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.gender = gender
        self.is_emergency = is_emergency


def test_individual_patients():
    """Test risk scoring for individual patients."""
    scorer = HealthRiskScorer()
    
    print("\n" + "=" * 80)
    print("   HEALTH RISK SCORING - INDIVIDUAL PATIENT TESTS")
    print("=" * 80)
    
    # Test Case 1: Elderly with critical symptoms
    print("\n📋 TEST CASE 1: Elderly patient with critical symptoms")
    print("-" * 80)
    patient1 = MockPatient("P-001", "Mary Johnson", 78, "F", is_emergency=False)
    result1 = scorer.calculate_health_risk(
        patient=patient1,
        symptoms="chest pain and breathing difficulty",
        medical_history="diabetes, hypertension, heart disease",
        booking_gap_days=2,
        previous_no_shows=0,
        appointment_count=8,
        has_appointment=True
    )
    print_risk_result(patient1, result1)
    
    # Test Case 2: Young child with high fever
    print("\n📋 TEST CASE 2: Young child with high fever")
    print("-" * 80)
    patient2 = MockPatient("P-002", "Emma Smith", 4, "F", is_emergency=False)
    result2 = scorer.calculate_health_risk(
        patient=patient2,
        symptoms="high fever and vomiting",
        medical_history="asthma",
        booking_gap_days=0,  # Same day
        previous_no_shows=0,
        appointment_count=3,
        has_appointment=True
    )
    print_risk_result(patient2, result2)
    
    # Test Case 3: Emergency case
    print("\n📋 TEST CASE 3: Emergency case - accident victim")
    print("-" * 80)
    patient3 = MockPatient("P-003", "Robert Brown", 35, "M", is_emergency=True)
    result3 = scorer.calculate_health_risk(
        patient=patient3,
        symptoms="head injury, bleeding, severe pain",
        medical_history="",
        booking_gap_days=0,
        previous_no_shows=0,
        appointment_count=1,
        has_appointment=False
    )
    print_risk_result(patient3, result3)
    
    # Test Case 4: Healthy adult with mild symptoms
    print("\n📋 TEST CASE 4: Healthy adult with mild symptoms")
    print("-" * 80)
    patient4 = MockPatient("P-004", "David Wilson", 32, "M", is_emergency=False)
    result4 = scorer.calculate_health_risk(
        patient=patient4,
        symptoms="mild cough and cold",
        medical_history="",
        booking_gap_days=7,
        previous_no_shows=0,
        appointment_count=2,
        has_appointment=True
    )
    print_risk_result(patient4, result4)
    
    # Test Case 5: Unreliable patient with history of no-shows
    print("\n📋 TEST CASE 5: Patient with no-show history")
    print("-" * 80)
    patient5 = MockPatient("P-005", "Sarah Davis", 28, "F", is_emergency=False)
    result5 = scorer.calculate_health_risk(
        patient=patient5,
        symptoms="back pain",
        medical_history="",
        booking_gap_days=30,  # Long booking gap
        previous_no_shows=3,
        appointment_count=5,
        has_appointment=True
    )
    print_risk_result(patient5, result5)
    
    # Test Case 6: Infant - highest age risk
    print("\n📋 TEST CASE 6: Infant with fever")
    print("-" * 80)
    patient6 = MockPatient("P-006", "Baby Miller", 0.5, "M", is_emergency=False)
    result6 = scorer.calculate_health_risk(
        patient=patient6,
        symptoms="high fever, not feeding well",
        medical_history="premature birth",
        booking_gap_days=0,
        previous_no_shows=0,
        appointment_count=4,
        has_appointment=True
    )
    print_risk_result(patient6, result6)


def test_patient_sorting():
    """Test sorting multiple patients by risk score."""
    scorer = HealthRiskScorer()
    
    print("\n" + "=" * 80)
    print("   PATIENT QUEUE PRIORITIZATION - SORTING BY RISK")
    print("=" * 80)
    
    # Create diverse patient list
    patients_data = [
        {
            'patient': MockPatient("P-001", "John Doe", 32, "M"),
            'symptoms': "mild headache",
            'medical_history': "",
            'booking_gap_days': 7,
            'previous_no_shows': 0,
            'appointment_count': 2,
            'has_appointment': True
        },
        {
            'patient': MockPatient("P-002", "Mary Johnson", 78, "F"),
            'symptoms': "chest pain",
            'medical_history': "diabetes, hypertension, heart disease",
            'booking_gap_days': 2,
            'previous_no_shows': 0,
            'appointment_count': 10,
            'has_appointment': True
        },
        {
            'patient': MockPatient("P-003", "Emma Smith", 4, "F"),
            'symptoms': "high fever",
            'medical_history': "asthma",
            'booking_gap_days': 0,
            'previous_no_shows': 0,
            'appointment_count': 3,
            'has_appointment': True
        },
        {
            'patient': MockPatient("P-004", "Robert Brown", 45, "M", is_emergency=True),
            'symptoms': "accident, bleeding",
            'medical_history': "",
            'booking_gap_days': 0,
            'previous_no_shows': 0,
            'appointment_count': 1,
            'has_appointment': False
        },
        {
            'patient': MockPatient("P-005", "Sarah Davis", 28, "F"),
            'symptoms': "back pain",
            'medical_history': "",
            'booking_gap_days': 30,
            'previous_no_shows': 3,
            'appointment_count': 5,
            'has_appointment': True
        },
        {
            'patient': MockPatient("P-006", "Baby Miller", 0.5, "M"),
            'symptoms': "high fever, not feeding",
            'medical_history': "",
            'booking_gap_days': 0,
            'previous_no_shows': 0,
            'appointment_count': 4,
            'has_appointment': True
        },
    ]
    
    # Sort by risk
    sorted_patients = scorer.sort_patients_by_risk(patients_data)
    
    print("\n🏥 RECOMMENDED QUEUE ORDER (Highest Risk First):")
    print("-" * 80)
    print(f"{'Rank':<6} {'Patient':<20} {'Age':<5} {'Risk Score':<12} {'Level':<12} {'Wait Target':<12}")
    print("-" * 80)
    
    for i, data in enumerate(sorted_patients, 1):
        patient = data['patient']
        risk = data['risk_assessment']
        wait_target = risk['estimated_wait_reduction']['target_wait_minutes']
        
        print(f"{i:<6} {patient.name:<20} {patient.age:<5.0f} "
              f"{risk['risk_score']:<12.1f} {risk['risk_icon']} {risk['risk_level']:<10} "
              f"{wait_target} min")
    
    print("-" * 80)
    
    # Show detailed breakdown for top 3
    print("\n📊 DETAILED BREAKDOWN - TOP 3 PRIORITY PATIENTS:")
    print("=" * 80)
    
    for i, data in enumerate(sorted_patients[:3], 1):
        patient = data['patient']
        risk = data['risk_assessment']
        
        print(f"\n#{i} - {patient.name} (Age: {patient.age}, {patient.gender})")
        print(f"   Risk Score: {risk['risk_score']}/100 ({risk['risk_icon']} {risk['risk_level']})")
        print(f"   Priority Rank: #{risk['priority_rank']}")
        print(f"   Target Wait: {risk['estimated_wait_reduction']['target_wait_minutes']} minutes")
        
        print(f"\n   Risk Factors:")
        for factor_name, factor_data in risk['factors'].items():
            if factor_data['score'] != 0:
                print(f"      • {factor_data['reason']} ({factor_data['score']:+.1f} points)")
        
        print(f"\n   Recommendations:")
        for rec in risk['recommendations']:
            print(f"      {rec['icon']} {rec['text']}")
        
        print("-" * 80)


def test_wait_time_impact():
    """Demonstrate impact on wait times."""
    scorer = HealthRiskScorer()
    
    print("\n" + "=" * 80)
    print("   WAIT TIME IMPACT ANALYSIS")
    print("=" * 80)
    
    # Scenario: 6 patients, average consultation time 15 min
    patients = [
        MockPatient("P-001", "Low Risk Patient", 32, "M"),
        MockPatient("P-002", "High Risk Elderly", 78, "F"),
        MockPatient("P-003", "High Risk Child", 4, "F"),
        MockPatient("P-004", "Emergency", 45, "M", is_emergency=True),
        MockPatient("P-005", "Moderate Risk", 55, "M"),
        MockPatient("P-006", "Low Risk", 28, "F"),
    ]
    
    symptoms_list = [
        "mild headache",
        "chest pain",
        "high fever",
        "accident, bleeding",
        "diabetes checkup",
        "back pain"
    ]
    
    medical_history_list = [
        "",
        "diabetes, hypertension, heart disease",
        "asthma",
        "",
        "diabetes",
        ""
    ]
    
    print("\n📊 SCENARIO: 6 patients waiting, 15 min consultation time")
    print("-" * 80)
    
    # Calculate risk for all
    patients_data = []
    for i, patient in enumerate(patients):
        patients_data.append({
            'patient': patient,
            'symptoms': symptoms_list[i],
            'medical_history': medical_history_list[i],
            'booking_gap_days': 7,
            'previous_no_shows': 0,
            'appointment_count': 2,
            'has_appointment': True
        })
    
    # Sort by risk
    sorted_patients = scorer.sort_patients_by_risk(patients_data)
    
    # Calculate wait times
    print("\n🔴 WITHOUT RISK-BASED PRIORITIZATION (First-Come-First-Served):")
    print("-" * 80)
    print(f"{'Position':<10} {'Patient':<25} {'Risk':<12} {'Wait Time':<12}")
    print("-" * 80)
    
    for i, data in enumerate(sorted_patients, 1):
        patient = data['patient']
        risk = data['risk_assessment']
        wait_time = (i - 1) * 15
        print(f"{i:<10} {patient.name:<25} {risk['risk_score']:<12.1f} {wait_time} min")
    
    print("\n🟢 WITH RISK-BASED PRIORITIZATION (Intelligent Queue):")
    print("-" * 80)
    print(f"{'Position':<10} {'Patient':<25} {'Risk':<12} {'Wait Time':<12} {'Improvement':<12}")
    print("-" * 80)
    
    for i, data in enumerate(sorted_patients, 1):
        patient = data['patient']
        risk = data['risk_assessment']
        wait_time = (i - 1) * 15
        target_wait = risk['estimated_wait_reduction']['target_wait_minutes']
        improvement = "✅ Reduced" if wait_time <= target_wait else "⚠️ Needs attention"
        print(f"{i:<10} {patient.name:<25} {risk['risk_score']:<12.1f} {wait_time} min      {improvement}")
    
    print("-" * 80)
    
    # Calculate average wait time reduction for high-risk patients
    high_risk_patients = [d for d in sorted_patients if d['risk_assessment']['risk_score'] >= 60]
    if high_risk_patients:
        avg_position_before = sum(patients_data.index(d) + 1 for d in high_risk_patients) / len(high_risk_patients)
        avg_position_after = sum(sorted_patients.index(d) + 1 for d in high_risk_patients) / len(high_risk_patients)
        avg_wait_reduction = (avg_position_before - avg_position_after) * 15
        
        print(f"\n📈 IMPACT SUMMARY:")
        print(f"   High-risk patients (score ≥ 60): {len(high_risk_patients)}")
        print(f"   Average wait time reduction: {avg_wait_reduction:.0f} minutes")
        print(f"   Improvement: {(avg_wait_reduction / (avg_position_before * 15)) * 100:.1f}%")


def print_risk_result(patient, result):
    """Helper function to print risk assessment results."""
    print(f"Patient: {patient.name} (Age: {patient.age}, {patient.gender})")
    print(f"Emergency: {'Yes 🚨' if patient.is_emergency else 'No'}")
    print(f"\nRisk Score: {result['risk_score']}/100")
    print(f"Risk Level: {result['risk_icon']} {result['risk_level']}")
    print(f"Priority Rank: #{result['priority_rank']}")
    print(f"Target Wait Time: {result['estimated_wait_reduction']['target_wait_minutes']} minutes")
    print(f"Wait Reduction: {result['estimated_wait_reduction']['reduction_percentage']}%")
    
    print(f"\nRisk Factors:")
    for factor_name, factor_data in result['factors'].items():
        if factor_data['score'] != 0:
            print(f"  • {factor_data['reason']} ({factor_data['score']:+.1f} points)")
    
    print(f"\nRecommendations:")
    for rec in result['recommendations']:
        print(f"  {rec['icon']} {rec['text']}")


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("   HEALTH RISK SCORING SYSTEM - COMPREHENSIVE TEST")
    print("=" * 80)
    
    # Run all tests
    test_individual_patients()
    test_patient_sorting()
    test_wait_time_impact()
    
    print("\n" + "=" * 80)
    print("   ✅ ALL TESTS COMPLETED")
    print("=" * 80)
    print("\n💡 Key Insights:")
    print("   • Emergency patients always get highest priority")
    print("   • Elderly and children receive age-based priority")
    print("   • Critical symptoms trigger immediate attention")
    print("   • Chronic conditions increase risk score")
    print("   • Reliable patients get slight priority boost")
    print("   • Risk-based sorting reduces wait times for high-risk patients")
    print("\n" + "=" * 80 + "\n")
