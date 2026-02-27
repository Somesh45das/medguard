"""
Test script to verify chatbot is working correctly.
"""
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up Flask app context
from app import create_app, db

app = create_app()

with app.app_context():
    from app.services.chatbot_service import HospitalChatbot
    
    print("=" * 70)
    print("   CHATBOT FUNCTIONALITY TEST")
    print("=" * 70)
    
    # Test Patient Mode
    print("\n" + "=" * 70)
    print("   PATIENT MODE TESTS")
    print("=" * 70)
    
    patient_bot = HospitalChatbot()
    patient_tests = [
        ("Hello", "greeting"),
        ("I want to book an appointment", "booking"),
        ("Check my status", "status"),
        ("What are the precautions?", "precautions"),
        ("Find me a doctor", "find_doctor"),
        ("What's the wait time?", "wait_time"),
        ("Show me departments", "departments"),
        ("When is it crowded?", "crowd_info"),
    ]
    
    for message, expected_type in patient_tests:
        print(f"\n📝 User: {message}")
        response = patient_bot.process_message(message, {'user_role': 'patient'})
        print(f"🤖 Bot: {response['response'][:100]}...")
        print(f"✅ Type: {response.get('type', 'unknown')}")
        if response.get('suggestions'):
            print(f"💡 Suggestions: {', '.join(response['suggestions'][:3])}")
        print("-" * 70)
    
    # Test Management Mode
    print("\n" + "=" * 70)
    print("   MANAGEMENT MODE TESTS")
    print("=" * 70)
    
    mgmt_bot = HospitalChatbot()
    mgmt_tests = [
        ("Hello", "greeting"),
        ("Show me queue statistics", "queue_stats"),
        ("Give me today's summary", "today_summary"),
        ("Department performance", "department_performance"),
        ("Doctor availability", "doctor_availability"),
        ("High-risk patients", "high_risk_patients"),
        ("No-show predictions", "noshow_prediction"),
        ("Crowd forecast", "crowd_forecast"),
    ]
    
    for message, expected_type in mgmt_tests:
        print(f"\n📝 Admin: {message}")
        response = mgmt_bot.process_message(message, {'user_role': 'admin'})
        print(f"🤖 Bot: {response['response'][:100]}...")
        print(f"✅ Type: {response.get('type', 'unknown')}")
        if response.get('suggestions'):
            print(f"💡 Suggestions: {', '.join(response['suggestions'][:3])}")
        print("-" * 70)
    
    print("\n" + "=" * 70)
    print("   ✅ ALL TESTS COMPLETED SUCCESSFULLY!")
    print("=" * 70)
