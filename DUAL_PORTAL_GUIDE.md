# 🏥 Smart Hospital - Dual Portal System

The application is now divided into **two separate portals**:

## 🔵 1. Patient Portal (Public Access)
**URL:** `http://127.0.0.1:5000/patient`

### Features:
- ✅ User-friendly interface for patients
- ✅ Self-service appointment booking
- ✅ **Automatic SMS confirmation** with all appointment details
- ✅ Smart slot recommendations (AI-powered)
- ✅ Check appointment status by phone number
- ✅ No login required
- ✅ Mobile-responsive design

### Patient Journey:
1. Visit patient portal home page
2. Click "Book Appointment"
3. Enter personal details (name, age, phone number)
4. Select department and doctor
5. Choose preferred date and time slot
6. Submit booking
7. **Receive instant SMS** with:
   - Appointment number
   - Date and time
   - Doctor name
   - Department and floor
   - Instructions to arrive early

### SMS Notification Example:
```
🏥 SmartCare Hospital - Appointment Confirmed

Dear John Doe,

Your appointment has been booked successfully!

📅 Date: Monday, February 24, 2026
⏰ Time: 10:00 AM
👨‍⚕️ Doctor: Dr. Aisha Sharma
🏢 Department: General Medicine
🎫 Appointment #: APT-20260224-001

📍 Location: SmartCare Hospital, Floor 1

⚠️ Please arrive 15 minutes early.
📱 For queries, call: +91-1800-XXX-XXXX

Thank you for choosing SmartCare Hospital!
```

---

## 🔴 2. Management Portal (Staff Only)
**URL:** `http://127.0.0.1:5000/management`

### Login Credentials:
- **Username:** `admin`
- **Password:** `admin123`

### Features:
- ✅ Full dashboard with real-time statistics
- ✅ ML-powered crowd prediction
- ✅ Priority-based queue management
- ✅ Appointment management (CRUD operations)
- ✅ Doctor availability management
- ✅ Live queue with token system
- ✅ Analytics and reporting
- ✅ Notification system
- ✅ **Can also send SMS** when booking for patients

### Management Capabilities:
1. **Dashboard** (`/admin`)
   - Real-time stats
   - Department-wise crowd levels
   - Prediction charts
   - Notifications

2. **Appointments** (`/admin/appointments`)
   - View all appointments
   - Filter by date, department, status
   - Book appointments for patients
   - Check-in patients
   - Cancel appointments
   - **SMS sent automatically on booking**

3. **Queue Management** (`/admin/queue`)
   - Add walk-in patients
   - Priority-based ordering
   - Call next patient
   - Track consultation status
   - Real-time position updates

4. **Doctor Management** (`/admin/doctors`)
   - View all doctors
   - Toggle availability
   - Monitor patient load
   - Track capacity

---

## 📱 SMS Integration

### Current Implementation:
The SMS service is **simulated** and prints to console. In production, integrate with:

- **Twilio** (Recommended)
- **AWS SNS**
- **Nexmo/Vonage**
- **MSG91** (India)
- **TextLocal** (India)

### To Enable Real SMS:
Edit `app/services/sms_service.py` and uncomment the Twilio integration:

```python
from twilio.rest import Client

client = Client(account_sid, auth_token)
client.messages.create(
    body=message,
    from_='+1234567890',
    to=patient.phone
)
```

### SMS Triggers:
1. **Appointment Confirmation** - Sent immediately after booking
2. **Appointment Reminder** - Can be scheduled (24 hours before)
3. **Queue Token** - Sent to walk-in patients

---

## 🚀 Quick Start

### 1. Start the Server
```bash
.\venv\Scripts\Activate.ps1
python run.py
```

### 2. Access Portals

**For Patients:**
```
http://127.0.0.1:5000/patient
```

**For Hospital Staff:**
```
http://127.0.0.1:5000/management
Login: admin / admin123
```

---

## 🔐 Security Features

### Patient Portal:
- No authentication required (public access)
- Phone number verification for status checks
- Session-based appointment tracking

### Management Portal:
- Login required for all admin routes
- Session-based authentication
- Logout functionality
- Protected routes with decorators

---

## 📊 Key Differences

| Feature | Patient Portal | Management Portal |
|---------|---------------|-------------------|
| **Access** | Public | Login Required |
| **Interface** | Simple, user-friendly | Comprehensive, data-rich |
| **Booking** | Self-service only | Can book for anyone |
| **Queue** | View status only | Full control |
| **SMS** | Auto-sent on booking | Auto-sent + manual options |
| **Analytics** | None | Full dashboard |
| **Priority** | System-assigned | Can override |

---

## 🎯 Use Cases

### Patient Portal:
- Patients booking their own appointments
- Checking appointment status
- Receiving SMS confirmations
- No technical knowledge required

### Management Portal:
- Reception desk booking appointments
- Managing walk-in patients
- Monitoring queue and crowd levels
- Doctor schedule management
- Emergency priority handling
- Analytics and reporting

---

## 📞 SMS Configuration (Production)

### Twilio Setup:
1. Sign up at https://www.twilio.com
2. Get Account SID and Auth Token
3. Purchase a phone number
4. Update `app/services/sms_service.py`
5. Add credentials to environment variables

### Environment Variables:
```bash
export TWILIO_ACCOUNT_SID="your_account_sid"
export TWILIO_AUTH_TOKEN="your_auth_token"
export TWILIO_PHONE_NUMBER="+1234567890"
```

---

## 🔄 Workflow Example

### Patient Self-Booking:
1. Patient visits `/patient`
2. Clicks "Book Appointment"
3. Fills form with phone number
4. Selects optimal time slot (AI-recommended)
5. Submits booking
6. **SMS sent instantly**
7. Confirmation page displayed
8. Can check status anytime using phone number

### Staff-Assisted Booking:
1. Staff logs into `/management`
2. Goes to Appointments
3. Books appointment for patient
4. Enters patient's phone number
5. **SMS sent to patient**
6. Patient receives confirmation

---

## 🎨 Customization

### Branding:
- Update hospital name in `config.py`
- Modify colors in templates
- Add logo to navigation

### SMS Templates:
- Edit messages in `app/services/sms_service.py`
- Add custom fields
- Support multiple languages

### Business Rules:
- Adjust priority scoring in `priority_scorer.py`
- Modify slot duration in `config.py`
- Configure OPD hours

---

## 📈 Future Enhancements

- [ ] Email notifications alongside SMS
- [ ] WhatsApp integration
- [ ] Patient mobile app
- [ ] QR code for check-in
- [ ] Payment gateway integration
- [ ] Prescription management
- [ ] Medical records integration
- [ ] Multi-language support

---

## 🆘 Support

For issues or questions:
- Check console logs for SMS output
- Verify phone number format
- Ensure all dependencies installed
- Check session configuration

---

**Enjoy your dual-portal hospital management system with SMS notifications!** 🎉
