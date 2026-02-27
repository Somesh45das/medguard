"""
Test SMS configuration and check if real SMS is enabled.
"""
from config import Config

print("\n" + "="*80)
print("SMS CONFIGURATION STATUS")
print("="*80 + "\n")

print(f"SMS Enabled: {Config.SMS_ENABLED}")
print(f"SMS Provider: {Config.SMS_PROVIDER}")
print()

if Config.SMS_ENABLED:
    if Config.SMS_PROVIDER == "twilio":
        print("Twilio Configuration:")
        print(f"  Account SID: {Config.TWILIO_ACCOUNT_SID[:10]}..." if Config.TWILIO_ACCOUNT_SID else "  Account SID: NOT SET")
        print(f"  Auth Token: {'*' * 20}" if Config.TWILIO_AUTH_TOKEN else "  Auth Token: NOT SET")
        print(f"  Phone Number: {Config.TWILIO_PHONE_NUMBER}" if Config.TWILIO_PHONE_NUMBER else "  Phone Number: NOT SET")
        print()
        
        if all([Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN, Config.TWILIO_PHONE_NUMBER]):
            print("✅ Twilio is CONFIGURED - Real SMS will be sent!")
            print()
            print("To test:")
            print("1. Start app: python run.py")
            print("2. Book appointment with YOUR phone number")
            print("3. Check your phone for SMS!")
        else:
            print("⚠️  Twilio is NOT fully configured")
            print()
            print("To enable real SMS:")
            print("1. Sign up at: https://www.twilio.com/try-twilio")
            print("2. Get Account SID, Auth Token, and Phone Number")
            print("3. Update config.py with your credentials")
            print("4. Restart the app")
    
    elif Config.SMS_PROVIDER == "aws_sns":
        print("AWS SNS Configuration:")
        print(f"  Access Key: {Config.AWS_ACCESS_KEY_ID[:10]}..." if Config.AWS_ACCESS_KEY_ID else "  Access Key: NOT SET")
        print(f"  Secret Key: {'*' * 20}" if Config.AWS_SECRET_ACCESS_KEY else "  Secret Key: NOT SET")
        print(f"  Region: {Config.AWS_REGION}")
        print()
        
        if all([Config.AWS_ACCESS_KEY_ID, Config.AWS_SECRET_ACCESS_KEY]):
            print("✅ AWS SNS is CONFIGURED - Real SMS will be sent!")
        else:
            print("⚠️  AWS SNS is NOT fully configured")
    
    else:
        print(f"⚠️  Unknown SMS provider: {Config.SMS_PROVIDER}")
        print("   Valid providers: 'twilio', 'aws_sns', 'simulation'")

else:
    print("📱 SMS is in SIMULATION MODE")
    print()
    print("Messages will print to console instead of sending to phones.")
    print()
    print("To enable real SMS:")
    print("1. Edit config.py")
    print("2. Set SMS_ENABLED = True")
    print("3. Set SMS_PROVIDER = 'twilio' or 'aws_sns'")
    print("4. Add provider credentials")
    print("5. Restart the app")
    print()
    print("See ENABLE_REAL_SMS_GUIDE.md for detailed instructions")

print()
print("="*80)
print("CURRENT MODE: " + ("REAL SMS ✅" if Config.SMS_ENABLED and Config.SMS_PROVIDER != "simulation" else "SIMULATION 📱"))
print("="*80)
