"""
Intelligent Chatbot Service for Hospital System.
Role-based assistance for Patients and Management.
"""
import re
from datetime import date, datetime, timedelta
from app.models.models import Department, Doctor, Appointment, Patient
from app.services.slot_optimizer import SlotOptimizer
from app.services.crowd_predictor import CrowdPredictor
from app.services.health_risk_scorer import HealthRiskScorer
from app.services.noshow_predictor import NoShowPredictor
from app.services.chatbot_handlers import PatientHandlers, ManagementHandlers


class HospitalChatbot:
    """
    AI-powered chatbot with role-based features.
    - Patient Mode: Booking, status, precautions, wait times
    - Management Mode: Analytics, queue management, reports
    """
    
    def __init__(self):
        self.context = {}
        self.slot_optimizer = SlotOptimizer()
        self.crowd_predictor = CrowdPredictor()
        self.risk_scorer = HealthRiskScorer()
        self.noshow_predictor = NoShowPredictor()
        
        # Patient-specific intents
        self.patient_intents = {
            'greeting': [
                r'\b(hi|hello|hey|good morning|good afternoon|good evening)\b',
            ],
            'book_appointment': [
                r'\b(book|schedule|make|need|want).*(appointment|booking)\b',
                r'\b(appointment|booking).*(book|schedule|make)\b',
                r'\bbook\b',
            ],
            'check_status': [
                r'\b(check|view|see|track).*(status|appointment)\b',
                r'\b(where|what).*(my appointment|appointment status)\b',
                r'\bstatus\b',
            ],
            'estimated_time': [
                r'\b(estimated|expected|approximate).*(time|arrival|appointment)\b',
                r'\b(when|what time).*(my turn|my appointment)\b',
                r'\bestimated time\b',
            ],
            'precautions': [
                r'\b(precaution|preparation|prepare|before|advice)\b',
                r'\bwhat (should|to).*(bring|prepare|do)\b',
                r'\bprecautions?\b',
            ],
            'find_doctor': [
                r'\b(find|search|show|list).*(doctor|specialist)\b',
                r'\b(doctor|specialist).*(available|list)\b',
                r'\bdoctors?\b',
            ],
            'wait_time': [
                r'\b(wait|waiting).*(time|long|how long)\b',
                r'\bhow long.*(wait|take)\b',
                r'\bwait time\b',
            ],
            'departments': [
                r'\b(department|departments|specialt(y|ies))\b',
                r'\bwhat.*(department|specialty)\b',
            ],
            'crowd_info': [
                r'\b(crowd|busy|crowded|rush|peak)\b',
                r'\b(best time|when to visit)\b',
            ],
            'help': [
                r'\b(help|assist|support|guide)\b',
                r'\bwhat can you do\b',
            ],
            'thanks': [
                r'\b(thank|thanks|appreciate)\b',
            ],
            'bye': [
                r'\b(bye|goodbye|see you|exit|quit)\b',
            ],
        }
        
        # Management-specific intents
        self.management_intents = {
            'greeting': [
                r'\b(hi|hello|hey|good morning|good afternoon|good evening)\b',
            ],
            'queue_stats': [
                r'\b(queue|waiting).*(stats|statistics|status|count)\b',
                r'\bhow many.*(waiting|queue|patients)\b',
                r'\bqueue (status|stats)\b',
            ],
            'today_summary': [
                r'\b(today|daily).*(summary|report|stats|overview)\b',
                r'\bsummary.*(today|daily)\b',
                r'\btoday summary\b',
            ],
            'department_performance': [
                r'\b(department|dept).*(performance|stats|metrics)\b',
                r'\bhow.*(department|dept).*(doing|performing)\b',
                r'\bdepartment performance\b',
            ],
            'doctor_availability': [
                r'\b(doctor|staff).*(availability|available|schedule)\b',
                r'\bwho.*(available|on duty)\b',
                r'\bdoctor availability\b',
            ],
            'high_risk_patients': [
                r'\b(high.?risk|priority|urgent|critical).*(patient|case)\b',
                r'\bpriority patients\b',
                r'\bhigh.?risk\b',
                r'\bhigh risk patients\b',
            ],
            'noshow_prediction': [
                r'\b(no.?show|miss|skip).*(predict|risk|likely)\b',
                r'\bpredict.*(no.?show|miss)\b',
                r'\bno.?show\b',
            ],
            'crowd_forecast': [
                r'\b(crowd|traffic).*(forecast|predict|tomorrow)\b',
                r'\bforecast.*(crowd|busy)\b',
                r'\bcrowd forecast\b',
            ],
            'help': [
                r'\b(help|assist|support|guide)\b',
                r'\bwhat can you do\b',
            ],
            'thanks': [
                r'\b(thank|thanks|appreciate)\b',
            ],
            'bye': [
                r'\b(bye|goodbye|see you|exit|quit)\b',
            ],
        }
    
    def process_message(self, message: str, user_context: dict = None) -> dict:
        """
        Process user message and return appropriate response.
        
        Args:
            message: User's message text
            user_context: Optional context (patient_id, phone, user_role, etc.)
        
        Returns:
            dict with response, suggestions, and actions
        """
        message_lower = message.lower().strip()
        
        # Update context
        if user_context:
            self.context.update(user_context)
        
        # Determine user role
        user_role = self.context.get('user_role', 'patient')  # Default to patient
        
        # Detect intent based on role
        intent = self._detect_intent(message_lower, user_role)
        
        # Route to appropriate handler based on role
        if user_role == 'admin' or user_role == 'management':
            return self._handle_management_intent(intent, message_lower)
        else:
            return self._handle_patient_intent(intent, message_lower)
    
    def _handle_patient_intent(self, intent: str, message: str) -> dict:
        """Handle patient-specific intents."""
        if intent == 'greeting':
            return self._handle_patient_greeting()
        elif intent == 'book_appointment':
            return self._handle_book_appointment(message)
        elif intent == 'check_status':
            return self._handle_check_status(message)
        elif intent == 'estimated_time':
            return self._handle_estimated_time(message)
        elif intent == 'precautions':
            return self._handle_precautions(message)
        elif intent == 'find_doctor':
            return self._handle_find_doctor(message)
        elif intent == 'wait_time':
            return self._handle_wait_time(message)
        elif intent == 'departments':
            return self._handle_departments()
        elif intent == 'crowd_info':
            return self._handle_crowd_info(message)
        elif intent == 'help':
            return self._handle_patient_help()
        elif intent == 'thanks':
            return self._handle_thanks()
        elif intent == 'bye':
            return self._handle_bye()
        else:
            return self._handle_patient_unknown(message)
    
    def _handle_management_intent(self, intent: str, message: str) -> dict:
        """Handle management-specific intents."""
        if intent == 'greeting':
            return self._handle_management_greeting()
        elif intent == 'queue_stats':
            return self._handle_queue_stats()
        elif intent == 'today_summary':
            return self._handle_today_summary()
        elif intent == 'department_performance':
            return self._handle_department_performance()
        elif intent == 'doctor_availability':
            return self._handle_doctor_availability()
        elif intent == 'high_risk_patients':
            return self._handle_high_risk_patients()
        elif intent == 'noshow_prediction':
            return self._handle_noshow_prediction()
        elif intent == 'crowd_forecast':
            return self._handle_crowd_forecast()
        elif intent == 'help':
            return self._handle_management_help()
        elif intent == 'thanks':
            return self._handle_thanks()
        elif intent == 'bye':
            return self._handle_bye()
        else:
            return self._handle_management_unknown(message)
    
    def _detect_intent(self, message: str, user_role: str = 'patient') -> str:
        """Detect user intent from message based on role."""
        intents = self.management_intents if user_role in ['admin', 'management'] else self.patient_intents
        
        for intent, patterns in intents.items():
            for pattern in patterns:
                if re.search(pattern, message, re.IGNORECASE):
                    return intent
        return 'unknown'
    
    def _handle_patient_greeting(self) -> dict:
        """Handle patient greeting messages."""
        return {
            'response': "👋 Hello! I'm your SmartCare Patient Assistant. How can I help you today?",
            'suggestions': [
                "Book an appointment",
                "Check my status",
                "Estimated time",
                "Precautions & advice",
                "Find a doctor"
            ],
            'type': 'greeting',
            'role': 'patient'
        }
    
    def _handle_management_greeting(self) -> dict:
        """Handle management greeting messages."""
        return {
            'response': "👋 Hello! I'm your SmartCare Management Assistant. What would you like to know?",
            'suggestions': [
                "Queue statistics",
                "Today's summary",
                "High-risk patients",
                "Department performance",
                "Crowd forecast"
            ],
            'type': 'greeting',
            'role': 'management'
        }
    
    def _handle_book_appointment(self, message: str) -> dict:
        """Handle appointment booking requests."""
        # Check if department mentioned
        departments = Department.query.filter_by(is_active=True).all()
        dept_names = [d.name.lower() for d in departments]
        
        mentioned_dept = None
        for dept in departments:
            if dept.name.lower() in message:
                mentioned_dept = dept
                break
        
        if mentioned_dept:
            # Get available doctors
            doctors = Doctor.query.filter_by(
                department_id=mentioned_dept.id,
                is_available=True
            ).all()
            
            if doctors:
                doctor_list = "\n".join([
                    f"• Dr. {d.name} - {d.specialization} ({d.experience_years} years exp.)"
                    for d in doctors[:5]
                ])
                
                return {
                    'response': f"Great! I can help you book an appointment in {mentioned_dept.name}.\n\n"
                               f"Available doctors:\n{doctor_list}\n\n"
                               f"Would you like to proceed with booking?",
                    'suggestions': [
                        f"Book with Dr. {doctors[0].name}",
                        "See more doctors",
                        "Check best time to visit",
                        "Go back"
                    ],
                    'type': 'booking_doctors',
                    'data': {
                        'department_id': mentioned_dept.id,
                        'doctors': [{'id': d.id, 'name': d.name} for d in doctors]
                    }
                }
        
        # No department mentioned - show options
        dept_list = "\n".join([f"• {d.name}" for d in departments])
        
        return {
            'response': f"I'd be happy to help you book an appointment! 📅\n\n"
                       f"Which department would you like to visit?\n\n{dept_list}",
            'suggestions': [d.name for d in departments[:4]] + ["Show all departments"],
            'type': 'booking_department',
            'data': {
                'departments': [{'id': d.id, 'name': d.name} for d in departments]
            }
        }
    
    def _handle_check_status(self, message: str) -> dict:
        """Handle appointment status check."""
        # Extract phone number if present
        phone_match = re.search(r'\b\d{10}\b', message)
        
        if phone_match:
            phone = phone_match.group()
            patients = Patient.query.filter_by(phone=phone).all()
            
            if patients:
                appointments = []
                for patient in patients:
                    appts = Appointment.query.filter_by(patient_id=patient.id).order_by(
                        Appointment.appointment_date.desc()
                    ).limit(3).all()
                    appointments.extend(appts)
                
                if appointments:
                    appt_list = "\n".join([
                        f"• {a.appointment_number} - {a.appointment_date} at {a.appointment_time.strftime('%H:%M')} "
                        f"({a.status})"
                        for a in appointments[:3]
                    ])
                    
                    return {
                        'response': f"Found your appointments! 📋\n\n{appt_list}\n\n"
                                   f"Would you like more details about any of these?",
                        'suggestions': [
                            "Show full details",
                            "Book new appointment",
                            "Cancel appointment"
                        ],
                        'type': 'status_found',
                        'data': {
                            'appointments': [
                                {
                                    'id': a.id,
                                    'number': a.appointment_number,
                                    'date': a.appointment_date.isoformat(),
                                    'time': a.appointment_time.strftime('%H:%M'),
                                    'status': a.status
                                }
                                for a in appointments[:3]
                            ]
                        }
                    }
                else:
                    return {
                        'response': "I couldn't find any appointments for this phone number. 😕\n\n"
                                   "Would you like to book a new appointment?",
                        'suggestions': [
                            "Book appointment",
                            "Try different number",
                            "Contact support"
                        ],
                        'type': 'status_not_found'
                    }
        
        # No phone number provided
        return {
            'response': "I can help you check your appointment status! 🔍\n\n"
                       "Please provide your 10-digit phone number.",
            'suggestions': [
                "Enter phone number",
                "I don't have phone number",
                "Go back"
            ],
            'type': 'status_request_phone'
        }
    
    def _handle_find_doctor(self, message: str) -> dict:
        """Handle doctor search requests."""
        # Check if specialty mentioned
        specialties = [
            'cardiology', 'neurology', 'orthopedic', 'pediatric',
            'general', 'dermatology', 'ent', 'gynecology'
        ]
        
        mentioned_specialty = None
        for spec in specialties:
            if spec in message:
                mentioned_specialty = spec
                break
        
        if mentioned_specialty:
            doctors = Doctor.query.filter(
                Doctor.specialization.ilike(f'%{mentioned_specialty}%'),
                Doctor.is_available == True
            ).all()
            
            if doctors:
                doctor_list = "\n".join([
                    f"• Dr. {d.name} - {d.specialization}\n"
                    f"  {d.experience_years} years exp. | Rating: {d.rating}⭐"
                    for d in doctors[:5]
                ])
                
                return {
                    'response': f"Found {len(doctors)} {mentioned_specialty} specialist(s):\n\n{doctor_list}",
                    'suggestions': [
                        f"Book with Dr. {doctors[0].name}",
                        "See more doctors",
                        "Check availability",
                        "Go back"
                    ],
                    'type': 'doctors_found',
                    'data': {
                        'doctors': [
                            {
                                'id': d.id,
                                'name': d.name,
                                'specialization': d.specialization,
                                'experience': d.experience_years,
                                'rating': d.rating
                            }
                            for d in doctors
                        ]
                    }
                }
        
        # Show all doctors
        doctors = Doctor.query.filter_by(is_available=True).limit(10).all()
        
        if doctors:
            doctor_list = "\n".join([
                f"• Dr. {d.name} - {d.specialization}"
                for d in doctors[:8]
            ])
            
            return {
                'response': f"Here are our available doctors:\n\n{doctor_list}\n\n"
                           f"Which specialty are you looking for?",
                'suggestions': [
                    "Cardiology",
                    "Neurology",
                    "Pediatrics",
                    "General Medicine",
                    "Show all"
                ],
                'type': 'doctors_list'
            }
        
        return {
            'response': "I'm sorry, I couldn't find any available doctors at the moment. "
                       "Please try again later or contact our support team.",
            'suggestions': ["Contact support", "Go back"],
            'type': 'error'
        }
    
    def _handle_wait_time(self, message: str) -> dict:
        """Handle wait time inquiries."""
        departments = Department.query.filter_by(is_active=True).all()
        
        # Try to predict current wait times
        wait_info = []
        for dept in departments[:5]:
            # Get current crowd level
            try:
                prediction = self.crowd_predictor.predict_crowd_level(
                    department_id=dept.id,
                    target_date=date.today(),
                    hour=datetime.now().hour
                )
                
                # Estimate wait time based on crowd
                wait_estimates = {
                    'low': '10-15 minutes',
                    'medium': '20-30 minutes',
                    'high': '35-50 minutes',
                    'critical': '60+ minutes'
                }
                
                wait_time = wait_estimates.get(prediction['level'], '20-30 minutes')
                wait_info.append(f"• {dept.name}: ~{wait_time} ({prediction['level']} crowd)")
            except:
                wait_info.append(f"• {dept.name}: ~20-30 minutes")
        
        wait_list = "\n".join(wait_info)
        
        return {
            'response': f"Current estimated wait times:\n\n{wait_list}\n\n"
                       f"💡 Tip: Book an appointment to reduce your wait time!",
            'suggestions': [
                "Book appointment",
                "Check best time to visit",
                "View crowd predictions",
                "Go back"
            ],
            'type': 'wait_time_info'
        }
    
    def _handle_departments(self) -> dict:
        """Handle department inquiries."""
        departments = Department.query.filter_by(is_active=True).all()
        
        dept_list = "\n".join([
            f"• {d.name} (Floor {d.floor})"
            for d in departments
        ])
        
        return {
            'response': f"We have the following departments:\n\n{dept_list}\n\n"
                       f"Which department would you like to know more about?",
            'suggestions': [d.name for d in departments[:4]] + ["Book appointment"],
            'type': 'departments_list',
            'data': {
                'departments': [
                    {
                        'id': d.id,
                        'name': d.name,
                        'floor': d.floor
                    }
                    for d in departments
                ]
            }
        }
    
    def _handle_crowd_info(self, message: str) -> dict:
        """Handle crowd/busy time inquiries."""
        try:
            # Get predictions for tomorrow
            tomorrow = date.today() + timedelta(days=1)
            predictions = []
            
            # Sample hours: 8 AM, 12 PM, 4 PM
            sample_hours = [8, 12, 16]
            
            for hour in sample_hours:
                pred = self.crowd_predictor.predict_crowd_level(
                    department_id=1,  # General Medicine
                    target_date=tomorrow,
                    hour=hour
                )
                
                time_label = f"{hour}:00 {'AM' if hour < 12 else 'PM'}"
                predictions.append(f"• {time_label}: {pred['level'].title()} crowd")
            
            pred_list = "\n".join(predictions)
            
            return {
                'response': f"📊 Crowd predictions for tomorrow:\n\n{pred_list}\n\n"
                           f"💡 Best times to visit: Early morning (8-9 AM) or late afternoon (5-6 PM)",
                'suggestions': [
                    "Book for 8 AM",
                    "Book for 5 PM",
                    "See full predictions",
                    "Go back"
                ],
                'type': 'crowd_predictions'
            }
        except:
            return {
                'response': "💡 Best times to visit:\n\n"
                           "• Early morning (8-9 AM) - Usually less crowded\n"
                           "• Lunch time (12-1 PM) - Moderate crowd\n"
                           "• Late afternoon (5-6 PM) - Less crowded\n\n"
                           "Avoid: Monday mornings and 10-11 AM (peak hours)",
                'suggestions': [
                    "Book appointment",
                    "Check wait times",
                    "Go back"
                ],
                'type': 'crowd_tips'
            }
    
    def _handle_help(self) -> dict:
        """Handle help requests."""
        return {
            'response': "I can help you with:\n\n"
                       "📅 Book appointments\n"
                       "🔍 Check appointment status\n"
                       "👨‍⚕️ Find doctors\n"
                       "⏱️ Get wait time estimates\n"
                       "🏥 View departments\n"
                       "📊 Check crowd predictions\n\n"
                       "Just ask me anything!",
            'suggestions': [
                "Book appointment",
                "Check status",
                "Find doctor",
                "Wait times",
                "Departments"
            ],
            'type': 'help'
        }
    
    def _handle_thanks(self) -> dict:
        """Handle thank you messages."""
        return {
            'response': "You're welcome! 😊 Is there anything else I can help you with?",
            'suggestions': [
                "Book appointment",
                "Check status",
                "Find doctor",
                "No, thanks"
            ],
            'type': 'thanks'
        }
    
    def _handle_bye(self) -> dict:
        """Handle goodbye messages."""
        return {
            'response': "Goodbye! Take care and stay healthy! 👋\n\n"
                       "Feel free to chat with me anytime you need assistance.",
            'suggestions': [],
            'type': 'bye'
        }
    
    def _handle_unknown(self, message: str) -> dict:
        """Handle unknown/unclear messages."""
        return {
            'response': "I'm not sure I understood that. 🤔\n\n"
                       "I can help you with:\n"
                       "• Booking appointments\n"
                       "• Checking appointment status\n"
                       "• Finding doctors\n"
                       "• Getting wait time info\n\n"
                       "What would you like to do?",
            'suggestions': [
                "Book appointment",
                "Check status",
                "Find doctor",
                "Get help"
            ],
            'type': 'unknown'
        }
    
    # ===== MANAGEMENT-SPECIFIC HANDLERS =====
    
    def _handle_queue_stats(self) -> dict:
        """Handle queue statistics queries."""
        return ManagementHandlers.handle_queue_stats()
    
    def _handle_today_summary(self) -> dict:
        """Handle today's summary report."""
        return ManagementHandlers.handle_today_summary()
    
    def _handle_high_risk_patients(self) -> dict:
        """Handle high-risk patient queries."""
        return ManagementHandlers.handle_high_risk_patients()
    
    def _handle_department_performance(self) -> dict:
        """Handle department performance queries."""
        return ManagementHandlers.handle_department_performance()
    
    def _handle_doctor_availability(self) -> dict:
        """Handle doctor availability queries."""
        return ManagementHandlers.handle_doctor_availability()
    
    def _handle_noshow_prediction(self) -> dict:
        """Handle no-show prediction queries."""
        return ManagementHandlers.handle_noshow_prediction()
    
    def _handle_crowd_forecast(self) -> dict:
        """Handle crowd forecast queries."""
        return ManagementHandlers.handle_crowd_forecast()
    
    def _handle_management_help(self) -> dict:
        """Handle management help requests."""
        return {
            'response': "📊 Management Dashboard Help\n\n"
                       "I can provide:\n"
                       "• Queue statistics and wait times\n"
                       "• Today's summary and reports\n"
                       "• Department performance metrics\n"
                       "• Doctor availability status\n"
                       "• High-risk patient alerts\n"
                       "• No-show predictions\n"
                       "• Crowd forecasts\n\n"
                       "What would you like to know?",
            'suggestions': [
                "Queue statistics",
                "Today's summary",
                "High-risk patients",
                "Department performance",
                "Crowd forecast"
            ],
            'type': 'help',
            'role': 'management'
        }
    
    def _handle_management_unknown(self, message: str) -> dict:
        """Handle unknown management messages."""
        return {
            'response': "I'm not sure I understood that. 🤔\n\n"
                       "I can help you with:\n"
                       "• Queue statistics\n"
                       "• Today's summary\n"
                       "• Department performance\n"
                       "• Doctor availability\n"
                       "• High-risk patients\n"
                       "• No-show predictions\n"
                       "• Crowd forecasts\n\n"
                       "What would you like to know?",
            'suggestions': [
                "Queue statistics",
                "Today's summary",
                "High-risk patients",
                "Department performance"
            ],
            'type': 'unknown',
            'role': 'management'
        }
    
    def _handle_estimated_time(self, message: str) -> dict:
        """Handle estimated time queries."""
        return PatientHandlers.handle_estimated_time(message, self.context)
    
    def _handle_precautions(self, message: str) -> dict:
        """Handle precautions queries."""
        return PatientHandlers.handle_precautions(message, self.context)
    
    def _handle_patient_help(self) -> dict:
        """Handle patient help requests."""
        return {
            'response': "I'm here to help! 😊\n\n"
                       "I can assist you with:\n"
                       "📅 Booking appointments\n"
                       "🔍 Checking appointment status\n"
                       "👨‍⚕️ Finding doctors\n"
                       "⏱️ Get wait time estimates\n"
                       "🏥 View departments\n"
                       "📊 Check crowd predictions\n\n"
                       "Just ask me anything!",
            'suggestions': [
                "Book appointment",
                "Check status",
                "Estimated time",
                "Precautions",
                "Find doctor"
            ],
            'type': 'help',
            'role': 'patient'
        }
    
    def _handle_patient_unknown(self, message: str) -> dict:
        """Handle unknown patient messages."""
        return {
            'response': "I'm not sure I understood that. 🤔\n\n"
                       "I can help you with:\n"
                       "• Booking appointments\n"
                       "• Checking appointment status\n"
                       "• Getting estimated time\n"
                       "• Viewing precautions\n"
                       "• Finding doctors\n\n"
                       "What would you like to do?",
            'suggestions': [
                "Book appointment",
                "Check status",
                "Estimated time",
                "Precautions",
                "Get help"
            ],
            'type': 'unknown',
            'role': 'patient'
        }


# Example usage
if __name__ == "__main__":
    bot = HospitalChatbot()
    
    # Test conversations
    test_messages = [
        "Hello",
        "I want to book an appointment",
        "Find me a cardiologist",
        "What's the wait time?",
        "Check my appointment status for 9876543210",
        "Thanks!"
    ]
    
    print("=" * 60)
    print("   HOSPITAL CHATBOT TEST")
    print("=" * 60)
    
    for msg in test_messages:
        print(f"\nUser: {msg}")
        response = bot.process_message(msg)
        print(f"Bot: {response['response']}")
        if response.get('suggestions'):
            print(f"Suggestions: {', '.join(response['suggestions'][:3])}")
        print("-" * 60)
