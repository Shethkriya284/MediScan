#!/usr/bin/env python3
"""
Quick script to check if all doctors have been seeded properly
"""
import sqlite3

def check_doctors():
    try:
        # Connect to the database
        conn = sqlite3.connect('instance/mediscan.db')
        cursor = conn.cursor()
        
        # Query to get all doctors with their profiles
        query = """
        SELECT u.username, dp.specialization, dp.hospital, dp.experience, dp.image_url
        FROM user u
        JOIN doctor_profile dp ON u.id = dp.user_id
        WHERE u.role = 'doctor'
        ORDER BY dp.specialization, u.username
        """
        
        cursor.execute(query)
        doctors = cursor.fetchall()
        
        print(f"🏥 MEDISCAN DOCTOR DATABASE VERIFICATION")
        print(f"=" * 60)
        print(f"Total Doctors Found: {len(doctors)}")
        print(f"=" * 60)
        
        # Group by specialization
        specializations = {}
        for doctor in doctors:
            name, spec, hospital, exp, img = doctor
            if spec not in specializations:
                specializations[spec] = []
            specializations[spec].append({
                'name': name,
                'hospital': hospital,
                'experience': exp,
                'image': img
            })
        
        # Display by specialization
        for spec, docs in specializations.items():
            print(f"\n📋 {spec.upper()} ({len(docs)} doctors)")
            print("-" * 40)
            for doc in docs:
                print(f"  👨‍⚕️ {doc['name']}")
                print(f"     🏥 {doc['hospital']}")
                print(f"     📅 {doc['experience']} years experience")
                if doc['image']:
                    print(f"     🖼️  Image: {doc['image'][:50]}...")
                else:
                    print(f"     🖼️  Image: No image")
                print()
        
        # Summary
        print(f"\n📊 SPECIALIZATION SUMMARY:")
        print("-" * 30)
        for spec, docs in specializations.items():
            print(f"  {spec}: {len(docs)} doctors")
        
        conn.close()
        
        return len(doctors)
        
    except Exception as e:
        print(f"❌ Error checking doctors: {e}")
        return 0

if __name__ == "__main__":
    total = check_doctors()
    print(f"\n✅ Database verification complete! {total} doctors found.")