"""
Quick test for specific intents.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
app = create_app()

with app.app_context():
    from app.services.chatbot_service import HospitalChatbot
    
    bot = HospitalChatbot()
    
    # Test high-risk and no-show intents
    tests = [
        ("High-risk patients", "admin"),
        ("No-show predictions", "admin"),
        ("Show high risk patients", "admin"),
        ("no show prediction", "admin"),
    ]
    
    for message, role in tests:
        print(f"\nMessage: '{message}'")
        response = bot.process_message(message, {'user_role': role})
        print(f"Type: {response.get('type')}")
        print(f"Response: {response['response'][:80]}...")
