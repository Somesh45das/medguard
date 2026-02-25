"""
Debug script to check appointments in database.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db
from app.models.models import Appointment, Patient, Doctor, Department
from app.models.user import User
from datetime import date, datetime

def debug_appointments():
    """Debug appointment visibility issue."""
    app = create_app()
    with app.app_context():
        print("\n" + "="*70)
        print("DEBUGGING APPOINTMENT VISIBILITY")
        print("="*70)
        
        # Check test user
        test_user = User.query.filter_by(email="test@patient.com").first()
        if test_user:
            print(f"\n✅ Test User:")
            print(f"   ID: {test_user.id}")
            print(f"   Name: {test_user.name}")
            print(f"   Email: {test_user.email}")
            print(f"   Patient ID (FK): {test_user.patient_id}")
            
            if test_user.patient:
                patient = test_user.patient
                print(f"\n✅ Linked Patient Record:")
                print(f"   Patient DB ID: {patient.id}")
                print(f"   Patient ID String: {patient.patient_id}")
                print(f"   Name: {patient.name}")
                print(f"   Phone: {patient.phone}")
                
                # Check appointments for this patient
                appointments = Appointment.query.filter_by(patient_id=patient.id).all()
                print(f"\n📅 Appointments for Patient ID {patient.id}:")
                print(f"   Total: {len(appointments)}")
                
                if appointments:
                    for apt in appointments:
                        print(f"\n   Appointment #{apt.appointment_number}:")
                        print(f"      DB ID: {apt.id}")
                        print(f"      Patient ID (FK): {apt.patient_id}")
                        print(f"      Doctor ID: {apt.doctor_id}")
                        print(f"      Department ID: {apt.department_id}")
                        print(f"      Date: {apt.appointment_date}")
                        print(f"      Time: {apt.appointment_time}")
                        print(f"      Status: {apt.status}")
                        print(f"      Doctor: {apt.doctor.name if apt.doctor else 'N/A'}")
                        print(f"      Department: {apt.department.name if apt.department else 'N/A'}")
                else:
                    print("   ⚠️ No appointments found for this patient")
            else:
                print("\n❌ No patient record linked to user!")
        else:
            print("\n❌ Test user not found")
        
        # Check ALL appointments in database
        print("\n" + "="*70)
        print("ALL APPOINTMENTS IN DATABASE")
        print("="*70)
        
        all_appointments = Appointment.query.all()
        print(f"\nTotal appointments: {len(all_appointments)}")
        
        if all_appointments:
            print("\nGrouped by date:")
            dates = {}
            for apt in all_appointments:
                date_str = apt.appointment_date.isoformat()
                if date_str not in dates:
                    dates[date_str] = []
                dates[date_str].append(apt)
            
            for date_str, apts in sorted(dates.items()):
                print(f"\n  {date_str}: {len(apts)} appointments")
                for apt in apts[:3]:  # Show first 3
                    print(f"    - {apt.appointment_number}: {apt.patient.name} → Dr. {apt.doctor.name} ({apt.status})")
                if len(apts) > 3:
                    print(f"    ... and {len(apts) - 3} more")
        
        # Check today's appointments specifically
        today = date.today()
        today_apts = Appointment.query.filter_by(appointment_date=today).all()
        print(f"\n📊 Today's appointments ({today}): {len(today_apts)}")
        
        if today_apts:
            for apt in today_apts:
                print(f"   - {apt.appointment_number}: Patient ID {apt.patient_id} ({apt.patient.name})")
        
        # Check what admin panel query would return
        print("\n" + "="*70)
        print("SIMULATING ADMIN PANEL QUERY")
        print("="*70)
        
        # This is what appointments.py does
        filter_date = today
        query = Appointment.query.filter(Appointment.appointment_date == filter_date)
        admin_results = query.order_by(Appointment.appointment_time.asc()).all()
        
        print(f"\nQuery: Appointment.query.filter(appointment_date == {filter_date})")
        print(f"Results: {len(admin_results)} appointments")
        
        if admin_results:
            print("\nAppointments that admin would see:")
            for apt in admin_results:
                print(f"   {apt.appointment_number}:")
                print(f"      Patient: {apt.patient.name}")
                print(f"      Doctor: Dr. {apt.doctor.name}")
                print(f"      Time: {apt.appointment_time}")
                print(f"      Status: {apt.status}")
        else:
            print("\n⚠️ Admin panel would show NO appointments for today!")
            print(f"   Reason: No appointments with date = {filter_date}")
        
        # Check departments and doctors
        print("\n" + "="*70)
        print("DEPARTMENTS AND DOCTORS")
        print("="*70)
        
        depts = Department.query.filter_by(is_active=True).all()
        print(f"\nActive Departments: {len(depts)}")
        for dept in depts:
            print(f"   - {dept.name} (ID: {dept.id})")
        
        doctors = Doctor.query.filter_by(is_available=True).all()
        print(f"\nAvailable Doctors: {len(doctors)}")
        for doc in doctors[:5]:
            print(f"   - Dr. {doc.name} - {doc.specialization} (ID: {doc.id})")
        
        print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    debug_appointments()
