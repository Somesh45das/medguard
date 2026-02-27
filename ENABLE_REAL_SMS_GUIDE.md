# Enable Real SMS - Step-by-Step Guide

## Current Status
✅ SMS system is **READY** but in **simulation mode**  
✅ Messages print to console instead of sending to phones  
✅ To enable real SMS, follow steps below (5 minutes)

---

## Option 1: Twilio (Recommended - Easiest)

### Step 1: Sign Up for Twilio (2 minutes)

1. Go to: https://www.twilio.com/try-twilio
2. Sign up for free account
3. Verify your email and phone number
4. You get **$15 free credit** (enough for ~2,000 SMS)

### Step 2: Get Your Credentials (1 minute)

1. Go to Twilio Console: https://console.twilio.com/
2. Find your **Account SID** and **Auth Token**
3. Get a Twilio phone number:
   - Click "Get a Trial Number" or
   - Go to Phone Numbers → Buy a Number

### Step 3: Install Twilio SDK (30 seconds)

```bash
pip install twilio
```

### Step 4: Configure Your App (1 minute)

**Option A: Environment Variables (Recommended for Production)**

Create a `.env` file in your project root:
```bash
SMS_ENABLED=true
SMS_PROVIDER=twilio
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+1234567890
```

Then install python-dotenv:
```bash
pip install python-dotenv
```

Add to `config.py` at the top:
```python
from dotenv import load_dotenv
load_dotenv()
```

**Option B: Direct Configuration (Quick Testing)**

Edit `config.py` and change these lines:
```python
# SMS Configuration
SMS_ENABLED = True  # Change from False to True
SMS_PROVIDER = "twilio"  # Change from "simulation" to "twilio"

# Twilio Configuration
TWILIO_ACCOUNT_SID = "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # Your SID
TWILIO_AUTH_TOKEN = "your_auth_token_here"  # Your token
TWILIO_PHONE_NUMBER = "+1234567890"  # Your Twilio number
```

### Step 5: Restart Your App (10 seconds)

```bash
python run.py
```

You should see:
```
✅ Twilio SMS client initialized
```

### Step 6: Test It! (30 seconds)

Book an appointment with YOUR phone number and you'll receive a real SMS!

---

## Option 2: AWS SNS (For AWS Users)

### Step 1: Install Boto3

```bash
pip install boto3
```

### Step 2: Get AWS Credentials

1. Go to AWS Console → IAM
2. Create user with SNS permissions
3. Get Access Key ID and Secret Access Key

### Step 3: Configure

Edit `config.py`:
```python
SMS_ENABLED = True
SMS_PROVIDER = "aws_sns"
AWS_ACCESS_KEY_ID = "your_access_key"
AWS_SECRET_ACCESS_KEY = "your_secret_key"
AWS_REGION = "us-east-1"
```

### Step 4: Restart and Test

```bash
python run.py
```

---

## Verification

### Check if SMS is Enabled

When you start the app, you should see:
```
✅ Twilio SMS client initialized
```
or
```
✅ AWS SNS client initialized
```

If you see:
```
📱 SMS SIMULATION - TO: +91-9876543210
   (SMS_ENABLED = False in config)
```
Then SMS is still in simulation mode.

### Test Real SMS

1. Start your app: `python run.py`
2. Book an appointment at: http://localhost:5000/patient/book
3. Use YOUR phone number
4. Check your phone for SMS!

You should see in console:
```
✅ REAL SMS SENT via Twilio to +1234567890
   Message SID: SMxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   Status: queued
```

---

## Troubleshooting

### "Twilio not installed"
```bash
pip install twilio
```

### "Invalid credentials"
- Double-check your Account SID and Auth Token
- Make sure there are no extra spaces
- Verify in Twilio Console

### "Phone number not verified" (Trial Account)
- Twilio trial accounts can only send to verified numbers
- Verify your phone in Twilio Console
- Or upgrade to paid account (no trial restrictions)

### "SMS not sending"
Check console output:
- ✅ = SMS sent successfully
- ❌ = Error (check error message)
- 📱 SIMULATION = Still in simulation mode

### Still in Simulation Mode?
1. Check `config.py`: `SMS_ENABLED = True`
2. Check `config.py`: `SMS_PROVIDER = "twilio"`
3. Check credentials are set
4. Restart the app
5. Look for "✅ Twilio SMS client initialized" on startup

---

## Cost Information

### Twilio Pricing
- **Free Trial**: $15 credit
- **SMS Cost**: ~$0.0075 per SMS (varies by country)
- **India**: ~₹0.50 per SMS
- **USA**: ~$0.0075 per SMS
- **Monthly**: ~$1 for 100 SMS

### AWS SNS Pricing
- **First 100 SMS**: Free (monthly)
- **After 100**: $0.00645 per SMS
- Very cost-effective for high volume

---

## For Development/Testing

If you want to keep simulation mode for development but enable real SMS for production:

```python
# config.py
import os

# Use environment variable to control SMS
SMS_ENABLED = os.environ.get("SMS_ENABLED", "False").lower() == "true"
```

Then:
- **Development**: Don't set SMS_ENABLED → Simulation mode
- **Production**: Set `SMS_ENABLED=true` → Real SMS

---

## Quick Reference

### Current Configuration (Simulation Mode)
```python
SMS_ENABLED = False
SMS_PROVIDER = "simulation"
```

### Enable Twilio
```python
SMS_ENABLED = True
SMS_PROVIDER = "twilio"
TWILIO_ACCOUNT_SID = "ACxxxx..."
TWILIO_AUTH_TOKEN = "your_token"
TWILIO_PHONE_NUMBER = "+1234567890"
```

### Enable AWS SNS
```python
SMS_ENABLED = True
SMS_PROVIDER = "aws_sns"
AWS_ACCESS_KEY_ID = "your_key"
AWS_SECRET_ACCESS_KEY = "your_secret"
AWS_REGION = "us-east-1"
```

---

## Summary

✅ **Current**: Simulation mode (prints to console)  
✅ **To Enable**: Set `SMS_ENABLED = True` and configure provider  
✅ **Providers**: Twilio (easiest) or AWS SNS  
✅ **Cost**: Free trial or ~$1 per 100 SMS  
✅ **Time**: 5 minutes to set up

**The SMS system is production-ready - just add your credentials!**
