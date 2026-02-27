# 🔄 Dashboard Login Flow Diagram

## What Should Happen When You Login

```
┌─────────────────────────────────────────────────────────────┐
│  1. User visits: http://127.0.0.1:5000/auth/login          │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  2. Login page loads with:                                  │
│     • Email field                                           │
│     • Password field                                        │
│     • Role selection (Admin/Patient)                        │
│     • Sign In button                                        │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  3. User enters credentials and clicks "Sign In"            │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  4. Flask receives POST request to /auth/login              │
│     • Validates form data                                   │
│     • Looks up user by email                                │
│     • Checks password                                       │
└─────────────────────────────────────────────────────────────┘
                            ↓
                    ┌───────┴───────┐
                    │               │
            ✅ Valid          ❌ Invalid
                    │               │
                    ↓               ↓
    ┌───────────────────────┐   ┌──────────────────────┐
    │ 5a. Login Success     │   │ 5b. Login Failed     │
    │  • Create session     │   │  • Show error        │
    │  • Set current_user   │   │  • Stay on login     │
    │  • Flash welcome msg  │   └──────────────────────┘
    └───────────────────────┘
                ↓
        ┌───────┴───────┐
        │               │
    Admin           Patient
        │               │
        ↓               ↓
┌──────────────┐  ┌──────────────────────┐
│ 6a. Admin    │  │ 6b. Patient          │
│ Redirect to: │  │ Redirect to:         │
│ /admin       │  │ /patient/dashboard   │
└──────────────┘  └──────────────────────┘
        │               │
        ↓               ↓
┌──────────────┐  ┌──────────────────────┐
│ 7a. Admin    │  │ 7b. Patient          │
│ Dashboard    │  │ Dashboard            │
│ Loads        │  │ Loads                │
└──────────────┘  └──────────────────────┘
```

---

## Admin Login Flow Details

```
Email: admin@hospital.com
Password: admin123
         ↓
┌─────────────────────────────────────┐
│ auth.py → login() function          │
│  • Find user by email               │
│  • Check password: ✅               │
│  • Check is_admin(): ✅             │
│  • login_user(user)                 │
│  • Flash: "Welcome back, Admin!"    │
│  • return redirect('/admin')        │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│ dashboard.py → index() function     │
│  • @admin_required decorator        │
│  • Load statistics                  │
│  • Render admin dashboard           │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│ Browser shows:                      │
│  • Admin sidebar                    │
│  • Statistics cards                 │
│  • Department info                  │
│  • Queue management                 │
└─────────────────────────────────────┘
```

---

## Patient Login Flow Details

```
Email: test@patient.com
Password: test123
         ↓
┌─────────────────────────────────────┐
│ auth.py → login() function          │
│  • Find user by email               │
│  • Check password: ✅               │
│  • Check is_admin(): ❌             │
│  • login_user(user)                 │
│  • Flash: "Welcome back, Test!"     │
│  • return redirect('/patient/dash') │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│ patient_portal.py → dashboard()     │
│  • @user_required decorator         │
│  • Check current_user.patient ✅    │
│  • Load appointments                │
│  • Render patient dashboard         │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│ Browser shows:                      │
│  • Patient sidebar                  │
│  • Upcoming appointments            │
│  • Quick actions                    │
│  • Chatbot widget                   │
└─────────────────────────────────────┘
```

---

## Where Things Can Go Wrong

### ❌ Problem 1: Server Not Restarted
```
Login page changes made
         ↓
Server still running old code
         ↓
Routes not updated
         ↓
Dashboard doesn't load
```
**Fix**: Restart server (Ctrl+C, then `python run.py`)

---

### ❌ Problem 2: Browser Cache
```
New login page created
         ↓
Browser shows cached old page
         ↓
Form submits to wrong endpoint
         ↓
Dashboard doesn't load
```
**Fix**: Hard refresh (Ctrl+Shift+R)

---

### ❌ Problem 3: Patient Record Not Linked
```
User logs in successfully
         ↓
Redirects to /patient/dashboard
         ↓
dashboard() checks current_user.patient
         ↓
current_user.patient is None ❌
         ↓
Flash: "Please complete your profile"
         ↓
Redirects back to home
```
**Fix**: Run `python seed_data.py`

---

### ❌ Problem 4: Session Not Created
```
Login form submitted
         ↓
Password correct
         ↓
login_user() called
         ↓
Session not saved ❌
         ↓
Redirect happens
         ↓
@user_required checks current_user
         ↓
current_user is anonymous
         ↓
Redirects back to login
```
**Fix**: Clear cookies, check SECRET_KEY in config

---

## Debugging Checklist

### Before Login
- [ ] Flask server running
- [ ] No errors in console
- [ ] Database has users
- [ ] Routes registered

### During Login
- [ ] Form submits
- [ ] POST request to /auth/login
- [ ] No 404 or 500 errors
- [ ] Flash message appears

### After Login
- [ ] Redirect happens
- [ ] Dashboard URL loads
- [ ] No redirect loop
- [ ] Content displays

---

## Expected Console Output

### When Server Starts
```
============================================================
  🏥 Smart Hospital Queue & Appointment Optimizer
============================================================

✅ ML model loaded.

🚀 Starting server at http://127.0.0.1:5000
   Press Ctrl+C to stop.

 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

### When Admin Logs In
```
127.0.0.1 - - [DATE] "GET /auth/login HTTP/1.1" 200 -
127.0.0.1 - - [DATE] "POST /auth/login HTTP/1.1" 302 -
127.0.0.1 - - [DATE] "GET /admin HTTP/1.1" 200 -
```

### When Patient Logs In
```
127.0.0.1 - - [DATE] "GET /auth/login HTTP/1.1" 200 -
127.0.0.1 - - [DATE] "POST /auth/login HTTP/1.1" 302 -
127.0.0.1 - - [DATE] "GET /patient/dashboard HTTP/1.1" 200 -
```

---

## Quick Test

Run this in order:

```bash
# 1. Check setup
python check_login_setup.py

# 2. Start server (if not running)
python run.py

# 3. In browser:
http://127.0.0.1:5000/auth/login

# 4. Try admin login:
admin@hospital.com / admin123

# 5. Should redirect to:
http://127.0.0.1:5000/admin
```

---

## Success Indicators

✅ Login page loads with new design
✅ Credentials accepted
✅ Flash message: "Welcome back, [Name]!"
✅ URL changes to dashboard
✅ Dashboard content displays
✅ No errors in console
✅ Sidebar navigation works

---

**If you see all ✅ above, it's working!**
**If you see any ❌, check the troubleshooting section.**
