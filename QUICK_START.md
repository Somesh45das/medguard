# 🚀 Quick Start Guide

## Start the Server

```bash
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Run the application
python run.py
```

## Access the Portals

### 👥 For Patients
**URL:** http://127.0.0.1:5000/patient

**What you can do:**
- Book appointments online
- Get instant SMS confirmation
- Check appointment status
- No login needed!

### 🏥 For Hospital Staff
**URL:** http://127.0.0.1:5000/management

**Login:**
- Username: `admin`
- Password: `admin123`

**What you can do:**
- View dashboard with real-time stats
- Manage appointments (with SMS)
- Control queue with priority
- Monitor doctors and capacity
- View ML-powered predictions

## Test SMS Feature

When you book an appointment, check the **console/terminal** where the server is running. You'll see the SMS message that would be sent to the patient's phone:

```
============================================================
📱 SMS SENT TO: +91-9876543210
============================================================
🏥 SmartCare Hospital - Appointment Confirmed

Dear John Doe,

Your appointment has been booked successfully!

📅 Date: Monday, February 24, 2026
⏰ Time: 10:00 AM
👨‍⚕️ Doctor: Dr. Aisha Sharma
...
============================================================
```

## Key URLs

| Portal | URL | Access |
|--------|-----|--------|
| Patient Home | http://127.0.0.1:5000/patient | Public |
| Book Appointment | http://127.0.0.1:5000/patient/book | Public |
| Check Status | http://127.0.0.1:5000/patient/check-status | Public |
| Management Login | http://127.0.0.1:5000/management | Login Required |
| Admin Dashboard | http://127.0.0.1:5000/admin | After Login |
| Appointments | http://127.0.0.1:5000/admin/appointments | After Login |
| Queue | http://127.0.0.1:5000/admin/queue | After Login |
| Doctors | http://127.0.0.1:5000/admin/doctors | After Login |

## Features to Test

### Patient Portal:
1. ✅ Book an appointment with your phone number
2. ✅ See SMS confirmation in console
3. ✅ Check appointment status using phone number
4. ✅ View smart slot recommendations

### Management Portal:
1. ✅ Login with admin/admin123
2. ✅ View real-time dashboard
3. ✅ See ML crowd predictions
4. ✅ Manage queue with priority
5. ✅ Book appointments (SMS sent automatically)
6. ✅ Monitor doctor availability

## Need Help?

- Check `DUAL_PORTAL_GUIDE.md` for detailed documentation
- SMS messages appear in the console (not sent to real phones by default)
- To enable real SMS, see SMS Integration section in the guide

**Enjoy your Smart Hospital System!** 🎉
