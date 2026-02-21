#!/usr/bin/env python3
"""
Check if there are appointments that can generate medical reports
"""
from app import app, db, User, Appointment, DoctorProfile
from datetime import datetime, timedelta
import random

def check_and_create_sample_data():
    """Check existing data and create sample appointments if needed"""
    with app.app_context():
        print("🔍 Checking Medical Reports Data...")
        print("=" * 50)
        
        # Check users
        patients = User.query.filter_by(role='patient').all()
        doctors = User.query.filter_by(role='doctor').all()
        
        print(f"📊 Found {len(patients)} patients and {len(doctors)} doctors")
        
        # Check appointments
        appointments = Appointment.query.all()
        completed_appointments = Appointment.query.filter_by(status='Completed').all()
        
        print(f"📅 Found {len(appointments)} total appointments")
        print(f"✅ Found {len(completed_appointments)} completed appointments")
        
        if len(completed_appointments) == 0:
            print("\n🔧 Creating sample completed appointments for testing...")
            
            # Get a patient and doctor
            patient = User.query.filter_by(email='patient@mediscan.com').first()
            doctor_profile = DoctorProfile.query.first()
            
            if patient and doctor_profile:
                # Create 3 completed appointments
                for i in range(3):
                    days_ago = random.randint(7, 30)  # 1-4 weeks ago
                    appointment_date = datetime.utcnow() - timedelta(days=days_ago)
                    
                    appointment = Appointment(
                        patient_id=patient.id,
                        doctor_id=doctor_profile.id,
                        date_time=appointment_date,
                        status='Completed',
                        consultation_fee=500.0,
                        notes=f'Sample consultation {i+1} - completed for testing reports'
                    )
                    db.session.add(appointment)
                
                db.session.commit()
                print("✅ Created 3 sample completed appointments")
                
                # Verify creation
                new_completed = Appointment.query.filter_by(status='Completed').all()
                print(f"📊 Now have {len(new_completed)} completed appointments")
            else:
                print("❌ Could not find patient or doctor to create sample appointments")
        
        print("\n📋 Sample Report Data:")
        if completed_appointments or len(Appointment.query.filter_by(status='Completed').all()) > 0:
            sample_appointment = Appointment.query.filter_by(status='Completed').first()
            if sample_appointment:
                print(f"   Patient: {sample_appointment.patient_id}")
                print(f"   Doctor: {sample_appointment.doctor_profile.user.username if sample_appointment.doctor_profile else 'Unknown'}")
                print(f"   Date: {sample_appointment.date_time}")
                print(f"   Status: {sample_appointment.status}")
                
                # Test report generation
                from app import generate_medical_report
                try:
                    report_data = generate_medical_report(sample_appointment)
                    print(f"   Report ID: {report_data['report_id']}")
                    print(f"   Diagnosis: {report_data['diagnosis']}")
                    print("✅ Report generation working correctly")
                except Exception as e:
                    print(f"❌ Report generation failed: {e}")
        
        print("\n" + "=" * 50)
        print("✅ Data Check Complete!")
        print("\nTo test reports:")
        print("1. Go to http://127.0.0.1:5001/login")
        print("2. Login with: patient@mediscan.com / patient123")
        print("3. Navigate to Reports section")
        print("4. Click View/Download buttons on available reports")

if __name__ == "__main__":
    check_and_create_sample_data()