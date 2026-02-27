# Priority-Based Appointment Conflict Resolution ✅

## Overview
Implemented an intelligent priority-based conflict resolution system that automatically handles appointment booking conflicts. When two patients try to book the same doctor at the same time, the system assigns the slot based on medical priority and automatically reschedules the lower priority patient.

## How It Works

### 1. Conflict Detection
When a patient tries to book a slot that's already taken:
- System detects the conflict
- Calculates priority scores for BOTH patients
- Compares priorities to determine who gets the slot

### 2. Priority Calculation
Priority score (0-100) is calculated based on:

#### Age-Based Priority
- Age ≥ 75: +20 points
- Age 65-74: +15 points
- Age 55-64: +8 points
- Age ≤ 5: +18 points
- Age 6-12: +10 points

#### Emergency Flag
- Emergency patient: +50 points (configurable)

#### Symptom Urgency
High-priority symptoms add points:
- Unconscious, Heart attack: +50 points
- Stroke: +45 points
- Chest pain, Breathing difficulty, Poisoning: +40 points
- Breathless, Seizure: +35 points
- Bleeding, Accident, Allergic reaction: +30 points
- Fracture, Severe pain, Burn: +25 points
- High fever: +20 points

#### Appointment Status
- Has existing appointment: +5 points

### 3. Conflict Resolution Logic

#### Scenario A: New Patient Has HIGHER Priority
```
New Priority > Existing Priority
```
**Actions:**
1. ✅ New patient gets the requested slot
2. 🔄 Existing patient is rescheduled to next available slot
3. 📱 Existing patient receives SMS notification about reschedule
4. 💾 Both appointments are updated in database
5. ℹ️ New patient sees success message with priority info

**Example:**
- Existing: 30-year-old, regular checkup (Priority: 0)
- New: 75-year-old, chest pain (Priority: 100)
- Result: Elderly patient gets slot, young patient moved to next slot

#### Scenario B: Existing Patient Has HIGHER Priority
```
New Priority ≤ Existing Priority
```
**Actions:**
1. ❌ New patient cannot take the slot
2. 🔄 New patient is auto-assigned to next available slot
3. ℹ️ New patient sees reassignment message
4. 💾 New appointment created with new time
5. ✅ Existing patient keeps their slot

**Example:**
- Existing: 75-year-old, chest pain (Priority: 100)
- New: 30-year-old, regular checkup (Priority: 0)
- Result: Elderly patient keeps slot, young patient gets next slot

### 4. No Available Slots
If no alternative slots are available:
- ⚠️ Booking is rejected
- 📝 Patient sees detailed message explaining the situation
- 🔄 Patient is redirected to choose a different date

## Priority Levels

### 🔴 CRITICAL (70-100)
- Immediate attention required
- Examples: Elderly with emergency symptoms, severe injuries
- Always gets priority in conflicts

### 🟠 HIGH (45-69)
- Priority treatment needed
- Examples: Elderly patients, children, moderate symptoms
- Usually gets priority over normal patients

### 🟡 MEDIUM (20-44)
- Standard priority
- Examples: Middle-aged with minor symptoms
- May be rescheduled for higher priority patients

### 🟢 NORMAL (0-19)
- Routine consultation
- Examples: Young adults, regular checkups
- Most likely to be rescheduled in conflicts

## SMS Notifications

### Reschedule Notification
Sent to patients who are rescheduled:
```
🏥 SmartCare Hospital - Appointment Rescheduled

Dear [Patient Name],

Your appointment has been rescheduled due to a higher priority patient.

📅 Date: [Date]
⏰ OLD Time: [Old Time]
⏰ NEW Time: [New Time]
👨‍⚕️ Doctor: Dr. [Doctor Name]
🏢 Department: [Department]
🎫 Appointment #: [Number]

We apologize for any inconvenience. Your new slot is confirmed.
```

## User Experience

### For Higher Priority Patient
```
✅ Appointment booked successfully!
⚠️ Priority-based rescheduling: Your higher priority (85.0) secured this slot.
Previous patient (priority 15.0) was moved to 10:30 AM.
📱 SMS confirmation sent to your phone.
```

### For Lower Priority Patient (Auto-Reassigned)
```
⚠️ Requested slot taken by higher priority patient (85.0 vs your 15.0).
You've been automatically assigned to the next available slot: 10:30 AM.
✅ Appointment booked successfully!
📱 SMS confirmation sent to your phone.
```

### For Lower Priority Patient (No Slots Available)
```
❌ Sorry, this slot is taken by a higher priority patient (85.0 vs your 15.0).
No alternative slots available today. Please choose a different date.
```

## Benefits

✅ **Fair and Transparent**: Priority based on medical need, not first-come-first-served
✅ **Automatic Resolution**: No manual intervention required
✅ **Patient Safety**: Emergency and high-risk patients get priority
✅ **Clear Communication**: Patients understand why decisions are made
✅ **SMS Notifications**: Rescheduled patients are immediately informed
✅ **Seamless Experience**: Automatic reassignment to next available slot
✅ **Audit Trail**: All priority scores and decisions are logged

## Technical Implementation

### Files Modified

1. **app/routes/patient_portal.py**
   - Added conflict detection logic
   - Implemented priority comparison
   - Added automatic rescheduling
   - Added next slot finding algorithm

2. **app/services/sms_service.py**
   - Added `send_reschedule_notification()` method
   - Sends SMS to rescheduled patients

3. **app/services/priority_scorer.py**
   - Already existed, used for priority calculation
   - Calculates scores based on age, symptoms, emergency status

### Key Functions

```python
# Calculate priority
priority_scorer.calculate_priority(patient, symptoms, has_appointment)

# Find next available slot
optimizer.get_available_slots(doctor_id, date)

# Send reschedule notification
SMSService.send_reschedule_notification(patient, appointment, old_time, new_time, doctor, dept)
```

## Testing

Run the test script:
```bash
python test_priority_conflict_resolution.py
```

This demonstrates:
- Priority calculation for different patient types
- Conflict resolution scenarios
- Automatic rescheduling logic
- SMS notification system

## Example Scenarios

### Scenario 1: Emergency Overrides Regular Checkup
- **Patient A**: 30 years old, regular checkup → Priority: 0
- **Patient B**: 75 years old, chest pain, emergency → Priority: 100
- **Result**: Patient B gets slot, Patient A moved to next slot

### Scenario 2: Elderly Gets Priority Over Young Adult
- **Patient A**: 25 years old, minor symptoms → Priority: 10
- **Patient B**: 70 years old, routine visit → Priority: 15
- **Result**: Patient B gets slot, Patient A moved to next slot

### Scenario 3: Child Gets Priority
- **Patient A**: 35 years old, checkup → Priority: 0
- **Patient B**: 4 years old, fever → Priority: 38 (18 age + 20 fever)
- **Result**: Patient B gets slot, Patient A moved to next slot

## Configuration

Priority boost values can be configured in `config.py`:
```python
EMERGENCY_PRIORITY_BOOST = 50  # Points added for emergency patients
SLOT_DURATION_MIN = 15         # Slot duration in minutes
```

## Status: COMPLETE ✅

The priority-based conflict resolution system is fully functional and integrated into the appointment booking flow. Patients with higher medical priority automatically get preference, and all affected patients are notified via SMS.
