# 🔧 Fix Dashboard Not Loading Issue

## Quick 3-Step Fix

### Step 1: Run Diagnostic
```bash
python check_login_setup.py
```

This will check if everything is configured correctly.

---

### Step 2: Restart Flask Server

**Stop the server:**
- Press `Ctrl + C` in the terminal where Flask is running

**Start it again:**
```bash
python run.py
```

---

### Step 3: Clear Browser Cache & Try Again

1. Open your browser
2. Press `Ctrl + Shift + R` (hard refresh)
3. Go to: http://127.0.0.1:5000/auth/login
4. Try logging in:
   - **Admin**: admin@hospital.com / admin123
   - **Patient**: test@patient.com / test123

---

## If Still Not Working

### Check Flask Console

Look at the terminal where Flask is running. You should see:
```
* Running on http://127.0.0.1:5000
```

When you try to login, watch for:
- Any error messages
- 404 errors
- 500 errors
- Python stack traces

**Copy any error messages you see!**

---

### Check Browser Console

1. Press `F12` to open DevTools
2. Go to "Console" tab
3. Look for red error messages
4. Go to "Network" tab
5. Try logging in
6. Look for failed requests (red)

**Copy any error messages you see!**

---

### Reset Database (If Needed)

If the diagnostic script shows issues:

```bash
python seed_data.py
```

This will recreate all test data including:
- Admin user (admin@hospital.com / admin123)
- Test patient (test@patient.com / test123)

---

## What Should Happen

### Admin Login (admin@hospital.com)
1. Enter credentials
2. Click "Sign In"
3. See: "Welcome back, Admin User!"
4. Redirect to: http://127.0.0.1:5000/admin
5. See: Admin dashboard with statistics

### Patient Login (test@patient.com)
1. Enter credentials
2. Click "Sign In"
3. See: "Welcome back, Test Patient!"
4. Redirect to: http://127.0.0.1:5000/patient/dashboard
5. See: Patient dashboard with appointments

---

## Common Issues

### Issue: "Please complete your profile"
**Cause**: Patient record not linked to user account
**Fix**: Run `python seed_data.py`

### Issue: Redirects back to login
**Cause**: Session not being created
**Fix**: 
1. Clear browser cookies
2. Check Flask console for errors
3. Restart server

### Issue: 404 Not Found
**Cause**: Routes not registered
**Fix**: Restart Flask server

### Issue: Old login page showing
**Cause**: Browser cache
**Fix**: Hard refresh (Ctrl+Shift+R)

---

## Need More Help?

Run the diagnostic and share the output:
```bash
python check_login_setup.py
```

Also share:
1. Flask console output (any errors)
2. Browser console errors (F12 → Console)
3. What happens when you try to login

---

## Quick Test Commands

```bash
# 1. Check setup
python check_login_setup.py

# 2. Reset database (if needed)
python seed_data.py

# 3. Start server
python run.py

# 4. In browser:
# http://127.0.0.1:5000/auth/login
```

---

**Most likely fix: Restart the Flask server and clear browser cache!**
