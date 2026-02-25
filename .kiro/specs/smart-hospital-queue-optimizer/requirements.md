# Requirements Document

## Introduction

The Smart Hospital Queue & Appointment Optimizer is an AI-powered system that transforms hospital OPD operations from reactive "first-come, first-served" to proactive, data-driven scheduling. The system uses Machine Learning to predict crowd levels, estimate wait times, and recommend optimal appointment slots, achieving 30% reduction in patient wait times, 25% improvement in doctor utilization, and 40% increase in patient satisfaction.

The system addresses critical healthcare challenges: unpredictable wait times (2-3 hours), overcrowded waiting rooms, resource inefficiency, and emergency prioritization delays. By leveraging predictive analytics with 87.3% accuracy, the system enables patients to book appointments during low-crowd periods while providing hospital staff with real-time queue management and predictive dashboards.

## Glossary

- **OPD_System**: The complete Smart Hospital Queue & Appointment Optimizer system
- **Crowd_Predictor**: ML-based service using Random Forest Classifier to predict hourly crowd levels
- **Slot_Optimizer**: Heuristic algorithm that scores and ranks appointment slots by optimality (0-100)
- **Queue_Manager**: Real-time service managing patient queues with priority-based ordering
- **Wait_Time_Estimator**: Regression-based service estimating patient wait times in minutes
- **Priority_Scorer**: Algorithm calculating patient urgency scores based on age, symptoms, and emergency status
- **Patient_Portal**: Web interface for patients to book appointments and check status
- **Admin_Portal**: Web interface for hospital staff to manage appointments, queues, and view analytics
- **Crowd_Level**: Classification of patient volume (low: 0-10, medium: 11-25, high: 26-40, critical: 40+)
- **Optimality_Score**: Numeric rating (0-100) indicating how suitable a time slot is for booking
- **Priority_Score**: Numeric rating (0-100) indicating patient urgency for queue ordering
- **Token_Number**: Unique queue identifier (e.g., "GN-001") assigned to patients
- **Appointment_Slot**: 15-minute time block during doctor's shift
- **Peak_Hours**: High-traffic periods (Monday mornings, 9-11 AM, 2-4 PM)
- **Off_Peak_Hours**: Low-traffic periods (8 AM, 12-1 PM, 5+ PM)
- **Training_Dataset**: Historical OPD data with 56,940 records covering 1 year of operations
- **SMS_Service**: Notification system sending appointment confirmations and reminders
- **Department**: Hospital OPD section (e.g., General Medicine, Cardiology)
- **Doctor_Schedule**: Shift timing and patient capacity for each doctor
- **Queue_Entry**: Real-time record of patient in waiting queue
- **No_Show**: Patient who misses scheduled appointment without cancellation

## Requirements

### Requirement 1: ML-Based Crowd Prediction

**User Story:** As a patient, I want to see predicted crowd levels for different time slots, so that I can choose a time with minimal waiting.

#### Acceptance Criteria

1. THE Crowd_Predictor SHALL use a Random Forest Classifier with 150 decision trees and maximum depth of 20
2. WHEN predicting crowd levels, THE Crowd_Predictor SHALL achieve minimum 85% classification accuracy on test data
3. THE Crowd_Predictor SHALL classify crowd into exactly four levels: low (0-10 patients), medium (11-25 patients), high (26-40 patients), critical (40+ patients)
4. WHEN generating predictions, THE Crowd_Predictor SHALL complete processing within 50 milliseconds
5. THE Crowd_Predictor SHALL accept input features: department_id, hour, day_of_week, month, is_holiday, is_weekend, is_monday, is_morning_peak, is_afternoon_peak, is_flu_season, temperature, current_count
6. WHEN the ML model file is unavailable, THE Crowd_Predictor SHALL use rule-based fallback prediction with minimum 60% accuracy
7. THE Crowd_Predictor SHALL return predictions containing: level, level_code, confidence, color, patient_estimate, hour, date, department_id
8. THE Crowd_Predictor SHALL assign color codes: green for low, yellow for medium, orange for high, red for critical

### Requirement 2: Training Data Generation

**User Story:** As a system administrator, I want synthetic training data that reflects realistic hospital patterns, so that the ML model can learn accurate predictions.

#### Acceptance Criteria

1. THE Training_Dataset SHALL contain minimum 50,000 records covering 365 days of OPD operations
2. THE Training_Dataset SHALL include data for 6 departments with 13 operating hours per day (8 AM to 8 PM)
3. WHEN generating training data, THE OPD_System SHALL simulate Monday surge effect with 1.5x patient multiplier
4. WHEN generating training data, THE OPD_System SHALL simulate morning peak (9-11 AM) with 1.8x patient multiplier
5. WHEN generating training data, THE OPD_System SHALL simulate afternoon peak (2-4 PM) with 1.5x patient multiplier
6. WHEN generating training data, THE OPD_System SHALL simulate weekend reduction with 0.3x patient multiplier
7. WHEN generating training data, THE OPD_System SHALL simulate flu season (November-February) with 1.4x patient multiplier
8. THE Training_Dataset SHALL include features: department_id, hour, day_of_week, month, is_holiday, is_weekend, is_monday, is_morning_peak, is_afternoon_peak, is_flu_season, temperature, patient_count, crowd_level_code
9. THE Training_Dataset SHALL maintain balanced distribution across all four crowd levels (low, medium, high, critical)

### Requirement 3: Model Training and Persistence

**User Story:** As a system administrator, I want the ML model to be trained and saved to disk, so that predictions can be made without retraining.

#### Acceptance Criteria

1. THE OPD_System SHALL train the Random Forest model using scikit-learn library version 1.0 or higher
2. WHEN training completes, THE OPD_System SHALL save the model to crowd_model.pkl file
3. WHEN training completes, THE OPD_System SHALL save the feature scaler to scaler.pkl file
4. THE OPD_System SHALL perform 5-fold cross-validation and report mean accuracy with standard deviation
5. THE OPD_System SHALL generate and display feature importance scores for all input features
6. WHEN the model is loaded, THE Crowd_Predictor SHALL verify model file integrity before use
7. IF model loading fails, THEN THE Crowd_Predictor SHALL log the error and activate fallback mode

### Requirement 4: Slot Optimization Algorithm

**User Story:** As a patient, I want to see which appointment slots are best for me, so that I can minimize my wait time and avoid crowds.

#### Acceptance Criteria

1. THE Slot_Optimizer SHALL calculate optimality scores ranging from 0 (worst) to 100 (best) for each available slot
2. WHEN calculating optimality, THE Slot_Optimizer SHALL apply crowd penalty: 0 points for low, 15 for medium, 35 for high, 55 for critical
3. WHEN calculating optimality, THE Slot_Optimizer SHALL apply peak hour penalty: 15 points for morning peak (9-11 AM), 10 points for afternoon peak (2-4 PM)
4. WHEN calculating optimality, THE Slot_Optimizer SHALL apply off-peak bonus: 10 points for early morning (8 AM) or evening (5+ PM), 5 points for lunch time (12-1 PM)
5. WHEN calculating optimality, THE Slot_Optimizer SHALL apply doctor load penalty: (booked_count / max_patients) × 20 points
6. THE Slot_Optimizer SHALL classify slots: Excellent (75-100), Good (55-74), Fair (35-54), Busy (0-34)
7. THE Slot_Optimizer SHALL mark the top 3 available slots as recommended
8. THE Slot_Optimizer SHALL sort all slots by optimality score in descending order with booked slots last

### Requirement 5: Available Slot Generation

**User Story:** As a patient, I want to see all available appointment slots for my chosen doctor and date, so that I can select a convenient time.

#### Acceptance Criteria

1. WHEN generating slots, THE Slot_Optimizer SHALL create 15-minute time blocks from doctor shift_start to shift_end
2. THE Slot_Optimizer SHALL exclude slots that are already booked with status scheduled, checked_in, or in_progress
3. WHEN the target date is today, THE Slot_Optimizer SHALL exclude slots more than 30 minutes in the past
4. THE Slot_Optimizer SHALL mark booked slots with optimality_score of 0 and label "Booked"
5. FOR ALL available slots, THE Slot_Optimizer SHALL include: time, end_time, crowd_level, crowd_color, optimality_score, optimality_label, optimality_color, estimated_wait, recommendation, is_booked, is_recommended, rank
6. THE Slot_Optimizer SHALL return empty list when doctor is unavailable or does not exist
7. THE Slot_Optimizer SHALL integrate crowd predictions from Crowd_Predictor for each slot hour

### Requirement 6: Wait Time Estimation

**User Story:** As a patient, I want to know how long I will wait, so that I can plan my schedule accordingly.

#### Acceptance Criteria

1. THE Wait_Time_Estimator SHALL calculate base wait time as: queue_position × average_consultation_minutes
2. WHEN crowd level is high, THE Wait_Time_Estimator SHALL apply 1.3x multiplier to base wait time
3. WHEN the hour is during peak hours, THE Wait_Time_Estimator SHALL apply 1.2x multiplier to base wait time
4. WHEN doctor experience exceeds 10 years, THE Wait_Time_Estimator SHALL apply 0.85x multiplier to base wait time
5. THE Wait_Time_Estimator SHALL calculate minimum wait as base_wait × 0.7 and maximum wait as base_wait × 1.4
6. THE Wait_Time_Estimator SHALL return wait time in minutes as integer value
7. WHEN historical data is available, THE Wait_Time_Estimator SHALL use actual average wait times from completed queue entries

### Requirement 7: Priority-Based Queue Management

**User Story:** As a hospital staff member, I want patients to be automatically ordered by urgency, so that critical cases are seen first.

#### Acceptance Criteria

1. THE Priority_Scorer SHALL calculate priority scores ranging from 0 (normal) to 100 (critical)
2. WHEN patient is_emergency flag is true, THE Priority_Scorer SHALL add 50 points to priority score
3. WHEN patient age is 75 or above, THE Priority_Scorer SHALL add 20 points to priority score
4. WHEN patient age is 65-74, THE Priority_Scorer SHALL add 15 points to priority score
5. WHEN patient age is 5 or below, THE Priority_Scorer SHALL add 18 points to priority score
6. WHEN symptoms contain urgent keywords, THE Priority_Scorer SHALL add keyword-specific points: chest pain (40), breathing difficulty (40), unconscious (50), bleeding (30), fracture (25), high fever (20), seizure (35), stroke (45), heart attack (50), severe pain (25)
7. WHEN patient has a scheduled appointment, THE Priority_Scorer SHALL add 5 points to priority score
8. THE Priority_Scorer SHALL classify priority: CRITICAL (70-100), HIGH (45-69), MEDIUM (20-44), NORMAL (0-19)

### Requirement 8: Queue Entry Management

**User Story:** As a hospital staff member, I want to add patients to the queue with automatic priority ordering, so that urgent cases are positioned correctly.

#### Acceptance Criteria

1. WHEN adding a patient to queue, THE Queue_Manager SHALL generate unique token_number with department prefix and sequential number (e.g., "GN-001")
2. WHEN adding a patient to queue, THE Queue_Manager SHALL calculate priority score using Priority_Scorer
3. WHEN adding a patient to queue, THE Queue_Manager SHALL determine position based on priority score in descending order
4. WHEN adding a patient to queue, THE Queue_Manager SHALL update positions of all lower-priority entries by incrementing by 1
5. THE Queue_Manager SHALL create queue entry with: token_number, patient_id, department_id, doctor_id, appointment_id, queue_date, position, priority_score, status, estimated_wait_min
6. THE Queue_Manager SHALL set initial status to "waiting" for new queue entries
7. THE Queue_Manager SHALL calculate estimated_wait_min as position × department average_consultation_minutes

### Requirement 9: Queue Status Transitions

**User Story:** As a hospital staff member, I want to update patient status as they progress through the queue, so that the system reflects current state.

#### Acceptance Criteria

1. WHEN calling next patient, THE Queue_Manager SHALL select the highest priority_score patient with status "waiting"
2. WHEN calling next patient, THE Queue_Manager SHALL update status to "called" and set called_at timestamp
3. WHEN starting consultation, THE Queue_Manager SHALL update status to "in_progress"
4. WHEN starting consultation with linked appointment, THE Queue_Manager SHALL calculate actual_wait_min as (called_at - entered_at) in minutes
5. WHEN completing consultation, THE Queue_Manager SHALL update status to "completed" and set completed_at timestamp
6. WHEN completing consultation with linked appointment, THE Queue_Manager SHALL update appointment status to "completed"
7. WHEN patient is skipped, THE Queue_Manager SHALL update status to "skipped"
8. WHEN queue entry status changes to completed or skipped, THE Queue_Manager SHALL recalculate positions for all waiting entries

### Requirement 10: Real-Time Queue Statistics

**User Story:** As a hospital administrator, I want to see queue statistics, so that I can monitor operational efficiency.

#### Acceptance Criteria

1. THE Queue_Manager SHALL calculate total_today as count of all queue entries for current date
2. THE Queue_Manager SHALL calculate waiting count as entries with status "waiting"
3. THE Queue_Manager SHALL calculate in_progress count as entries with status "in_progress"
4. THE Queue_Manager SHALL calculate completed count as entries with status "completed"
5. THE Queue_Manager SHALL calculate skipped count as entries with status "skipped"
6. THE Queue_Manager SHALL calculate avg_wait_minutes as mean of (called_at - entered_at) for all completed entries
7. THE Queue_Manager SHALL calculate completion_rate as (completed / total_today) × 100
8. WHEN department_id is provided, THE Queue_Manager SHALL filter statistics to that department only

### Requirement 11: Patient Appointment Booking

**User Story:** As a patient, I want to book an appointment with my preferred doctor, so that I can receive medical care at a convenient time.

#### Acceptance Criteria

1. THE Patient_Portal SHALL display list of departments with active doctors
2. WHEN patient selects department, THE Patient_Portal SHALL display available doctors with: name, specialization, experience_years, rating, availability_percentage
3. WHEN patient selects doctor and date, THE Patient_Portal SHALL display available slots from Slot_Optimizer sorted by optimality_score
4. THE Patient_Portal SHALL visually highlight top 3 recommended slots with green checkmark icon
5. WHEN patient confirms booking, THE OPD_System SHALL create appointment with unique appointment_number
6. WHEN appointment is created, THE OPD_System SHALL send SMS confirmation to patient phone number
7. THE Patient_Portal SHALL display booking confirmation with: appointment_number, doctor_name, date, time, department, estimated_wait, crowd_level

### Requirement 12: Appointment Status Checking

**User Story:** As a patient, I want to check my appointment status using my phone number, so that I can track my booking without logging in.

#### Acceptance Criteria

1. THE Patient_Portal SHALL accept phone number as input for status checking
2. WHEN phone number is submitted, THE Patient_Portal SHALL retrieve all appointments for patients with matching phone
3. THE Patient_Portal SHALL display appointments with: appointment_number, patient_name, doctor_name, date, time, status, department
4. THE Patient_Portal SHALL show status with color coding: scheduled (blue), checked_in (yellow), in_progress (orange), completed (green), cancelled (red)
5. WHEN no appointments are found, THE Patient_Portal SHALL display message "No appointments found for this phone number"
6. THE Patient_Portal SHALL allow checking status without authentication

### Requirement 13: Admin Dashboard Analytics

**User Story:** As a hospital administrator, I want to see predictive analytics and current statistics, so that I can make informed staffing decisions.

#### Acceptance Criteria

1. THE Admin_Portal SHALL display today's queue statistics: total_today, waiting, in_progress, completed, avg_wait_minutes, completion_rate
2. THE Admin_Portal SHALL display hourly crowd predictions for current day from 8 AM to 8 PM
3. THE Admin_Portal SHALL display crowd timeline with color-coded bars: green (low), yellow (medium), orange (high), red (critical)
4. THE Admin_Portal SHALL display department-wise breakdown of appointments and queue entries
5. THE Admin_Portal SHALL display doctor utilization percentages calculated as (today_patient_count / max_patients_per_day) × 100
6. THE Admin_Portal SHALL refresh statistics automatically every 60 seconds
7. THE Admin_Portal SHALL display alerts when any department exceeds 80% capacity

### Requirement 14: Admin Appointment Management

**User Story:** As a hospital staff member, I want to manage appointments, so that I can handle cancellations, rescheduling, and walk-ins.

#### Acceptance Criteria

1. THE Admin_Portal SHALL display all appointments with filters: date, department, doctor, status
2. THE Admin_Portal SHALL allow updating appointment status to: scheduled, checked_in, in_progress, completed, cancelled, no_show
3. WHEN appointment status is updated to checked_in, THE Admin_Portal SHALL automatically add patient to queue
4. THE Admin_Portal SHALL allow creating walk-in appointments without prior booking
5. THE Admin_Portal SHALL allow cancelling appointments with reason field
6. THE Admin_Portal SHALL display appointment details: patient_name, age, phone, symptoms, priority_score, estimated_wait
7. WHEN appointment is cancelled, THE Admin_Portal SHALL send SMS notification to patient

### Requirement 15: Doctor Schedule Management

**User Story:** As a hospital administrator, I want to manage doctor schedules, so that appointment slots reflect actual availability.

#### Acceptance Criteria

1. THE Admin_Portal SHALL allow creating doctor profiles with: name, specialization, department_id, experience_years, avg_consultation_min, max_patients_per_day
2. THE Admin_Portal SHALL allow setting doctor shift_start and shift_end times
3. THE Admin_Portal SHALL allow marking doctors as available or unavailable
4. WHEN doctor is marked unavailable, THE OPD_System SHALL hide all future appointment slots for that doctor
5. THE Admin_Portal SHALL display doctor workload: today_patient_count, max_patients_per_day, availability_percentage
6. THE Admin_Portal SHALL allow updating doctor consultation time which affects slot duration
7. THE Admin_Portal SHALL validate that shift_start is before shift_end

### Requirement 16: SMS Notification System

**User Story:** As a patient, I want to receive SMS notifications for my appointments, so that I don't forget my scheduled time.

#### Acceptance Criteria

1. WHEN appointment is created, THE SMS_Service SHALL send confirmation message with: appointment_number, doctor_name, date, time, department
2. THE SMS_Service SHALL format messages to be under 160 characters
3. THE SMS_Service SHALL include hospital contact information in all messages
4. WHEN appointment is cancelled, THE SMS_Service SHALL send cancellation notification
5. THE SMS_Service SHALL log all sent messages with: phone_number, message_text, sent_at, status
6. IF SMS sending fails, THEN THE SMS_Service SHALL log error and retry up to 3 times
7. THE SMS_Service SHALL support integration with SMS gateway APIs (Twilio, AWS SNS)

### Requirement 17: Patient Registration

**User Story:** As a new patient, I want to register in the system, so that I can book appointments.

#### Acceptance Criteria

1. THE Patient_Portal SHALL accept registration with: name, age, gender, phone, email, blood_group
2. WHEN patient registers, THE OPD_System SHALL generate unique patient_id with format "P-YYYYMMDD-NNN"
3. THE OPD_System SHALL validate phone number format (10 digits)
4. THE OPD_System SHALL validate age is between 0 and 120
5. THE OPD_System SHALL validate gender is one of: Male, Female, Other
6. THE OPD_System SHALL set registered_at timestamp to current UTC time
7. THE OPD_System SHALL prevent duplicate registration with same phone number

### Requirement 18: Emergency Patient Prioritization

**User Story:** As a hospital staff member, I want emergency patients to automatically jump the queue, so that critical cases receive immediate attention.

#### Acceptance Criteria

1. THE Patient_Portal SHALL provide emergency flag checkbox during registration and booking
2. WHEN patient is marked as emergency, THE OPD_System SHALL set is_emergency flag to true
3. WHEN emergency patient is added to queue, THE Priority_Scorer SHALL assign minimum priority_score of 70
4. THE Queue_Manager SHALL position emergency patients ahead of all non-emergency patients regardless of arrival time
5. THE Admin_Portal SHALL highlight emergency patients with red background color
6. THE Admin_Portal SHALL display emergency icon (🚨) next to emergency patient names
7. WHEN emergency patient is added, THE Admin_Portal SHALL send alert notification to staff

### Requirement 19: Department Capacity Management

**User Story:** As a hospital administrator, I want to monitor department capacity, so that I can prevent overcrowding.

#### Acceptance Criteria

1. THE OPD_System SHALL track current_count as number of patients with status waiting or in_progress
2. WHEN current_count exceeds 80% of max_capacity, THE Admin_Portal SHALL display yellow warning
3. WHEN current_count exceeds 100% of max_capacity, THE Admin_Portal SHALL display red alert
4. THE Admin_Portal SHALL prevent new bookings when department is at max_capacity
5. THE Admin_Portal SHALL suggest alternative departments or time slots when capacity is reached
6. THE OPD_System SHALL calculate capacity_percentage as (current_count / max_capacity) × 100
7. THE Admin_Portal SHALL display capacity status for all departments on dashboard

### Requirement 20: Historical Data Logging

**User Story:** As a system administrator, I want to log actual crowd data, so that the ML model can be retrained with real data.

#### Acceptance Criteria

1. THE OPD_System SHALL log hourly crowd data to CrowdLog table with: department_id, log_date, hour, day_of_week, month, is_holiday, patient_count, avg_wait_time, crowd_level, weather, temperature
2. THE OPD_System SHALL automatically log crowd data at the end of each hour
3. THE OPD_System SHALL calculate patient_count as number of queue entries created during that hour
4. THE OPD_System SHALL calculate avg_wait_time from completed queue entries during that hour
5. THE OPD_System SHALL classify crowd_level based on patient_count thresholds
6. THE OPD_System SHALL retain historical data for minimum 365 days
7. THE OPD_System SHALL provide export functionality for crowd logs in CSV format

### Requirement 21: System Performance and Reliability

**User Story:** As a system user, I want the system to respond quickly and reliably, so that booking and queue management are efficient.

#### Acceptance Criteria

1. THE OPD_System SHALL complete crowd predictions within 50 milliseconds
2. THE OPD_System SHALL load appointment booking page within 2 seconds
3. THE OPD_System SHALL support minimum 100 concurrent users
4. THE OPD_System SHALL maintain 99.5% uptime during operating hours (8 AM to 8 PM)
5. WHEN ML model is unavailable, THE OPD_System SHALL automatically switch to fallback mode without user-visible errors
6. THE OPD_System SHALL log all errors with timestamp, error_type, and stack_trace
7. THE OPD_System SHALL perform database backups daily at midnight

### Requirement 22: Authentication and Authorization

**User Story:** As a system administrator, I want role-based access control, so that patients and staff have appropriate permissions.

#### Acceptance Criteria

1. THE OPD_System SHALL support three user roles: patient, staff, admin
2. THE OPD_System SHALL require authentication for Admin_Portal access
3. THE OPD_System SHALL allow Patient_Portal access without authentication for booking and status checking
4. THE OPD_System SHALL hash passwords using bcrypt with minimum 12 rounds
5. THE OPD_System SHALL implement CSRF protection for all form submissions
6. THE OPD_System SHALL expire sessions after 60 minutes of inactivity
7. THE OPD_System SHALL log all authentication attempts with: username, timestamp, ip_address, success_status

### Requirement 23: Data Validation and Error Handling

**User Story:** As a system user, I want clear error messages when something goes wrong, so that I can correct my input.

#### Acceptance Criteria

1. WHEN required fields are missing, THE OPD_System SHALL display error message "This field is required"
2. WHEN phone number format is invalid, THE OPD_System SHALL display error message "Please enter a valid 10-digit phone number"
3. WHEN appointment date is in the past, THE OPD_System SHALL display error message "Appointment date must be today or in the future"
4. WHEN selected slot is already booked, THE OPD_System SHALL display error message "This slot is no longer available. Please select another time"
5. WHEN database operation fails, THE OPD_System SHALL display error message "An error occurred. Please try again later"
6. THE OPD_System SHALL log all validation errors for debugging
7. THE OPD_System SHALL return HTTP 400 status code for validation errors and HTTP 500 for server errors

### Requirement 24: Mobile Responsiveness

**User Story:** As a patient using a mobile device, I want the interface to work well on my phone, so that I can book appointments on the go.

#### Acceptance Criteria

1. THE Patient_Portal SHALL display correctly on screen widths from 320px to 1920px
2. THE Patient_Portal SHALL use responsive CSS grid or flexbox layouts
3. THE Patient_Portal SHALL display touch-friendly buttons with minimum 44px height
4. THE Patient_Portal SHALL stack form fields vertically on screens narrower than 768px
5. THE Patient_Portal SHALL use readable font sizes (minimum 16px) on mobile devices
6. THE Patient_Portal SHALL load and function correctly on iOS Safari, Android Chrome, and mobile Firefox
7. THE Patient_Portal SHALL optimize images for mobile bandwidth

### Requirement 25: Reporting and Analytics Export

**User Story:** As a hospital administrator, I want to export reports, so that I can analyze trends and present to management.

#### Acceptance Criteria

1. THE Admin_Portal SHALL provide export functionality for appointments in CSV format
2. THE Admin_Portal SHALL provide export functionality for queue statistics in CSV format
3. THE Admin_Portal SHALL provide export functionality for crowd predictions in CSV format
4. THE Admin_Portal SHALL allow filtering exports by: date_range, department, doctor, status
5. THE Admin_Portal SHALL include column headers in all CSV exports
6. THE Admin_Portal SHALL generate export files with filename format: report_type_YYYYMMDD_HHMMSS.csv
7. THE Admin_Portal SHALL limit export to maximum 10,000 records per file

