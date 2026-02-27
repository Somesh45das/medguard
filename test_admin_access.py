"""
Test admin dashboard access
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app
from app.models.user import User

def test_admin():
    """Test admin dashboard."""
    app = create_app()
    
    with app.app_context():
        print("\n" + "="*60)
        print("🔍 TESTING ADMIN DASHBOARD ACCESS")
        print("="*60 + "\n")
        
        # Get admin user
        admin = User.query.filter_by(email="admin@hospital.com").first()
        if not admin:
            print("❌ Admin user not found!")
            return
        
        print(f"✅ Admin user found: {admin.name}")
        print(f"   Email: {admin.email}")
        print(f"   Role: {admin.role}")
        print(f"   Is Admin: {admin.is_admin()}")
        print(f"   Is Active: {admin.is_active}")
        
        # Test with logged in admin
        with app.test_client() as client:
            # Login as admin
            print("\n1️⃣  Logging in as admin...")
            response = client.post('/auth/login', data={
                'email': 'admin@hospital.com',
                'password': 'admin123',
                'remember_me': False
            }, follow_redirects=False)
            
            print(f"   Login response: {response.status_code}")
            if response.status_code == 302:
                print(f"   ✅ Login successful, redirects to: {response.location}")
            else:
                print(f"   ❌ Login failed")
                return
            
            # Now try to access admin dashboard
            print("\n2️⃣  Accessing admin dashboard...")
            response = client.get('/admin/', follow_redirects=False)
            print(f"   Response status: {response.status_code}")
            
            if response.status_code == 200:
                print("   ✅ Admin dashboard loads successfully!")
                print(f"   Response length: {len(response.data)} bytes")
                
                # Check if it's HTML
                if b'<!DOCTYPE html>' in response.data or b'<html' in response.data:
                    print("   ✅ Response is HTML")
                else:
                    print("   ⚠️  Response might not be HTML")
                
                # Check for common elements
                if b'dashboard' in response.data.lower():
                    print("   ✅ Contains 'dashboard' text")
                if b'admin' in response.data.lower():
                    print("   ✅ Contains 'admin' text")
                    
            elif response.status_code == 302:
                print(f"   🔄 Redirects to: {response.location}")
                print("   ⚠️  This shouldn't happen after login!")
            elif response.status_code == 500:
                print("   ❌ Server error (500)")
                print("   Check Flask console for error details")
            else:
                print(f"   ❌ Unexpected status: {response.status_code}")
            
            # Try accessing with follow_redirects=True
            print("\n3️⃣  Accessing with follow redirects...")
            response = client.get('/admin/', follow_redirects=True)
            print(f"   Final status: {response.status_code}")
            print(f"   Final URL: {response.request.path if hasattr(response, 'request') else 'unknown'}")
            
            if response.status_code == 200:
                print("   ✅ Page loads")
                # Show first 200 chars
                preview = response.data[:200].decode('utf-8', errors='ignore')
                print(f"   Preview: {preview}...")
            
        print("\n" + "="*60)
        print("✅ TESTING COMPLETE")
        print("="*60 + "\n")


if __name__ == "__main__":
    test_admin()
