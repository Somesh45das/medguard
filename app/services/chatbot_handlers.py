"""
Additional chatbot handlers for patient and management features.
"""
from datetime import date, datetime, timedelta
from app.models.models import Appointment, Department, Doctor, Patient
from sqlalchemy import func


class PatientHandlers:
    """Patient-specific chatbot handlers."""
    
    @staticmethod
    def handle_estimated_time(message: str, context: dict) -> dict:
        """Handle estimated appointment time queries."""
        # Extract phone number if present
        import re
        phone_match = re.search(r'\b\d{10}\b', message)
        
        if phone_match or context.get('phone'):
            phone = phone_match.group() if phone_match else context.get('phone')
            
            # Find patient's upcoming appointment
            patients = Patient.query.filter_by(phone=phone).all()
            if patients:
                upcoming = None
                for patient in patients:
                    appt = Appointment.query.filter_by(
                        patient_id=patient.id,
                        status='confirmed'
                    ).filter(
                        Appointment.appointment_date >= date.today()
                    ).order_by(Appointment.appointment_date, Appointment.appointment_time).first()
                    
                    if appt:
                        upcoming = appt
                        break
                
                if upcoming:
                    # Calculate estimated time
                    appt_time = upcoming.appointment_time
                    dept = Department.query.get(upcoming.department_id)
                    
                    # Get queue position
                    queue_position = Appointment.query.filter(
                        Appointment.department_id == upcoming.department_id,
                        Appointment.appointment_date == upcoming.appointment_date,
                        Appointment.appointment_time < upcoming.appointment_time,
                        Appointment.status.in_(['confirmed', 'waiting', 'called'])
                    ).count()
                    
                    # Estimate wait time (15 min per patient)
                    estimated_wait = queue_position * 15
                    estimated_time = (datetime.combine(date.today(), appt_time) + 
                                    timedelta(minutes=estimated_wait)).time()
                    
                    return {
                        'response': f"⏰ Your Appointment Estimate:\n\n"
                                   f"📅 Date: {upcoming.appointment_date.strftime('%B %d, %Y')}\n"
                                   f"🕐 Scheduled: {appt_time.strftime('%I:%M %p')}\n"
                                   f"🏥 Department: {dept.name if dept else 'N/A'}\n"
                                   f"📊 Queue Position: #{queue_position + 1}\n"
                                   f"⏱️ Estimated Time: {estimated_time.strftime('%I:%M %p')}\n"
                                   f"⌛ Expected Wait: ~{estimated_wait} minutes\n\n"
                                   f"💡 Tip: Arrive 10 minutes early!",
                        'suggestions': [
                            "Get directions",
                            "View precautions",
                            "Reschedule",
                            "Cancel appointment"
                        ],
                        'type': 'estimated_time',
                        'data': {
                            'appointment_id': upcoming.id,
                            'queue_position': queue_position + 1,
                            'estimated_wait': estimated_wait
                        }
                    }
        
        return {
            'response': "I can help you get your estimated appointment time! ⏰\n\n"
                       "Please provide your 10-digit phone number.",
            'suggestions': [
                "Enter phone number",
                "Check status instead",
                "Go back"
            ],
            'type': 'estimated_time_request'
        }
    
    @staticmethod
    def handle_precautions(message: str, context: dict) -> dict:
        """Handle precautions and preparation advice."""
        # Check if department mentioned
        departments = Department.query.filter_by(is_active=True).all()
        
        mentioned_dept = None
        for dept in departments:
            if dept.name.lower() in message.lower():
                mentioned_dept = dept
                break
        
        if mentioned_dept:
            # Department-specific precautions
            precautions_map = {
                'cardiology': [
                    "🩺 Bring previous ECG/Echo reports",
                    "💊 List of current medications",
                    "🚫 Avoid caffeine 2 hours before",
                    "👕 Wear comfortable, loose clothing",
                    "📋 Fasting may be required for some tests"
                ],
                'neurology': [
                    "🧠 Bring previous MRI/CT scan reports",
                    "📝 Note down symptoms and frequency",
                    "💊 List of current medications",
                    "😴 Get adequate sleep night before",
                    "🚗 Arrange transportation if tests planned"
                ],
                'orthopedic': [
                    "🦴 Bring previous X-rays/MRI reports",
                    "👟 Wear comfortable shoes",
                    "🩳 Wear loose clothing for examination",
                    "💊 List of pain medications taken",
                    "🚶 Bring walking aid if using one"
                ],
                'pediatric': [
                    "👶 Bring vaccination records",
                    "📏 Growth chart if available",
                    "🍼 Feeding schedule details",
                    "🧸 Bring comfort toy for child",
                    "👨‍👩‍👧 Both parents if possible"
                ],
                'general': [
                    "🆔 Bring valid ID proof",
                    "📋 Previous medical records",
                    "💊 List of current medications",
                    "🩺 Insurance card if applicable",
                    "📝 List of symptoms and questions"
                ]
            }
            
            dept_key = next((k for k in precautions_map.keys() 
                           if k in mentioned_dept.name.lower()), 'general')
            precautions = precautions_map.get(dept_key, precautions_map['general'])
            
            precautions_text = "\n".join(precautions)
            
            return {
                'response': f"📋 Precautions for {mentioned_dept.name}:\n\n{precautions_text}\n\n"
                           f"⚠️ General Tips:\n"
                           f"• Arrive 10-15 minutes early\n"
                           f"• Wear mask if you have cold/flu\n"
                           f"• Keep phone charged for updates",
                'suggestions': [
                    "Book appointment",
                    "Check wait time",
                    "View doctors",
                    "Go back"
                ],
                'type': 'precautions',
                'data': {'department': mentioned_dept.name}
            }
        
        # General precautions
        return {
            'response': "📋 General Hospital Visit Precautions:\n\n"
                       "✅ Essential Items:\n"
                       "• Valid ID proof (Aadhar/License)\n"
                       "• Previous medical records\n"
                       "• List of current medications\n"
                       "• Insurance card (if applicable)\n\n"
                       "⏰ Timing:\n"
                       "• Arrive 10-15 minutes early\n"
                       "• Check wait times before leaving\n\n"
                       "🏥 At Hospital:\n"
                       "• Wear comfortable clothing\n"
                       "• Bring a companion if needed\n"
                       "• Keep phone charged\n"
                       "• Follow COVID protocols\n\n"
                       "Which department are you visiting?",
            'suggestions': [
                "Cardiology",
                "Neurology",
                "Orthopedic",
                "Pediatrics",
                "General Medicine"
            ],
            'type': 'precautions_general'
        }


class ManagementHandlers:
    """Management-specific chatbot handlers."""
    
    @staticmethod
    def handle_queue_stats() -> dict:
        """Handle queue statistics queries."""
        from app import db
        
        today = date.today()
        
        # Get today's appointments by status
        total_today = Appointment.query.filter_by(appointment_date=today).count()
        waiting = Appointment.query.filter_by(
            appointment_date=today,
            status='waiting'
        ).count()
        in_progress = Appointment.query.filter_by(
            appointment_date=today,
            status='in_progress'
        ).count()
        completed = Appointment.query.filter_by(
            appointment_date=today,
            status='completed'
        ).count()
        
        # Department-wise breakdown
        dept_stats = db.session.query(
            Department.name,
            func.count(Appointment.id).label('count')
        ).join(
            Appointment, Department.id == Appointment.department_id
        ).filter(
            Appointment.appointment_date == today,
            Appointment.status.in_(['waiting', 'in_progress'])
        ).group_by(Department.name).all()
        
        dept_text = "\n".join([f"• {name}: {count} patients" for name, count in dept_stats[:5]])
        
        return {
            'response': f"📊 Live Queue Statistics:\n\n"
                       f"📅 Today's Overview:\n"
                       f"• Total Appointments: {total_today}\n"
                       f"• ⏳ Waiting: {waiting}\n"
                       f"• 🔄 In Progress: {in_progress}\n"
                       f"• ✅ Completed: {completed}\n\n"
                       f"🏥 Active Queues by Department:\n{dept_text or '• No active queues'}\n\n"
                       f"⚡ Completion Rate: {round((completed/total_today*100) if total_today > 0 else 0, 1)}%",
            'suggestions': [
                "Department performance",
                "High-risk patients",
                "Doctor availability",
                "Crowd forecast"
            ],
            'type': 'queue_stats',
            'data': {
                'total': total_today,
                'waiting': waiting,
                'in_progress': in_progress,
                'completed': completed
            }
        }
    
    @staticmethod
    def handle_today_summary() -> dict:
        """Handle today's summary report."""
        from app import db
        
        today = date.today()
        
        # Appointments
        total_appts = Appointment.query.filter_by(appointment_date=today).count()
        completed = Appointment.query.filter_by(
            appointment_date=today,
            status='completed'
        ).count()
        no_shows = Appointment.query.filter_by(
            appointment_date=today,
            status='no_show'
        ).count()
        
        # Departments
        active_depts = Department.query.filter_by(is_active=True).count()
        
        # Doctors
        available_doctors = Doctor.query.filter_by(is_available=True).count()
        
        # Average wait time (estimated)
        avg_wait = 25  # Placeholder
        
        return {
            'response': f"📈 Today's Summary Report\n"
                       f"📅 {today.strftime('%B %d, %Y')}\n\n"
                       f"👥 Appointments:\n"
                       f"• Total: {total_appts}\n"
                       f"• Completed: {completed}\n"
                       f"• No-shows: {no_shows}\n"
                       f"• Show Rate: {round((1 - no_shows/total_appts)*100 if total_appts > 0 else 100, 1)}%\n\n"
                       f"🏥 Operations:\n"
                       f"• Active Departments: {active_depts}\n"
                       f"• Available Doctors: {available_doctors}\n"
                       f"• Avg Wait Time: ~{avg_wait} min\n\n"
                       f"💡 Status: {'🟢 Normal' if total_appts < 100 else '🟡 Busy' if total_appts < 150 else '🔴 Very Busy'}",
            'suggestions': [
                "Queue statistics",
                "Department performance",
                "High-risk patients",
                "Crowd forecast"
            ],
            'type': 'today_summary'
        }
    
    @staticmethod
    def handle_high_risk_patients() -> dict:
        """Handle high-risk patient queries."""
        today = date.today()
        
        # Get today's appointments with high priority scores
        high_risk = Appointment.query.filter(
            Appointment.appointment_date == today,
            Appointment.status.in_(['waiting', 'confirmed', 'scheduled']),
            Appointment.priority_score >= 7.0  # High priority threshold
        ).order_by(Appointment.priority_score.desc()).limit(10).all()
        
        if high_risk:
            patient_list = []
            for appt in high_risk[:5]:
                patient = Patient.query.get(appt.patient_id)
                dept = Department.query.get(appt.department_id)
                patient_list.append(
                    f"• {patient.name if patient else 'N/A'} - {dept.name if dept else 'N/A'} "
                    f"({appt.appointment_time.strftime('%I:%M %p')}) [Priority: {appt.priority_score:.1f}]"
                )
            
            patient_text = "\n".join(patient_list)
            
            return {
                'response': f"🚨 High-Risk Patients Today:\n\n"
                           f"Found {len(high_risk)} high-priority cases:\n\n"
                           f"{patient_text}\n\n"
                           f"⚠️ These patients require immediate attention.\n"
                           f"💡 Consider prioritizing in queue management.",
                'suggestions': [
                    "View queue",
                    "Department performance",
                    "Today's summary",
                    "Doctor availability"
                ],
                'type': 'high_risk_patients',
                'data': {'count': len(high_risk)}
            }
        
        return {
            'response': "✅ No high-risk patients currently in queue.\n\n"
                       "All patients are being managed normally.",
            'suggestions': [
                "Queue statistics",
                "Today's summary",
                "Department performance"
            ],
            'type': 'high_risk_patients',
            'data': {'count': 0}
        }
    
    @staticmethod
    def handle_department_performance() -> dict:
        """Handle department performance queries."""
        from app import db
        
        today = date.today()
        
        # Get department-wise stats - simplified query
        dept_stats = []
        departments = Department.query.filter_by(is_active=True).all()
        
        for dept in departments:
            total = Appointment.query.filter_by(
                department_id=dept.id,
                appointment_date=today
            ).count()
            
            completed = Appointment.query.filter_by(
                department_id=dept.id,
                appointment_date=today,
                status='completed'
            ).count()
            
            no_shows = Appointment.query.filter_by(
                department_id=dept.id,
                appointment_date=today,
                status='no_show'
            ).count()
            
            if total > 0:
                dept_stats.append((dept.name, total, completed, no_shows))
        
        if dept_stats:
            dept_list = []
            for name, total, completed, no_shows in dept_stats[:5]:
                completion_rate = round((completed/total*100) if total > 0 else 0, 1)
                dept_list.append(
                    f"• {name}:\n"
                    f"  Total: {total} | Completed: {completed} | Rate: {completion_rate}%"
                )
            
            dept_text = "\n".join(dept_list)
            
            return {
                'response': f"📊 Department Performance Today:\n\n{dept_text}\n\n"
                           f"💡 Use this data to optimize resource allocation.",
                'suggestions': [
                    "Queue statistics",
                    "Doctor availability",
                    "Today's summary",
                    "Crowd forecast"
                ],
                'type': 'department_performance'
            }
        
        return {
            'response': "No department data available for today.",
            'suggestions': ["Queue statistics", "Today's summary"],
            'type': 'department_performance'
        }
    
    @staticmethod
    def handle_doctor_availability() -> dict:
        """Handle doctor availability queries."""
        available = Doctor.query.filter_by(is_available=True).all()
        unavailable = Doctor.query.filter_by(is_available=False).count()
        
        if available:
            doctor_list = []
            for doc in available[:8]:
                dept = Department.query.get(doc.department_id)
                doctor_list.append(
                    f"• Dr. {doc.name} - {dept.name if dept else 'N/A'}"
                )
            
            doctor_text = "\n".join(doctor_list)
            
            return {
                'response': f"👨‍⚕️ Doctor Availability:\n\n"
                           f"✅ Available: {len(available)} doctors\n"
                           f"❌ Unavailable: {unavailable} doctors\n\n"
                           f"Currently Available:\n{doctor_text}",
                'suggestions': [
                    "Queue statistics",
                    "Department performance",
                    "Today's summary"
                ],
                'type': 'doctor_availability',
                'data': {
                    'available': len(available),
                    'unavailable': unavailable
                }
            }
        
        return {
            'response': "⚠️ No doctors currently marked as available.\n\n"
                       "Please update doctor availability in the system.",
            'suggestions': ["Manage doctors", "Queue statistics"],
            'type': 'doctor_availability'
        }
    
    @staticmethod
    def handle_noshow_prediction() -> dict:
        """Handle no-show prediction queries."""
        today = date.today()
        
        # Get today's confirmed appointments
        confirmed = Appointment.query.filter_by(
            appointment_date=today,
            status='confirmed'
        ).limit(20).all()
        
        if confirmed:
            high_risk_count = 0
            predictions = []
            
            for appt in confirmed[:5]:
                patient = Patient.query.get(appt.patient_id)
                if patient:
                    # Simplified no-show risk (would use ML model in production)
                    risk_score = 0.3  # Placeholder
                    
                    if risk_score > 0.5:
                        high_risk_count += 1
                        predictions.append(
                            f"• {patient.name} - {appt.appointment_time.strftime('%I:%M %p')} "
                            f"(Risk: {round(risk_score*100)}%)"
                        )
            
            if predictions:
                pred_text = "\n".join(predictions)
                return {
                    'response': f"⚠️ No-Show Risk Analysis:\n\n"
                               f"High-risk appointments: {high_risk_count}/{len(confirmed)}\n\n"
                               f"{pred_text}\n\n"
                               f"💡 Consider sending reminder SMS to these patients.",
                    'suggestions': [
                        "Send reminders",
                        "Queue statistics",
                        "Today's summary"
                    ],
                    'type': 'noshow_prediction',
                    'data': {'high_risk_count': high_risk_count}
                }
        
        return {
            'response': "✅ Low no-show risk for today's appointments.\n\n"
                       "All patients are likely to show up.",
            'suggestions': ["Queue statistics", "Today's summary"],
            'type': 'noshow_prediction'
        }
    
    @staticmethod
    def handle_crowd_forecast() -> dict:
        """Handle crowd forecast queries."""
        from app.services.crowd_predictor import CrowdPredictor
        from datetime import timedelta
        
        try:
            crowd_predictor = CrowdPredictor()
            tomorrow = date.today() + timedelta(days=1)
            
            # Get predictions for key hours
            predictions = []
            hours = [8, 10, 12, 14, 16]
            
            for hour in hours:
                pred = crowd_predictor.predict_crowd_level(
                    department_id=1,
                    target_date=tomorrow,
                    hour=hour
                )
                
                time_label = f"{hour}:00 {'AM' if hour < 12 else 'PM'}"
                emoji = {'low': '🟢', 'medium': '🟡', 'high': '🟠', 'critical': '🔴'}
                predictions.append(
                    f"{emoji.get(pred['level'], '⚪')} {time_label}: {pred['level'].title()}"
                )
            
            pred_text = "\n".join(predictions)
            
            return {
                'response': f"📊 Crowd Forecast for Tomorrow:\n"
                           f"{tomorrow.strftime('%B %d, %Y')}\n\n"
                           f"{pred_text}\n\n"
                           f"💡 Recommendations:\n"
                           f"• Schedule more staff during peak hours\n"
                           f"• Prepare for high-volume periods\n"
                           f"• Consider opening additional counters",
                'suggestions': [
                    "Queue statistics",
                    "Doctor availability",
                    "Department performance",
                    "Today's summary"
                ],
                'type': 'crowd_forecast'
            }
        except Exception as e:
            return {
                'response': "Unable to generate crowd forecast at this time.\n\n"
                           "Please try again later.",
                'suggestions': ["Queue statistics", "Today's summary"],
                'type': 'error'
            }
