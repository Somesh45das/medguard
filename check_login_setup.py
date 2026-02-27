"""
Quick diagnostic script to verify login setup.
Run this to check if everything is configured correctly.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db
from app.models.user import User
from app.models.models import Patient

def check_setup():
    """Check if login system is properly configured."""
    app = create_app()
    
    with app.app_context():
        print("\n" + "="*60)
        print("🔍 LOGIN SETUP DIAGNOSTIC")
        print("="*60 + "\n")
        
        # Check database tables
        print("1️⃣  Checking database tables...")
        try:
            user_count = User.query.count()
            patient_count = Patient.query.count()
            print(f"   ✅ Users table: {user_count} users")
            print(f"   ✅ Patients table: {patient_count} patients")
        except Exception as e:
            print(f"   ❌ Database error: {e}")
            print("   💡 Run: python seed_data.py")
            return
        
        # Check admin user
        print("\n2️⃣  Checking admin account...")
        admin = User.query.filter_by(email="admin@hospital.com").first()
        if admin:
            print(f"   ✅ Admin found: {admin.name}")
            print(f"   ✅ Role: {admin.role}")
            print(f"   ✅ Active: {admin.is_active}")
            print(f"   ✅ Is Admin: {admin.is_admin()}")
        else:
            print("   ❌ Admin user not found")
            print("   💡 Run: python seed_data.py")
        
        # Check test patient user
        print("\n3️⃣  Checking test patient account...")
        test_user = User.query.filter_by(email="test@patient.com").first()
        if test_user:
            print(f"   ✅ Test user found: {test_user.name}")
            print(f"   ✅ Role: {test_user.role}")
            print(f"   ✅ Active: {test_user.is_active}")
            print(f"   ✅ Patient ID: {test_user.patient_id}")
            
            if test_user.patient:
                print(f"   ✅ Patient record linked: {test_user.patient.name}")
                print(f"   ✅ Patient phone: {test_user.patient.phone}")
            else:
                print("   ⚠️  Patient record NOT linked")
                print("   💡 Run: python seed_data.py")
        else:
            print("   ❌ Test user not found")
            print("   💡 Run: python seed_data.py")
        
        # Check routes
        print("\n4️⃣  Checking registered routes...")
        routes = {
            'auth.login': False,
            'dashboard.index': False,
            'patient_portal.dashboard': False
        }
        
        for rule in app.url_map.iter_rules():
            if rule.endpoint in routes:
                routes[rule.endpoint] = True
                print(f"   ✅ {rule.endpoint} → {rule.rule}")
        
        for endpoint, found in routes.items():
            if not found:
                print(f"   ❌ {endpoint} NOT FOUND")
        
        # Test password verification
        print("\n5️⃣  Testing password verification...")
        if admin:
            if admin.check_password("admin123"):
                print("   ✅ Admin password verification works")
            else:
                print("   ❌ Admin password verification failed")
        
        if test_user:
            if test_user.check_password("test123"):
                print("   ✅ Test user password verification works")
            else:
                print("   ❌ Test user password verification failed")
        
        # Summary
        print("\n" + "="*60)
        print("📊 SUMMARY")
        print("="*60)
        
        all_good = True
        
        if not admin or not admin.check_password("admin123"):
            print("❌ Admin account issue")
            all_good = False
        else:
            print("✅ Admin account ready")
        
        if not test_user or not test_user.patient or not test_user.check_password("test123"):
            print("❌ Test patient account issue")
            all_good = False
        else:
            print("✅ Test patient account ready")
        
        if not all(routes.values()):
            print("❌ Some routes missing")
            all_good = False
        else:
            print("✅ All routes registered")
        
        print("\n" + "="*60)
        
        if all_good:
            print("🎉 EVERYTHING LOOKS GOOD!")
            print("\n📝 Next steps:")
            print("   1. Make sure Flask server is running: python run.py")
            print("   2. Clear browser cache (Ctrl+Shift+R)")
            print("   3. Try logging in:")
            print("      • Admin: admin@hospital.com / admin123")
            print("      • Patient: test@patient.com / test123")
        else:
            print("⚠️  ISSUES FOUND - Run: python seed_data.py")
        
        print("="*60 + "\n")


if __name__ == "__main__":
    check_setup()
