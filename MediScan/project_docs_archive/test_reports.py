#!/usr/bin/env python3
"""
Test script to verify medical reports functionality
"""
import requests
import json

# Test configuration
BASE_URL = "http://127.0.0.1:5001"
TEST_CREDENTIALS = {
    "email": "patient@mediscan.com",
    "password": "patient123"
}

def test_reports_system():
    """Test the medical reports system"""
    session = requests.Session()
    
    print("🔍 Testing Medical Reports System...")
    print("=" * 50)
    
    # Test 1: Login
    print("1. Testing login...")
    login_response = session.post(f"{BASE_URL}/login", data=TEST_CREDENTIALS)
    if login_response.status_code == 200:
        print("✅ Login successful")
    else:
        print(f"❌ Login failed: {login_response.status_code}")
        return
    
    # Test 2: Access reports page
    print("2. Testing reports page access...")
    reports_response = session.get(f"{BASE_URL}/reports")
    if reports_response.status_code == 200:
        print("✅ Reports page accessible")
        # Check if page contains expected content
        if "Medical Reports" in reports_response.text:
            print("✅ Reports page contains correct content")
        else:
            print("⚠️  Reports page missing expected content")
    else:
        print(f"❌ Reports page failed: {reports_response.status_code}")
    
    # Test 3: Check if there are any appointments to generate reports from
    print("3. Checking for available reports...")
    if "No Medical Reports Available" in reports_response.text:
        print("ℹ️  No reports available - this is expected for new users")
        print("   Reports are generated from completed appointments")
    elif "Total Reports" in reports_response.text:
        print("✅ Reports are available")
        
        # Try to find a view button and test it
        import re
        view_links = re.findall(r'/reports/view/(\d+)', reports_response.text)
        if view_links:
            appointment_id = view_links[0]
            print(f"4. Testing report view for appointment {appointment_id}...")
            
            view_response = session.get(f"{BASE_URL}/reports/view/{appointment_id}")
            if view_response.status_code == 200:
                print("✅ Report view working")
                if "MEDICAL REPORT" in view_response.text:
                    print("✅ Report contains medical data")
                else:
                    print("⚠️  Report missing medical content")
            else:
                print(f"❌ Report view failed: {view_response.status_code}")
            
            print(f"5. Testing report download for appointment {appointment_id}...")
            download_response = session.get(f"{BASE_URL}/reports/download/{appointment_id}")
            if download_response.status_code == 200:
                print("✅ Report download working")
                if "Content-Disposition" in download_response.headers:
                    print("✅ Download headers set correctly")
                else:
                    print("⚠️  Download headers missing")
            else:
                print(f"❌ Report download failed: {download_response.status_code}")
    
    print("\n" + "=" * 50)
    print("✅ Medical Reports System Test Complete!")
    print("\nTo test with actual reports:")
    print("1. Login as patient@mediscan.com / patient123")
    print("2. Book appointments with doctors")
    print("3. Have admin/doctor mark appointments as 'Completed'")
    print("4. Check /reports page for generated reports")

if __name__ == "__main__":
    try:
        test_reports_system()
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Flask app. Make sure it's running on port 5001")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")