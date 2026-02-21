#!/usr/bin/env python3
"""
Debug script to check Dr. Rajesh Patel's email in database
"""
import sqlite3

def debug_rajesh_email():
    try:
        # Connect to the database
        conn = sqlite3.connect('instance/mediscan.db')
        cursor = conn.cursor()
        
        # Query to find Dr. Rajesh Patel specifically
        query = """
        SELECT u.id, u.username, u.email, u.role, dp.specialization, dp.hospital
        FROM user u
        LEFT JOIN doctor_profile dp ON u.id = dp.user_id
        WHERE u.username LIKE '%Rajesh%' OR u.email LIKE '%rajesh%'
        """
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        print(f"🔍 DEBUGGING DR. RAJESH PATEL EMAIL")
        print(f"=" * 50)
        
        if results:
            for result in results:
                user_id, username, email, role, spec, hospital = result
                print(f"User ID: {user_id}")
                print(f"Username: '{username}'")
                print(f"Email: '{email}'")
                print(f"Role: {role}")
                print(f"Specialization: {spec}")
                print(f"Hospital: {hospital}")
                print("-" * 30)
        else:
            print("❌ No user found with 'Rajesh' in name or email")
        
        # Also check all doctor emails
        print(f"\n📧 ALL DOCTOR EMAILS IN DATABASE:")
        print("-" * 40)
        
        query2 = """
        SELECT u.username, u.email
        FROM user u
        WHERE u.role = 'doctor'
        ORDER BY u.username
        """
        
        cursor.execute(query2)
        all_doctors = cursor.fetchall()
        
        for name, email in all_doctors:
            print(f"{name}: {email}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    debug_rajesh_email()