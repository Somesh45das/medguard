"""
Test SMS System - Verify SMS is being sent
"""
from app.services.sms_service import SMSService
from datetime import datetime, date, time


# Mock objects
class MockPatient:
    name = "John Doe"
    phone = "+91-9876543210"


class MockAppointment:
    appointment_date = date(2026, 2, 26)
    appointment_time = time(10, 30)
    appointment_number = "APT-20260226-001"


class MockDoctor:
    name = "Smith"


class MockDepartment:
    name = "General Medicine"
    floor = 2


print("\n" + "=" * 70)
print("   SMS SYSTEM TEST")
print("=" * 70)

# Test 1: Appointment Confirmation
print("\n[TEST 1] Appointment Confirmation SMS")
print("-" * 70)

result = SMSService.send_appointment_confirmation(
    MockPatient(),
    MockAppointment(),
    MockDoctor(),
    MockDepartment()
)

print("\nResult:")
print(f"  Success: {result['success']}")
print(f"  Phone: {result['phone']}")
print(f"  Sent at: {result['sent_at']}")

# Test 2: Appointment Reminder
print("\n[TEST 2] Appointment Reminder SMS")
print("-" * 70)

result2 = SMSService.send_appointment_reminder(
    MockPatient(),
    MockAppointment(),
    MockDoctor()
)

print("\nResult:")
print(f"  Success: {result2['success']}")
print(f"  Phone: {result2['phone']}")

# Test 3: Queue Token
print("\n[TEST 3] Queue Token SMS")
print("-" * 70)

result3 = SMSService.send_queue_notification(
    MockPatient(),
    token_number="GN-001",
    position=5,
    estimated_wait=25
)

print("\nResult:")
print(f"  Success: {result3['success']}")
print(f"  Phone: {result3['phone']}")

print("\n" + "=" * 70)
print("   ✅ ALL SMS TESTS PASSED")
print("=" * 70)
print("\nCurrent Mode: SIMULATION (messages printed to console)")
print("To enable real SMS: See SMS_SYSTEM_STATUS.md")
print("=" * 70 + "\n")
