"""
Debug script to check appointments and doctor assignments.
"""
from app import create_app, db
from app.models.models import Appointment, Doctor
from datetime import date

app = create_app()

with app.app_context():
    today = date.today()
    
    print("="*70)
    print("APPOINTMENT DEBUG - TODAY'S APPOINTMENTS")
    print("="*70)
    
    # Get all appointments for today
    today_appointments = Appointment.query.filter(
        Appointment.appointment_date == today
    ).all()
    
    print(f"\nTotal appointments for today ({today}): {len(today_appointments)}")
    
    if today_appointments:
        print("\nAppointment Details:")
        print("-"*70)
        for apt in today_appointments:
            print(f"\nAppointment #{apt.appointment_number}")
            print(f"  Patient: {apt.patient.name}")
            print(f"  Doctor ID: {apt.doctor_id}")
            print(f"  Doctor: {apt.doctor.name if apt.doctor else 'NOT ASSIGNED'}")
            print(f"  Time: {apt.appointment_time.strftime('%I:%M %p')}")
            print(f"  Status: {apt.status}")
            print(f"  Date: {apt.appointment_date}")
    
    # Check all doctors
    print("\n" + "="*70)
    print("DOCTOR STATISTICS")
    print("="*70)
    
    doctors = Doctor.query.all()
    for doc in doctors:
        # Count today's appointments
        count = Appointment.query.filter(
            Appointment.doctor_id == doc.id,
            Appointment.appointment_date == today,
            Appointment.status.in_(["scheduled", "checked_in", "in_progress"])
        ).count()
        
        # Get all appointments for this doctor today
        doc_appointments = Appointment.query.filter(
            Appointment.doctor_id == doc.id,
            Appointment.appointment_date == today
        ).all()
        
        print(f"\nDr. {doc.name} (ID: {doc.id})")
        print(f"  Department: {doc.department.name}")
        print(f"  Today's count (active): {count}")
        print(f"  Today's count (all): {len(doc_appointments)}")
        
        if doc_appointments:
            print(f"  Appointments:")
            for apt in doc_appointments:
                print(f"    - {apt.appointment_time.strftime('%I:%M %p')} | {apt.patient.name} | {apt.status}")
    
    # Check if appointments have correct date
    print("\n" + "="*70)
    print("DATE CHECK")
    print("="*70)
    print(f"Today's date: {today}")
    print(f"Today's date type: {type(today)}")
    
    all_appointments = Appointment.query.all()
    print(f"\nTotal appointments in database: {len(all_appointments)}")
    
    date_distribution = {}
    for apt in all_appointments:
        date_str = apt.appointment_date.strftime('%Y-%m-%d')
        if date_str not in date_distribution:
            date_distribution[date_str] = 0
        date_distribution[date_str] += 1
    
    print("\nAppointments by date:")
    for date_str, count in sorted(date_distribution.items()):
        marker = " <-- TODAY" if date_str == today.strftime('%Y-%m-%d') else ""
        print(f"  {date_str}: {count} appointments{marker}")
