#!/usr/bin/env python3
"""
Fix appointments: Remove Sarah Wilson appointments and create Rajesh Patel appointments with current dates
"""
import sqlite3
from datetime import datetime, timedelta

def fix_appointments():
    try:
        # Connect to the database
        conn = sqlite3.connect('instance/mediscan.db')
        cursor = conn.cursor()
        
        print(f"🔧 FIXING APPOINTMENTS DATABASE")
        print(f"=" * 50)
        
        # 1. Check current appointments
        print(f"\n📋 CURRENT APPOINTMENTS:")
        cursor.execute("""
            SELECT a.id, a.patient_id, a.doctor_id, a.date_time, a.status,
                   u.username as patient_name, du.username as doctor_name
            FROM appointment a
            JOIN user u ON a.patient_id = u.id
            JOIN doctor_profile dp ON a.doctor_id = dp.id
            JOIN user du ON dp.user_id = du.id
            ORDER BY a.date_time DESC
        """)
        
        current_appointments = cursor.fetchall()
        print(f"Found {len(current_appointments)} appointments")
        
        for apt in current_appointments:
            apt_id, patient_id, doctor_id, date_time, status, patient_name, doctor_name = apt
            print(f"  ID {apt_id}: {patient_name} → {doctor_name} ({status})")
        
        # 2. Delete all Sarah Wilson appointments
        print(f"\n❌ REMOVING SARAH WILSON APPOINTMENTS:")
        cursor.execute("""
            DELETE FROM appointment 
            WHERE doctor_id IN (
                SELECT dp.id FROM doctor_profile dp 
                JOIN user u ON dp.user_id = u.id 
                WHERE u.username = 'Dr. Sarah Wilson'
            )
        """)
        
        deleted_count = cursor.rowcount
        print(f"Deleted {deleted_count} Sarah Wilson appointments")
        
        # 3. Get patient and Dr. Rajesh Patel IDs
        cursor.execute("SELECT id FROM user WHERE email = 'patient@mediscan.com'")
        patient_result = cursor.fetchone()
        
        cursor.execute("""
            SELECT dp.id FROM doctor_profile dp 
            JOIN user u ON dp.user_id = u.id 
            WHERE u.email = 'rajesh.patel@mediscan.com'
        """)
        doctor_result = cursor.fetchone()
        
        if not patient_result or not doctor_result:
            print("❌ Could not find patient or Dr. Rajesh Patel")
            return False
        
        patient_id = patient_result[0]
        doctor_id = doctor_result[0]
        
        print(f"✅ Found Patient ID: {patient_id}")
        print(f"✅ Found Dr. Rajesh Patel ID: {doctor_id}")
        
        # 4. Create new appointments with current/future dates
        print(f"\n➕ CREATING NEW RAJESH PATEL APPOINTMENTS:")
        
        # Get current date and time
        now = datetime.now()
        
        # Create appointments for different dates
        appointments_to_create = [
            {
                'date': now + timedelta(hours=2),  # Today, 2 hours from now
                'status': 'Scheduled',
                'notes': 'Cardiology consultation - Heart checkup',
                'fee': 750.0
            },
            {
                'date': now + timedelta(days=1, hours=10),  # Tomorrow, 10 AM
                'status': 'Scheduled', 
                'notes': 'Follow-up cardiology consultation',
                'fee': 750.0
            },
            {
                'date': now + timedelta(days=3, hours=14),  # 3 days from now, 2 PM
                'status': 'Scheduled',
                'notes': 'Cardiac stress test consultation',
                'fee': 1000.0
            },
            {
                'date': now - timedelta(days=7),  # 1 week ago (completed)
                'status': 'Completed',
                'notes': 'Initial cardiac evaluation - Completed successfully',
                'fee': 750.0
            },
            {
                'date': now - timedelta(days=14),  # 2 weeks ago (completed)
                'status': 'Completed',
                'notes': 'ECG and blood pressure monitoring - Normal results',
                'fee': 500.0
            }
        ]
        
        created_appointments = []
        
        for i, apt_data in enumerate(appointments_to_create):
            cursor.execute("""
                INSERT INTO appointment (patient_id, doctor_id, date_time, status, notes, consultation_fee)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (patient_id, doctor_id, apt_data['date'], apt_data['status'], apt_data['notes'], apt_data['fee']))
            
            new_apt_id = cursor.lastrowid
            created_appointments.append(new_apt_id)
            
            print(f"  ✅ Created Appointment {new_apt_id}:")
            print(f"     Date: {apt_data['date'].strftime('%Y-%m-%d %H:%M')}")
            print(f"     Status: {apt_data['status']}")
            print(f"     Notes: {apt_data['notes']}")
            print()
        
        # 5. Commit changes
        conn.commit()
        
        # 6. Verify new appointments
        print(f"🔍 VERIFICATION - NEW APPOINTMENTS:")
        cursor.execute("""
            SELECT a.id, a.date_time, a.status, a.notes
            FROM appointment a
            JOIN doctor_profile dp ON a.doctor_id = dp.id
            JOIN user du ON dp.user_id = du.id
            WHERE du.email = 'rajesh.patel@mediscan.com'
            ORDER BY a.date_time DESC
        """)
        
        new_appointments = cursor.fetchall()
        print(f"Found {len(new_appointments)} Dr. Rajesh Patel appointments:")
        
        for apt in new_appointments:
            apt_id, date_time, status, notes = apt
            print(f"  ID {apt_id}: {date_time} - {status}")
            print(f"    Notes: {notes}")
        
        # 7. Count scheduled appointments for video calls
        scheduled_count = len([a for a in new_appointments if a[2] == 'Scheduled'])
        print(f"\n🎥 READY FOR VIDEO CALLS: {scheduled_count} scheduled appointments")
        
        conn.close()
        
        print(f"\n✅ APPOINTMENTS FIXED SUCCESSFULLY!")
        print(f"   • Removed: {deleted_count} Sarah Wilson appointments")
        print(f"   • Created: {len(created_appointments)} Rajesh Patel appointments")
        print(f"   • Scheduled: {scheduled_count} ready for video calls")
        print(f"   • Current date: {now.strftime('%Y-%m-%d %H:%M')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error fixing appointments: {e}")
        return False

if __name__ == "__main__":
    success = fix_appointments()
    if success:
        print(f"\n🎉 Database updated! Patient dashboard will now show Dr. Rajesh Patel appointments.")
        print(f"🌐 Refresh the application: http://127.0.0.1:5002")
    else:
        print(f"\n❌ Failed to update appointments. Check the error above.")