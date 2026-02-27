"""
Test script to verify patient details page functionality.
"""
from app import create_app, db
from app.models.models import Patient, QueueEntry, Appointment
from datetime import date

app = create_app()

with app.app_context():
    # Get a patient from the queue
    today = date.today()
    queue_entry = QueueEntry.query.filter_by(queue_date=today).first()
    
    if queue_entry:
        patient = queue_entry.patient
        print(f"\n✅ Found patient in queue:")
        print(f"   Patient ID: {patient.patient_id}")
        print(f"   Name: {patient.name}")
        print(f"   Age: {patient.age}")
        print(f"   Gender: {patient.gender}")
        print(f"   Phone: {patient.phone}")
        print(f"   Blood Group: {patient.blood_group}")
        
        # Check appointments
        appointments = Appointment.query.filter_by(patient_id=patient.id).all()
        print(f"\n   Appointments: {len(appointments)}")
        for appt in appointments:
            print(f"   - {appt.appointment_number}: {appt.appointment_date} at {appt.appointment_time}")
        
        print(f"\n✅ Patient details page URL:")
        print(f"   http://127.0.0.1:5000/admin/queue/patient/{patient.id}")
        print(f"\n   Click the patient name '{patient.name}' in the queue to view details!")
    else:
        print("\n⚠️  No patients in today's queue")
        print("   Run sync_appointments_to_queue.py first or add a patient to the queue")
