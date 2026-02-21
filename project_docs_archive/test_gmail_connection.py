#!/usr/bin/env python3
"""
Test Gmail SMTP Connection
Diagnose why emails aren't being sent
"""
import smtplib
from email_service import SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD

def test_gmail_connection():
    """Test if Gmail credentials work"""
    print("=" * 70)
    print("  GMAIL CONNECTION TEST")
    print("=" * 70)
    print()
    
    print("📧 Configuration:")
    print(f"   SMTP Server: {SMTP_SERVER}")
    print(f"   SMTP Port: {SMTP_PORT}")
    print(f"   Sender Email: {SENDER_EMAIL}")
    print(f"   Password: {'*' * len(SENDER_PASSWORD)} ({len(SENDER_PASSWORD)} characters)")
    print()
    
    # Check password
    if SENDER_PASSWORD in ['YOUR_16_CHAR_APP_PASSWORD_HERE', 'YOUR_GMAIL_APP_PASSWORD_HERE']:
        print("❌ ERROR: Password is still a placeholder!")
        print()
        print("   You need to set a real Gmail App Password.")
        print("   See: FIX_EMAIL_NOW.md")
        print()
        return False
    
    print("🔍 Testing connection to Gmail...")
    print()
    
    try:
        # Try to connect
        print("   Step 1: Connecting to SMTP server...")
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10)
        print("   ✅ Connected to SMTP server")
        
        print("   Step 2: Starting TLS encryption...")
        server.starttls()
        print("   ✅ TLS encryption started")
        
        print("   Step 3: Logging in with credentials...")
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        print("   ✅ Login successful!")
        
        server.quit()
        print()
        print("=" * 70)
        print("🎉 SUCCESS! Gmail connection works!")
        print("=" * 70)
        print()
        print("Your email system should now send emails to Gmail.")
        print("Try signing up at: http://localhost:5001/auth")
        print()
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"   ❌ Authentication failed!")
        print()
        print("=" * 70)
        print("🚨 PROBLEM: Gmail rejected your credentials")
        print("=" * 70)
        print()
        print(f"Error: {str(e)}")
        print()
        print("📋 Possible Reasons:")
        print("   1. App Password is incorrect")
        print("   2. 2-Factor Authentication not enabled")
        print("   3. App Password was revoked")
        print("   4. Using regular password instead of App Password")
        print()
        print("🔧 Solution:")
        print("   1. Go to: https://myaccount.google.com/security")
        print("   2. Enable 2-Factor Authentication")
        print("   3. Go to: https://myaccount.google.com/apppasswords")
        print("   4. Generate NEW App Password")
        print("   5. Update email_service.py line 13")
        print("   6. Run this test again")
        print()
        print("📚 Detailed Guide: FIX_EMAIL_NOW.md")
        print()
        return False
        
    except smtplib.SMTPException as e:
        print(f"   ❌ SMTP error!")
        print()
        print(f"Error: {str(e)}")
        print()
        print("This might be a network or server issue.")
        print()
        return False
        
    except Exception as e:
        print(f"   ❌ Unexpected error!")
        print()
        print(f"Error: {str(e)}")
        print()
        return False

if __name__ == "__main__":
    try:
        success = test_gmail_connection()
        
        if not success:
            print("=" * 70)
            print("📞 NEXT STEPS:")
            print("=" * 70)
            print()
            print("1. Read: FIX_EMAIL_NOW.md")
            print("2. Enable 2FA on Gmail")
            print("3. Generate App Password")
            print("4. Update email_service.py")
            print("5. Run this test again")
            print()
            print("OR")
            print()
            print("Continue using console OTP (works perfectly for testing)")
            print()
            
    except KeyboardInterrupt:
        print("\n\nTest interrupted.")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
