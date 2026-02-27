"""
Test login functionality directly
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db
from app.models.user import User

def test_login():
    """Test login functionality."""
    app = create_app()
    
    with app.app_context():
        print("\n" + "="*60)
        print("🔐 TESTING LOGIN FUNCTIONALITY")
        print("="*60 + "\n")
        
        # Test admin login
        print("1️⃣  Testing Admin Login...")
        admin = User.query.filter_by(email="admin@hospital.com").first()
        if admin:
            print(f"   ✅ Admin user found: {admin.name}")
            print(f"   ✅ Email: {admin.email}")
            print(f"   ✅ Role: {admin.role}")
            print(f"   ✅ Is Admin: {admin.is_admin()}")
            print(f"   ✅ Is Active: {admin.is_active}")
            
            # Test password
            if admin.check_password("admin123"):
                print("   ✅ Password 'admin123' is CORRECT")
            else:
                print("   ❌ Password 'admin123' is WRONG")
        else:
            print("   ❌ Admin user NOT FOUND")
        
        # Test patient login
        print("\n2️⃣  Testing Patient Login...")
        patient_user = User.query.filter_by(email="test@patient.com").first()
        if patient_user:
            print(f"   ✅ Patient user found: {patient_user.name}")
            print(f"   ✅ Email: {patient_user.email}")
            print(f"   ✅ Role: {patient_user.role}")
            print(f"   ✅ Is Admin: {patient_user.is_admin()}")
            print(f"   ✅ Is Active: {patient_user.is_active}")
            print(f"   ✅ Patient ID: {patient_user.patient_id}")
            
            if patient_user.patient:
                print(f"   ✅ Patient record linked: {patient_user.patient.name}")
            else:
                print("   ⚠️  Patient record NOT linked")
            
            # Test password
            if patient_user.check_password("test123"):
                print("   ✅ Password 'test123' is CORRECT")
            else:
                print("   ❌ Password 'test123' is WRONG")
        else:
            print("   ❌ Patient user NOT FOUND")
        
        # Test Flask-Login integration
        print("\n3️⃣  Testing Flask-Login Integration...")
        from flask_login import login_user, current_user
        
        with app.test_request_context():
            # Test admin login
            if admin:
                login_user(admin)
                print(f"   ✅ Admin login_user() successful")
                print(f"   ✅ current_user.is_authenticated: {current_user.is_authenticated}")
                print(f"   ✅ current_user.name: {current_user.name}")
                print(f"   ✅ current_user.is_admin(): {current_user.is_admin()}")
        
        # Test routes
        print("\n4️⃣  Testing Routes...")
        with app.test_client() as client:
            # Test login page
            response = client.get('/auth/login')
            print(f"   GET /auth/login: {response.status_code}")
            if response.status_code == 200:
                print("   ✅ Login page loads")
            else:
                print("   ❌ Login page error")
            
            # Test admin dashboard (should redirect to login)
            response = client.get('/admin/', follow_redirects=False)
            print(f"   GET /admin/: {response.status_code}")
            if response.status_code in [302, 401]:
                print("   ✅ Admin dashboard protected (redirects)")
            else:
                print("   ⚠️  Admin dashboard not protected")
            
            # Test patient dashboard (should redirect to login)
            response = client.get('/patient/dashboard', follow_redirects=False)
            print(f"   GET /patient/dashboard: {response.status_code}")
            if response.status_code in [302, 401]:
                print("   ✅ Patient dashboard protected (redirects)")
            else:
                print("   ⚠️  Patient dashboard not protected")
        
        # Test actual login POST
        print("\n5️⃣  Testing Login POST...")
        with app.test_client() as client:
            # Test admin login
            response = client.post('/auth/login', data={
                'email': 'admin@hospital.com',
                'password': 'admin123',
                'remember_me': False
            }, follow_redirects=False)
            
            print(f"   POST /auth/login (admin): {response.status_code}")
            if response.status_code == 302:
                print(f"   ✅ Login successful (redirect)")
                print(f"   ✅ Redirect to: {response.location}")
            else:
                print(f"   ❌ Login failed")
                print(f"   Response: {response.data[:200]}")
        
        print("\n" + "="*60)
        print("✅ TESTING COMPLETE")
        print("="*60 + "\n")


if __name__ == "__main__":
    test_login()
