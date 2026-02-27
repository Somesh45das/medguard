"""Test chatbot functionality"""
from app import create_app

app = create_app()

print("\n" + "="*60)
print("🤖 TESTING CHATBOT")
print("="*60 + "\n")

# Test 1: Patient chatbot
print("1️⃣  Testing Patient Chatbot...")
with app.test_client() as client:
    # Login as patient
    client.post('/auth/login', data={'email': 'test@patient.com', 'password': 'test123'})
    
    # Test greeting
    response = client.post('/chatbot/message', json={'message': 'hello'})
    data = response.get_json()
    print(f"   Status: {response.status_code}")
    print(f"   Response: {data.get('response', 'No response')[:100]}...")
    print(f"   Role: {data.get('role', 'Unknown')}")
    print(f"   Suggestions: {len(data.get('suggestions', []))} suggestions")
    
    # Test booking query
    response = client.post('/chatbot/message', json={'message': 'book appointment'})
    data = response.get_json()
    print(f"\n   Book appointment query:")
    print(f"   Response: {data.get('response', 'No response')[:100]}...")

# Test 2: Admin chatbot
print("\n2️⃣  Testing Admin Chatbot...")
with app.test_client() as client:
    # Login as admin
    client.post('/auth/login', data={'email': 'admin@hospital.com', 'password': 'admin123'})
    
    # Test greeting
    response = client.post('/chatbot/message', json={'message': 'hello'})
    data = response.get_json()
    print(f"   Status: {response.status_code}")
    print(f"   Response: {data.get('response', 'No response')[:100]}...")
    print(f"   Role: {data.get('role', 'Unknown')}")
    print(f"   Suggestions: {len(data.get('suggestions', []))} suggestions")
    
    # Test stats query
    response = client.post('/chatbot/message', json={'message': 'queue stats'})
    data = response.get_json()
    print(f"\n   Queue stats query:")
    print(f"   Response: {data.get('response', 'No response')[:100]}...")

# Test 3: Unauthenticated
print("\n3️⃣  Testing Unauthenticated Chatbot...")
with app.test_client() as client:
    response = client.post('/chatbot/message', json={'message': 'hello'})
    data = response.get_json()
    print(f"   Status: {response.status_code}")
    print(f"   Response: {data.get('response', 'No response')[:100]}...")
    print(f"   Role: {data.get('role', 'Unknown')}")

print("\n" + "="*60)
print("✅ TESTING COMPLETE")
print("="*60 + "\n")
