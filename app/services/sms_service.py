"""
SMS notification service for patient appointment confirmations.
Uses Twilio for SMS delivery (can be configured with other providers).
"""
from datetime import datetime


class SMSService:
    """Handles SMS notifications to patients."""

    @staticmethod
    def send_appointment_confirmation(patient, appointment, doctor, department):
        """
        Send appointment confirmation SMS to patient.
        
        In production, integrate with Twilio, AWS SNS, or other SMS gateway.
        For now, we'll simulate and log the SMS.
        """
        message = f"""
🏥 SmartCare Hospital - Appointment Confirmed

Dear {patient.name},

Your appointment has been booked successfully!

📅 Date: {appointment.appointment_date.strftime('%A, %B %d, %Y')}
⏰ Time: {appointment.appointment_time.strftime('%I:%M %p')}
👨‍⚕️ Doctor: Dr. {doctor.name}
🏢 Department: {department.name}
🎫 Appointment #: {appointment.appointment_number}

📍 Location: SmartCare Hospital, Floor {department.floor}

⚠️ Please arrive 15 minutes early.
📱 For queries, call: +91-1800-XXX-XXXX

Thank you for choosing SmartCare Hospital!
        """.strip()

        # In production, use actual SMS gateway:
        # from twilio.rest import Client
        # client = Client(account_sid, auth_token)
        # client.messages.create(
        #     body=message,
        #     from_='+1234567890',
        #     to=patient.phone
        # )

        # For now, log the SMS
        print("\n" + "=" * 60)
        print("📱 SMS SENT TO:", patient.phone)
        print("=" * 60)
        print(message)
        print("=" * 60 + "\n")

        return {
            "success": True,
            "phone": patient.phone,
            "message": message,
            "sent_at": datetime.utcnow().isoformat()
        }

    @staticmethod
    def send_appointment_reminder(patient, appointment, doctor):
        """Send appointment reminder SMS (can be scheduled)."""
        message = f"""
🏥 SmartCare Hospital - Appointment Reminder

Dear {patient.name},

Reminder: You have an appointment tomorrow!

📅 Date: {appointment.appointment_date.strftime('%A, %B %d, %Y')}
⏰ Time: {appointment.appointment_time.strftime('%I:%M %p')}
👨‍⚕️ Doctor: Dr. {doctor.name}
🎫 Appointment #: {appointment.appointment_number}

Please arrive 15 minutes early.
        """.strip()

        print("\n" + "=" * 60)
        print("📱 REMINDER SMS SENT TO:", patient.phone)
        print("=" * 60)
        print(message)
        print("=" * 60 + "\n")

        return {"success": True, "phone": patient.phone}

    @staticmethod
    def send_queue_notification(patient, token_number, position, estimated_wait):
        """Send queue token SMS to walk-in patients."""
        message = f"""
🏥 SmartCare Hospital - Queue Token

Dear {patient.name},

Your queue token: {token_number}
Position: #{position}
Estimated wait: ~{estimated_wait} minutes

Please stay near the waiting area.
You'll be called when it's your turn.
        """.strip()

        print("\n" + "=" * 60)
        print("📱 QUEUE SMS SENT TO:", patient.phone)
        print("=" * 60)
        print(message)
        print("=" * 60 + "\n")

        return {"success": True, "phone": patient.phone}
