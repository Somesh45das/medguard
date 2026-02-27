# Risk Score Calculation Formula - Complete Explanation

## Overview
The risk score (also called priority score) is used to determine which patients should be seen first in the queue. The score ranges from 0 to 100, where higher scores indicate more urgent cases.

---

## The Formula

```
Priority Score = Emergency Points + Age Points + Symptom Points + Appointment Points
```

**Maximum Score**: 100 (capped)  
**Minimum Score**: 0

---

## Component Breakdown

### 1. Emergency Flag Points
**Range**: 0 or 50 points

```python
if patient.is_emergency:
    score += 50  # EMERGENCY_PRIORITY_BOOST from config.py
```

- If patient is marked as emergency: **+50 points**
- If not emergency: **+0 points**

**Example**:
- Emergency patient: +50
- Regular patient: +0

---

### 2. Age-Based Points
**Range**: 0 to 20 points

The system prioritizes elderly patients and young children:

```python
if age >= 75:
    score += 20      # Very elderly
elif age >= 65:
    score += 15      # Elderly
elif age >= 55:
    score += 8       # Senior
elif age <= 5:
    score += 18      # Infant/Toddler
elif age <= 12:
    score += 10      # Child
else:
    score += 0       # Adult (13-54 years)
```

**Age Priority Table**:
| Age Range | Points | Category |
|-----------|--------|----------|
| 75+ years | +20 | Very Elderly |
| 65-74 years | +15 | Elderly |
| 55-64 years | +8 | Senior |
| 0-5 years | +18 | Infant/Toddler |
| 6-12 years | +10 | Child |
| 13-54 years | +0 | Adult |

**Examples**:
- 80-year-old patient: +20 points
- 3-year-old child: +18 points
- 30-year-old adult: +0 points

---

### 3. Symptom-Based Points
**Range**: 0 to 50 points

The system analyzes the patient's symptoms and assigns points based on urgency:

```python
URGENT_SYMPTOMS = {
    "unconscious": 50,
    "heart attack": 50,
    "chest pain": 40,
    "breathing difficulty": 40,
    "poisoning": 40,
    "stroke": 45,
    "seizure": 35,
    "breathless": 35,
    "allergic reaction": 30,
    "bleeding": 30,
    "accident": 30,
    "fracture": 25,
    "severe pain": 25,
    "burn": 25,
    "high fever": 20,
}
```

**Important**: Only the HIGHEST matching symptom is counted (not cumulative).

**Examples**:
- "Patient is unconscious" → +50 points
- "Chest pain and difficulty breathing" → +40 points (highest match)
- "Mild headache" → +0 points (no match)
- "High fever and cough" → +20 points (high fever matches)

---

### 4. Appointment Status Points
**Range**: 0 or 5 points

```python
if has_appointment:
    score += 5
```

- Patient with scheduled appointment: **+5 points**
- Walk-in patient: **+0 points**

This gives a slight priority to patients who booked in advance.

---

## Priority Levels

Based on the final score, patients are categorized into 4 priority levels:

| Score Range | Priority Level | Color | Icon | Meaning |
|-------------|---------------|-------|------|---------|
| 70-100 | CRITICAL | Red (#dc3545) | 🔴 | Life-threatening, immediate attention |
| 45-69 | HIGH | Orange (#fd7e14) | 🟠 | Urgent, see soon |
| 20-44 | MEDIUM | Yellow (#ffc107) | 🟡 | Moderate urgency |
| 0-19 | NORMAL | Green (#28a745) | 🟢 | Routine care |

---

## Real-World Examples

### Example 1: Critical Emergency
**Patient**: 78-year-old with chest pain, marked as emergency

```
Calculation:
- Emergency flag: +50
- Age (78 years): +20
- Symptom (chest pain): +40
- Appointment: +0 (walk-in)
----------------------------
Total: 110 → Capped at 100
Priority: CRITICAL 🔴
```

---

### Example 2: High Priority Child
**Patient**: 4-year-old with high fever, has appointment

```
Calculation:
- Emergency flag: +0
- Age (4 years): +18
- Symptom (high fever): +20
- Appointment: +5
----------------------------
Total: 43
Priority: MEDIUM 🟡
```

---

### Example 3: Elderly with Fracture
**Patient**: 70-year-old with fracture, walk-in

```
Calculation:
- Emergency flag: +0
- Age (70 years): +15
- Symptom (fracture): +25
- Appointment: +0
----------------------------
Total: 40
Priority: MEDIUM 🟡
```

---

### Example 4: Adult Routine Checkup
**Patient**: 35-year-old for routine checkup, has appointment

```
Calculation:
- Emergency flag: +0
- Age (35 years): +0
- Symptom (none): +0
- Appointment: +5
----------------------------
Total: 5
Priority: NORMAL 🟢
```

---

### Example 5: Stroke Patient
**Patient**: 60-year-old showing stroke symptoms, emergency

```
Calculation:
- Emergency flag: +50
- Age (60 years): +8
- Symptom (stroke): +45
- Appointment: +0
----------------------------
Total: 103 → Capped at 100
Priority: CRITICAL 🔴
```

---

### Example 6: Child with Breathing Difficulty
**Patient**: 8-year-old with breathing difficulty, walk-in

```
Calculation:
- Emergency flag: +0
- Age (8 years): +10
- Symptom (breathing difficulty): +40
- Appointment: +0
----------------------------
Total: 50
Priority: HIGH 🟠
```

---

## How It's Used in the System

### 1. Queue Ordering
Patients in the queue are automatically sorted by priority score (highest first).

### 2. Conflict Resolution
When two patients book the same time slot:
- System calculates priority for both
- Higher priority patient gets the slot
- Lower priority patient is moved to next available slot
- SMS notification sent to rescheduled patient

### 3. Wait Time Estimation
Higher priority patients are moved up in the queue, affecting wait times for others.

### 4. Visual Indicators
Queue displays color-coded badges based on priority level for quick identification.

---

## Configuration

The emergency boost value can be adjusted in `config.py`:

```python
EMERGENCY_PRIORITY_BOOST = 50  # Default value
```

To make emergencies even more prioritized, increase this value (e.g., 60 or 70).

---

## Key Design Decisions

### Why These Ranges?

1. **Emergency (50 points)**: Ensures emergency patients always get high priority
2. **Age (0-20 points)**: Recognizes vulnerability of elderly and children
3. **Symptoms (0-50 points)**: Life-threatening symptoms can override other factors
4. **Appointment (5 points)**: Small bonus to reward advance booking

### Why Cap at 100?

- Provides a consistent scale for comparison
- Prevents score inflation
- Makes priority levels meaningful

### Why Only Highest Symptom?

- Prevents double-counting related symptoms
- Simplifies calculation
- Most urgent symptom is what matters most

---

## Code Location

The formula is implemented in:
- **File**: `app/services/priority_scorer.py`
- **Class**: `PriorityScorer`
- **Method**: `calculate_priority()`

---

## Summary

The risk score formula balances multiple factors to ensure:
- Life-threatening cases get immediate attention
- Vulnerable populations (elderly, children) are prioritized
- Scheduled appointments are respected
- Fair and transparent prioritization

**Formula**: `Emergency (0-50) + Age (0-20) + Symptoms (0-50) + Appointment (0-5) = Score (0-100)`
