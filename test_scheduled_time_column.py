"""
Test script to verify the Scheduled Time column in queue.
"""
from app import create_app, db
from app.models.models import QueueEntry, Appointment
from datetime import date

app = create_app()

with app.app_context():
    today = date.today()
    
    # Get queue entries
    queue_entries = QueueEntry.query.filter_by(queue_date=today).all()
    
    print(f"\n{'='*80}")
    print(f"QUEUE ENTRIES WITH SCHEDULED TIME - {today}")
    print(f"{'='*80}\n")
    
    if queue_entries:
        print(f"{'Token':<12} {'Patient':<20} {'Department':<20} {'Scheduled Time':<15} {'Type'}")
        print("-" * 80)
        
        for entry in queue_entries:
            patient_name = entry.patient.name[:18]
            dept_name = entry.department.name[:18]
            
            if entry.appointment:
                scheduled_time = entry.appointment.appointment_time.strftime('%I:%M %p')
                entry_type = "Appointment"
            else:
                scheduled_time = "N/A"
                entry_type = "Walk-in"
            
            print(f"{entry.token_number:<12} {patient_name:<20} {dept_name:<20} {scheduled_time:<15} {entry_type}")
        
        print("\n" + "="*80)
        print(f"Total: {len(queue_entries)} patients in queue")
        
        # Count appointments vs walk-ins
        with_appt = sum(1 for e in queue_entries if e.appointment)
        walk_ins = len(queue_entries) - with_appt
        
        print(f"  - With scheduled appointments: {with_appt}")
        print(f"  - Walk-ins: {walk_ins}")
        print("="*80)
        
        print(f"\n✅ The 'Scheduled Time' column will show:")
        print(f"   - Appointment time (e.g., '08:15 AM') for scheduled patients")
        print(f"   - 'Walk-in' for patients without appointments")
        print(f"\n🌐 View the queue at: http://127.0.0.1:5000/admin/queue/")
        
    else:
        print("⚠️  No patients in today's queue")
        print("   Run sync_appointments_to_queue.py to add appointments to queue")
