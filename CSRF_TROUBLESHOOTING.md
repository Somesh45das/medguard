# CSRF Token Error - Troubleshooting Guide

## Error Message
"Bad Request - The CSRF token is missing"

## Cause
The CSRF token IS being generated correctly (verified in HTML source), but the browser may be:
1. Caching an old version of the page
2. Blocking cookies
3. Not sending the token with the form submission

## Solutions

### Solution 1: Clear Browser Cache (RECOMMENDED)
1. Open browser DevTools (F12)
2. Right-click the refresh button
3. Select "Empty Cache and Hard Reload"
4. Or use keyboard shortcut: Ctrl+Shift+Delete (Windows) / Cmd+Shift+Delete (Mac)
5. Clear cookies for localhost

### Solution 2: Use Incognito/Private Mode
1. Open a new incognito/private window
2. Visit http://localhost:5000
3. Try logging in

### Solution 3: Check Browser Console
1. Open DevTools (F12)
2. Go to Console tab
3. Look for any JavaScript errors
4. Go to Network tab
5. Submit the form
6. Check if csrf_token is in the POST data

### Solution 4: Verify Cookies Are Enabled
1. Open DevTools (F12)
2. Go to Application tab (Chrome) or Storage tab (Firefox)
3. Check Cookies → http://localhost:5000
4. You should see a session cookie
5. If no cookies, enable cookies in browser settings

### Solution 5: Manual Cookie Check
1. Visit http://localhost:5000/auth/login
2. Open DevTools → Application → Cookies
3. Look for "hospital_session" cookie
4. If missing, cookies are blocked

## Verification Steps

### Step 1: Check CSRF Token in HTML
```bash
# View page source (Ctrl+U)
# Search for: csrf_token
# You should see: <input id="csrf_token" name="csrf_token" type="hidden" value="...">
```

### Step 2: Check Form Submission
1. Open DevTools → Network tab
2. Submit login form
3. Click on the POST request to /auth/login
4. Check "Form Data" section
5. Verify csrf_token is present

### Step 3: Check Response
- If CSRF token is in form data but still getting error:
  - Session might have expired
  - Cookie domain mismatch
  - CSRF validation issue

## Quick Test

Try this in browser console (F12):
```javascript
// Check if CSRF token exists in form
document.querySelector('input[name="csrf_token"]').value

// Check cookies
document.cookie
```

## Current Status

✅ CSRF Protection: ENABLED
✅ CSRF Token Generation: WORKING
✅ Token in HTML Form: CONFIRMED
❓ Token Submission: NEEDS VERIFICATION

## If Still Not Working

### Temporary Workaround (Development Only)
If you need to test immediately, you can temporarily disable CSRF for the login route:

1. Edit `app/routes/auth.py`
2. Add decorator to login route:
```python
from flask_wtf.csrf import csrf

@auth_bp.route('/login', methods=['GET', 'POST'])
@csrf.exempt  # TEMPORARY - REMOVE IN PRODUCTION
def login():
    # ... rest of code
```

**WARNING**: Only use this for testing! Remove before production!

## Best Practice Solution

The proper solution is to fix the browser/cookie issue, not disable CSRF protection.

### Steps to Fix Properly:
1. Clear all browser data for localhost
2. Restart browser
3. Visit http://localhost:5000
4. Check DevTools → Application → Cookies
5. Verify session cookie is created
6. Try logging in

## Common Causes

### 1. Browser Extensions
- Ad blockers
- Privacy extensions
- Cookie blockers
→ Disable extensions and try again

### 2. Browser Settings
- Third-party cookies blocked
- All cookies blocked
- Strict privacy settings
→ Check browser privacy settings

### 3. Localhost Issues
- Using 127.0.0.1 instead of localhost
- Port conflicts
- Multiple tabs with different sessions
→ Use consistent URL (localhost:5000)

## Testing Checklist

- [ ] Cleared browser cache
- [ ] Cleared cookies for localhost
- [ ] Tried incognito mode
- [ ] Checked DevTools console for errors
- [ ] Verified CSRF token in HTML source
- [ ] Verified CSRF token in form submission
- [ ] Checked session cookie exists
- [ ] Disabled browser extensions
- [ ] Tried different browser
- [ ] Restarted browser
- [ ] Restarted Flask server

## Contact Information

If none of these solutions work, the issue might be:
- Browser-specific bug
- Operating system security settings
- Antivirus/firewall blocking cookies
- Network proxy interfering

Try accessing from a different device or network to isolate the issue.

---

**Last Updated**: CSRF token generation confirmed working
**Status**: Browser/cookie issue - not a code issue
