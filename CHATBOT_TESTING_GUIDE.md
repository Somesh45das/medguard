# 🧪 Chatbot Testing Guide

## Complete Testing Instructions for Role-Based Chatbot

---

## Prerequisites

### 1. Start the Application
```bash
python run.py
```

### 2. Ensure Database is Seeded
```bash
python seed_data.py
```

### 3. Test Accounts
- **Patient**: `test@patient.com` / `test123`
- **Admin**: `admin@hospital.com` / `admin123`

---

## Test Plan

### Phase 1: Patient Mode Testing
### Phase 2: Management Mode Testing
### Phase 3: Role Switching Testing
### Phase 4: Error Handling Testing

---

## Phase 1: Patient Mode Testing

### Setup
1. Login as patient: `test@patient.com` / `test123`
2. Navigate to any page
3. Click the purple chat button (bottom-right)

### Test 1.1: Greeting
```
Input: "Hello"
Expected: Patient greeting with patient-specific suggestions
Verify: 
  ✅ Greeting mentions "Patient Assistant"
  ✅ Suggestions include: Book appointment, Check status, Estimated time
```

### Test 1.2: Book Appointment
```
Input: "Book an appointment"
Expected: List of departments
Verify:
  ✅ Shows active departments
  ✅ Suggestion buttons for departments
  ✅ Can click department to proceed

Follow-up: Click "Cardiology"
Expected: List of cardiologists
Verify:
  ✅ Shows doctors with specialization
  ✅ Shows experience and ratings
  ✅ Suggestion buttons for doctors
```

### Test 1.3: Check Status
```
Input: "Check my appointment status"
Expected: Request for phone number
Verify:
  ✅ Asks for 10-digit phone number
  ✅ Provides suggestions

Follow-up: "9876543210"
Expected: List of appointments or "not found"
Verify:
  ✅ Shows appointment details if exists
  ✅ Shows appointment number, date, time, status
  ✅ Provides relevant suggestions
```

### Test 1.4: Estimated Time
```
Input: "What's my estimated time?"
Expected: Request for phone number or show estimate
Verify:
  ✅ Shows appointment date and time
  ✅ Shows queue position
  ✅ Shows estimated actual time
  ✅ Shows expected wait duration
  ✅ Provides helpful tip
```

### Test 1.5: Precautions
```
Input: "Precautions for cardiology"
Expected: Cardiology-specific precautions
Verify:
  ✅ Shows department-specific advice
  ✅ Lists what to bring
  ✅ Lists preparation steps
  ✅ Shows general tips
  ✅ Provides relevant suggestions

Test variations:
  - "Precautions for neurology"
  - "What should I bring?"
  - "How to prepare?"
```

### Test 1.6: Find Doctor
```
Input: "Find a cardiologist"
Expected: List of cardiologists
Verify:
  ✅ Shows doctors with cardiology specialty
  ✅ Shows experience years
  ✅ Shows ratings
  ✅ Provides booking suggestions

Test variations:
  - "Find a neurologist"
  - "Show me doctors"
  - "Find specialist"
```

### Test 1.7: Wait Time
```
Input: "What's the wait time?"
Expected: Current wait times by department
Verify:
  ✅ Shows multiple departments
  ✅ Shows estimated wait time
  ✅ Shows crowd level
  ✅ Provides helpful tip
  ✅ Suggests booking appointment
```

### Test 1.8: Departments
```
Input: "Show me departments"
Expected: List of all departments
Verify:
  ✅ Shows department names
  ✅ Shows floor numbers
  ✅ Provides department suggestions
```

### Test 1.9: Crowd Info
```
Input: "When should I visit?"
Expected: Crowd predictions and best times
Verify:
  ✅ Shows tomorrow's predictions
  ✅ Shows multiple time slots
  ✅ Shows crowd levels
  ✅ Provides best time recommendations
```

### Test 1.10: Help
```
Input: "Help"
Expected: List of patient features
Verify:
  ✅ Shows all patient capabilities
  ✅ Uses patient-friendly language
  ✅ Provides patient-specific suggestions
```

---

## Phase 2: Management Mode Testing

### Setup
1. Logout from patient account
2. Login as admin: `admin@hospital.com` / `admin123`
3. Click the purple chat button

### Test 2.1: Greeting
```
Input: "Hello"
Expected: Management greeting with management-specific suggestions
Verify:
  ✅ Greeting mentions "Management Assistant"
  ✅ Suggestions include: Queue statistics, Today's summary, High-risk patients
```

### Test 2.2: Queue Statistics
```
Input: "Queue statistics"
Expected: Real-time queue data
Verify:
  ✅ Shows total appointments today
  ✅ Shows waiting count
  ✅ Shows in-progress count
  ✅ Shows completed count
  ✅ Shows completion rate
  ✅ Shows department-wise breakdown
```

### Test 2.3: Today's Summary
```
Input: "Today's summary"
Expected: Comprehensive daily report
Verify:
  ✅ Shows today's date
  ✅ Shows appointment statistics
  ✅ Shows no-show count and rate
  ✅ Shows active departments
  ✅ Shows available doctors
  ✅ Shows average wait time
  ✅ Shows system status indicator
```

### Test 2.4: Department Performance
```
Input: "Department performance"
Expected: Performance metrics by department
Verify:
  ✅ Shows multiple departments
  ✅ Shows total appointments per dept
  ✅ Shows completed count
  ✅ Shows completion rate
  ✅ Provides actionable insights
```

### Test 2.5: Doctor Availability
```
Input: "Doctor availability"
Expected: Staff availability status
Verify:
  ✅ Shows count of available doctors
  ✅ Shows count of unavailable doctors
  ✅ Lists currently available doctors
  ✅ Shows department assignments
```

### Test 2.6: High-Risk Patients
```
Input: "High-risk patients"
Expected: Priority patient alerts
Verify:
  ✅ Shows count of high-risk cases
  ✅ Lists patient names (if any)
  ✅ Shows departments
  ✅ Shows appointment times
  ✅ Provides priority recommendations
```

### Test 2.7: No-Show Predictions
```
Input: "No-show predictions"
Expected: Risk analysis for appointments
Verify:
  ✅ Shows high-risk appointment count
  ✅ Lists patients with risk scores
  ✅ Shows appointment times
  ✅ Suggests sending reminders
```

### Test 2.8: Crowd Forecast
```
Input: "Crowd forecast"
Expected: Tomorrow's predictions
Verify:
  ✅ Shows tomorrow's date
  ✅ Shows hour-by-hour predictions
  ✅ Shows crowd levels with indicators
  ✅ Provides staffing recommendations
```

### Test 2.9: Help
```
Input: "Help"
Expected: List of management features
Verify:
  ✅ Shows all management capabilities
  ✅ Uses management-appropriate language
  ✅ Provides management-specific suggestions
```

---

## Phase 3: Role Switching Testing

### Test 3.1: Patient to Admin Switch
```
1. Login as patient
2. Open chatbot, send "Hello"
3. Verify patient greeting
4. Logout
5. Login as admin
6. Open chatbot, send "Hello"
7. Verify management greeting
```

### Test 3.2: Admin to Patient Switch
```
1. Login as admin
2. Open chatbot, send "Queue statistics"
3. Verify management response
4. Logout
5. Login as patient
6. Open chatbot, send "Queue statistics"
7. Verify patient-appropriate response or unknown message
```

### Test 3.3: Unauthenticated Access
```
1. Logout completely
2. Navigate to public page
3. Open chatbot
4. Send "Hello"
5. Verify defaults to patient mode
```

---

## Phase 4: Error Handling Testing

### Test 4.1: Invalid Commands
```
Patient Mode:
Input: "Queue statistics"
Expected: Unknown message with patient suggestions

Management Mode:
Input: "Book appointment"
Expected: Unknown message with management suggestions
```

### Test 4.2: Empty Messages
```
Input: "" (empty)
Expected: Graceful handling, prompt for input
```

### Test 4.3: Very Long Messages
```
Input: (500+ character message)
Expected: Processes without error, provides relevant response
```

### Test 4.4: Special Characters
```
Input: "Hello!!! @#$%"
Expected: Detects greeting intent, responds normally
```

### Test 4.5: Phone Number Formats
```
Test various formats:
- "9876543210" (valid)
- "987-654-3210" (with dashes)
- "987 654 3210" (with spaces)
- "12345" (invalid)
Expected: Handles gracefully, validates format
```

---

## Phase 5: UI/UX Testing

### Test 5.1: Chat Window
```
✅ Opens smoothly when button clicked
✅ Closes when X button clicked
✅ Stays open when clicking inside
✅ Closes when clicking outside (optional)
```

### Test 5.2: Messages
```
✅ User messages appear on right (purple)
✅ Bot messages appear on left (white)
✅ Messages have proper spacing
✅ Long messages wrap correctly
✅ Emojis display properly
```

### Test 5.3: Suggestions
```
✅ Suggestion buttons appear below bot messages
✅ Buttons are clickable
✅ Clicking sends message automatically
✅ Buttons have hover effects
```

### Test 5.4: Typing Indicator
```
✅ Appears when message sent
✅ Shows animated dots
✅ Disappears when response received
```

### Test 5.5: Scrolling
```
✅ Auto-scrolls to latest message
✅ Scroll bar appears when needed
✅ Can manually scroll up
✅ Returns to bottom on new message
```

### Test 5.6: Input Field
```
✅ Can type in input field
✅ Enter key sends message
✅ Send button works
✅ Input clears after sending
✅ Placeholder text visible when empty
```

---

## Phase 6: Mobile Responsiveness

### Test 6.1: Mobile View
```
Device: iPhone/Android
✅ Chat button visible and clickable
✅ Chat window fits screen
✅ Messages readable
✅ Buttons tappable
✅ Input field accessible
✅ Keyboard doesn't cover input
```

### Test 6.2: Tablet View
```
Device: iPad/Android Tablet
✅ Chat window sized appropriately
✅ All elements visible
✅ Touch interactions work
```

---

## Phase 7: Performance Testing

### Test 7.1: Response Time
```
Measure response times:
✅ Patient queries: < 500ms
✅ Management queries: < 800ms
✅ Database queries: < 200ms
```

### Test 7.2: Concurrent Users
```
Simulate multiple users:
✅ 5 users simultaneously
✅ 10 users simultaneously
✅ No performance degradation
```

### Test 7.3: Memory Usage
```
Monitor during extended use:
✅ No memory leaks
✅ Stable performance over time
```

---

## Test Results Template

### Test Session: [Date]
**Tester**: [Name]
**Environment**: [Dev/Staging/Production]

| Test ID | Feature | Status | Notes |
|---------|---------|--------|-------|
| 1.1 | Patient Greeting | ✅ Pass | |
| 1.2 | Book Appointment | ✅ Pass | |
| 1.3 | Check Status | ✅ Pass | |
| ... | ... | ... | ... |

### Issues Found
1. [Issue description]
2. [Issue description]

### Overall Status
- Total Tests: X
- Passed: Y
- Failed: Z
- Pass Rate: %

---

## Automated Testing (Optional)

### Unit Tests
```python
# test_chatbot_service.py
def test_patient_greeting():
    bot = HospitalChatbot()
    response = bot.process_message("Hello", {"user_role": "patient"})
    assert "Patient Assistant" in response['response']
    assert response['role'] == 'patient'

def test_management_greeting():
    bot = HospitalChatbot()
    response = bot.process_message("Hello", {"user_role": "admin"})
    assert "Management Assistant" in response['response']
    assert response['role'] == 'management'
```

---

## Checklist Summary

### Patient Mode
- [ ] Greeting works
- [ ] Book appointment works
- [ ] Check status works
- [ ] Estimated time works
- [ ] Precautions work
- [ ] Find doctor works
- [ ] Wait time works
- [ ] Departments work
- [ ] Crowd info works
- [ ] Help works

### Management Mode
- [ ] Greeting works
- [ ] Queue statistics work
- [ ] Today's summary works
- [ ] Department performance works
- [ ] Doctor availability works
- [ ] High-risk patients work
- [ ] No-show predictions work
- [ ] Crowd forecast works
- [ ] Help works

### General
- [ ] Role detection works
- [ ] Role switching works
- [ ] Error handling works
- [ ] UI/UX is smooth
- [ ] Mobile responsive
- [ ] Performance acceptable

---

## Sign-Off

**Tested By**: _______________
**Date**: _______________
**Status**: ✅ Approved / ❌ Needs Work
**Notes**: _______________
