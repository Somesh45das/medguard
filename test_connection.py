"""
Quick test to verify patient-appointment connection.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db
from app.models.models import Appointment, Patient
from app.models.user import User
from datetime import date

def test_connection():
    """Test if patient appointments are properly linked."""
    app = create_app()
    with app.app_context():
        print("\n" + "="*60)
        print("TESTING PATIENT-APPOINTMENT CONNECTION")
        print("="*60)
        
        # Check if test user exists
        test_user = User.query.filter_by(email="test@patient.com").first()
        if test_user:
            print(f"\n✅ Test User Found:")
            print(f"   Name: {test_user.name}")
            print(f"   Email: {test_user.email}")
            print(f"   Role: {test_user.role}")
            print(f"   Has Patient Record: {'Yes' if test_user.patient else 'No'}")
            
            if test_user.patient:
                patient = test_user.patient
                print(f"\n✅ Patient Record:")
                print(f"   Patient ID: {patient.patient_id}")
                print(f"   Name: {patient.name}")
                print(f"   Phone: {patient.phone}")
                
                # Check appointments
                appointments = Appointment.query.filter_by(patient_id=patient.id).all()
                print(f"\n📅 Appointments for this patient: {len(appointments)}")
                for apt in appointments:
                    print(f"   - {apt.appointment_number}: {apt.appointment_date} at {apt.appointment_time} ({apt.status})")
        else:
            print("\n❌ Test user not found. Run seed_data.py first.")
        
        # Check all appointments
        today = date.today()
        all_appointments = Appointment.query.filter_by(appointment_date=today).all()
        print(f"\n📊 Total appointments today: {len(all_appointments)}")
        
        # Check if appointments have valid patient links
        valid_links = 0
        for apt in all_appointments:
            if apt.patient and apt.patient.name:
                valid_links += 1
        
        print(f"   Valid patient links: {valid_links}/{len(all_appointments)}")
        
        if valid_links == len(all_appointments):
            print("\n✅ ALL APPOINTMENTS PROPERLY LINKED!")
        else:
            print(f"\n⚠️ {len(all_appointments) - valid_links} appointments have broken links")
        
        print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    test_connection()
