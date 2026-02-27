"""
Intelligent Notification Manager
Handles automatic SMS notifications based on system events and predictions.
"""
from datetime import datetime, date, timedelta
from app import db
from app.models.models import Appointment, QueueEntry, Doctor, Department
from app.services.sms_service import SMSService
from app.services.crowd_predictor import CrowdPredictor
from app.services.wait_time_estimator import WaitTimeEstimator


class NotificationManager:
    """Manages intelligent SMS notifications based on system state."""

    def __init__(self):
        self.crowd_predictor = CrowdPredictor()
        self.wait_estimator = WaitTimeEstimator()

    def check_and_send_delay_notifications(self, department_id=None):
        """
        Check for delays and send notifications to affected patients.
        Called periodically or when queue updates.
        """
        today = date.today()
        
        # Get today's appointments
        query = Appointment.query.filter(
            Appointment.appointment_date == today,
            Appointment.status.in_(['scheduled', 'waiting', 'checked_in'])
        )
        
        if department_id:
            query = query.filter_by(department_id=department_id)
        
        appointments = query.all()
        notifications_sent = 0
        
        for appt in appointments:
            # Check if appointment is in queue
            queue_entry = QueueEntry.query.filter_by(
                appointment_id=appt.id,
                queue_date=today
            ).first()
            
            if queue_entry:
                # Calculate actual wait time
                wait_info = self.wait_estimator.estimate(
                    appt.department_id,
                    queue_entry.position,
                    appt.doctor_id
                )
                
                actual_wait = wait_info.get('estimated_wait_min', 0)
                expected_wait = 15  # Standard appointment buffer
                
                # If delay is more than 20 minutes, send notification
                if actual_wait > expected_wait + 20:
                    delay_minutes = actual_wait - expected_wait
                    
                    # Check if notification already sent (to avoid spam)
                    if not hasattr(appt, '_delay_notified'):
                        SMSService.send_delay_notification(
                            appt.patient,
                            appt,
                            appt.doctor,
                            appt.department,
                            delay_minutes,
                            reason="high patient volume"
                        )
                        appt._delay_notified = True
                        notifications_sent += 1
        
        return notifications_sent

    def check_and_send_congestion_alerts(self, department_id=None):
        """
        Check for high congestion and alert upcoming patients.
        Called when crowd level reaches 'high' or 'critical'.
        """
        today = date.today()
        current_hour = datetime.now().hour
        notifications_sent = 0
        
        # Get departments to check
        if department_id:
            departments = [Department.query.get(department_id)]
        else:
            departments = Department.query.filter_by(is_active=True).all()
        
        for dept in departments:
            if not dept:
                continue
                
            # Predict crowd level for current hour
            crowd = self.crowd_predictor.predict_crowd_level(
                dept.id,
                today,
                current_hour
            )
            
            # If high or critical congestion
            if crowd['level_code'] >= 2:  # 2=high, 3=critical
                # Get upcoming appointments in next 2 hours
                upcoming_appointments = Appointment.query.filter(
                    Appointment.department_id == dept.id,
                    Appointment.appointment_date == today,
                    Appointment.appointment_time >= datetime.now().time(),
                    Appointment.appointment_time <= (datetime.now() + timedelta(hours=2)).time(),
                    Appointment.status.in_(['scheduled', 'confirmed'])
                ).all()
                
                for appt in upcoming_appointments:
                    # Check if not already notified
                    if not hasattr(appt, '_congestion_notified'):
                        estimated_wait = crowd.get('estimated_wait', 30)
                        
                        SMSService.send_congestion_alert(
                            appt.patient,
                            appt,
                            appt.doctor,
                            appt.department,
                            crowd['level'],
                            estimated_wait
                        )
                        appt._congestion_notified = True
                        notifications_sent += 1
        
        return notifications_sent

    def notify_doctor_unavailable(self, doctor_id, reason="emergency", date_affected=None, alternative_doctor_id=None):
        """
        Notify all patients when a doctor becomes unavailable.
        Called when doctor marks themselves unavailable.
        """
        if date_affected is None:
            date_affected = date.today()
        
        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            return 0
        
        alternative_doctor = None
        if alternative_doctor_id:
            alternative_doctor = Doctor.query.get(alternative_doctor_id)
        
        # Get all appointments for this doctor on affected date
        appointments = Appointment.query.filter(
            Appointment.doctor_id == doctor_id,
            Appointment.appointment_date == date_affected,
            Appointment.status.in_(['scheduled', 'confirmed', 'waiting'])
        ).all()
        
        notifications_sent = 0
        for appt in appointments:
            # If alternative doctor provided, reassign
            if alternative_doctor:
                appt.doctor_id = alternative_doctor.id
                db.session.commit()
            
            SMSService.send_doctor_unavailable_notification(
                appt.patient,
                appt,
                doctor,
                appt.department,
                reason,
                alternative_doctor
            )
            notifications_sent += 1
        
        return notifications_sent

    def send_followup_after_completion(self, appointment_id):
        """
        Send follow-up SMS after appointment is completed.
        Called when appointment status changes to 'completed'.
        """
        appt = Appointment.query.get(appointment_id)
        if not appt or appt.status != 'completed':
            return False
        
        SMSService.send_followup_request(
            appt.patient,
            appt,
            appt.doctor,
            appt.department
        )
        
        return True

    def send_immediate_confirmation(self, appointment_id):
        """
        Send immediate confirmation after booking.
        This is already integrated in booking routes.
        """
        appt = Appointment.query.get(appointment_id)
        if not appt:
            return False
        
        SMSService.send_appointment_confirmation(
            appt.patient,
            appt,
            appt.doctor,
            appt.department
        )
        
        return True

    def check_all_notifications(self):
        """
        Master function to check all notification conditions.
        Can be called periodically (e.g., every 15 minutes via cron job).
        """
        results = {
            'delay_notifications': 0,
            'congestion_alerts': 0,
            'timestamp': datetime.now().isoformat()
        }
        
        # Check for delays
        results['delay_notifications'] = self.check_and_send_delay_notifications()
        
        # Check for congestion
        results['congestion_alerts'] = self.check_and_send_congestion_alerts()
        
        return results
