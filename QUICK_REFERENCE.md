# Quick Reference Guide

## 🚀 Getting Started

### Start the Application
```bash
python run.py
```
Visit: http://localhost:5000

### Default Login Credentials
```
Admin:
  Email: admin@hospital.com
  Password: admin123

Patient:
  Register at: /auth/register
```

## 📋 URL Quick Reference

### Public URLs
| URL | Description |
|-----|-------------|
| `/` | Landing page (redirects to login) |
| `/auth/login` | Login page |
| `/auth/register` | Patient registration |
| `/auth/forgot-password` | Password reset request |
| `/patient/` | Patient portal home (public) |

### Admin URLs (Requires Admin Login)
| URL | Description |
|-----|-------------|
| `/admin/` | Admin dashboard |
| `/admin/appointments/` | View/manage appointments |
| `/admin/appointments/book` | Book appointment (admin) |
| `/admin/queue/` | View/manage queue |
| `/admin/doctors/` | View doctors |
| `/admin/manage/doctors` | Manage doctors (CRUD) |
| `/admin/manage/doctors/add` | Add new doctor |
| `/admin/manage/departments` | Manage departments (CRUD) |
| `/admin/manage/departments/add` | Add new department |

### Patient URLs (Requires Patient Login)
| URL | Description |
|-----|-------------|
| `/patient/dashboard` | Patient dashboard |
| `/patient/book` | Book appointment |
| `/patient/confirmation` | Appointment confirmation |
| `/patient/check-status` | Check appointment status |

## 🔐 Security Features

### Authentication
- ✅ Password hashing (bcrypt)
- ✅ Session management (Flask-Login)
- ✅ CSRF protection (Flask-WTF)
- ✅ JWT tokens (for API)

### Access Control
- ✅ Admin-only routes
- ✅ Patient-only routes
- ✅ Automatic role-based redirection
- ✅ Unauthorized access prevention

## 👥 User Roles

### Admin
**Can Access:**
- Dashboard with analytics
- All appointments
- Queue management
- Doctor management (CRUD)
- Department management (CRUD)
- System settings

**Cannot Access:**
- Patient-specific pages

### Patient/User
**Can Access:**
- Personal dashboard
- Book appointments
- View own appointments
- Check appointment status

**Cannot Access:**
- Admin dashboard
- Management features
- Other patients' data

## 🛠️ Common Tasks

### Add a New Doctor (Admin)
1. Login as admin
2. Go to `/admin/manage/doctors`
3. Click "Add New Doctor"
4. Fill form and submit

### Add a New Department (Admin)
1. Login as admin
2. Go to `/admin/manage/departments`
3. Click "Add New Department"
4. Fill form and submit

### Book an Appointment (Patient)
1. Login as patient
2. Go to `/patient/book`
3. Select department, doctor, date, time
4. Fill patient details
5. Submit and receive SMS confirmation

### Check Appointment Status (Patient)
1. Go to `/patient/check-status`
2. Enter phone number
3. View all appointments

### Reset Password
1. Click "Forgot Password" on login page
2. Enter email
3. Check console for reset link
4. Click link and set new password

## 📊 Database Tables

### Core Tables
- `users` - User accounts (admin/patient)
- `patients` - Patient records
- `doctors` - Doctor information
- `departments` - Hospital departments
- `appointments` - Scheduled appointments
- `queue_entries` - Walk-in queue
- `notifications` - System notifications
- `crowd_logs` - Crowd prediction data
- `password_reset_tokens` - Password reset

## 🔧 Configuration

### Session Settings (config.py)
```python
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
```

### Security Settings
```python
SECRET_KEY = "smart-hospital-secret-key-2024"
WTF_CSRF_ENABLED = True
```

## 🐛 Troubleshooting

### "Please login to access this page"
**Solution**: You need to login first

### "Access denied. Admin privileges required"
**Solution**: You're logged in as patient, need admin account

### "Access denied. This page is for patients only"
**Solution**: You're logged in as admin, need patient account

### CSRF Token Missing
**Solution**: Ensure `{{ form.hidden_tag() }}` in all forms

### Session Expires Too Quickly
**Solution**: Adjust `PERMANENT_SESSION_LIFETIME` in config.py

## 📝 Form Validation Rules

### Registration
- Name: 2-150 characters
- Email: Valid email format, unique
- Phone: 10-15 characters
- Password: Minimum 8 characters
- Confirm Password: Must match

### Doctor Form
- Name: 2-150 characters
- Specialization: Required, max 100 chars
- Department: Required (dropdown)
- Experience: 0-60 years
- Consultation Time: 5-120 minutes
- Max Patients: 1-100 per day
- Shift Times: Required

### Department Form
- Name: 2-100 characters
- Floor: 1-20
- Max Capacity: 10-200 patients
- Avg Consultation: 5-60 minutes

## 🔑 Security Decorators

### In Route Files
```python
from app.services.auth_service import admin_required, user_required

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    # Only admins can access
    pass

@app.route('/patient/dashboard')
@user_required
def patient_dashboard():
    # Only patients can access
    pass
```

## 📱 SMS Notifications

Currently simulated (prints to console):
- Appointment confirmation
- Appointment reminders
- Queue updates

To enable real SMS:
1. Integrate Twilio/AWS SNS
2. Update `app/services/sms_service.py`
3. Add API credentials to config

## 🎯 Testing Checklist

- [ ] Admin can login
- [ ] Patient can register
- [ ] Patient can login
- [ ] Admin can access admin routes
- [ ] Patient can access patient routes
- [ ] Admin cannot access patient-only routes
- [ ] Patient cannot access admin routes
- [ ] Unauthorized users redirected to login
- [ ] Password reset works
- [ ] CSRF protection active
- [ ] Forms validate correctly
- [ ] Doctor CRUD works
- [ ] Department CRUD works
- [ ] Appointment booking works
- [ ] SMS confirmation sent

## 📚 Documentation Files

- `README.md` - Project overview
- `AUTHENTICATION_GUIDE.md` - Complete auth documentation
- `SECURITY_IMPLEMENTATION_COMPLETE.md` - Implementation summary
- `DUAL_PORTAL_GUIDE.md` - Dual portal architecture
- `IMPLEMENTATION_SUMMARY.md` - Original implementation
- `QUICK_START.md` - Quick start guide
- `QUICK_REFERENCE.md` - This file

## 🚨 Important Notes

1. **Change default admin password in production**
2. **Set SESSION_COOKIE_SECURE = True with HTTPS**
3. **Use strong SECRET_KEY in production**
4. **Enable real email service for password reset**
5. **Set up proper logging and monitoring**
6. **Configure database backups**
7. **Add rate limiting for login attempts**

## 💡 Tips

- Use Chrome DevTools to inspect CSRF tokens
- Check browser console for JavaScript errors
- Check Flask console for server logs
- Use Incognito mode to test different user sessions
- Clear cookies if experiencing session issues

---

**Need Help?** Check the full documentation in `AUTHENTICATION_GUIDE.md`

**Server Status**: ✅ Running at http://127.0.0.1:5000
