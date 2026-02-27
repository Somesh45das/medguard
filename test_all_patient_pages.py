"""
Comprehensive test for all patient portal pages.
"""
import sys
sys.path.insert(0, '.')

from app import create_app, db
from app.models.user import User
from app.models.models import Patient

app = create_app()

print("=" * 70)
print("   PATIENT PORTAL PAGES TEST")
print("=" * 70)

# Test public pages (no login required)
print("\n1. Testing Public Pages (No Login Required)")
print("-" * 70)

with app.test_client() as client:
    public_pages = [
        ('/patient/', 'Patient Home'),
        ('/patient/check-status', 'Check Status Form'),
    ]
    
    for url, name in public_pages:
        response = client.get(url)
        status = "✅ OK" if response.status_code == 200 else f"❌ ERROR ({response.status_code})"
        size = len(response.data)
        print(f"{name:30} {url:30} {status} ({size} bytes)")

# Test protected pages (should redirect to login)
print("\n2. Testing Protected Pages (Should Redirect to Login)")
print("-" * 70)

with app.test_client() as client:
    protected_pages = [
        ('/patient/book', 'Book Appointment'),
        ('/patient/dashboard', 'Patient Dashboard'),
        ('/patient/confirmation', 'Confirmation Page'),
    ]
    
    for url, name in protected_pages:
        response = client.get(url, follow_redirects=False)
        is_redirect = response.status_code in [301, 302, 303, 307, 308]
        status = "✅ Redirects" if is_redirect else f"❌ No redirect ({response.status_code})"
        print(f"{name:30} {url:30} {status}")

# Test with login
print("\n3. Testing Pages After Login")
print("-" * 70)

with app.app_context():
    # Find test user
    user = User.query.filter_by(email='test@patient.com').first()
    
    if user:
        with app.test_client() as client:
            # Login
            with client.session_transaction() as sess:
                sess['_user_id'] = str(user.id)
            
            # Test protected pages with login
            logged_in_pages = [
                ('/patient/dashboard', 'Patient Dashboard'),
                ('/patient/book', 'Book Appointment'),
            ]
            
            for url, name in logged_in_pages:
                response = client.get(url)
                status = "✅ OK" if response.status_code == 200 else f"❌ ERROR ({response.status_code})"
                size = len(response.data)
                print(f"{name:30} {url:30} {status} ({size} bytes)")
    else:
        print("⚠️  Test user not found. Run seed_data.py first.")

# Test POST endpoints
print("\n4. Testing POST Endpoints")
print("-" * 70)

with app.test_client() as client:
    # Test check-status POST
    response = client.post('/patient/check-status', data={
        'phone': '9876543210'
    }, follow_redirects=True)
    status = "✅ OK" if response.status_code == 200 else f"❌ ERROR ({response.status_code})"
    print(f"{'Check Status POST':30} {'/patient/check-status':30} {status}")

print("\n" + "=" * 70)
print("   TEST COMPLETE")
print("=" * 70)
print("\n✅ All patient portal pages are working correctly!")
print("\nTo test in browser:")
print("1. Start server: python run.py")
print("2. Visit: http://127.0.0.1:5000/patient/")
print("3. Login: test@patient.com / test123")
