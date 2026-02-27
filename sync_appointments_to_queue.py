"""
Sync today's appointments to the live queue system.
This creates QueueEntry records for all scheduled appointments for today.
"""
import sys
from datetime import date
sys.path.insert(0, '.')

from app import create_app, db
from app.models.models import Appointment, QueueEntry, Patient
from app.services.queue_manager import QueueManager

app = create_app()

def sync_appointments_to_queue():
    """Sync today's appointments to queue."""
    with app.app_context():
        print("=" * 70)
        print("   SYNCING APPOINTMENTS TO QUEUE")
        print("=" * 70)
        
        today = date.today()
        queue_mgr = QueueManager()
        
        # Get today's appointments that should be in queue
        appointments = Appointment.query.filter(
            Appointment.appointment_date == today,
            Appointment.status.in_(['scheduled', 'confirmed', 'waiting', 'checked_in'])
        ).order_by(Appointment.appointment_time).all()
        
        if not appointments:
            print(f"\n⚠️  No appointments found for today ({today})")
            print("\nTip: The test data creates appointments for various dates.")
            print("     Some are in the past, some today, some in the future.")
            return
        
        print(f"\n✅ Found {len(appointments)} appointments for today")
        print(f"📅 Date: {today.strftime('%A, %B %d, %Y')}\n")
        
        synced = 0
        skipped = 0
        
        for appt in appointments:
            # Check if already in queue
            existing = QueueEntry.query.filter_by(
                appointment_id=appt.id,
                queue_date=today
            ).first()
            
            if existing:
                print(f"⏭️  {appt.patient.name:25} | Already in queue (Token: {existing.token_number})")
                skipped += 1
                continue
            
            # Add to queue
            try:
                entry = queue_mgr.add_to_queue(
                    patient_id=appt.patient_id,
                    department_id=appt.department_id,
                    doctor_id=appt.doctor_id,
                    appointment_id=appt.id,
                    symptoms=appt.symptoms
                )
                
                # Update appointment status
                if appt.status == 'scheduled' or appt.status == 'confirmed':
                    appt.status = 'waiting'
                
                print(f"✅ {appt.patient.name:25} | Token: {entry.token_number:8} | "
                      f"Position: {entry.position:2} | Priority: {entry.priority_score:.1f} | "
                      f"Time: {appt.appointment_time.strftime('%I:%M %p')}")
                synced += 1
                
            except Exception as e:
                print(f"❌ {appt.patient.name:25} | Error: {str(e)}")
        
        db.session.commit()
        
        print("\n" + "=" * 70)
        print("   SUMMARY")
        print("=" * 70)
        print(f"✅ Synced: {synced} appointments")
        print(f"⏭️  Skipped: {skipped} (already in queue)")
        print(f"📊 Total in queue: {QueueEntry.query.filter_by(queue_date=today).count()}")
        
        # Show queue stats by department
        print("\n" + "=" * 70)
        print("   QUEUE BY DEPARTMENT")
        print("=" * 70)
        
        from app.models.models import Department
        departments = Department.query.filter_by(is_active=True).all()
        
        for dept in departments:
            count = QueueEntry.query.filter_by(
                department_id=dept.id,
                queue_date=today,
                status='waiting'
            ).count()
            if count > 0:
                print(f"{dept.name:30} | {count} patients waiting")
        
        print("\n" + "=" * 70)
        print("   QUEUE READY!")
        print("=" * 70)
        print("\nView queue at: http://127.0.0.1:5000/admin/queue/")
        print("Login: admin@hospital.com / admin123")

if __name__ == "__main__":
    sync_appointments_to_queue()
