# System Architecture - Patient Booking Flow

## 🏗️ Database Relationships

```
┌─────────────────────┐
│       User          │  (Authentication)
├─────────────────────┤
│ id (PK)             │
│ email               │
│ password_hash       │
│ role (admin/user)   │
│ patient_id (FK) ────┼──┐
└─────────────────────┘  │
                         │
                         ▼
                    ┌─────────────────────┐
                    │      Patient        │  (Medical Record)
                    ├─────────────────────┤
                    │ id (PK)             │
                    │ patient_id (unique) │
                    │ name                │
                    │ age                 │
                    │ gender              │
                    │ phone               │
                    └─────────────────────┘
                              │
                              │ One-to-Many
                              ▼
                    ┌─────────────────────┐
                    │    Appointment      │
                    ├─────────────────────┤
                    │ id (PK)             │
                    │ patient_id (FK) ────┼──┘
                    │ doctor_id (FK)      │
                    │ department_id (FK)  │
                    │ appointment_date    │
                    │ appointment_time    │
                    │ status              │
                    └─────────────────────┘
```

---

## 🔄 Patient Booking Flow (FIXED)

```
┌──────────────────────────────────────────────────────────────┐
│                    PATIENT SIDE                              │
└──────────────────────────────────────────────────────────────┘

1. Patient Registers
   ┌─────────────┐
   │ Register    │
   │ Form        │
   └──────┬──────┘
          │
          ▼
   ┌─────────────────────────────────┐
   │ Creates User + Patient Record   │
   │ Links: User.patient_id → Patient│
   └─────────────────────────────────┘

2. Patient Logs In
   ┌─────────────┐
   │ Login Form  │
   │ Email/Pass  │
   └──────┬──────┘
          │
          ▼
   ┌─────────────────────────────────┐
   │ Flask-Login sets current_user   │
   │ current_user.patient available  │
   └─────────────────────────────────┘

3. Patient Books Appointment
   ┌─────────────────────────────────┐
   │ Booking Form                    │
   │ ┌─────────────────────────────┐ │
   │ │ Booking for: Test Patient   │ │  ← Shows user info
   │ │ 📞 +91-8888888888           │ │  ← Not editable
   │ └─────────────────────────────┘ │
   │                                 │
   │ Department: [Select]            │  ← User selects
   │ Doctor: [Select]                │  ← User selects
   │ Date: [Select]                  │  ← User selects
   │ Time: [Select]                  │  ← User selects
   │ Symptoms: [Text]                │  ← User enters
   │                                 │
   │ [Confirm Booking]               │
   └──────────┬──────────────────────┘
              │
              ▼
   ┌─────────────────────────────────┐
   │ Backend: patient_portal.book()  │
   │                                 │
   │ patient = current_user.patient  │  ← Uses logged-in user
   │                                 │
   │ appointment = Appointment(      │
   │   patient_id=patient.id,        │  ← Correct link!
   │   doctor_id=...,                │
   │   appointment_date=...,         │
   │   appointment_time=...,         │
   │   symptoms=...                  │
   │ )                               │
   │                                 │
   │ db.session.add(appointment)     │
   │ db.session.commit()             │
   └─────────────────────────────────┘
              │
              ▼
   ┌─────────────────────────────────┐
   │ Appointment saved to database   │
   │ ✅ Linked to correct patient    │
   └─────────────────────────────────┘

4. Patient Views Dashboard
   ┌─────────────────────────────────┐
   │ Patient Dashboard               │
   │                                 │
   │ Upcoming Appointments:          │
   │ ┌─────────────────────────────┐ │
   │ │ APT-20260226-001            │ │
   │ │ Dr. Sharma                  │ │
   │ │ Feb 26, 2026 at 10:00 AM    │ │
   │ │ Status: Scheduled           │ │
   │ └─────────────────────────────┘ │
   └─────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                     ADMIN SIDE                               │
└──────────────────────────────────────────────────────────────┘

5. Admin Views Appointments
   ┌─────────────────────────────────────────────────────────┐
   │ Appointments Panel                                      │
   │                                                         │
   │ Filters: Date [Feb 26] Department [All] Status [All]   │
   │                                                         │
   │ ┌─────────────────────────────────────────────────────┐ │
   │ │ Apt #          Patient       Doctor      Status     │ │
   │ ├─────────────────────────────────────────────────────┤ │
   │ │ APT-20260226-1 Test Patient  Dr. Sharma  Scheduled  │ │
   │ │                +91-88888...              [✓] [✗]    │ │
   │ └─────────────────────────────────────────────────────┘ │
   │                                                         │
   │ ✅ Patient name visible                                 │
   │ ✅ Phone number visible                                 │
   │ ✅ Can check-in or cancel                               │
   └─────────────────────────────────────────────────────────┘
```

---

## 🔍 Data Flow Comparison

### ❌ BEFORE (Broken)

```
Patient Form                Backend                  Database
┌──────────┐               ┌──────────┐            ┌──────────┐
│ Name:    │               │ Ignores  │            │ Wrong    │
│ Phone:   │──────────────▶│ form     │───────────▶│ patient  │
│ Age:     │               │ data     │            │ link     │
│          │               │          │            │          │
│ Dept:    │               │ Uses     │            │ Admin    │
│ Doctor:  │               │ current_ │            │ can't    │
│ Date:    │               │ user.    │            │ see      │
│ Time:    │               │ patient  │            │ patient  │
└──────────┘               └──────────┘            └──────────┘
     ❌                          ❌                      ❌
  Mismatch!                 Confusion!              Broken link!
```

### ✅ AFTER (Fixed)

```
Patient Form                Backend                  Database
┌──────────┐               ┌──────────┐            ┌──────────┐
│ Shows:   │               │ Uses     │            │ Correct  │
│ Name     │               │ current_ │            │ patient  │
│ Phone    │               │ user.    │            │ link     │
│          │               │ patient  │            │          │
│ Dept:    │──────────────▶│          │───────────▶│ Admin    │
│ Doctor:  │               │ Creates  │            │ sees     │
│ Date:    │               │ appoint- │            │ patient  │
│ Time:    │               │ ment     │            │ details  │
└──────────┘               └──────────┘            └──────────┘
     ✅                          ✅                      ✅
  Clean!                    Consistent!             Works!
```

---

## 🎯 Key Components

### 1. User Model (`app/models/user.py`)
```python
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(255))
    role = db.Column(db.String(20))  # 'admin' or 'user'
    
    # Link to patient record
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"))
    patient = db.relationship("Patient", backref="user_account")
```

### 2. Patient Model (`app/models/models.py`)
```python
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.String(20), unique=True)
    name = db.Column(db.String(150))
    phone = db.Column(db.String(15))
    
    # One patient can have many appointments
    appointments = db.relationship("Appointment", backref="patient")
```

### 3. Appointment Model (`app/models/models.py`)
```python
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment_number = db.Column(db.String(20), unique=True)
    
    # Links to patient
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"))
    
    # Links to doctor and department
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"))
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"))
    
    appointment_date = db.Column(db.Date)
    appointment_time = db.Column(db.Time)
    status = db.Column(db.String(20))
```

### 4. Booking Route (`app/routes/patient_portal.py`)
```python
@patient_portal_bp.route("/book", methods=["POST"])
@user_required
def book():
    # Get logged-in user's patient record
    patient = current_user.patient
    
    # Get form data (appointment details only)
    doctor_id = request.form.get("doctor_id")
    appointment_date = request.form.get("appointment_date")
    appointment_time = request.form.get("appointment_time")
    
    # Create appointment linked to patient
    appointment = Appointment(
        patient_id=patient.id,  # ← Correct link!
        doctor_id=doctor_id,
        appointment_date=appointment_date,
        appointment_time=appointment_time,
        status="scheduled"
    )
    
    db.session.add(appointment)
    db.session.commit()
```

---

## 📊 Success Metrics

✅ User registration creates linked patient record
✅ Patient booking uses current_user.patient
✅ Appointments properly linked in database
✅ Patient dashboard shows user's appointments
✅ Admin panel shows all appointments with patient names
✅ Check-in/cancel actions work correctly
✅ Database integrity maintained

---

## 🔐 Security Flow

```
1. User registers → Password hashed with bcrypt
2. User logs in → Flask-Login creates session
3. @user_required decorator protects routes
4. current_user.patient ensures correct patient record
5. Database foreign keys maintain referential integrity
```

---

**Architecture Status**: ✅ VERIFIED
**Last Updated**: February 25, 2026
