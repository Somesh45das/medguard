# 🏥 Smart Hospital Queue & Appointment Optimizer

A full-stack Python project with **dual-portal architecture**, ML-based crowd prediction, real-time queue management, and **SMS notifications**.

## 🌟 New Features

### Two Separate Portals:
1. **Patient Portal** - User-friendly interface for patients to book appointments and receive SMS confirmations
2. **Management Portal** - Comprehensive dashboard for hospital staff with full control

### SMS Notifications:
- Automatic SMS confirmation on appointment booking
- Includes all appointment details (date, time, doctor, location)
- Phone number-based status checking

## Features

- **ML-Powered Crowd Prediction**: Random Forest classifier predicts OPD crowd levels (100% accuracy on training data)
- **Smart Slot Optimization**: Recommends best appointment times based on crowd predictions
- **Real-Time Queue Management**: Priority-based queue with token generation and wait time estimation
- **Dual Portal System**: Separate interfaces for patients and staff
- **SMS Notifications**: Instant appointment confirmations via SMS
- **Interactive Dashboard**: Live stats, crowd levels, and prediction charts
- **Priority Scoring**: Age, emergency status, and symptom-based patient prioritization

## Quick Start

### 1. Setup Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python run.py
```

This will:
1. Train the ML model (first run only)
2. Seed the database with sample data (first run only)
3. Start the Flask server at http://127.0.0.1:5000

### 3. Access the Portals

**Patient Portal (Public):**
```
http://127.0.0.1:5000/patient
```
- Book appointments
- Receive SMS confirmations
- Check appointment status

**Management Portal (Staff):**
```
http://127.0.0.1:5000/management
```
- Login: `admin` / `admin123`
- Full dashboard and controls
- Queue management
- Analytics

## Portal Comparison

| Feature | Patient Portal | Management Portal |
|---------|---------------|-------------------|
| Access | Public | Login Required |
| Booking | Self-service | Can book for anyone |
| SMS | Auto-sent | Auto-sent + manual |
| Queue | View only | Full control |
| Analytics | None | Full dashboard |
| Priority | System-assigned | Can override |

## SMS Integration

Currently simulated (prints to console). To enable real SMS:

1. Sign up for Twilio/AWS SNS
2. Update `app/services/sms_service.py`
3. Add credentials to environment

See `DUAL_PORTAL_GUIDE.md` for detailed SMS setup instructions.

## Project Structure

```
smart_hospital_queue/
├── app/
│   ├── routes/
│   │   ├── patient_portal.py    # Patient-facing routes
│   │   ├── management_portal.py # Staff authentication
│   │   ├── dashboard.py          # Admin dashboard
│   │   ├── appointments.py       # Appointment management
│   │   ├── queue_routes.py       # Queue management
│   │   └── doctors.py            # Doctor management
│   ├── services/
│   │   ├── sms_service.py        # SMS notifications
│   │   ├── crowd_predictor.py    # ML predictions
│   │   ├── slot_optimizer.py     # Slot recommendations
│   │   └── queue_manager.py      # Queue operations
│   ├── templates/
│   │   ├── patient/              # Patient portal templates
│   │   ├── management/           # Management templates
│   │   └── ...                   # Admin templates
│   └── ...
├── DUAL_PORTAL_GUIDE.md          # Detailed portal guide
└── ...
```

## Technologies Used

- **Backend**: Flask, SQLAlchemy
- **ML**: scikit-learn, pandas, numpy
- **Frontend**: Bootstrap 5, Chart.js
- **Database**: SQLite
- **SMS**: Twilio-ready (simulated by default)

## Documentation

- `README.md` - This file (quick start)
- `DUAL_PORTAL_GUIDE.md` - Comprehensive dual-portal guide
- SMS setup instructions
- Workflow examples

## License

MIT License - Feel free to use this project for learning and development.
