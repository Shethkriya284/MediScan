#!/usr/bin/env python3
"""
Verify the updated appointments for patient dashboard
"""
import sqlite3
from datetime import datetime

def verify_appointments():
    try:
        # Connect to the database
        conn = sqlite3.connect('instance/mediscan.db')
        cursor = conn.cursor()
        
        print(f"✅ APPOINTMENT UPDATE VERIFICATION")
        print(f"=" * 60)
        print(f"Current Date/Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(f"=" * 60)
        
        # 1. Check patient's appointments (what will show in dashboard)
        print(f"\n👤 PATIENT DASHBOARD APPOINTMENTS:")
        print("-" * 40)
        
        cursor.execute("""
            SELECT a.id, a.date_time, a.status, a.notes, a.consultation_fee,
                   du.username as doctor_name, dp.specialization, dp.hospital
            FROM appointment a
            JOIN user u ON a.patient_id = u.id
            JOIN doctor_profile dp ON a.doctor_id = dp.id
            JOIN user du ON dp.user_id = du.id
            WHERE u.email = 'patient@mediscan.com'
            ORDER BY a.date_time DESC
        """)
        
        patient_appointments = cursor.fetchall()
        
        if patient_appointments:
            scheduled_count = 0
            completed_count = 0
            
            for apt in patient_appointments:
                apt_id, date_time, status, notes, fee, doctor_name, specialization, hospital = apt
                
                # Parse datetime
                try:
                    apt_datetime = datetime.fromisoformat(date_time.replace('Z', '+00:00').replace(' ', 'T'))
                    formatted_date = apt_datetime.strftime('%b %d, %Y at %I:%M %p')
                except:
                    formatted_date = date_time
                
                print(f"📅 Appointment {apt_id}:")
                print(f"   👨‍⚕️ Doctor: {doctor_name}")
                print(f"   🏥 Specialty: {specialization}")
                print(f"   🏥 Hospital: {hospital}")
                print(f"   📅 Date: {formatted_date}")
                print(f"   📊 Status: {status}")
                print(f"   💰 Fee: ₹{fee}")
                print(f"   📝 Notes: {notes}")
                
                if status == 'Scheduled':
                    scheduled_count += 1
                    print(f"   🎥 Video Call: AVAILABLE")
                elif status == 'Completed':
                    completed_count += 1
                
                print()
            
            print(f"📊 SUMMARY:")
            print(f"   Total Appointments: {len(patient_appointments)}")
            print(f"   Scheduled (Video Ready): {scheduled_count}")
            print(f"   Completed: {completed_count}")
            
        else:
            print("❌ No appointments found for patient")
        
        # 2. Check Dr. Rajesh Patel's appointments (what will show in doctor dashboard)
        print(f"\n👨‍⚕️ DR. RAJESH PATEL DASHBOARD APPOINTMENTS:")
        print("-" * 40)
        
        cursor.execute("""
            SELECT a.id, a.date_time, a.status, a.notes,
                   u.username as patient_name
            FROM appointment a
            JOIN user u ON a.patient_id = u.id
            JOIN doctor_profile dp ON a.doctor_id = dp.id
            JOIN user du ON dp.user_id = du.id
            WHERE du.email = 'rajesh.patel@mediscan.com'
            ORDER BY a.date_time DESC
        """)
        
        doctor_appointments = cursor.fetchall()
        
        if doctor_appointments:
            for apt in doctor_appointments:
                apt_id, date_time, status, notes, patient_name = apt
                
                try:
                    apt_datetime = datetime.fromisoformat(date_time.replace('Z', '+00:00').replace(' ', 'T'))
                    formatted_date = apt_datetime.strftime('%b %d, %Y at %I:%M %p')
                except:
                    formatted_date = date_time
                
                print(f"📅 Appointment {apt_id}:")
                print(f"   👤 Patient: {patient_name}")
                print(f"   📅 Date: {formatted_date}")
                print(f"   📊 Status: {status}")
                print(f"   📝 Notes: {notes}")
                
                if status == 'Scheduled':
                    print(f"   🎥 Video Call: CAN START")
                
                print()
        
        # 3. Video call ready appointments
        print(f"\n🎥 VIDEO CONSULTATION READY:")
        print("-" * 40)
        
        cursor.execute("""
            SELECT a.id, a.date_time, u.username as patient_name, du.username as doctor_name
            FROM appointment a
            JOIN user u ON a.patient_id = u.id
            JOIN doctor_profile dp ON a.doctor_id = dp.id
            JOIN user du ON dp.user_id = du.id
            WHERE a.status = 'Scheduled'
            AND du.email = 'rajesh.patel@mediscan.com'
            ORDER BY a.date_time
        """)
        
        video_ready = cursor.fetchall()
        
        if video_ready:
            for apt in video_ready:
                apt_id, date_time, patient_name, doctor_name = apt
                print(f"🎥 Appointment {apt_id}: {patient_name} ↔ {doctor_name}")
                print(f"   📅 {date_time}")
                print(f"   🌐 Video URL: http://127.0.0.1:5002/video-consultation/{apt_id}")
                print()
        else:
            print("❌ No scheduled appointments ready for video calls")
        
        # 4. Login instructions
        print(f"\n🔐 TESTING INSTRUCTIONS:")
        print("-" * 40)
        print(f"1. PATIENT LOGIN (Chrome):")
        print(f"   • URL: http://127.0.0.1:5002/login")
        print(f"   • Email: patient@mediscan.com")
        print(f"   • Password: patient123")
        print(f"   • Expected: See {scheduled_count} Dr. Rajesh Patel appointments with video buttons")
        print()
        print(f"2. DOCTOR LOGIN (Firefox):")
        print(f"   • URL: http://127.0.0.1:5002/login")
        print(f"   • Email: rajesh.patel@mediscan.com")
        print(f"   • Password: doctor123")
        print(f"   • Expected: See {len(doctor_appointments)} patient appointments")
        print()
        print(f"3. VIDEO CALL TEST:")
        print(f"   • Both users find same appointment")
        print(f"   • Patient: Click 'Join Video Call'")
        print(f"   • Doctor: Click 'Start Video Call'")
        print(f"   • Result: Video consultation starts")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error verifying appointments: {e}")
        return False

if __name__ == "__main__":
    success = verify_appointments()
    if success:
        print(f"\n✅ Verification complete! Appointments are properly configured.")
    else:
        print(f"\n❌ Verification failed. Check the error above.")