"""
SMS notification service for patient appointment confirmations.
Uses Twilio, AWS SNS, or simulation mode.
"""
from datetime import datetime
from config import Config

# Initialize SMS provider if enabled
twilio_client = None
sns_client = None

if Config.SMS_ENABLED:
    if Config.SMS_PROVIDER == "twilio":
        try:
            from twilio.rest import Client
            twilio_client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
            print("✅ Twilio SMS client initialized")
        except ImportError:
            print("⚠️  Twilio not installed. Run: pip install twilio")
        except Exception as e:
            print(f"⚠️  Twilio initialization failed: {e}")
    
    elif Config.SMS_PROVIDER == "aws_sns":
        try:
            import boto3
            sns_client = boto3.client(
                'sns',
                aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
                region_name=Config.AWS_REGION
            )
            print("✅ AWS SNS client initialized")
        except ImportError:
            print("⚠️  Boto3 not installed. Run: pip install boto3")
        except Exception as e:
            print(f"⚠️  AWS SNS initialization failed: {e}")


class SMSService:
    """Handles SMS notifications to patients."""

    @staticmethod
    def _send_sms(phone: str, message: str) -> dict:
        """
        Internal method to send SMS via configured provider.
        Falls back to simulation if provider not configured.
        """
        # Real SMS via Twilio
        if Config.SMS_ENABLED and Config.SMS_PROVIDER == "twilio" and twilio_client:
            try:
                result = twilio_client.messages.create(
                    body=message,
                    from_=Config.TWILIO_PHONE_NUMBER,
                    to=phone
                )
                
                print(f"\n✅ REAL SMS SENT via Twilio to {phone}")
                print(f"   Message SID: {result.sid}")
                print(f"   Status: {result.status}\n")
                
                return {
                    "success": True,
                    "phone": phone,
                    "message": message,
                    "sent_at": datetime.utcnow().isoformat(),
                    "provider": "twilio",
                    "sid": result.sid,
                    "status": result.status
                }
            except Exception as e:
                print(f"\n❌ Twilio SMS failed to {phone}: {e}\n")
                return {
                    "success": False,
                    "phone": phone,
                    "error": str(e),
                    "provider": "twilio"
                }
        
        # Real SMS via AWS SNS
        elif Config.SMS_ENABLED and Config.SMS_PROVIDER == "aws_sns" and sns_client:
            try:
                response = sns_client.publish(
                    PhoneNumber=phone,
                    Message=message
                )
                
                print(f"\n✅ REAL SMS SENT via AWS SNS to {phone}")
                print(f"   Message ID: {response['MessageId']}\n")
                
                return {
                    "success": True,
                    "phone": phone,
                    "message": message,
                    "sent_at": datetime.utcnow().isoformat(),
                    "provider": "aws_sns",
                    "message_id": response['MessageId']
                }
            except Exception as e:
                print(f"\n❌ AWS SNS SMS failed to {phone}: {e}\n")
                return {
                    "success": False,
                    "phone": phone,
                    "error": str(e),
                    "provider": "aws_sns"
                }
        
        # Simulation mode (default)
        else:
            print("\n" + "=" * 60)
            print(f"📱 SMS SIMULATION - TO: {phone}")
            if not Config.SMS_ENABLED:
                print("   (SMS_ENABLED = False in config)")
            elif Config.SMS_PROVIDER == "simulation":
                print("   (SMS_PROVIDER = simulation)")
            else:
                print(f"   (Provider '{Config.SMS_PROVIDER}' not configured)")
            print("=" * 60)
            print(message)
            print("=" * 60 + "\n")
            
            return {
                "success": True,
                "phone": phone,
                "message": message,
                "sent_at": datetime.utcnow().isoformat(),
                "provider": "simulation"
            }

    @staticmethod
    def send_appointment_confirmation(patient, appointment, doctor, department):
        """
        Send appointment confirmation SMS to patient.
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

        return SMSService._send_sms(patient.phone, message)

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

    @staticmethod
    def send_reschedule_notification(patient, appointment, old_time, new_time, doctor, department):
        """Send SMS notification when appointment is rescheduled due to priority conflict."""
        message = f"""
🏥 SmartCare Hospital - Appointment Rescheduled

Dear {patient.name},

Your appointment has been rescheduled due to a higher priority patient.

📅 Date: {appointment.appointment_date.strftime('%A, %B %d, %Y')}
⏰ OLD Time: {old_time}
⏰ NEW Time: {new_time}
👨‍⚕️ Doctor: Dr. {doctor.name}
🏢 Department: {department.name}
🎫 Appointment #: {appointment.appointment_number}

We apologize for any inconvenience. Your new slot is confirmed.

📍 Location: SmartCare Hospital, Floor {department.floor}
📱 For queries, call: +91-1800-XXX-XXXX

Thank you for your understanding!
        """.strip()

        print("\n" + "=" * 60)
        print("📱 RESCHEDULE SMS SENT TO:", patient.phone)
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
    def send_delay_notification(patient, appointment, doctor, department, delay_minutes, reason="high patient volume"):
        """Send SMS when delay is predicted for appointment."""
        message = f"""
🏥 SmartCare Hospital - Appointment Delay Alert

Dear {patient.name},

We regret to inform you that your appointment may be delayed.

📅 Date: {appointment.appointment_date.strftime('%A, %B %d, %Y')}
⏰ Original Time: {appointment.appointment_time.strftime('%I:%M %p')}
⏱️ Expected Delay: ~{delay_minutes} minutes
👨‍⚕️ Doctor: Dr. {doctor.name}
🎫 Appointment #: {appointment.appointment_number}

Reason: {reason.capitalize()}

You may arrive {delay_minutes} minutes later than scheduled.
We apologize for the inconvenience.

📱 For queries, call: +91-1800-XXX-XXXX
        """.strip()

        print("\n" + "=" * 60)
        print("📱 DELAY ALERT SMS SENT TO:", patient.phone)
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
    def send_congestion_alert(patient, appointment, doctor, department, crowd_level, estimated_wait):
        """Send SMS when high congestion is detected."""
        message = f"""
🏥 SmartCare Hospital - High Congestion Alert

Dear {patient.name},

⚠️ HIGH PATIENT VOLUME DETECTED

📅 Your Appointment: {appointment.appointment_date.strftime('%A, %B %d, %Y')}
⏰ Time: {appointment.appointment_time.strftime('%I:%M %p')}
👨‍⚕️ Doctor: Dr. {doctor.name}
🏢 Department: {department.name}

Current Status:
🔴 Crowd Level: {crowd_level.upper()}
⏱️ Estimated Wait: ~{estimated_wait} minutes

Recommendations:
• Arrive on time or slightly later
• Bring entertainment/reading material
• Consider rescheduling if urgent

📱 To reschedule, call: +91-1800-XXX-XXXX

We appreciate your patience!
        """.strip()

        print("\n" + "=" * 60)
        print("📱 CONGESTION ALERT SMS SENT TO:", patient.phone)
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
    def send_doctor_unavailable_notification(patient, appointment, doctor, department, reason="emergency", alternative_doctor=None):
        """Send SMS when doctor becomes unavailable."""
        if alternative_doctor:
            alt_message = f"""
Alternative Arrangement:
👨‍⚕️ New Doctor: Dr. {alternative_doctor.name}
🏢 Same Department: {department.name}
⏰ Same Time: {appointment.appointment_time.strftime('%I:%M %p')}

Your appointment will proceed as scheduled with Dr. {alternative_doctor.name}.
            """.strip()
        else:
            alt_message = """
Please call us to reschedule:
📱 Phone: +91-1800-XXX-XXXX

We will help you book with another doctor at your convenience.
            """.strip()

        message = f"""
🏥 SmartCare Hospital - Doctor Unavailable

Dear {patient.name},

We regret to inform you that Dr. {doctor.name} is unavailable.

📅 Your Appointment: {appointment.appointment_date.strftime('%A, %B %d, %Y')}
⏰ Time: {appointment.appointment_time.strftime('%I:%M %p')}
🎫 Appointment #: {appointment.appointment_number}

Reason: {reason.capitalize()}

{alt_message}

We sincerely apologize for any inconvenience.

Thank you for your understanding.
        """.strip()

        print("\n" + "=" * 60)
        print("📱 DOCTOR UNAVAILABLE SMS SENT TO:", patient.phone)
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
    def send_followup_request(patient, appointment, doctor, department):
        """Send follow-up SMS after appointment completion."""
        message = f"""
🏥 SmartCare Hospital - Follow-Up

Dear {patient.name},

Thank you for visiting SmartCare Hospital!

Your Recent Visit:
📅 Date: {appointment.appointment_date.strftime('%A, %B %d, %Y')}
👨‍⚕️ Doctor: Dr. {doctor.name}
🏢 Department: {department.name}

We hope you're feeling better! 

📋 Follow-Up Actions:
• Take medications as prescribed
• Follow doctor's instructions
• Schedule follow-up if advised

💬 Feedback:
Rate your experience: [Link would go here]

⚠️ If you experience any issues:
📱 Emergency: +91-1800-XXX-XXXX
🏥 Visit: SmartCare Hospital

Get well soon! 🌟
        """.strip()

        print("\n" + "=" * 60)
        print("📱 FOLLOW-UP SMS SENT TO:", patient.phone)
        print("=" * 60)
        print(message)
        print("=" * 60 + "\n")

        return {
            "success": True,
            "phone": patient.phone,
            "message": message,
            "sent_at": datetime.utcnow().isoformat()
        }
