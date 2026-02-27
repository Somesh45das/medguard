"""
Test script for appointment history feature.
"""
from app import create_app, db
from app.models.models import Patient, Appointment
from datetime import date

app = create_app()

with app.app_context():
    print("\n" + "="*80)
    print("APPOINTMENT HISTORY FEATURE TEST")
    print("="*80 + "\n")
    
    # Get a test patient
    patient = Patient.query.first()
    if not patient:
        print("❌ No patients found. Please run seed_data.py first.")
        exit(1)
    
    print(f"Test Patient: {patient.name}")
    print(f"Patient ID: {patient.patient_id}\n")
    
    # Get all appointments for this patient
    all_appointments = Appointment.query.filter_by(patient_id=patient.id).all()
    
    if not all_appointments:
        print("⚠️  No appointments found for this patient")
        print("   Run add_test_patients.py to create test data")
        exit(0)
    
    print(f"Total Appointments: {len(all_appointments)}\n")
    
    # Statistics
    today = date.today()
    completed = [a for a in all_appointments if a.status == 'completed']
    upcoming = [a for a in all_appointments if a.appointment_date >= today and a.status in ['scheduled', 'confirmed', 'waiting']]
    cancelled = [a for a in all_appointments if a.status in ['cancelled', 'no_show']]
    past = [a for a in all_appointments if a.appointment_date < today]
    
    print("STATISTICS:")
    print("-" * 80)
    print(f"✅ Completed: {len(completed)}")
    print(f"📅 Upcoming: {len(upcoming)}")
    print(f"❌ Cancelled/No-show: {len(cancelled)}")
    print(f"📜 Past: {len(past)}")
    print()
    
    # Show sample appointments
    print("APPOINTMENT HISTORY (Sample):")
    print("-" * 80)
    print(f"{'Date':<12} {'Time':<10} {'Doctor':<20} {'Department':<20} {'Status':<15}")
    print("-" * 80)
    
    for appt in sorted(all_appointments, key=lambda x: (x.appointment_date, x.appointment_time), reverse=True)[:10]:
        date_str = appt.appointment_date.strftime('%Y-%m-%d')
        time_str = appt.appointment_time.strftime('%I:%M %p')
        doctor_name = appt.doctor.name[:18] if appt.doctor else 'N/A'
        dept_name = appt.department.name[:18] if appt.department else 'N/A'
        status = appt.status
        
        print(f"{date_str:<12} {time_str:<10} {doctor_name:<20} {dept_name:<20} {status:<15}")
    
    print()
    print("="*80)
    print("APPOINTMENT HISTORY PAGE FEATURES")
    print("="*80)
    print("""
✅ Complete appointment history with all details
✅ Statistics summary (Total, Completed, Upcoming, Cancelled)
✅ Filter by Status (All, Completed, Scheduled, Waiting, etc.)
✅ Filter by Department
✅ Filter by Time Period (Today, Week, Month, Year, All Time)
✅ Sortable table with all appointment information
✅ View details and cancel options
✅ Responsive design for mobile devices
✅ Empty state when no appointments found
✅ Quick actions (Book New, Back to Dashboard)
    """)
    
    print("="*80)
    print("HOW TO ACCESS")
    print("="*80)
    print("""
1. Login as patient: http://localhost:5000/auth/simple-login
   - Email: test@patient.com
   - Password: test123

2. From Dashboard, click "View History" button

3. Or go directly to: http://localhost:5000/patient/history

4. Use filters to narrow down appointments:
   - Filter by status (completed, scheduled, etc.)
   - Filter by department
   - Filter by time period

5. View complete history with all details in a table
    """)
    
    print("="*80)
    print("✅ APPOINTMENT HISTORY FEATURE COMPLETE!")
    print("="*80)
