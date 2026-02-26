# 🤖 Role-Based Chatbot System

## Overview

The SmartCare Hospital Chatbot now features **role-based intelligence** that provides different features and responses based on whether the user is a **Patient** or **Management/Admin**.

## Two Distinct Modes

### 👤 Patient Mode
**For**: Patients and visitors
**Focus**: Personal assistance, appointments, health information

### 👨‍💼 Management Mode  
**For**: Hospital administrators and staff
**Focus**: Analytics, operations, queue management, reports

---

## Patient Mode Features

### 1. 📅 Book Appointments
- Browse departments
- View available doctors
- Check doctor ratings and experience
- Select appointment slots

**Example:**
```
Patient: "Book an appointment"
Bot: Shows departments → Select doctor → Choose time
```

### 2. 🔍 Check Appointment Status
- Track appointment by phone number
- View appointment details
- See current status (confirmed, waiting, completed)

**Example:**
```
Patient: "Check my status"
Bot: "Please provide your phone number"
Patient: "9876543210"
Bot: Shows all appointments with status
```

### 3. ⏰ Estimated Appointment Time
**NEW FEATURE** - Get precise timing information:
- Scheduled appointment time
- Current queue position
- Estimated actual time
- Expected wait duration

**Example:**
```
Patient: "What's my estimated time?"
Bot: 
"⏰ Your Appointment Estimate:
📅 Date: March 15, 2024
🕐 Scheduled: 10:00 AM
📊 Queue Position: #3
⏱️ Estimated Time: 10:30 AM
⌛ Expected Wait: ~30 minutes"
```

### 4. 📋 Precautions & Preparation
**NEW FEATURE** - Department-specific guidance:
- What to bring
- How to prepare
- Fasting requirements
- Clothing recommendations
- Timing advice

**Example:**
```
Patient: "Precautions for cardiology"
Bot:
"📋 Precautions for Cardiology:
🩺 Bring previous ECG/Echo reports
💊 List of current medications
🚫 Avoid caffeine 2 hours before
👕 Wear comfortable, loose clothing
📋 Fasting may be required for some tests"
```

**Department-Specific Precautions:**
- **Cardiology**: ECG prep, medication list, avoid caffeine
- **Neurology**: MRI reports, symptom notes, adequate sleep
- **Orthopedic**: X-rays, comfortable shoes, walking aids
- **Pediatrics**: Vaccination records, growth chart, comfort toys
- **General**: ID proof, medical records, insurance

### 5. 👨‍⚕️ Find Doctors
- Search by specialty
- View doctor ratings
- Check experience years
- See availability

### 6. ⏱️ Wait Time Estimates
- Current wait times by department
- Crowd level indicators
- Best time to visit recommendations

### 7. 🏥 Department Information
- List all departments
- Floor locations
- Available services

### 8. 📊 Crowd Predictions
- Best times to visit
- Peak hour warnings
- Tomorrow's forecast

---

## Management Mode Features

### 1. 📊 Queue Statistics
**Real-time operational data:**
- Total appointments today
- Patients waiting
- Patients in progress
- Completed consultations
- Completion rate
- Department-wise breakdown

**Example:**
```
Admin: "Queue statistics"
Bot:
"📊 Live Queue Statistics:
📅 Today's Overview:
• Total Appointments: 45
• ⏳ Waiting: 12
• 🔄 In Progress: 8
• ✅ Completed: 25
🏥 Active Queues by Department:
• Cardiology: 5 patients
• Neurology: 3 patients
• Orthopedic: 4 patients
⚡ Completion Rate: 55.6%"
```

### 2. 📈 Today's Summary Report
**Comprehensive daily overview:**
- Total appointments
- Completion statistics
- No-show rate
- Active departments
- Available doctors
- Average wait time
- System status indicator

**Example:**
```
Admin: "Today's summary"
Bot:
"📈 Today's Summary Report
📅 March 15, 2024
👥 Appointments:
• Total: 45
• Completed: 25
• No-shows: 2
• Show Rate: 95.6%
🏥 Operations:
• Active Departments: 8
• Available Doctors: 15
• Avg Wait Time: ~25 min
💡 Status: 🟢 Normal"
```

### 3. 🏥 Department Performance
**Performance metrics by department:**
- Total appointments per department
- Completion rates
- No-show rates
- Efficiency analysis

**Example:**
```
Admin: "Department performance"
Bot:
"📊 Department Performance Today:
• Cardiology:
  Total: 15 | Completed: 10 | Rate: 66.7%
• Neurology:
  Total: 12 | Completed: 8 | Rate: 66.7%
• Orthopedic:
  Total: 10 | Completed: 5 | Rate: 50.0%"
```

### 4. 👨‍⚕️ Doctor Availability
**Staff availability tracking:**
- Number of available doctors
- Number of unavailable doctors
- List of currently available doctors
- Department assignments

**Example:**
```
Admin: "Doctor availability"
Bot:
"👨‍⚕️ Doctor Availability:
✅ Available: 15 doctors
❌ Unavailable: 3 doctors
Currently Available:
• Dr. John Smith - Cardiology
• Dr. Sarah Johnson - Neurology
• Dr. Mike Brown - Orthopedic"
```

### 5. 🚨 High-Risk Patient Alerts
**Priority patient identification:**
- Emergency cases
- High-risk patients
- Patients requiring immediate attention
- Appointment times
- Department assignments

**Example:**
```
Admin: "High-risk patients"
Bot:
"🚨 High-Risk Patients Today:
Found 3 high-priority cases:
• John Doe - Cardiology (10:00 AM)
• Jane Smith - Neurology (11:30 AM)
• Bob Wilson - Emergency (09:45 AM)
⚠️ These patients require immediate attention.
💡 Consider prioritizing in queue management."
```

### 6. ⚠️ No-Show Predictions
**ML-powered predictions:**
- Identify high no-show risk appointments
- Risk percentage for each patient
- Proactive reminder suggestions

**Example:**
```
Admin: "No-show predictions"
Bot:
"⚠️ No-Show Risk Analysis:
High-risk appointments: 3/45
• Patient A - 10:00 AM (Risk: 65%)
• Patient B - 02:30 PM (Risk: 58%)
• Patient C - 04:00 PM (Risk: 52%)
💡 Consider sending reminder SMS to these patients."
```

### 7. 📉 Crowd Forecast
**Predictive analytics:**
- Tomorrow's crowd predictions
- Hour-by-hour forecast
- Peak time identification
- Staffing recommendations

**Example:**
```
Admin: "Crowd forecast"
Bot:
"📊 Crowd Forecast for Tomorrow:
March 16, 2024
🟢 8:00 AM: Low
🟡 10:00 AM: Medium
🟠 12:00 PM: High
🟡 2:00 PM: Medium
🟢 4:00 PM: Low
💡 Recommendations:
• Schedule more staff during peak hours
• Prepare for high-volume periods
• Consider opening additional counters"
```

---

## How Role Detection Works

### Automatic Detection
The chatbot automatically detects user role based on:
1. **Authentication Status**: Checks if user is logged in
2. **User Type**: Checks `current_user.is_admin()`
3. **Context**: Uses session and user data

### Role Assignment
```python
if current_user.is_authenticated:
    if current_user.is_admin():
        role = "admin"  # Management Mode
    else:
        role = "patient"  # Patient Mode
else:
    role = "patient"  # Default to Patient Mode
```

---

## Comparison Table

| Feature | Patient Mode | Management Mode |
|---------|-------------|-----------------|
| **Book Appointments** | ✅ Yes | ❌ No |
| **Check Status** | ✅ Yes (own) | ❌ No |
| **Estimated Time** | ✅ Yes | ❌ No |
| **Precautions** | ✅ Yes | ❌ No |
| **Find Doctors** | ✅ Yes | ✅ Yes |
| **Wait Times** | ✅ Yes | ✅ Yes |
| **Queue Statistics** | ❌ No | ✅ Yes |
| **Today's Summary** | ❌ No | ✅ Yes |
| **Dept Performance** | ❌ No | ✅ Yes |
| **Doctor Availability** | ❌ No | ✅ Yes |
| **High-Risk Alerts** | ❌ No | ✅ Yes |
| **No-Show Predictions** | ❌ No | ✅ Yes |
| **Crowd Forecast** | ✅ Limited | ✅ Detailed |

---

## Testing the Role-Based System

### Test as Patient
1. Login as patient: `test@patient.com` / `test123`
2. Open chatbot
3. Try these commands:
   - "Hello"
   - "Book appointment"
   - "Check my status"
   - "What's my estimated time?"
   - "Precautions for cardiology"
   - "Find a doctor"

### Test as Admin
1. Login as admin: `admin@hospital.com` / `admin123`
2. Open chatbot
3. Try these commands:
   - "Hello"
   - "Queue statistics"
   - "Today's summary"
   - "High-risk patients"
   - "Department performance"
   - "Doctor availability"
   - "No-show predictions"
   - "Crowd forecast"

---

## Technical Implementation

### Files Modified/Created

#### Created:
- ✅ `app/services/chatbot_handlers.py` - Patient and Management handlers

#### Modified:
- ✅ `app/services/chatbot_service.py` - Role-based routing
- ✅ `app/routes/chatbot.py` - User role detection

### Key Classes

```python
class HospitalChatbot:
    - process_message() - Main entry point
    - _handle_patient_intent() - Route patient requests
    - _handle_management_intent() - Route management requests
    - _detect_intent() - Role-based intent detection

class PatientHandlers:
    - handle_estimated_time() - Appointment timing
    - handle_precautions() - Health advice

class ManagementHandlers:
    - handle_queue_stats() - Queue analytics
    - handle_today_summary() - Daily reports
    - handle_high_risk_patients() - Priority alerts
```

---

## Benefits

### For Patients
✅ **Personalized assistance** for their specific needs
✅ **Estimated timing** reduces uncertainty
✅ **Precautions** help them prepare properly
✅ **Easy booking** process
✅ **Status tracking** without calling

### For Management
✅ **Real-time analytics** for decision making
✅ **Performance metrics** for optimization
✅ **Risk alerts** for proactive management
✅ **Predictive insights** for planning
✅ **Operational efficiency** improvements

---

## Future Enhancements

### Phase 2 (Potential)
1. **Patient Mode**:
   - Complete booking through chat
   - Payment integration
   - Medical history access
   - Prescription reminders
   - Lab report notifications

2. **Management Mode**:
   - Staff scheduling assistance
   - Resource allocation suggestions
   - Financial analytics
   - Patient satisfaction metrics
   - Automated report generation

---

## Summary

The role-based chatbot system provides:

✅ **Two distinct modes** for different user types
✅ **8 patient features** for personal assistance
✅ **7 management features** for operations
✅ **Automatic role detection** based on login
✅ **Context-aware responses** for each role
✅ **Real-time data integration** with ML models
✅ **Production-ready** implementation

This enhancement makes the chatbot more useful and relevant to each user type, improving overall system efficiency and user satisfaction.
