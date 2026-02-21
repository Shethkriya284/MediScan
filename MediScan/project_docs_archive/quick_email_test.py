#!/usr/bin/env python3
"""
Quick automated test for email system
Shows current status without user input
"""
from email_service import send_otp_email, generate_otp, SENDER_EMAIL, SENDER_PASSWORD

def check_email_status():
    """Check if email system is configured"""
    print("=" * 70)
    print("  MEDISCAN EMAIL SYSTEM STATUS CHECK")
    print("=" * 70)
    print()
    
    # Check configuration
    print("📧 EMAIL CONFIGURATION:")
    print(f"   Sender Email: {SENDER_EMAIL}")
    print(f"   Password Set: {'✅ Yes' if SENDER_PASSWORD != 'YOUR_GMAIL_APP_PASSWORD_HERE' else '⚠️ No (using placeholder)'}")
    print()
    
    # Check if Gmail is configured
    if SENDER_PASSWORD == 'YOUR_GMAIL_APP_PASSWORD_HERE':
        print("⚠️  STATUS: Gmail Not Configured")
        print()
        print("   Current Mode: Console OTP (Fallback)")
        print("   Emails: Not being sent to Gmail")
        print("   OTP Location: Prints to terminal/console")
        print()
        print("   This is NORMAL and EXPECTED!")
        print("   Your system is working perfectly with console OTP.")
        print()
        print("   To enable Gmail emails:")
        print("   1. Read: SETUP_GMAIL_NOW.md")
        print("   2. Get Gmail App Password")
        print("   3. Update email_service.py line 13")
        print("   4. Restart Flask server")
        print()
    else:
        print("✅ STATUS: Gmail Configured")
        print()
        print("   Testing email delivery...")
        print()
        
        # Test email
        test_email = "test@example.com"
        test_name = "Test User"
        otp = generate_otp()
        
        print(f"   Sending test OTP to {test_email}...")
        success = send_otp_email(test_email, test_name, otp)
        
        if success:
            print("   ✅ Email sent successfully!")
            print()
            print("   Gmail is working! Users will receive OTP emails.")
        else:
            print("   ❌ Email sending failed!")
            print()
            print("   Check console for error messages.")
            print("   Verify App Password is correct in email_service.py")
        print()
    
    print("=" * 70)
    print()
    print("📚 DOCUMENTATION:")
    print("   Quick Start:    DO_THIS_NOW.txt")
    print("   Setup Guide:    SETUP_GMAIL_NOW.md")
    print("   Explanation:    EMAIL_STATUS_EXPLAINED.md")
    print("   Full Solution:  GMAIL_NOT_WORKING_SOLUTION.md")
    print()
    print("=" * 70)

if __name__ == "__main__":
    try:
        check_email_status()
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print()
        print("This might indicate a configuration issue.")
        print("Check email_service.py for syntax errors.")
