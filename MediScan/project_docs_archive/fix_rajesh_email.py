#!/usr/bin/env python3
"""
Fix Dr. Rajesh Patel's email to match the intended email
"""
import sqlite3

def fix_rajesh_email():
    try:
        # Connect to the database
        conn = sqlite3.connect('instance/mediscan.db')
        cursor = conn.cursor()
        
        # Update Dr. Rajesh Patel's email
        update_query = """
        UPDATE user 
        SET email = 'rajesh.patel@mediscan.com'
        WHERE username = 'Dr. Rajesh Patel' AND email = 'doctor@mediscan.com'
        """
        
        cursor.execute(update_query)
        rows_affected = cursor.rowcount
        
        if rows_affected > 0:
            conn.commit()
            print(f"✅ Successfully updated Dr. Rajesh Patel's email!")
            print(f"   Old email: doctor@mediscan.com")
            print(f"   New email: rajesh.patel@mediscan.com")
            
            # Verify the change
            verify_query = """
            SELECT username, email FROM user WHERE username = 'Dr. Rajesh Patel'
            """
            cursor.execute(verify_query)
            result = cursor.fetchone()
            
            if result:
                name, email = result
                print(f"\n🔍 Verification:")
                print(f"   Name: {name}")
                print(f"   Email: {email}")
        else:
            print("❌ No rows were updated. Dr. Rajesh Patel not found or email already correct.")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error fixing email: {e}")

if __name__ == "__main__":
    fix_rajesh_email()