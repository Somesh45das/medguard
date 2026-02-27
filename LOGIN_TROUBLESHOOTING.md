# 🔧 Login Dashboard Issue - Troubleshooting Guide

## Issue
After signing in, the dashboard is not showing.

---

## ✅ Quick Fix (Most Common)

### 1. Restart the Flask Server

The server needs to be restarted to load the new login page changes.

**Stop the server:**
- Press `Ctrl + C` in the terminal where Flask is running

**Start the server again:**
```bash
python run.py
```

**Then try logging in again.**

---

## 🔍 Diagnostic Steps

### Step 1: Check if Server is Running
```bash
# You should see output like:
# * Running on http://127.0.0.1:5000
# * Running on http://localhost:5000
```

### Step 2: Clear Browser Cache
1. Open browser DevTools (F12)
2. Right-click the refresh button
3. Select "Empty Cache and Hard Reload"

### Step 3: Check Browser Console
1. Open DevTools (F12)
2. Go to Console tab
3. Look for any JavaScript errors
4. Look for any 404 or 500 errors

### Step 4: Check Flask Console
Look in the terminal where Flask is running for:
- Any Python errors
- 404 errors
- 500 errors
- Stack traces

---

## 🎯 Common Issues & Solutions

### Issue 1: Server Not Restarted
**Symptom**: Login page looks different but dashboard doesn't load
**Solution**: 
```bash
# Stop server (Ctrl + C)
python run.py
```

### Issue 2: Browser Cache
**Symptom**: Old login page still showing
**Solution**: Hard refresh (Ctrl + Shift + R) or clear cache

### Issue 3: Database Not Initialized
**Symptom**: Error about missing tables
**Solution**:
```bash
python
>>> from app import create_app, db
>>> app = create_app()
>>> with app.app_context():
...     db.create_all()
>>> exit()
```

### Issue 4: No Admin User
**Symptom**: Can't login with admin credentials
**Solution**:
```bash
python seed_data.py
```

### Issue 5: Session Issues
**Symptom**: Login succeeds but redirects back to login
**Solution**: Clear browser cookies for localhost

---

## 📋 Verification Checklist

### Before Login
- [ ] Flask server is running
- [ ] No errors in Flask console
- [ ] Login page loads correctly
- [ ] Browser console has no errors

### During Login
- [ ] Email and password entered correctly
- [ ] No validation errors shown
- [ ] "Signing in..." message appears
- [ ] No errors in browser console

### After Login
- [ ] Success message appears
- [ ] Redirects to dashboard
- [ ] Dashboard loads correctly
- [ ] No 404 or 500 errors

---

## 🔐 Test Credentials

### Admin Account
```
Email: admin@hospital.com
Password: admin123
Should redirect to: /admin (Admin Dashboard)
```

### Patient Account
```
Email: test@patient.com
Password: test123
Should redirect to: /patient/dashboard (Patient Dashboard)
```

---

## 🛠️ Manual Testing Steps

### Test Admin Login
1. Go to http://localhost:5000/auth/login
2. Enter: admin@hospital.com / admin123
3. Click "Sign In"
4. Should see: "Welcome back, Admin!"
5. Should redirect to: http://localhost:5000/admin
6. Should see: Admin Dashboard with statistics

### Test Patient Login
1. Go to http://localhost:5000/auth/login
2. Enter: test@patient.com / test123
3. Click "Sign In"
4. Should see: "Welcome back, Test Patient!"
5. Should redirect to: http://localhost:5000/patient/dashboard
6. Should see: Patient Dashboard

---

## 🔍 Debug Mode

### Enable Debug Output
Edit `run.py` or `config.py`:

```python
# In run.py
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
```

This will show detailed error messages.

---

## 📊 Check Routes

### Verify Routes are Registered
```bash
python
>>> from app import create_app
>>> app = create_app()
>>> print(app.url_map)
```

Should see:
- `/auth/login`
- `/admin/` (dashboard.index)
- `/patient/dashboard` (patient_portal.dashboard)

---

## 🚨 Error Messages & Solutions

### "404 Not Found"
**Cause**: Route doesn't exist
**Solution**: Restart server, check blueprints are registered

### "500 Internal Server Error"
**Cause**: Python error in route
**Solution**: Check Flask console for stack trace

### "Unauthorized" or redirects to login
**Cause**: Session not created or expired
**Solution**: Clear cookies, try again

### "CSRF Token Missing"
**Cause**: CSRF protection issue
**Solution**: Check if CSRF is disabled in config

---

## 🔄 Complete Reset (If Nothing Works)

### 1. Stop Server
```bash
Ctrl + C
```

### 2. Clear Browser Data
- Clear all cookies for localhost
- Clear cache
- Close and reopen browser

### 3. Reset Database (Optional)
```bash
# Backup first if needed
rm instance/hospital.db
python seed_data.py
```

### 4. Restart Server
```bash
python run.py
```

### 5. Try Login Again
Use admin@hospital.com / admin123

---

## 📞 Still Not Working?

### Check These Files
1. `app/__init__.py` - Blueprints registered?
2. `app/routes/auth.py` - Login route correct?
3. `app/routes/dashboard.py` - Dashboard route exists?
4. `app/routes/patient_portal.py` - Patient dashboard exists?

### Collect This Information
1. Flask console output (copy all errors)
2. Browser console errors (F12 → Console)
3. Network tab (F12 → Network) - check failed requests
4. Python version: `python --version`
5. Flask version: `pip show flask`

---

## ✅ Expected Behavior

### Admin Login Flow
```
1. Visit /auth/login
2. Enter admin credentials
3. Click "Sign In"
4. See flash message: "Welcome back, Admin!"
5. Redirect to /admin
6. See dashboard with:
   - Statistics cards
   - Department crowd levels
   - Queue information
   - Charts and graphs
```

### Patient Login Flow
```
1. Visit /auth/login
2. Enter patient credentials
3. Click "Sign In"
4. See flash message: "Welcome back, [Name]!"
5. Redirect to /patient/dashboard
6. See dashboard with:
   - Upcoming appointments
   - Quick actions
   - Status information
```

---

## 🎯 Most Likely Solution

**90% of the time, the issue is:**

1. **Server not restarted** after login page changes
   - Solution: Stop (Ctrl+C) and restart (`python run.py`)

2. **Browser cache** showing old page
   - Solution: Hard refresh (Ctrl+Shift+R)

3. **Wrong credentials** being used
   - Solution: Use exact credentials from demo box

**Try these three things first!**

---

## 📝 Quick Command Reference

```bash
# Stop server
Ctrl + C

# Start server
python run.py

# Reset database
python seed_data.py

# Check Python version
python --version

# Check Flask version
pip show flask

# Test database connection
python
>>> from app import create_app, db
>>> app = create_app()
>>> with app.app_context():
...     from app.models.user import User
...     print(User.query.all())
>>> exit()
```

---

## ✨ Success Indicators

You'll know it's working when:
- ✅ Login page loads with new design
- ✅ Credentials are accepted
- ✅ Flash message appears
- ✅ Dashboard loads (not login page)
- ✅ Sidebar shows navigation
- ✅ Statistics cards display
- ✅ No errors in console

---

**Need more help? Check the Flask console output for specific error messages!**
