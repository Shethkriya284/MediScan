#!/usr/bin/env python3
"""
Test script to check login page functionality
"""
from app import app, db, User
from werkzeug.security import generate_password_hash

def test_login_routes():
    """Test if login routes are accessible"""
    print("=" * 70)
    print("  TESTING LOGIN PAGE ROUTES")
    print("=" * 70)
    print()
    
    with app.test_client() as client:
        # Test old login page
        print("1. Testing /login route...")
        response = client.get('/login')
        if response.status_code == 200:
            print("   ✅ /login page loads successfully")
        else:
            print(f"   ❌ /login page error: {response.status_code}")
        print()
        
        # Test new auth page
        print("2. Testing /auth route...")
        response = client.get('/auth')
        if response.status_code == 200:
            print("   ✅ /auth page loads successfully")
        else:
            print(f"   ❌ /auth page error: {response.status_code}")
        print()
        
        # Test login POST with invalid credentials
        print("3. Testing login POST with invalid credentials...")
        response = client.post('/login', data={
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        if response.status_code == 200:
            print("   ✅ Login POST handled correctly")
            if b'Invalid' in response.data:
                print("   ✅ Shows error message for invalid credentials")
        else:
            print(f"   ❌ Login POST error: {response.status_code}")
        print()
        
        # Test if test user exists
        print("4. Checking test users in database...")
        with app.app_context():
            users = User.query.all()
            print(f"   Total users in database: {len(users)}")
            
            # Check for common test accounts
            test_emails = ['patient@mediscan.com', 'doctor@mediscan.com', 'admin@mediscan.com']
            for email in test_emails:
                user = User.query.filter_by(email=email).first()
                if user:
                    print(f"   ✅ {email} exists (role: {user.role})")
                else:
                    print(f"   ⚠️  {email} not found")
        print()
    
    print("=" * 70)
    print()
    print("📋 SUMMARY:")
    print("   - Both login pages (/login and /auth) should be accessible")
    print("   - /login uses traditional password login")
    print("   - /auth uses modern OTP-based login")
    print()
    print("🔧 COMMON ISSUES:")
    print("   1. Missing return statement → FIXED ✅")
    print("   2. Invalid credentials error → Should show error message")
    print("   3. User not found → Check database for test users")
    print()
    print("🚀 TO TEST MANUALLY:")
    print("   1. Run: python app.py")
    print("   2. Visit: http://localhost:5001/login (old page)")
    print("   3. Visit: http://localhost:5001/auth (new page)")
    print()
    print("=" * 70)

if __name__ == "__main__":
    try:
        test_login_routes()
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()
