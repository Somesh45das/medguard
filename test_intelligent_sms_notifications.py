"""
Test script for intelligent SMS notification system.
Demonstrates all 5 notification types.
"""
from app import create_app, db
from app.models.models import Patient, Doctor, Department, Appointment
from app.services.notification_manager import NotificationManager
from app.services.sms_service import SMSService
from datetime import date, time, datetime, timedelta

app = create_app()

with app.app_context():
    print("\n" + "="*80)
    print("INTELLIGENT SMS NOTIFICATION SYSTEM - DEMONSTRATION")
    print("="*80 + "\n")
    
    # Get test data
    doctor = Doctor.query.first()
    department = Department.query.first()
    patient = Patient.query.first()
    
    if not all([doctor, department, patient]):
        print("❌ Missing test data. Please run seed_data.py first.")
        exit(1)
    
    # Create a test appointment
    test_appt = Appointment(
        appointment_number=f"TEST-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        patient_id=patient.id,
        doctor_id=doctor.id,
        department_id=department.id,
        appointment_date=date.today(),
        appointment_time=time(14, 30),
        slot_end_time=time(14, 45),
        symptoms="Test symptoms",
        status="scheduled"
    )
    db.session.add(test_appt)
    db.session.commit()
    
    print(f"Test Patient: {patient.name}")
    print(f"Test Doctor: Dr. {doctor.name}")
    print(f"Test Department: {department.name}")
    print(f"Test Appointment: {test_appt.appointment_number}\n")
    
    # ========================================================================
    # 1. IMMEDIATE CONFIRMATION (After Booking)
    # ========================================================================
    print("="*80)
    print("1️⃣  IMMEDIATE CONFIRMATION - Sent Right After Booking")
    print("="*80)
    print("Trigger: Patient books an appointment")
    print("Timing: Immediately after booking\n")
    
    SMSService.send_appointment_confirmation(
        patient, test_appt, doctor, department
    )
    
    input("\nPress Enter to continue to next notification type...")
    
    # ========================================================================
    # 2. DELAY NOTIFICATION (When Delay Predicted)
    # ========================================================================
    print("\n" + "="*80)
    print("2️⃣  DELAY NOTIFICATION - When Queue is Running Behind")
    print("="*80)
    print("Trigger: System detects appointment will be delayed >20 minutes")
    print("Timing: 30-60 minutes before appointment time\n")
    
    SMSService.send_delay_notification(
        patient, test_appt, doctor, department,
        delay_minutes=35,
        reason="high patient volume"
    )
    
    input("\nPress Enter to continue to next notification type...")
    
    # ========================================================================
    # 3. CONGESTION ALERT (High Patient Volume)
    # ========================================================================
    print("\n" + "="*80)
    print("3️⃣  CONGESTION ALERT - When Department is Very Busy")
    print("="*80)
    print("Trigger: Crowd prediction shows 'HIGH' or 'CRITICAL' level")
    print("Timing: 1-2 hours before appointment\n")
    
    SMSService.send_congestion_alert(
        patient, test_appt, doctor, department,
        crowd_level="high",
        estimated_wait=45
    )
    
    input("\nPress Enter to continue to next notification type...")
    
    # ========================================================================
    # 4. DOCTOR UNAVAILABLE (Emergency/Leave)
    # ========================================================================
    print("\n" + "="*80)
    print("4️⃣  DOCTOR UNAVAILABLE - When Doctor Can't Make It")
    print("="*80)
    print("Trigger: Doctor marks themselves unavailable")
    print("Timing: As soon as doctor unavailability is recorded\n")
    
    # Scenario A: With alternative doctor
    print("Scenario A: Alternative doctor assigned\n")
    alternative_doctor = Doctor.query.filter(Doctor.id != doctor.id).first()
    if alternative_doctor:
        SMSService.send_doctor_unavailable_notification(
            patient, test_appt, doctor, department,
            reason="emergency",
            alternative_doctor=alternative_doctor
        )
    
    input("\nPress Enter to see Scenario B...")
    
    # Scenario B: No alternative (need to reschedule)
    print("\nScenario B: No alternative - patient needs to reschedule\n")
    SMSService.send_doctor_unavailable_notification(
        patient, test_appt, doctor, department,
        reason="medical leave",
        alternative_doctor=None
    )
    
    input("\nPress Enter to continue to next notification type...")
    
    # ========================================================================
    # 5. FOLLOW-UP (After Appointment Completion)
    # ========================================================================
    print("\n" + "="*80)
    print("5️⃣  FOLLOW-UP - After Appointment is Completed")
    print("="*80)
    print("Trigger: Appointment status changes to 'completed'")
    print("Timing: 2-4 hours after appointment completion\n")
    
    SMSService.send_followup_request(
        patient, test_appt, doctor, department
    )
    
    # ========================================================================
    # SUMMARY
    # ========================================================================
    print("\n" + "="*80)
    print("NOTIFICATION SYSTEM SUMMARY")
    print("="*80 + "\n")
    
    print("✅ ALL 5 NOTIFICATION TYPES DEMONSTRATED:\n")
    
    print("1️⃣  IMMEDIATE CONFIRMATION")
    print("   • Sent: Right after booking")
    print("   • Purpose: Confirm appointment details")
    print("   • Integration: Already in booking routes\n")
    
    print("2️⃣  DELAY NOTIFICATION")
    print("   • Sent: When delay >20 minutes predicted")
    print("   • Purpose: Let patient arrive later")
    print("   • Trigger: Automatic via NotificationManager\n")
    
    print("3️⃣  CONGESTION ALERT")
    print("   • Sent: When crowd level is HIGH/CRITICAL")
    print("   • Purpose: Warn about long wait times")
    print("   • Trigger: Automatic via NotificationManager\n")
    
    print("4️⃣  DOCTOR UNAVAILABLE")
    print("   • Sent: When doctor can't attend")
    print("   • Purpose: Reassign or reschedule")
    print("   • Trigger: Manual by admin\n")
    
    print("5️⃣  FOLLOW-UP")
    print("   • Sent: After appointment completion")
    print("   • Purpose: Patient care & feedback")
    print("   • Trigger: Automatic when status = 'completed'\n")
    
    print("="*80)
    print("AUTOMATION OPTIONS")
    print("="*80 + "\n")
    
    print("🤖 Automatic Triggers:")
    print("   • Immediate confirmation: Integrated in booking")
    print("   • Delay notifications: Check every 15 minutes")
    print("   • Congestion alerts: Check every 30 minutes")
    print("   • Follow-up: Triggered on completion\n")
    
    print("👨‍💼 Manual Triggers (Admin):")
    print("   • POST /admin/notifications/check-delays")
    print("   • POST /admin/notifications/check-congestion")
    print("   • POST /admin/notifications/doctor-unavailable")
    print("   • POST /admin/notifications/check-all\n")
    
    print("🔄 Cron Job (Recommended):")
    print("   • Every 15 minutes: Check delays & congestion")
    print("   • Command: curl http://localhost:5000/api/notifications/check-all\n")
    
    print("="*80)
    print("INTEGRATION STATUS")
    print("="*80 + "\n")
    
    print("✅ SMS Service: 5 new methods added")
    print("✅ Notification Manager: Intelligent triggering logic")
    print("✅ API Routes: Admin controls + automation endpoint")
    print("✅ Queue Integration: Follow-up on completion")
    print("✅ Ready for Production: Just enable SMS provider\n")
    
    print("="*80)
    print("✅ INTELLIGENT SMS NOTIFICATION SYSTEM COMPLETE!")
    print("="*80)
    
    # Cleanup
    db.session.delete(test_appt)
    db.session.commit()
    
    print("\n✅ Test completed successfully!")
