"""
Script to create a test doctor user account.
Run this to create a doctor login for testing.
"""
from app import create_app, db
from app.models.user import User
from app.models.models import Doctor

app = create_app()

with app.app_context():
    # Check if doctor user already exists
    doctor_user = User.query.filter_by(email="doctor@hospital.com").first()
    
    if doctor_user:
        print("✓ Doctor user already exists: doctor@hospital.com")
    else:
        # Get first doctor from database
        doctor = Doctor.query.first()
        
        if not doctor:
            print("✗ No doctors found in database. Please run seed_data.py first.")
            exit(1)
        
        # Create doctor user account
        doctor_user = User(
            name=doctor.name,
            email="doctor@hospital.com",
            phone="9876543210",
            role="doctor",
            is_active=True,
            is_verified=True,
            doctor_id=doctor.id
        )
        doctor_user.set_password("doctor123")
        
        db.session.add(doctor_user)
        db.session.commit()
        
        print("✓ Doctor user created successfully!")
        print(f"  Email: doctor@hospital.com")
        print(f"  Password: doctor123")
        print(f"  Linked to: Dr. {doctor.name} ({doctor.specialization})")
    
    # List all doctors and their user accounts
    print("\n" + "="*60)
    print("ALL DOCTORS IN SYSTEM:")
    print("="*60)
    
    doctors = Doctor.query.all()
    for doc in doctors:
        user = User.query.filter_by(doctor_id=doc.id).first()
        print(f"\nDr. {doc.name} ({doc.specialization})")
        print(f"  Department: {doc.department.name}")
        if user:
            print(f"  ✓ Has user account: {user.email}")
        else:
            print(f"  ✗ No user account linked")
    
    print("\n" + "="*60)
    print("LOGIN CREDENTIALS:")
    print("="*60)
    print("Admin:   admin@hospital.com / admin123")
    print("Patient: test@patient.com / test123")
    print("Doctor:  doctor@hospital.com / doctor123")
    print("="*60)
