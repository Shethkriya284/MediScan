import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import string

# Configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = 'igor@mediscanapp.com'
SENDER_PASSWORD = 'mediscan123' # Update this with real password
SENDER_NAME = 'MediScan Team'

def generate_otp():
    """Generate a 6-digit OTP"""
    return ''.join(random.choices(string.digits, k=6))

def send_email(to_email, subject, html_content, text_content=None):
    """Send email using Gmail SMTP"""
    try:
        # Create message
        message = MIMEMultipart('alternative')
        message['Subject'] = subject
        message['From'] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
        message['To'] = to_email
        
        # Default text content if not provided
        if not text_content:
            text_content = "Please view this email in a generic HTML compatible client."

        # Attach parts
        part1 = MIMEText(text_content, 'plain')
        part2 = MIMEText(html_content, 'html')
        message.attach(part1)
        message.attach(part2)
        
        # Send via SMTP
        if SENDER_PASSWORD == 'YOUR_GMAIL_APP_PASSWORD_HERE':
            print("[!] Password not configured. Email not sent.")
            return False

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(message)
            
        print(f"[OK] EMAIL SENT to {to_email}: {subject}")
        return True
        
    except Exception as e:
        print(f"[X] Email service error: {str(e)}")
        return False

def send_otp_email(to_email, username, otp_code):
    """Send OTP verification email"""
    subject = "MediScan - Your Verification Code"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; background-color: #f5f7fa; margin: 0; padding: 0; }}
            .container {{ max-width: 600px; margin: 20px auto; background: white; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.05); overflow: hidden; }}
            .header {{ background: linear-gradient(135deg, #2E8B57, #3CB371); color: white; padding: 40px 20px; text-align: center; }}
            .content {{ padding: 40px 30px; text-align: center; }}
            .otp-box {{ background: #f0fdf4; border: 2px dashed #2E8B57; border-radius: 12px; padding: 20px; margin: 30px 0; display: inline-block; min-width: 200px; }}
            .otp-code {{ font-size: 36px; font-weight: 800; color: #2E8B57; letter-spacing: 8px; margin: 10px 0; }}
            .footer {{ background: #f9fafb; padding: 20px; text-align: center; color: #6b7280; font-size: 13px; border-top: 1px solid #e5e7eb; }}
            h1 {{ margin: 0; font-size: 28px; }}
            p {{ color: #4b5563; line-height: 1.6; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🏥 MediScan</h1>
                <p style="color: rgba(255,255,255,0.9); margin-top: 5px;">Your Healthcare Companion</p>
            </div>
            <div class="content">
                <h2>Verify Your Account</h2>
                <p>Hello <strong>{username}</strong>,<br>Use the code below to complete your login or registration.</p>
                
                <div class="otp-box">
                    <span style="font-size: 12px; text-transform: uppercase; letter-spacing: 1px; color: #6b7280;">Verification Code</span>
                    <div class="otp-code">{otp_code}</div>
                    <span style="font-size: 12px; color: #ef4444;">Valid for 10 minutes</span>
                </div>
                
                <p style="font-size: 14px; margin-top: 30px;">
                    <strong>Security Notice:</strong><br>
                    Never share this code with anyone. MediScan staff will never ask for it.
                </p>
            </div>
            <div class="footer">
                <p>© 2026 MediScan Healthcare Platform<br>This is an automated message.</p>
            </div>
        </div>
    </body>
    </html>
    """
    return send_email(to_email, subject, html_content)

def send_welcome_email(to_email, username):
    """Send welcome email"""
    subject = "Welcome to MediScan! 🎉"
    html_content = f"<h1>Welcome {username}!</h1><p>We are glad to have you.</p>"
    return send_email(to_email, subject, html_content)

def send_otp_console(to_email, otp):
    """Fallback to console"""
    print(f"--- [MOCK EMAIL] To: {to_email} | OTP: {otp} ---")
