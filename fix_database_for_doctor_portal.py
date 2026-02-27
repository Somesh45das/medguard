"""
Complete database fix script for doctor portal.
This script will:
1. Add doctor_id column to users table
2. Create a test doctor user account
3. Verify everything is working
"""
from app import create_app, db
from app.models.user import User
from app.models.models import Doctor
from sqlalchemy import text

app = create_app()

print("="*70)
print("DOCTOR PORTAL DATABASE FIX")
print("="*70)

with app.app_context():
    try:
        # STEP 1: Check and add doctor_id column
        print("\n[STEP 1] Checking users table schema...")
        result = db.session.execute(text("PRAGMA table_info(users)"))
        columns = [row[1] for row in result]
        
        if 'doctor_id' in columns:
            print("  ✓ Column 'doctor_id' already exists")
        else:
            print("  → Adding 'doctor_id' column...")
            db.session.execute(text(
                "ALTER TABLE users ADD COLUMN doctor_id INTEGER"
            ))
            db.session.commit()
            print("  ✓ Successfully added 'doctor_id' column")
        
        # STEP 2: Verify doctors exist
        print("\n[STEP 2] Checking for doctors in database...")
        doctors = Doctor.query.all()
        
        if not doctors:
            print("  ✗ No doctors found in database!")
            print("  → Please run 'python seed_data.py' first to create sample data")
            exit(1)
        else:
            print(f"  ✓ Found {len(doctors)} doctor(s) in database")
        
        # STEP 3: Create or verify doctor user account
        print("\n[STEP 3] Creating doctor user account...")
        doctor_user = User.query.filter_by(email="doctor@hospital.com").first()
        
        if doctor_user:
            print("  ✓ Doctor user already exists")
            # Update to ensure it has doctor role and link
            if doctor_user.role != "doctor":
                doctor_user.role = "doctor"
                print("  → Updated role to 'doctor'")
            if not doctor_user.doctor_id:
                first_doctor = doctors[0]
                doctor_user.doctor_id = first_doctor.id
                print(f"  → Linked to Dr. {first_doctor.name}")
            db.session.commit()
        else:
            # Create new doctor user
            first_doctor = doctors[0]
            doctor_user = User(
                name=first_doctor.name,
                email="doctor@hospital.com",
                phone="9876543210",
                role="doctor",
                is_active=True,
                is_verified=True,
                doctor_id=first_doctor.id
            )
            doctor_user.set_password("doctor123")
            db.session.add(doctor_user)
            db.session.commit()
            print("  ✓ Created new doctor user account")
        
        # STEP 4: Display summary
        print("\n" + "="*70)
        print("DATABASE FIX COMPLETED SUCCESSFULLY!")
        print("="*70)
        
        print("\n📋 DOCTORS IN SYSTEM:")
        print("-"*70)
        for doc in doctors:
            user = User.query.filter_by(doctor_id=doc.id).first()
            print(f"\n  Dr. {doc.name}")
            print(f"    Specialization: {doc.specialization}")
            print(f"    Department: {doc.department.name}")
            if user:
                print(f"    ✓ User Account: {user.email}")
            else:
                print(f"    ✗ No user account")
        
        print("\n" + "="*70)
        print("🔑 LOGIN CREDENTIALS:")
        print("="*70)
        print("\n  Admin Portal:")
        print("    Email:    admin@hospital.com")
        print("    Password: admin123")
        print("    URL:      http://localhost:5000/auth/login")
        
        print("\n  Patient Portal:")
        print("    Email:    test@patient.com")
        print("    Password: test123")
        print("    URL:      http://localhost:5000/auth/login")
        
        print("\n  Doctor Portal:")
        print("    Email:    doctor@hospital.com")
        print("    Password: doctor123")
        print("    URL:      http://localhost:5000/auth/login")
        
        print("\n" + "="*70)
        print("✅ NEXT STEPS:")
        print("="*70)
        print("\n  1. Start the application:")
        print("     python run.py")
        print("\n  2. Open browser and go to:")
        print("     http://localhost:5000/auth/login")
        print("\n  3. Login with doctor credentials above")
        print("\n  4. You'll be redirected to the doctor dashboard")
        print("\n" + "="*70)
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        db.session.rollback()
        print("\nTroubleshooting:")
        print("  1. Make sure the application is not running")
        print("  2. Delete instance/hospital.db and run seed_data.py")
        print("  3. Run this script again")
        raise
