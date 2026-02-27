# Queue Priority Display Enhanced ✅

## Enhancement
Added visual priority level indicators with risk score percentages to the live queue management system.

## What Was Added

### 1. Priority Risk Score Display
Each patient in the queue now shows:
- **Priority Badge**: Color-coded badge with icon (🔴 CRITICAL, 🟠 HIGH, 🟡 MEDIUM, 🟢 NORMAL)
- **Progress Bar**: Visual representation of risk percentage (0-100%)
- **Risk Percentage**: Numeric percentage displayed in progress bar
- **Raw Score**: Actual priority score shown below progress bar

### 2. Priority Legend Card
Added informational card explaining risk levels:
- **🔴 CRITICAL** (70-100% Risk) - Immediate attention required
- **🟠 HIGH** (45-69% Risk) - Priority treatment needed
- **🟡 MEDIUM** (20-44% Risk) - Standard priority
- **🟢 NORMAL** (0-19% Risk) - Routine consultation

### 3. Visual Enhancements
- Color-coded progress bars matching priority level
- Icons for quick visual identification
- Responsive design for both single and multi-department views
- Smaller, compact display for all-departments view

## Priority Calculation

### Factors Considered
1. **Emergency Flag**: +50 points if marked as emergency
2. **Age-Based Priority**:
   - Age 75+: +20 points
   - Age 65-74: +15 points
   - Age 55-64: +8 points
   - Age ≤5: +18 points
   - Age 6-12: +10 points

3. **Symptom Urgency** (highest matching keyword):
   - Unconscious/Heart Attack: +50 points
   - Stroke: +45 points
   - Chest Pain/Breathing Difficulty/Poisoning: +40 points
   - Seizure/Breathless: +35 points
   - Bleeding/Accident/Allergic Reaction: +30 points
   - Fracture/Severe Pain/Burn: +25 points
   - High Fever: +20 points

4. **Appointment Holder**: +5 points

### Risk Score Formula
```
Risk Score = Emergency + Age + Symptoms + Appointment
Risk Percentage = (Risk Score / 100) × 100%
```

## Example Display

### Single Department View
```
Token    Patient         Doctor      Priority                    Wait    Status    Actions
GM-001   Harish Yadav    Dr. Patel   🔴 CRITICAL [████████] 55%  15 min  Waiting   [Start]
                                      Score: 55.0

O-002    Arjun Mehta     Dr. Kumar   🟢 NORMAL   [██░░░░░░] 5%   30 min  Waiting   [Start]
                                      Score: 5.0
```

### All Departments View
```
General Medicine
Token    Patient         Doctor      Priority                Status
GM-001   Manoj Tiwari    Dr. Sharma  🟢 NORMAL [██░░] 5%    Waiting
                                      5.0

Pediatrics
Token    Patient         Doctor      Priority                  Status
P-001    Harish Yadav    Dr. Patel   🔴 CRITICAL [████████] 55% Waiting
                                      55.0
```

## Visual Design

### Priority Colors
- **Critical**: Red (#dc3545) - Urgent cases requiring immediate attention
- **High**: Orange (#fd7e14) - High priority cases
- **Medium**: Yellow (#ffc107) - Standard priority
- **Normal**: Green (#28a745) - Routine cases

### Progress Bar
- Width: Proportional to risk percentage (0-100%)
- Color: Matches priority level
- Text: Shows percentage inside bar
- Height: 20px (single dept), 18px (all depts)

### Badge
- Icon: Emoji indicator (🔴🟠🟡🟢)
- Label: Priority level name
- Min-width: Consistent sizing
- Background: Priority color

## Benefits

### For Medical Staff
1. **Quick Visual Assessment**: Instantly identify high-risk patients
2. **Priority Ordering**: Patients automatically sorted by risk score
3. **Informed Decisions**: See exact risk percentage and factors
4. **Emergency Identification**: Critical cases stand out with red indicators

### For Queue Management
1. **Efficient Triage**: High-risk patients get priority
2. **Fair System**: Transparent scoring based on objective factors
3. **Compliance**: Ensures elderly and children get appropriate priority
4. **Documentation**: Risk scores recorded for audit trail

### For Analytics
1. **Risk Distribution**: See overall risk profile of queue
2. **Department Comparison**: Compare risk levels across departments
3. **Trend Analysis**: Track high-risk patient patterns
4. **Resource Allocation**: Deploy staff based on risk levels

## How to View

1. **Login as Admin**
   ```
   URL: http://127.0.0.1:5000/admin/queue/
   Email: admin@hospital.com
   Password: admin123
   ```

2. **View Queue**
   - See priority legend at top
   - Each patient shows risk score and percentage
   - Progress bars indicate risk level visually

3. **Filter by Department**
   - Select department from dropdown
   - See detailed view with all information
   - Manage patients with Start/Complete buttons

## Technical Implementation

### Template Changes (`app/templates/queue.html`)
1. Added priority legend card
2. Enhanced priority display with progress bars
3. Added risk percentage calculation
4. Included raw score display
5. Responsive design for different views

### Priority Scorer (`app/services/priority_scorer.py`)
- Already implemented with comprehensive scoring
- Returns priority label with color and icon
- Scores range from 0-100
- Four priority levels (Critical, High, Medium, Normal)

### Queue Manager (`app/services/queue_manager.py`)
- Calculates priority on queue entry
- Stores priority_score in database
- Orders queue by priority (highest first)

## Example Scenarios

### Scenario 1: Elderly Patient with Chest Pain
```
Age: 72 years (+15 points)
Symptom: "Chest pain" (+40 points)
Has Appointment: Yes (+5 points)
Total: 60 points = 60% Risk = 🟠 HIGH Priority
```

### Scenario 2: Child with Fever
```
Age: 8 years (+10 points)
Symptom: "High fever" (+20 points)
Has Appointment: Yes (+5 points)
Total: 35 points = 35% Risk = 🟡 MEDIUM Priority
```

### Scenario 3: Adult Routine Checkup
```
Age: 35 years (+0 points)
Symptom: "General checkup" (+0 points)
Has Appointment: Yes (+5 points)
Total: 5 points = 5% Risk = 🟢 NORMAL Priority
```

### Scenario 4: Emergency Case
```
Emergency Flag: Yes (+50 points)
Age: 45 years (+0 points)
Symptom: "Unconscious" (+50 points)
Total: 100 points = 100% Risk = 🔴 CRITICAL Priority
```

## Files Modified
- ✅ `app/templates/queue.html` - Enhanced priority display with progress bars and legend

## Status
🎉 **QUEUE PRIORITY DISPLAY ENHANCED WITH RISK SCORES** 🎉

The queue management system now provides clear visual indicators of patient risk levels with percentage-based progress bars and comprehensive priority information.
