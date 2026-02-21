#!/usr/bin/env python3
"""
Test script for MediScan Email OTP System
"""
from email_service import send_otp_email, generate_otp, send_welcome_email, send_otp_console

def test_otp_email():
    """Test sending OTP email"""
    print("🧪 Testing OTP Email System\n")
    
    # Generate OTP
    otp = generate_otp()
    print(f"Generated OTP: {otp}")
    
    # Test email
    test_email = input("Enter test email address: ").strip()
    test_name = input("Enter test name: ").strip() or "Test User"
    
    print(f"\n📧 Sending OTP to {test_email}...")
    
    # Try sending email
    success = send_otp_email(test_email, test_name, otp)
    
    if success:
        print("✅ Email sent successfully!")
        print(f"Check {test_email} for the OTP")
    else:
        print("❌ Email sending failed!")
        print("Displaying OTP in console instead:")
        send_otp_console(test_email, otp)
    
    return success

def test_welcome_email():
    """Test sending welcome email"""
    print("\n🧪 Testing Welcome Email\n")
    
    test_email = input("Enter test email address: ").strip()
    test_name = input("Enter test name: ").strip() or "Test User"
    
    print(f"\n📧 Sending welcome email to {test_email}...")
    
    success = send_welcome_email(test_email, test_name)
    
    if success:
        print("✅ Welcome email sent successfully!")
    else:
        print("❌ Welcome email sending failed!")
    
    return success

def main():
    """Main test function"""
    print("=" * 60)
    print("  MEDISCAN EMAIL SYSTEM TEST")
    print("=" * 60)
    
    while True:
        print("\nSelect test:")
        print("1. Test OTP Email")
        print("2. Test Welcome Email")
        print("3. Test Both")
        print("4. Exit")
        
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == '1':
            test_otp_email()
        elif choice == '2':
            test_welcome_email()
        elif choice == '3':
            test_otp_email()
            test_welcome_email()
        elif choice == '4':
            print("\n👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice!")
        
        print("\n" + "=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Test interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
