#!/usr/bin/env python3
"""
Fix today's appointment to be Scheduled instead of Completed
"""
import sqlite3
from datetime import datetime

def fix_today_appointment():
    try:
        conn = sqlite3.connect('instance/mediscan.db')
        cursor = conn.cursor()
        
        print("🔧 FIXING TODAY'S APPOINTMENT STATUS")
        print("=" * 40)
        
        # Update appointment 15 (today's appointment) to be Scheduled
        cursor.execute("""
            UPDATE appointment 
            SET status = 'Scheduled'
            WHERE id = 15
        """)
        
        if cursor.rowcount > 0:
            print("✅ Updated Appointment 15 status to 'Scheduled'")
        else:
            print("❌ No appointment found with ID 15")
        
        # Also create one more appointment for today (later time) to have more video call options
        cursor.execute("SELECT id FROM user WHERE email = 'patient@mediscan.com'")
        patient_id = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT dp.id FROM doctor_profile dp 
            JOIN user u ON dp.user_id = u.id 
            WHERE u.email = 'rajesh.patel@mediscan.com'
        """)
        doctor_id = cursor.fetchone()[0]
        
        # Create appointment for today evening
        today_evening = datetime.now().replace(hour=17, minute=0, second=0, microsecond=0)
        
        cursor.execute("""
            INSERT INTO appointment (patient_id, doctor_id, date_time, status, notes, consultation_fee)
            VALUES (?, ?, ?, 'Scheduled', 'Emergency cardiology consultation - Chest pain evaluation', 1200.0)
        """, (patient_id, doctor_id, today_evening))
        
        new_apt_id = cursor.lastrowid
        print(f"✅ Created new appointment {new_apt_id} for today evening")
        
        conn.commit()
        
        # Verify the changes
        print("\n📋 UPDATED SCHEDULED APPOINTMENTS:")
        cursor.execute("""
            SELECT a.id, a.date_time, a.status, a.notes
            FROM appointment a
            JOIN doctor_profile dp ON a.doctor_id = dp.id
            JOIN user du ON dp.user_id = du.id
            WHERE du.email = 'rajesh.patel@mediscan.com'
            AND a.status = 'Scheduled'
            ORDER BY a.date_time
        """)
        
        scheduled = cursor.fetchall()
        for apt in scheduled:
            apt_id, date_time, status, notes = apt
            print(f"  🎥 Appointment {apt_id}: {date_time} - {status}")
            print(f"     Notes: {notes}")
        
        conn.close()
        
        print(f"\n✅ APPOINTMENTS FIXED!")
        print(f"   • Total scheduled appointments: {len(scheduled)}")
        print(f"   • All ready for video calls")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    fix_today_appointment()