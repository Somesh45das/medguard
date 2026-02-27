# Config.py Changes to Enable Real SMS

## Current Configuration (Lines 48-59 in config.py)

```python
# SMS Configuration
SMS_ENABLED = os.environ.get("SMS_ENABLED", "False").lower() == "true"
SMS_PROVIDER = os.environ.get("SMS_PROVIDER", "simulation")  # "twilio", "aws_sns", or "simulation"

# Twilio Configuration (if using Twilio)
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN", "")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER", "")

# AWS SNS Configuration (if using AWS SNS)
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
```

---

## Option 1: Quick Test (Direct Configuration)

### Step 1: Get Twilio Credentials
1. Sign up at: https://www.twilio.com/try-twilio
2. Get your Account SID (starts with "AC...")
3. Get your Auth Token
4. Get a Twilio phone number

### Step 2: Install Twilio
```bash
pip install twilio
```

### Step 3: Replace Lines 48-59 in config.py

**REPLACE THIS:**
```python
# SMS Configuration
SMS_ENABLED = os.environ.get("SMS_ENABLED", "False").lower() == "true"
SMS_PROVIDER = os.environ.get("SMS_PROVIDER", "simulation")  # "twilio", "aws_sns", or "simulation"

# Twilio Configuration (if using Twilio)
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN", "")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER", "")

# AWS SNS Configuration (if using AWS SNS)
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
```

**WITH THIS:**
```python
# SMS Configuration
SMS_ENABLED = True  # ← CHANGED: Enable SMS
SMS_PROVIDER = "twilio"  # ← CHANGED: Use Twilio

# Twilio Configuration (if using Twilio)
TWILIO_ACCOUNT_SID = "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # ← ADD YOUR SID HERE
TWILIO_AUTH_TOKEN = "your_auth_token_here"  # ← ADD YOUR TOKEN HERE
TWILIO_PHONE_NUMBER = "+1234567890"  # ← ADD YOUR TWILIO NUMBER HERE

# AWS SNS Configuration (if using AWS SNS)
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
```

### Step 4: Restart Your App
```bash
python run.py
```

You should see:
```
✅ Twilio SMS client initialized
```

### Step 5: Test It!
- Book an appointment with YOUR phone number
- Check your phone for SMS!

---

## Option 2: Production Setup (Environment Variables)

This is better for production as credentials aren't in code.

### Step 1: Create .env File

Create a file named `.env` in your project root:

```bash
# .env file
SMS_ENABLED=true
SMS_PROVIDER=twilio
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+1234567890
```

### Step 2: Install python-dotenv

```bash
pip install python-dotenv
```

### Step 3: Update config.py

Add this at the TOP of config.py (after imports):

```python
"""
Application configuration.
"""
import os
from dotenv import load_dotenv  # ← ADD THIS

load_dotenv()  # ← ADD THIS

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
```

### Step 4: Keep SMS Configuration As Is

The existing config will now read from .env file:
```python
# SMS Configuration
SMS_ENABLED = os.environ.get("SMS_ENABLED", "False").lower() == "true"
SMS_PROVIDER = os.environ.get("SMS_PROVIDER", "simulation")
# ... rest stays the same
```

### Step 5: Restart and Test

```bash
python run.py
```

---

## Verification

### Check if SMS is Enabled

Run this command:
```bash
python test_sms_configuration.py
```

You should see:
```
✅ Twilio is CONFIGURED - Real SMS will be sent!
```

### Test Real SMS

1. Start app: `python run.py`
2. Look for: `✅ Twilio SMS client initialized`
3. Book appointment with YOUR phone number
4. Check console for: `✅ REAL SMS SENT via Twilio to +1234567890`
5. Check your phone!

---

## Troubleshooting

### Still Seeing "SMS SIMULATION"?

Check these:
1. ✅ `SMS_ENABLED = True` (not False)
2. ✅ `SMS_PROVIDER = "twilio"` (not "simulation")
3. ✅ All three Twilio credentials are filled in
4. ✅ App was restarted after changes
5. ✅ Twilio package is installed: `pip install twilio`

### "Twilio not installed"
```bash
pip install twilio
```

### "Invalid credentials"
- Double-check Account SID starts with "AC"
- Verify Auth Token is correct
- Check for extra spaces or quotes

### Trial Account Limitations
- Twilio trial can only send to verified numbers
- Verify your phone in Twilio Console
- Or upgrade to paid account (no restrictions)

---

## Summary

**Current:** Simulation mode (prints to console)

**To Enable Real SMS:**
1. Get Twilio credentials (free trial)
2. Change 3 lines in config.py:
   - `SMS_ENABLED = True`
   - `SMS_PROVIDER = "twilio"`
   - Add your credentials
3. Install: `pip install twilio`
4. Restart app
5. Test with your phone number

**Time Required:** 5 minutes  
**Cost:** Free trial ($15 credit) or ~$1 per 100 SMS

---

## Quick Copy-Paste Template

Replace lines 48-59 in config.py with this (add your credentials):

```python
# SMS Configuration
SMS_ENABLED = True
SMS_PROVIDER = "twilio"

# Twilio Configuration
TWILIO_ACCOUNT_SID = "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # Your SID
TWILIO_AUTH_TOKEN = "your_auth_token_here"  # Your token
TWILIO_PHONE_NUMBER = "+1234567890"  # Your Twilio number

# AWS SNS Configuration (not used if using Twilio)
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
```

Then restart: `python run.py`

Done! 🎉
