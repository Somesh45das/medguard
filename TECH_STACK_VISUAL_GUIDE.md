# Tech Stack Visual Guide

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                          USER INTERFACE                              │
│  ┌──────────────────┐              ┌──────────────────┐            │
│  │  Patient Portal  │              │   Admin Portal   │            │
│  │  - Book Appt     │              │  - Queue Mgmt    │            │
│  │  - View History  │              │  - Appointments  │            │
│  │  - Check Status  │              │  - Doctors       │            │
│  └──────────────────┘              └──────────────────┘            │
│         │                                    │                       │
│         └────────────────┬───────────────────┘                      │
│                          │                                           │
│                    ┌─────▼─────┐                                    │
│                    │  Chatbot  │                                    │
│                    │  Widget   │                                    │
│                    └───────────┘                                    │
└─────────────────────────────────────────────────────────────────────┘
                             │
                             │ HTTP Requests
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      FLASK WEB FRAMEWORK                             │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                    ROUTES (Blueprints)                        │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │  │
│  │  │   Auth   │ │ Patient  │ │  Queue   │ │   API    │       │  │
│  │  │  Routes  │ │  Routes  │ │  Routes  │ │  Routes  │       │  │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                             │                                        │
│                             ▼                                        │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                   BUSINESS LOGIC (Services)                   │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │  │
│  │  │Queue Manager │  │Priority Score│  │Slot Optimizer│      │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘      │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │  │
│  │  │SMS Service   │  │Chatbot       │  │Auth Service  │      │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘      │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                             │                                        │
│                    ┌────────┴────────┐                              │
│                    │                 │                              │
│                    ▼                 ▼                              │
│  ┌──────────────────────┐  ┌──────────────────────┐               │
│  │   ML PREDICTIONS     │  │   DATABASE ACCESS    │               │
│  │  ┌────────────────┐  │  │  ┌────────────────┐ │               │
│  │  │Crowd Predictor │  │  │  │  SQLAlchemy    │ │               │
│  │  │(Random Forest) │  │  │  │     ORM        │ │               │
│  │  └────────────────┘  │  │  └────────────────┘ │               │
│  │  ┌────────────────┐  │  │  ┌────────────────┐ │               │
│  │  │NoShow Predictor│  │  │  │    Models      │ │               │
│  │  │(Random Forest) │  │  │  │  (Tables)      │ │               │
│  │  └────────────────┘  │  │  └────────────────┘ │               │
│  └──────────────────────┘  └──────────────────────┘               │
└─────────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                          DATABASE                                    │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐              │
│  │Patients  │ │Doctors   │ │Appoint-  │ │  Queue   │              │
│  │          │ │          │ │  ments   │ │ Entries  │              │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘              │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐                           │
│  │Depart-   │ │  Users   │ │  Crowd   │                           │
│  │ ments    │ │          │ │   Logs   │                           │
│  └──────────┘ └──────────┘ └──────────┘                           │
│                                                                      │
│  SQLite (Development) / PostgreSQL (Production)                     │
└─────────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    EXTERNAL SERVICES                                 │
│  ┌──────────────────┐              ┌──────────────────┐            │
│  │  Twilio SMS API  │              │  Email Service   │            │
│  │  (Optional)      │              │  (Future)        │            │
│  └──────────────────┘              └──────────────────┘            │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Technology Stack Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │    HTML5    │  │ Bootstrap 5 │  │ JavaScript  │        │
│  │   Jinja2    │  │     CSS     │  │   jQuery    │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                   APPLICATION LAYER                          │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Flask 2.3.0                             │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐         │   │
│  │  │Blueprints│  │ Sessions │  │  Cookies │         │   │
│  │  └──────────┘  └──────────┘  └──────────┘         │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │           Flask-Login (Authentication)               │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                   BUSINESS LOGIC LAYER                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Python 3.10 Services                    │   │
│  │  ┌──────────────────┐  ┌──────────────────┐        │   │
│  │  │ Queue Management │  │ Priority Scoring │        │   │
│  │  └──────────────────┘  └──────────────────┘        │   │
│  │  ┌──────────────────┐  ┌──────────────────┐        │   │
│  │  │ Slot Optimization│  │  SMS Notifications│        │   │
│  │  └──────────────────┘  └──────────────────┘        │   │
│  │  ┌──────────────────┐  ┌──────────────────┐        │   │
│  │  │ Chatbot Service  │  │  Auth Service    │        │   │
│  │  └──────────────────┘  └──────────────────┘        │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                  MACHINE LEARNING LAYER                      │
│  ┌─────────────────────────────────────────────────────┐   │
│  │            Scikit-learn 1.3.0                        │   │
│  │  ┌──────────────────┐  ┌──────────────────┐        │   │
│  │  │ Random Forest    │  │ Random Forest    │        │   │
│  │  │ Crowd Predictor  │  │ NoShow Predictor │        │   │
│  │  │  (85% accuracy)  │  │ (87.3% accuracy) │        │   │
│  │  └──────────────────┘  └──────────────────┘        │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │         Pandas + NumPy (Data Processing)             │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                   DATA ACCESS LAYER                          │
│  ┌─────────────────────────────────────────────────────┐   │
│  │            SQLAlchemy 2.0 (ORM)                      │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐         │   │
│  │  │  Models  │  │ Queries  │  │Relations │         │   │
│  │  └──────────┘  └──────────┘  └──────────┘         │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                      DATABASE LAYER                          │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  SQLite (Development) / PostgreSQL (Production)      │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐         │   │
│  │  │  Tables  │  │  Indexes │  │ Relations│         │   │
│  │  └──────────┘  └──────────┘  └──────────┘         │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## Data Flow Diagram

```
┌──────────┐
│  Patient │
└────┬─────┘
     │ 1. Books Appointment
     ▼
┌─────────────────┐
│  Flask Route    │
│  /patient/book  │
└────┬────────────┘
     │ 2. Validates Input
     ▼
┌─────────────────────┐
│  Priority Scorer    │ ◄─── Patient Age, Symptoms
│  Calculates Score   │
└────┬────────────────┘
     │ 3. Priority = 45
     ▼
┌─────────────────────┐
│  Slot Optimizer     │ ◄─── Date, Doctor
│  Finds Best Slots   │
└────┬────────────────┘
     │ 4. Checks ML Model
     ▼
┌─────────────────────┐
│  Crowd Predictor    │ ◄─── Hour, Day, Weather
│  Predicts Crowd     │
└────┬────────────────┘
     │ 5. Crowd = Medium
     ▼
┌─────────────────────┐
│  Conflict Checker   │ ◄─── Existing Appointments
│  Resolves Conflicts │
└────┬────────────────┘
     │ 6. No Conflict
     ▼
┌─────────────────────┐
│  Database           │
│  Saves Appointment  │
└────┬────────────────┘
     │ 7. Appointment Created
     ▼
┌─────────────────────┐
│  SMS Service        │ ◄─── Patient Phone
│  Sends Confirmation │
└────┬────────────────┘
     │ 8. SMS Sent
     ▼
┌─────────────────────┐
│  Queue Manager      │ ◄─── If Today
│  Adds to Queue      │
└────┬────────────────┘
     │ 9. Token Generated
     ▼
┌──────────┐
│  Patient │ ◄─── Confirmation Page + SMS
└──────────┘
```

---

## Machine Learning Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                    TRAINING PHASE                            │
│                                                              │
│  ┌──────────────┐                                           │
│  │  CSV Dataset │                                           │
│  │  (Historical)│                                           │
│  └──────┬───────┘                                           │
│         │                                                    │
│         ▼                                                    │
│  ┌──────────────────┐                                       │
│  │  Pandas          │                                       │
│  │  Load & Clean    │                                       │
│  └──────┬───────────┘                                       │
│         │                                                    │
│         ▼                                                    │
│  ┌──────────────────┐                                       │
│  │  Feature         │                                       │
│  │  Engineering     │                                       │
│  └──────┬───────────┘                                       │
│         │                                                    │
│         ▼                                                    │
│  ┌──────────────────┐                                       │
│  │  Train/Test      │                                       │
│  │  Split (80/20)   │                                       │
│  └──────┬───────────┘                                       │
│         │                                                    │
│         ▼                                                    │
│  ┌──────────────────┐                                       │
│  │  Random Forest   │                                       │
│  │  Training        │                                       │
│  └──────┬───────────┘                                       │
│         │                                                    │
│         ▼                                                    │
│  ┌──────────────────┐                                       │
│  │  Model           │                                       │
│  │  Evaluation      │                                       │
│  └──────┬───────────┘                                       │
│         │                                                    │
│         ▼                                                    │
│  ┌──────────────────┐                                       │
│  │  Save Model      │                                       │
│  │  (.pkl file)     │                                       │
│  └──────────────────┘                                       │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   PREDICTION PHASE                           │
│                                                              │
│  ┌──────────────┐                                           │
│  │  User Input  │                                           │
│  │  (Features)  │                                           │
│  └──────┬───────┘                                           │
│         │                                                    │
│         ▼                                                    │
│  ┌──────────────────┐                                       │
│  │  Load Model      │                                       │
│  │  (.pkl file)     │                                       │
│  └──────┬───────────┘                                       │
│         │                                                    │
│         ▼                                                    │
│  ┌──────────────────┐                                       │
│  │  Preprocess      │                                       │
│  │  Features        │                                       │
│  └──────┬───────────┘                                       │
│         │                                                    │
│         ▼                                                    │
│  ┌──────────────────┐                                       │
│  │  Model.predict() │                                       │
│  │  Get Prediction  │                                       │
│  └──────┬───────────┘                                       │
│         │                                                    │
│         ▼                                                    │
│  ┌──────────────────┐                                       │
│  │  Return Result   │                                       │
│  │  to Application  │                                       │
│  └──────────────────┘                                       │
└─────────────────────────────────────────────────────────────┘
```

---

## Request-Response Cycle

```
┌─────────┐
│ Browser │
└────┬────┘
     │ HTTP GET /patient/book
     ▼
┌─────────────────┐
│  Flask Server   │
│  Port 5000      │
└────┬────────────┘
     │ Route to patient_portal.book()
     ▼
┌─────────────────┐
│  Route Handler  │
│  @app.route()   │
└────┬────────────┘
     │ Check Authentication
     ▼
┌─────────────────┐
│  Auth Service   │
│  @user_required │
└────┬────────────┘
     │ User Authenticated ✓
     ▼
┌─────────────────┐
│  Business Logic │
│  Get Departments│
│  Get Doctors    │
│  Get Slots      │
└────┬────────────┘
     │ Query Database
     ▼
┌─────────────────┐
│  SQLAlchemy     │
│  ORM Queries    │
└────┬────────────┘
     │ Return Data
     ▼
┌─────────────────┐
│  Jinja2 Engine  │
│  Render Template│
└────┬────────────┘
     │ HTML Generated
     ▼
┌─────────────────┐
│  Flask Response │
│  Send HTML      │
└────┬────────────┘
     │ HTTP Response
     ▼
┌─────────┐
│ Browser │ ◄─── Displays Page
└─────────┘
```

---

## File Structure Visual

```
smart-hospital-queue/
│
├── 📁 app/                      # Main application
│   ├── 📄 __init__.py          # App factory
│   │
│   ├── 📁 models/              # Database models
│   │   ├── 📄 models.py        # Patient, Appointment, Queue
│   │   └── 📄 user.py          # User authentication
│   │
│   ├── 📁 routes/              # URL routes
│   │   ├── 📄 auth.py          # Login/Register
│   │   ├── 📄 patient_portal.py # Patient features
│   │   ├── 📄 queue_routes.py  # Queue management
│   │   └── 📄 api.py           # REST API
│   │
│   ├── 📁 services/            # Business logic
│   │   ├── 📄 queue_manager.py # Queue operations
│   │   ├── 📄 priority_scorer.py # Priority calc
│   │   ├── 📄 crowd_predictor.py # ML predictions
│   │   └── 📄 sms_service.py   # SMS notifications
│   │
│   ├── 📁 ml/                  # Machine Learning
│   │   ├── 📄 train_model.py   # Train crowd model
│   │   ├── 📄 crowd_model.pkl  # Trained model
│   │   └── 📁 models/          # No-show models
│   │
│   ├── 📁 templates/           # HTML templates
│   │   ├── 📄 base.html        # Base template
│   │   ├── 📁 patient/         # Patient pages
│   │   └── 📁 admin/           # Admin pages
│   │
│   └── 📁 static/              # Static files
│       ├── 📁 css/             # Stylesheets
│       └── 📁 js/              # JavaScript
│
├── 📁 instance/                # Instance files
│   └── 📄 hospital.db          # SQLite database
│
├── 📄 config.py                # Configuration
├── 📄 run.py                   # Entry point
├── 📄 seed_data.py             # Initialize DB
└── 📄 requirements.txt         # Dependencies
```

---

This visual guide helps understand the complete architecture and data flow of the Smart Hospital Queue & Appointment Optimizer system!
