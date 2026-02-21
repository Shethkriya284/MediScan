from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import random
import string
import os
import numpy as np
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- Application Configuration ---
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mediscan-secret-key-123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mediscan.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Session configuration
app.config['SESSION_COOKIE_NAME'] = 'mediscan_session'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Email Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'igor@mediscanapp.com'
app.config['MAIL_PASSWORD'] = 'mediscan123'
app.config['MAIL_DEFAULT_SENDER'] = 'MediScan Team <igor@mediscanapp.com>'

# File Upload Configuration
app.config['UPLOAD_FOLDER'] = 'static/uploads/profile_pics'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'jfif', 'avif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']



# Initialize Extensions
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth'

# --- Helper Functions ---
app.jinja_env.globals.update(getattr=getattr)

def generate_otp():
    """Generate a 6-digit OTP"""
    return ''.join(random.choices(string.digits, k=6))

# --- Email Service Class ---

class EmailService:
    """
    Centralized Email Service for MediScan
    Handles OTPs, Notifications, and Reminders using SMTP
    """
    
    @staticmethod
    def send_email(to_email, subject, html_content, text_content=None):
        """Send email using Gmail SMTP"""
        try:
            sender_email = app.config['MAIL_USERNAME']
            sender_password = app.config['MAIL_PASSWORD']
            
            # Create message
            message = MIMEMultipart('alternative')
            message['Subject'] = subject
            message['From'] = f"MediScan Team <{sender_email}>"
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
            with smtplib.SMTP(app.config['MAIL_SERVER'], app.config['MAIL_PORT']) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(message)
                
            # print(f"[OK] EMAIL SENT to {to_email}: {subject}")
            return True
            
        except Exception as e:
            # print(f"[X] Email service error: {str(e)}")
            # Fallback to console for development/demo
            # print(f"--- [MOCK EMAIL] To: {to_email} | Subject: {subject} ---")
            return False

    @staticmethod
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
        return EmailService.send_email(to_email, subject, html_content)

    @staticmethod
    def send_welcome_email(to_email, username):
        """Send welcome email after registration"""
        subject = "Welcome to MediScan! 🎉"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: 'Segoe UI', Arial, sans-serif; background-color: #f5f7fa; margin: 0; padding: 0; }}
                .container {{ max-width: 600px; margin: 20px auto; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }}
                .header {{ background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; padding: 40px; text-align: center; }}
                .content {{ padding: 40px; }}
                .feature-item {{ background: #f0f9ff; padding: 15px; border-radius: 8px; margin-bottom: 10px; border-left: 4px solid #4facfe; }}
                .button {{ display: inline-block; padding: 12px 30px; background: #4facfe; color: white; text-decoration: none; border-radius: 25px; font-weight: bold; margin-top: 20px; }}
                .footer {{ background: #f9fafb; padding: 20px; text-align: center; color: #9ca3af; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Welcome Aboard! 🚀</h1>
                </div>
                <div class="content">
                    <h2>Hello {username},</h2>
                    <p>We're thrilled to have you join the MediScan family! Your journey to smarter, proactive healthcare starts now.</p>
                    
                    <h3 style="margin-top: 30px;">What you can do:</h3>
                    <div class="feature-item"><strong>📅 Book Appointments</strong> - Connect with top specialists instantly</div>
                    <div class="feature-item"><strong>💊 Medicine Tracker</strong> - Never miss a dose again</div>
                    
                    <div style="text-align: center; margin-top: 30px;">
                        <a href="http://127.0.0.1:5001/dashboard" class="button">Go to Dashboard</a>
                    </div>
                </div>
                <div class="footer">
                    © 2026 MediScan Healthcare Platform
                </div>
            </div>
        </body>
        </html>
        """
        return EmailService.send_email(to_email, subject, html_content)
    
    @staticmethod
    def send_appointment_confirmation(to_email, username, doctor_name, appointment_date, appointment_time):
        """Send appointment confirmation email"""
        subject = "Appointment Confirmed ✅ - MediScan"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: 'Segoe UI', Arial, sans-serif; background-color: #f5f5f5; }}
                .container {{ max-width: 600px; margin: 20px auto; background: white; border-radius: 12px; padding: 0; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
                .header {{ background: #10b981; color: white; padding: 30px; text-align: center; }}
                .content {{ padding: 40px; }}
                .details-card {{ background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 10px; padding: 25px; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Appointment Confirmed</h1>
                </div>
                <div class="content">
                    <p>Hello <strong>{username}</strong>,</p>
                    <p>Your appointment has been successfully scheduled.</p>
                    
                    <div class="details-card">
                        <h3 style="margin-top: 0; color: #166534;">Appointment Details</h3>
                        <p><strong>Doctor:</strong> {doctor_name}</p>
                        <p><strong>Date:</strong> {appointment_date}</p>
                        <p><strong>Time:</strong> {appointment_time}</p>
                    </div>
                    
                    <p>Please arrive 10 minutes early. Bring your ID and any previous medical records.</p>
                </div>
            </div>
        </body>
        </html>
        """
        return EmailService.send_email(to_email, subject, html_content)

    @staticmethod
    def send_health_reminder(to_email, username, reminder_type, message):
        """Send health reminder email"""
        subject = f"🔔 Health Reminder: {reminder_type}"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <body>
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e5e7eb; border-radius: 10px;">
                <h2 style="color: #d97706;">Running Low / Health Alert</h2>
                <p>Hello {username},</p>
                <div style="background: #fffbeb; padding: 15px; border-left: 4px solid #d97706; margin: 15px 0;">
                    <strong>{reminder_type}:</strong> {message}
                </div>
                <p>Stay healthy!</p>
                <p style="color: #9ca3af; font-size: 12px;">MediScan Automated Alerts</p>
            </div>
        </body>
        </html>
        """
        return EmailService.send_email(to_email, subject, html_content)

    @staticmethod
    def send_doctor_credentials(to_email, username, password):
        """Send credentials to newly added doctor"""
        subject = "Welcome Dr. to MediScan - Your Login Credentials"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: 'Segoe UI', Arial, sans-serif; background-color: #f5f7fa; }}
                .container {{ max-width: 600px; margin: 20px auto; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }}
                .header {{ background: #166534; color: white; padding: 30px; text-align: center; }}
                .content {{ padding: 40px; }}
                .credentials-box {{ background: #f0fdf4; border: 1px dashed #166534; border-radius: 8px; padding: 20px; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Welcome to MediScan</h1>
                    <p>Doctor Portal Access</p>
                </div>
                <div class="content">
                    <p>Hello <strong>Dr. {username}</strong>,</p>
                    <p>Your account has been created by the administrator. Please use the following credentials to login:</p>
                    
                    <div class="credentials-box">
                        <p><strong>Email:</strong> {to_email}</p>
                        <p><strong>Temporary Password:</strong> {password}</p>
                    </div>
                    
                    <p>Please login and change your password immediately.</p>
                    
                    <div style="text-align: center; margin-top: 30px;">
                        <a href="http://127.0.0.1:5001/auth" style="background: #166534; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; font-weight: bold;">Login to Dashboard</a>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        return EmailService.send_email(to_email, subject, html_content)

    @staticmethod
    def send_prescription_email(to_email, username, doctor_name, diagnosis, medications, notes):
        """Send prescription email to patient"""
        subject = f"Prescription from {doctor_name} - MediScan"
        
        meds_html = ""
        for med in medications:
            meds_html += f"""
            <div style="background: #f0f9ff; padding: 10px; margin-bottom: 10px; border-radius: 5px; border-left: 3px solid #0ea5e9;">
                <p style="margin: 0; font-weight: bold; color: #0369a1;">{med.get('name', '')}</p>
                <p style="margin: 5px 0 0 0; font-size: 0.9em; color: #555;">
                    {med.get('dosage', '')} • {med.get('instructions', '')}
                </p>
            </div>
            """

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: 'Segoe UI', Arial, sans-serif; background-color: #f5f7fa; }}
                .container {{ max-width: 600px; margin: 20px auto; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }}
                .header {{ background: #2563eb; color: white; padding: 30px; text-align: center; }}
                .content {{ padding: 40px; }}
                .section {{ margin-bottom: 25px; }}
                .label {{ font-size: 0.8em; text-transform: uppercase; color: #6b7280; font-weight: bold; margin-bottom: 5px; display: block; }}
                .value {{ font-size: 1.1em; color: #1f2937; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>💊 Digital Prescription</h1>
                    <p>Consultation with {doctor_name}</p>
                </div>
                <div class="content">
                    <p>Hello <strong>{username}</strong>,</p>
                    <p>Here is the digital prescription from your recent video consultation.</p>
                    
                    <div style="background: #f8fafc; padding: 20px; border-radius: 10px; border: 1px solid #e2e8f0;">
                        <div class="section">
                            <span class="label">Diagnosis</span>
                            <div class="value">{diagnosis}</div>
                        </div>
                        
                        <div class="section">
                            <span class="label">Prescribed Medications</span>
                            {meds_html}
                        </div>
                        
                        <div class="section">
                            <span class="label">Additional Notes</span>
                            <div class="value">{notes}</div>
                        </div>
                    </div>
                    
                    <p style="font-size: 0.9em; color: #6b7280; margin-top: 20px;">
                        You can also view this prescription in your MediScan dashboard.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        return EmailService.send_email(to_email, subject, html_content)



# --- Database Models ---

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True)
    password_hash = db.Column(db.String(128))
    otp_code = db.Column(db.String(6))
    otp_expiry = db.Column(db.DateTime)
    role = db.Column(db.String(20), nullable=False, default='patient') # patient, doctor, admin
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Profile Fields
    profile_image = db.Column(db.String(200))
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(10))
    blood_group = db.Column(db.String(5))
    is_online = db.Column(db.Boolean, default=True)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    patient_profile = db.relationship('PatientProfile', backref='user', uselist=False, cascade="all, delete-orphan")
    doctor_profile = db.relationship('DoctorProfile', backref='user', uselist=False, cascade="all, delete-orphan")
    health_metrics = db.relationship('HealthMetric', backref='user', cascade="all, delete-orphan")
    
    # Wallet & Rewards
    wallet_balance = db.Column(db.Float, default=0.0)
    rewards = db.relationship('UserReward', backref='user', lazy=True, cascade="all, delete-orphan")
    subscriptions = db.relationship('UserSubscription', backref='user', lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class UserReward(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reward_type = db.Column(db.String(50), nullable=False) # Cashback, Coupon, BetterLuck
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, default=0.0) # For cashback
    is_scratched = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class PatientProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    age = db.Column(db.Integer)
    medical_history = db.Column(db.Text)
    
    # Personal Details
    marital_status = db.Column(db.String(20))
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    emergency_contact = db.Column(db.String(20))
    
    # Medical Details (Extended)
    allergies = db.Column(db.Text)
    current_medications = db.Column(db.Text)
    past_medications = db.Column(db.Text)
    chronic_diseases = db.Column(db.Text)
    injuries = db.Column(db.Text)
    surgeries = db.Column(db.Text)
    
    # Lifestyle Details
    smoking_habits = db.Column(db.String(50))
    alcohol_consumption = db.Column(db.String(50))
    activity_level = db.Column(db.String(50))
    food_preference = db.Column(db.String(50))
    occupation = db.Column(db.String(100))

class DoctorProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    hospital = db.Column(db.String(100), nullable=False)
    experience = db.Column(db.Integer)
    image_url = db.Column(db.String(200))
    is_available = db.Column(db.Boolean, default=True)

class Medicine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    usage = db.Column(db.Text, nullable=False)
    age_group = db.Column(db.String(50))
    side_effects = db.Column(db.Text)
    description = db.Column(db.Text)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor_profile.id'), nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    consultation_type = db.Column(db.String(20), default='video')  # video, clinic, home
    time_slot = db.Column(db.String(20))  # e.g., "10:00 AM"
    status = db.Column(db.String(20), default='Scheduled')  # Scheduled, Completed, Cancelled
    payment_status = db.Column(db.String(20), default='Pending')  # Pending, Paid, Failed
    payment_method = db.Column(db.String(20))  # UPI, Card, NetBanking, Wallet
    transaction_id = db.Column(db.String(100))
    notes = db.Column(db.Text)
    consultation_fee = db.Column(db.Float, default=500.0)
    
    doctor_profile = db.relationship('DoctorProfile', backref='appointments', foreign_keys=[doctor_id])
    patient = db.relationship('User', backref='appointments', foreign_keys=[patient_id])
    video_prescription = db.relationship('VideoPrescription', backref='appointment', uselist=False, cascade="all, delete-orphan")

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class HealthMetric(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    heart_rate = db.Column(db.Integer)
    blood_pressure_systolic = db.Column(db.Integer)
    blood_pressure_diastolic = db.Column(db.Integer)
    temperature = db.Column(db.Float)
    weight = db.Column(db.Float)
    sleep_hours = db.Column(db.Float)
    recorded_date = db.Column(db.DateTime, default=datetime.utcnow)

class Dependent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    relation = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    blood_group = db.Column(db.String(10))
    date_of_birth = db.Column(db.Date)
    
    # Medical Details
    allergies = db.Column(db.Text)
    current_medications = db.Column(db.Text)
    past_medications = db.Column(db.Text)
    chronic_diseases = db.Column(db.Text)
    injuries = db.Column(db.Text)
    surgeries = db.Column(db.Text)

    prescriptions = db.relationship('Prescription', backref='dependent', lazy=True, cascade="all, delete-orphan")

class Prescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dependent_id = db.Column(db.Integer, db.ForeignKey('dependent.id'), nullable=False)
    medicine_name = db.Column(db.String(100), nullable=False)
    dosage = db.Column(db.String(50))
    frequency_per_day = db.Column(db.Integer, default=1)
    schedule_time = db.Column(db.String(100))
    current_stock = db.Column(db.Integer, default=0)
    last_refill_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def days_remaining(self):
        if self.frequency_per_day > 0:
            return self.current_stock // self.frequency_per_day
        return 0

class VideoPrescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'), nullable=False)
    diagnosis = db.Column(db.Text)
    medications = db.Column(db.Text)  # Stored as JSON string
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Offer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    price = db.Column(db.String(20))
    original_price = db.Column(db.String(20))
    discount_label = db.Column(db.String(20))
    background_gradient = db.Column(db.String(100)) # e.g., "linear-gradient(...)"
    expiry_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='active') # active, inactive
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserSubscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    offer_id = db.Column(db.Integer, db.ForeignKey('offer.id'), nullable=True) # Optional link to Offer
    plan_title = db.Column(db.String(100), nullable=False) # Store title in case Offer is deleted
    price_paid = db.Column(db.String(20))
    purchase_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Active') # Active, Expired

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Logic Functions ---

def analyze_symptoms_logic(symptoms_list):
    """
    Core AI Logic for Symptom Checker
    Analyses list of symptoms and returns probable conditions with confidence scores.
    """
    symptoms_list = [s.lower().strip() for s in symptoms_list]
    
    # Knowledge Base: Condition -> {Required, Associated, Severity}
    knowledge_base = {
        'Viral Fever': {'required': {'fever'}, 'associated': {'chills', 'body ache', 'fatigue'}, 'severity': 'Low'},
        'Migraine': {'required': {'headache'}, 'associated': {'nausea', 'sensitiv', 'throbbing'}, 'severity': 'Medium'},
        'COVID-19': {'required': {'fever', 'cough'}, 'associated': {'test', 'smell', 'breath'}, 'severity': 'High'},
        'Gastritis': {'required': {'stomach'}, 'associated': {'bloating', 'gas', 'vomiting'}, 'severity': 'Low'},
        'Cardiac Issue': {'required': {'chest pain'}, 'associated': {'breath', 'sweating', 'arm'}, 'severity': 'Critical'}
    }

    results = []
    
    for condition, data in knowledge_base.items():
        score = 0
        req_match = 0
        
        # Check required symptoms
        for req in data['required']:
            if any(req in s for s in symptoms_list):
                score += 50
                req_match += 1
        
        # Check associated symptoms
        for assoc in data['associated']:
            if any(assoc in s for s in symptoms_list):
                score += 10
        
        # Calculate confidence
        if req_match > 0:
            total_possible = 50 * len(data['required']) + 10 * len(data['associated'])
            confidence = min(int((score / total_possible) * 100), 99)
            if confidence > 30:
                results.append({
                    'condition': condition,
                    'confidence': confidence,
                    'severity': data['severity']
                })
    
    results.sort(key=lambda x: x['confidence'], reverse=True)
    return results if results else [{'condition': 'Unknown - Please Consult Doctor', 'confidence': 0, 'severity': 'Low'}]

def generate_medical_report(appointment):
    """
    Generates a realistic medical report based on appointment data and doctor specialization.
    Returns a dictionary structured for the report templates.
    """
    doctor_name = appointment.doctor_profile.user.username if appointment.doctor_profile else "Dr. August"
    specialization = appointment.doctor_profile.specialization if appointment.doctor_profile else "General Physician"
    patient_name = appointment.patient.username if appointment.patient else "Patient"
    
    # Base data
    report_data = {
        'report_id': f"REP-{appointment.id}-{random.randint(1000, 9999)}",
        'generated_date': appointment.date_time.strftime('%B %d, %Y'),
        'patient_name': patient_name,
        'patient_id': f"PAT-{appointment.patient_id}",
        'doctor_name': doctor_name,
        'hospital': appointment.doctor_profile.hospital if appointment.doctor_profile else "MediScan Multi-speciality Hospital",
        'symptoms': [],
        'diagnosis': "General Health Checkup",
        'vital_signs': {
            'heart_rate': "72 bpm",
            'blood_pressure': "120/80 mmHg",
            'temperature': "98.6 °F",
            'weight': "70 kg"
        },
        'tests_conducted': ["Physical Examination"],
        'medications': [],
        'recommendations': ["Stay hydrated", "Regular exercise"],
        'next_appointment': "In 3 months for follow-up"
    }
    
    # Customize based on specialization
    spec = specialization.lower()
    if 'cardio' in spec:
        report_data['diagnosis'] = "Mild Hypertension"
        report_data['symptoms'] = ["Occasional chest tightness", "Shortness of breath during exertion"]
        report_data['tests_conducted'] += ["ECG", "Lipid Profile"]
        report_data['medications'] = [{'name': 'Amlodipine', 'dosage': '5mg', 'frequency': 'Once daily'}]
        report_data['recommendations'] = ["Reduce salt intake", "Daily 30-min walk", "Avoid stress"]
    elif 'ortho' in spec:
        report_data['diagnosis'] = "Minor Muscle Strain"
        report_data['symptoms'] = ["Joint pain", "Swelling in lower back"]
        report_data['tests_conducted'] += ["X-Ray", "Physical Mobility Test"]
        report_data['medications'] = [{'name': 'Ibuprofen', 'dosage': '400mg', 'frequency': 'Twice daily after meals'}]
        report_data['recommendations'] = ["Apply warm compress", "Avoid heavy lifting", "Physiotherapy twice a week"]
    elif 'derm' in spec:
        report_data['diagnosis'] = "Contact Dermatitis"
        report_data['symptoms'] = ["Skin redness", "Itching", "Localised rash"]
        report_data['tests_conducted'] += ["Skin Patch Test"]
        report_data['medications'] = [{'name': 'Hydrocortisone cream', 'dosage': '1%', 'frequency': 'Apply twice daily'}]
        report_data['recommendations'] = ["Avoid trigger allergens", "Use mild soap", "Keep skin hydrated"]
    elif 'pediat' in spec:
        report_data['diagnosis'] = "Post-Vaccination Recovery"
        report_data['symptoms'] = ["Mild fever", "Loss of appetite"]
        report_data['tests_conducted'] = ["Weight & Height tracking", "Vaccination update"]
        report_data['medications'] = [{'name': 'Paracetamol drops', 'dosage': '0.5ml', 'frequency': 'If fever > 100°F'}]
        report_data['recommendations'] = ["Rest", "Fluid intake", "Monitor temperature"]
    else:
        # Default/General
        report_data['diagnosis'] = "Routine Wellness Check"
        report_data['symptoms'] = ["None reported"]
        report_data['medications'] = [{'name': 'Multivitamin', 'dosage': '1 tab', 'frequency': 'Daily after breakfast'}]

    # Override with appointment notes if available
    if appointment.notes and len(appointment.notes) > 10:
        report_data['diagnosis'] = appointment.notes.split('.')[0] # Use first sentence as diagnosis
        
    return report_data

def check_stock_alerts(user):
    """Checks prescription stock for user's dependents and creates notifications"""
    dependents = Dependent.query.filter_by(user_id=user.id).all()
    alerts = []
    
    for dep in dependents:
        for script in dep.prescriptions:
            days = script.days_remaining()
            if days <= 2:
                msg = f"Low Stock Alert: {script.medicine_name} for {dep.name} will run out in {days} days!"
                existing = Notification.query.filter_by(user_id=user.id, message=msg, is_read=False).first()
                if not existing:
                    notif = Notification(user_id=user.id, message=msg)
                    db.session.add(notif)
                    alerts.append(msg)
    
    if alerts:
        db.session.commit()

# --- Routes ---

@app.route('/')
def index():
    # create table if not exists (lazy migration)
    try:
        db.create_all() 
    except:
        pass
        
    offers = Offer.query.filter_by(status='active').order_by(Offer.created_at.desc()).all()
    return render_template('index.html', offers=offers)

# --- Authentication Routes ---

@app.route('/login', methods=['GET'])
@app.route('/auth', methods=['GET'])
def auth():
    """Modern Unified Auth Page with Animation"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    response = make_response(render_template('auth.html'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/google-login', methods=['GET', 'POST'])
def google_login():
    """Mock Google Login Flow"""
    if request.method == 'POST':
        # Simulate Google User Authentication
        email = request.form.get('email')
        password = request.form.get('password') # In a real app, verify this!
        
        # For this mock, we accept any password since we can't check Google's DB
        # We just check if the email exists in OUR system or create it
        
        user = User.query.filter_by(email=email).first()
        
        if not user:
            # Create a new user if not exists (Auto-signup via Google)
            username = email.split('@')[0].replace('.', ' ').title()
            user = User(
                username=username, 
                email=email, 
                role='patient',
                password_hash=generate_password_hash('google_dummy_password') # Dummy password for internal record
            )
            db.session.add(user)
            db.session.commit()
            
            # Create profile
            if not user.patient_profile:
                db.session.add(PatientProfile(user_id=user.id))
                db.session.commit()
                
        login_user(user)
        flash(f'Welcome, {user.username}! Signed in with Google.', 'success')
        return redirect(url_for('dashboard'))

    return render_template('mock_google_login.html')

@app.route('/login', methods=['POST'])
def login():
    """Handle traditional email/password login"""
    try:
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Please provide both email and password', 'error')
            return redirect(url_for('auth'))
        
        user = User.query.filter((User.email == email) | (User.phone == email)).first()
        
        if user and user.check_password(password):
            login_user(user)
            user.last_seen = datetime.utcnow()
            db.session.commit()
            
            # Ensure patient profile exists
            if user.role == 'patient' and not user.patient_profile:
                try:
                    db.session.add(PatientProfile(user_id=user.id))
                    db.session.commit()
                except:
                    pass
            
            flash('Login successful!', 'success')
            return redirect_based_on_role(user)
        else:
            flash('Invalid email or password', 'error')
            return redirect(url_for('auth'))
            
    except Exception as e:
        flash(f'Login failed: {str(e)}', 'error')
        return redirect(url_for('auth'))

@app.route('/old-login', methods=['GET', 'POST'])
def old_login():
    if request.method == 'GET':
        session.pop('_flashes', None)
    
    if request.method == 'POST':
        # OTP Login Verification
        if 'otp' in request.form:
            email_or_phone = request.form.get('email_or_phone')
            otp_input = request.form.get('otp')
            
            user = User.query.filter((User.email == email_or_phone) | (User.phone == email_or_phone)).first()
            
            if user and user.otp_code == otp_input and user.otp_expiry > datetime.utcnow():
                login_user(user)
                user.last_seen = datetime.utcnow()
                user.otp_code = None
                db.session.commit()
                flash('Login successful!', 'success')
                return redirect_based_on_role(user)
            else:
                flash('Invalid or Expired OTP', 'error')
                return render_template('verify_otp.html', email_or_phone=email_or_phone)

        # Standard Login or OTP Request
        email_or_phone = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter((User.email == email_or_phone) | (User.phone == email_or_phone)).first()
        
        if password: # Password Login
            if user and user.check_password(password):
                login_user(user)
                user.last_seen = datetime.utcnow()
                db.session.commit()
                flash('Login successful!', 'success')
                return redirect_based_on_role(user)
            else:
                flash('Invalid credentials', 'error')
        else: # OTP Request Logic
            if user:
                otp = generate_otp()
                user.otp_code = otp
                user.otp_expiry = datetime.utcnow() + timedelta(minutes=10)
                db.session.commit()
                
                if "@" in email_or_phone:
                    EmailService.send_otp_email(user.email, user.username, otp)
                    flash(f'OTP sent to {user.email}. Code: {otp}', 'success')
                else:
                    flash(f'OTP Sent to Phone: {otp} (Demo)', 'success')
                
                return render_template('verify_otp.html', email_or_phone=email_or_phone)
            else:
                flash('User not found', 'error')

    return render_template('login.html')

@app.route('/signup', methods=['POST'])
def signup():
    try:
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        phone = request.form.get('phone')
        
        if User.query.filter((User.email==email) | (User.username==username)).first():
            flash('User already exists', 'error')
            return redirect(url_for('auth'))
            
        new_user = User(username=username, email=email, phone=phone, role='patient')
        new_user.set_password(password)
        
        # Generate OTP for verification
        otp = generate_otp()
        new_user.otp_code = otp
        new_user.otp_expiry = datetime.utcnow() + timedelta(minutes=10)
        
        db.session.add(new_user)
        db.session.commit()
        
        # Create Patient Profile
        db.session.add(PatientProfile(user_id=new_user.id))
        db.session.commit()
        
        # Send OTP
        EmailService.send_otp_email(email, username, otp)
        
        session['pending_verification_email'] = email
        session['show_otp_verify'] = True
        flash(f'Account created! OTP Code: {otp}', 'success')
        
        return redirect(url_for('auth'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Registration failed: {str(e)}', 'error')
        return redirect(url_for('auth'))

@app.route('/admin/add-doctor', methods=['POST'])
@login_required
def add_doctor():
    if current_user.role != 'admin':
        flash('Unauthorized access', 'error')
        return redirect(url_for('index'))
        
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        specialization = request.form.get('specialization')
        hospital = request.form.get('hospital')
        
        # Check if user exists
        if User.query.filter_by(email=email).first():
            flash('User with this email already exists', 'error')
            return redirect(url_for('admin_dashboard'))
            
        # Generate temporary password
        temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        
        # Create User
        new_doctor = User(username=name, email=email, role='doctor')
        new_doctor.set_password(temp_password)
        db.session.add(new_doctor)
        db.session.commit()
        
        # Create Doctor Profile
        doctor_profile = DoctorProfile(
            user_id=new_doctor.id,
            specialization=specialization,
            hospital=hospital,
            experience=0, # Default
            is_available=True
        )
        db.session.add(doctor_profile)
        db.session.commit()
        
        # Send Email
        EmailService.send_doctor_credentials(email, name, temp_password)
        
        flash(f'Doctor added successfully! Credentials sent to {email}', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding doctor: {str(e)}', 'error')
        
    return redirect(url_for('admin_dashboard'))

@app.route('/reset-password', methods=['POST'])
@login_required
def reset_password():
    try:
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if not current_user.check_password(current_password):
            flash('Incorrect current password', 'error')
            return redirect(request.referrer)
            
        if new_password != confirm_password:
            flash('New passwords do not match', 'error')
            return redirect(request.referrer)
            
        current_user.set_password(new_password)
        db.session.commit()
        flash('Password updated successfully!', 'success')
        
    except Exception as e:
        flash(f'Error updating password: {str(e)}', 'error')
        
    return redirect(request.referrer)

def redirect_based_on_role(user):
    if user.role == 'admin': return redirect(url_for('admin_dashboard'))
    if user.role == 'doctor': return redirect(url_for('doctor_dashboard'))
    return redirect(url_for('patient_dashboard'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# --- Main Dashboard Routes ---

@app.route('/dashboard')
@login_required
def dashboard():
    check_stock_alerts(current_user)
    return redirect_based_on_role(current_user)

@app.route('/patient_dashboard')
@login_required
def patient_dashboard():
    if current_user.role != 'patient': return redirect(url_for('dashboard'))
    
    # Ensure patient profile exists
    if not current_user.patient_profile:
        try:
            db.session.add(PatientProfile(user_id=current_user.id))
            db.session.commit()
        except:
            pass
    
    try:
        appointments = Appointment.query.filter_by(patient_id=current_user.id).all()
    except:
        appointments = []
    
    # Generate Dynamic Notifications
    notifications = []
    
    # 1. Appointment Reminders
    if appointments:
        upcoming = [a for a in appointments if a.status == 'Scheduled']
        for appt in upcoming:
            doc_name = appt.doctor_profile.user.username if appt.doctor_profile else 'Doctor'
            notifications.append({
                'message': f"Upcoming Appointment: Dr. {doc_name} on {appt.date_time.strftime('%b %d')}",
                'timestamp': appt.date_time - timedelta(days=1), # Simulate reminder 1 day before
                'type': 'appointment'
            })
            
    # Sort by timestamp (newest first)
    notifications.sort(key=lambda x: x['timestamp'], reverse=True)

    # 2. Medication/Health Tips (ALWAYS PIN TO TOP)
    health_tips = [
        "Stay hydrated! Aim for 8 glasses of water today.",
        "Take a 10-minute walk to boost your circulation.",
        "Don't forget to take your vitamins after lunch!",
        "Screen time break: Look away every 20 minutes.",
        "Get enough sleep tonight for better immunity."
    ]
    today_seed = int(datetime.utcnow().strftime('%Y%m%d'))
    tip_index = today_seed % len(health_tips)
    
    # Insert at 0 to ensure it's always visible
    notifications.insert(0, {
        'message': f"Daily Health Tip: {health_tips[tip_index]}",
        'timestamp': datetime.utcnow(),
        'type': 'tip'
    })
    
    completed = [a for a in appointments if a.status == 'Completed']
    health_score = int((len(completed)/len(appointments)*100)) if appointments else 85
    
    # Fetch active offers for "Available Plans" section
    offers = Offer.query.filter_by(status='active').all()

    # Fetch active subscriptions
    active_plans = [sub for sub in current_user.subscriptions if sub.status == 'Active']

    return render_template('patient_dashboard.html', 
                         appointments=appointments,
                         notifications=notifications,
                         health_score=health_score,
                         reports_count=len(completed),
                         consultations_count=len(appointments),
                         offers=offers,
                         active_plans=active_plans)

@app.route('/doctor_dashboard')
@login_required
def doctor_dashboard():
    if current_user.role != 'doctor': return redirect(url_for('dashboard'))
    
    doc = current_user.doctor_profile
    today = datetime.utcnow().date()
    
    today_appts = Appointment.query.filter_by(doctor_id=doc.id).filter(db.func.date(Appointment.date_time) == today).all()
    all_appts = Appointment.query.filter_by(doctor_id=doc.id).order_by(Appointment.date_time.desc()).all()
    
    stats = {
        'today_appointments': len(today_appts),
        'total_patients': len(set([a.patient_id for a in all_appts])),
        'completed_consultations': len([a for a in all_appts if a.status == 'Completed']),
        'pending_appointments': len([a for a in all_appts if a.status == 'Scheduled' or a.status == 'In Progress'])
    }
    
    return render_template('doctor_dashboard.html', 
                         doctor_profile=doc,
                         today_appointments=today_appts,
                         appointments=all_appts,
                         stats=stats)

@app.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    try:
        # User Basic Info
        # Handle Image Upload
        if 'profile_image' in request.files:
            file = request.files['profile_image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                upload_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
                os.makedirs(upload_path, exist_ok=True)
                file.save(os.path.join(upload_path, filename))
                current_user.profile_image = url_for('static', filename='uploads/profile_pics/' + filename)
                db.session.commit() # Atomic commit for image
                # print(f"[OK] Profile image committed: {current_user.profile_image}")
        elif request.form.get('profile_image_url'):
             current_user.profile_image = request.form.get('profile_image_url')
             db.session.commit()

        # Robust Date Parsing
        dob_str = request.form.get('date_of_birth')
        if dob_str:
            try:
                current_user.date_of_birth = datetime.strptime(dob_str, '%Y-%m-%d')
            except (ValueError, TypeError):
                pass # Keep current or set to None implicitly if malformed

        current_user.blood_group = request.form.get('blood_group')
        current_user.gender = request.form.get('gender')
        
        # Ensure Patient Profile exists
        if not current_user.patient_profile:
            new_profile = PatientProfile(user_id=current_user.id)
            db.session.add(new_profile)
            db.session.commit()
            
        profile = current_user.patient_profile
        
        # Personal Details with Robust Float Parsing
        profile.marital_status = request.form.get('marital_status')
        
        try:
            height_str = request.form.get('height')
            profile.height = float(height_str) if height_str and height_str.strip() else None
        except ValueError:
            pass

        try:
            weight_str = request.form.get('weight')
            profile.weight = float(weight_str) if weight_str and weight_str.strip() else None
        except ValueError:
            pass

        profile.emergency_contact = request.form.get('emergency_contact', '')
        
        # Medical Details
        profile.allergies = request.form.get('allergies', '')
        profile.current_medications = request.form.get('current_medications', '')
        profile.past_medications = request.form.get('past_medications', '')
        profile.chronic_diseases = request.form.get('chronic_diseases', '')
        profile.injuries = request.form.get('injuries', '')
        profile.surgeries = request.form.get('surgeries', '')
        
        # Lifestyle Details
        profile.smoking_habits = request.form.get('smoking_habits', '')
        profile.alcohol_consumption = request.form.get('alcohol_consumption', '')
        profile.activity_level = request.form.get('activity_level', '')
        profile.food_preference = request.form.get('food_preference', '')
        profile.occupation = request.form.get('occupation', '')
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating profile: {str(e)}', 'error')
        # print(f"[X] Profile Update Error: {str(e)}")
        
    return redirect(url_for('profile'))

@app.route('/profile')
@login_required
def profile():
    if not current_user.patient_profile:
        # Create if missing
        try:
            db.session.add(PatientProfile(user_id=current_user.id))
            db.session.commit()
        except:
            pass
            
    # Get latest health metric for the health summary card
    latest_metric = HealthMetric.query.filter_by(user_id=current_user.id).order_by(HealthMetric.recorded_date.desc()).first()
    
    return render_template('profile.html', latest_metric=latest_metric)

# --- Feature Routes ---

@app.route('/lab-analysis', methods=['GET', 'POST'])
@login_required
def lab_analysis():
    analysis_result = None
    if request.method == 'POST':
        report_type = request.form.get('report_type')
        # Simulate AI analysis based on report type
        if report_type == 'Blood Test':
            analysis_result = {
                'severity': 'Normal',
                'report_type': 'Complete Blood Count (CBC)',
                'message': 'All parameters are within normal biological reference ranges.',
                'color': 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
                'icon': 'fa-check-circle',
                'recommendations': ['Continue balanced diet', 'Stay hydrated', 'Regular annual checkups']
            }
        elif report_type == 'X-Ray':
            analysis_result = {
                'severity': 'Action Required',
                'report_type': 'Chest X-Ray',
                'message': 'Minor congestion noted in the lower lobe of the left lung.',
                'color': 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)',
                'icon': 'fa-exclamation-triangle',
                'recommendations': ['Consult a pulmonologist', 'Avoid cold beverages', 'Deep breathing exercises']
            }
        else:
            analysis_result = {
                'severity': 'Healthy',
                'report_type': report_type,
                'message': 'Initial AI screening indicates no immediate cause for concern.',
                'color': 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)',
                'icon': 'fa-info-circle',
                'recommendations': ['Maintain healthy lifestyle', 'Monitor any new symptoms']
            }
    return render_template('lab_analysis.html', analysis_result=analysis_result)



@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/about')
def about():
    # Fetch real statistics for "Why Choose Us" section
    users_count = User.query.count()
    doctors_count = User.query.filter_by(role='doctor').count()
    patients_count = User.query.filter_by(role='patient').count()
    hospitals_count = 15 # Placeholder or count unique hospitals from doctors
    
    return render_template('about.html', 
                         users_count=users_count, 
                         doctors_count=doctors_count, 
                         patients_count=patients_count, 
                         hospitals_count=hospitals_count)

@app.route('/dr_august_ai')
def dr_august_ai():
    return render_template('dr_august_ai.html')

@app.route('/medicine_tracker')
@login_required
def medicine_tracker():
    return render_template('medicine_tracker.html')

@app.route('/reports')
@login_required
def reports():
    # Only show completed appointments as reports
    completed_appointments = Appointment.query.filter_by(patient_id=current_user.id, status='Completed').order_by(Appointment.date_time.desc()).all()
    return render_template('reports.html', appointments=completed_appointments)

@app.route('/consultations')
@login_required
def consultations():
    try:
        # Fetch all appointments for user
        appointments = Appointment.query.filter_by(patient_id=current_user.id).order_by(Appointment.date_time.desc()).all()
        
        # Calculate last 6 months (current month + past 5)
        today = datetime.now()
        chart_labels = []
        chart_data = []
        
        # Iterate backwards from current month (0 to 5)
        # But for graph left-to-right, we want oldest first.
        # So range(5, -1, -1) -> 5 months ago, 4 months ago ... 0 months ago (current)
        for i in range(5, -1, -1):
            # Calculate year and month for 'i' months ago
            year = today.year
            month = today.month - i
            while month <= 0:
                month += 12
                year -= 1
                
            month_name = datetime(year, month, 1).strftime('%b')
            chart_labels.append(month_name)
            
            # Count appointments in this specific month/year
            count = 0
            for appt in appointments:
                if appt.date_time.year == year and appt.date_time.month == month:
                    count += 1
            chart_data.append(count)
                
        return render_template('consultations.html', appointments=appointments, chart_data=chart_data, chart_labels=chart_labels)
    except Exception as e:
        # print(f"Error in consultations: {e}")
        # import traceback
        # traceback.print_exc()
        return f"An error occurred: {str(e)}", 500

@app.route('/dependents', methods=['GET', 'POST'])
@login_required
def dependents():
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            relation = request.form.get('relation')
            age = int(request.form.get('age', 0))
            
            new_dep = Dependent(user_id=current_user.id, name=name, relation=relation, age=age)
            db.session.add(new_dep)
            db.session.commit()
            flash(f'Added {name} to your family records.', 'success')
        except Exception as e:
            flash(f'Error adding family member: {str(e)}', 'error')
        return redirect(url_for('dependents'))

    # GET logic
    deps = Dependent.query.filter_by(user_id=current_user.id).all()
    
    total_meds = 0
    low_stock = 0
    for dep in deps:
        total_meds += len(dep.prescriptions)
        for p in dep.prescriptions:
            if p.current_stock <= (p.frequency_per_day * 3): # Less than 3 days remaining
                low_stock += 1
                
    return render_template('dependents.html', dependents=deps, total_medications=total_meds, low_stock_count=low_stock)

@app.route('/delete_dependent/<int:id>', methods=['POST'])
@login_required
def delete_dependent(id):
    dep = Dependent.query.get_or_404(id)
    if dep.user_id != current_user.id:
        return redirect(url_for('dashboard'))
        
    db.session.delete(dep)
    db.session.commit()
    flash('Family member removed.', 'success')
    return redirect(url_for('dependents'))

@app.route('/health_tracker', methods=['GET', 'POST'])
@login_required
def health_tracker():
    if request.method == 'POST':
        metric = HealthMetric(
            user_id=current_user.id,
            heart_rate=request.form.get('heart_rate') or None,
            blood_pressure_systolic=request.form.get('bp_systolic') or None,
            blood_pressure_diastolic=request.form.get('bp_diastolic') or None,
            temperature=request.form.get('temperature') or None,
            weight=request.form.get('weight') or None,
            sleep_hours=request.form.get('sleep_hours') or None
        )
        db.session.add(metric)
        db.session.commit()
        flash('Health metrics recorded!', 'success')
    
    metrics = HealthMetric.query.filter_by(user_id=current_user.id).order_by(HealthMetric.recorded_date.desc()).all()
    latest_metric = metrics[0] if metrics else None
    
    # Calculate health score
    health_score = 85  # Default score
    if latest_metric:
        score = 100
        # Deduct points for abnormal values
        if latest_metric.heart_rate and (latest_metric.heart_rate < 60 or latest_metric.heart_rate > 100):
            score -= 10
        if latest_metric.blood_pressure_systolic and (latest_metric.blood_pressure_systolic < 90 or latest_metric.blood_pressure_systolic > 140):
            score -= 15
        if latest_metric.temperature and (latest_metric.temperature < 36.1 or latest_metric.temperature > 37.2):
            score -= 10
        if latest_metric.sleep_hours and latest_metric.sleep_hours < 6:
            score -= 15
        health_score = max(score, 0)
    
    # Prepare chart data - ensure we have data or provide defaults
    if metrics:
        # Get last 6 months of data (approximately 180 days)
        recent_metrics = list(reversed(metrics[-180:]))
        weight_data = [float(m.weight) if m.weight else 0 for m in recent_metrics]
        heart_rate_data = [int(m.heart_rate) if m.heart_rate else 0 for m in recent_metrics]
        bp_systolic_data = [int(m.blood_pressure_systolic) if m.blood_pressure_systolic else 0 for m in recent_metrics]
        bp_diastolic_data = [int(m.blood_pressure_diastolic) if m.blood_pressure_diastolic else 0 for m in recent_metrics]
        sleep_data = [float(m.sleep_hours) if m.sleep_hours else 0 for m in recent_metrics]
        # Create Month labels - group by 30-day periods
        num_months = min(6, (len(recent_metrics) // 30) + 1)
        dates = [f'Month {i+1}' for i in range(num_months)] if num_months > 0 else ['Month 1']
        # Average data by month for cleaner display
        if len(recent_metrics) > 6:
            # Group into 6 months
            month_size = len(recent_metrics) // 6
            weight_data = [sum(weight_data[i:i+month_size]) / month_size for i in range(0, len(weight_data), month_size)][:6]
            heart_rate_data = [sum(heart_rate_data[i:i+month_size]) / month_size for i in range(0, len(heart_rate_data), month_size)][:6]
            bp_systolic_data = [sum(bp_systolic_data[i:i+month_size]) / month_size for i in range(0, len(bp_systolic_data), month_size)][:6]
            bp_diastolic_data = [sum(bp_diastolic_data[i:i+month_size]) / month_size for i in range(0, len(bp_diastolic_data), month_size)][:6]
            sleep_data = [sum(sleep_data[i:i+month_size]) / month_size for i in range(0, len(sleep_data), month_size)][:6]
            dates = ['Month 1', 'Month 2', 'Month 3', 'Month 4', 'Month 5', 'Month 6']
    else:
        # Default empty data for charts with 6 months
        weight_data = [0] * 6
        heart_rate_data = [0] * 6
        bp_systolic_data = [0] * 6
        bp_diastolic_data = [0] * 6
        sleep_data = [0] * 6
        dates = ['Month 1', 'Month 2', 'Month 3', 'Month 4', 'Month 5', 'Month 6']
    
    return render_template('health_tracker.html', 
                         metrics=metrics,
                         latest_metric=latest_metric,
                         health_score=health_score,
                         weight_data=weight_data,
                         heart_rate_data=heart_rate_data,
                         bp_systolic_data=bp_systolic_data,
                         bp_diastolic_data=bp_diastolic_data,
                         sleep_data=sleep_data,
                         dates=dates)

@app.route('/video_consultation')
@app.route('/video_consultation', methods=['GET'])
@app.route('/video_consultation/<int:appointment_id>', methods=['GET'])
@login_required
def video_consultation(appointment_id=None):
    appointment = None
    doctor = None
    patient = None
    
    if appointment_id:
        appointment = Appointment.query.get(appointment_id)
        if appointment:
            doctor = appointment.doctor_profile
            patient = User.query.get(appointment.patient_id)
    
    # If no appointment, use defaults for demo
    if not doctor:
        doctor = DoctorProfile.query.first()
    
    if not patient:
        patient = current_user if current_user.role == 'patient' else User.query.filter_by(role='patient').first()
    
    return render_template('video_consultation.html', 
                         appointment=appointment, 
                         doctor=doctor,
                         patient=patient)

@app.route('/medicine_detail/<int:id>')
def medicine_detail(id):
    med = Medicine.query.get_or_404(id)
    return render_template('medicine_detail.html', medicine=med)


@app.route('/prevention')
def prevention():
    return render_template('prevention.html')



@app.route('/email_settings')
@login_required
def email_settings():
    return render_template('email_settings.html')

@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('dashboard'))
    
    # --- Statistics ---
    total_users = User.query.count()
    total_doctors = User.query.filter_by(role='doctor').count()
    total_patients = User.query.filter_by(role='patient').count()
    total_appointments = Appointment.query.count()
    
    # Completion Rate (Mock logic or real if status exists)
    completed_appts = Appointment.query.filter_by(status='Completed').count()
    completion_rate = round((completed_appts / total_appointments * 100) if total_appointments > 0 else 0, 1)
    
    # Growth Rate (Mock logic for now, or compare to last month)
    growth_rate = 12.5 # Placeholder
    
    stats = {
        'total_users': total_users,
        'total_doctors': total_doctors,
        'total_patients': total_patients,
        'total_appointments': total_appointments,
        'completion_rate': completion_rate,
        'growth_rate': growth_rate,
        'user_retention': 85  # Mock retention rate
    }
    
    # --- System Health (Mock Data) ---
    system_health = {
        'server_uptime': '99.9%',
        'response_time': '120ms',
        'active_sessions': '42',
        'database_size': '1.2 GB',
        'daily_api_calls': 12500
    }
    
    # --- Graphs Data (Simulated for Demo Purposes but scaled to real totals) ---
    
    # 1. User Growth (Last 6 Months)
    # Simulate a growth curve ending at current totals
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    user_growth = []
    
    # Scale factors to create a realistic looking curve ending at current counts
    for i, month in enumerate(months):
        ratio = (i + 1) / len(months)
        user_growth.append({
            'month': month,
            'total': int(total_users * ratio), 
            'patients': int(total_patients * ratio),
            'doctors': int(total_doctors * ratio)
        })
        
    # 2. Revenue Growth (Mock Data)
    revenue_growth = [
        {'month': 'Jan', 'revenue': 12000, 'commission': 1200},
        {'month': 'Feb', 'revenue': 15000, 'commission': 1500},
        {'month': 'Mar', 'revenue': 18000, 'commission': 1800},
        {'month': 'Apr', 'revenue': 22000, 'commission': 2200},
        {'month': 'May', 'revenue': 28000, 'commission': 2800},
        {'month': 'Jun', 'revenue': 35000, 'commission': 3500},
    ]

    # 3. Geographic Data (Mock)
    geographic_data = [
        {'state': 'Maharashtra', 'users': 120},
        {'state': 'Delhi', 'users': 85},
        {'state': 'Karnataka', 'users': 70},
        {'state': 'Gujarat', 'users': 50},
        {'state': 'Others', 'users': 45}
    ]
    
    # 4. Feature Usage (Mock)
    feature_usage = [
        {'feature': 'AI Assessment', 'usage': 85},
        {'feature': 'Doctor Consult', 'usage': 65},
        {'feature': 'Medicine Tracker', 'usage': 45},
        {'feature': 'Lab Reports', 'usage': 30},
        {'feature': 'Health Blog', 'usage': 25}
    ]
    
    # --- Lists ---
    offers = Offer.query.filter_by(status='active').order_by(Offer.created_at.desc()).all()
    recent_users = User.query.order_by(User.created_date.desc()).limit(5).all()
    recent_appointments = Appointment.query.order_by(Appointment.date_time.desc()).limit(5).all()
    
    return render_template('admin_dashboard.html', 
                         stats=stats, 
                         system_health=system_health,
                         offers=offers,
                         recent_users=recent_users,
                         recent_appointments=recent_appointments,
                         user_growth=user_growth,
                         revenue_growth=revenue_growth,
                         geographic_data=geographic_data,
                         feature_usage=feature_usage)

@app.route('/health_analytics')
@login_required
def health_analytics():
    metrics = HealthMetric.query.filter_by(user_id=current_user.id).order_by(HealthMetric.recorded_date.desc()).all()
    
    # Prepare chart data for analytics
    weight_data = [float(m.weight) if m.weight else 0 for m in reversed(metrics[-30:])]
    heart_rate_data = [int(m.heart_rate) if m.heart_rate else 0 for m in reversed(metrics[-30:])]
    bp_systolic_data = [int(m.blood_pressure_systolic) if m.blood_pressure_systolic else 0 for m in reversed(metrics[-30:])]
    bp_diastolic_data = [int(m.blood_pressure_diastolic) if m.blood_pressure_diastolic else 0 for m in reversed(metrics[-30:])]
    sleep_data = [float(m.sleep_hours) if m.sleep_hours else 0 for m in reversed(metrics[-30:])]
    temp_data = [float(m.temperature) if m.temperature else 0 for m in reversed(metrics[-30:])]
    dates = [m.recorded_date.strftime('%m/%d') for m in reversed(metrics[-30:])]
    
    # Calculate averages
    avg_heart_rate = int(np.mean([m.heart_rate for m in metrics if m.heart_rate])) if any(m.heart_rate for m in metrics) else 0
    avg_bp_systolic = int(np.mean([m.blood_pressure_systolic for m in metrics if m.blood_pressure_systolic])) if any(m.blood_pressure_systolic for m in metrics) else 0
    avg_weight = round(np.mean([m.weight for m in metrics if m.weight]), 1) if any(m.weight for m in metrics) else 0
    avg_sleep = round(np.mean([m.sleep_hours for m in metrics if m.sleep_hours]), 1) if any(m.sleep_hours for m in metrics) else 0
    
    return render_template('health_analytics.html', 
                         metrics=metrics,
                         weight_data=weight_data,
                         heart_rate_data=heart_rate_data,
                         bp_systolic_data=bp_systolic_data,
                         bp_diastolic_data=bp_diastolic_data,
                         sleep_data=sleep_data,
                         temp_data=temp_data,
                         dates=dates,
                         avg_heart_rate=avg_heart_rate,
                         avg_bp_systolic=avg_bp_systolic,
                         avg_weight=avg_weight,
                         avg_sleep=avg_sleep)

@app.route('/doctor_update_appointment_status/<int:appointment_id>', methods=['POST'])
@login_required
def doctor_update_appointment_status(appointment_id):
    if current_user.role != 'doctor': return redirect(url_for('dashboard'))
    appt = Appointment.query.get_or_404(appointment_id)
    appt.status = request.form.get('status', 'Scheduled')
    db.session.commit()
    flash(f'Appointment status updated to {appt.status}', 'success')
    return redirect(url_for('doctor_dashboard'))

@app.route('/download_report/<int:appointment_id>')
@login_required
def download_report(appointment_id):
    appt = Appointment.query.get_or_404(appointment_id)
    # Ensure user owns this report
    if appt.patient_id != current_user.id:
        flash('Unauthorized access to report!', 'danger')
        return redirect(url_for('reports'))
    
    report_data = generate_medical_report(appt)
    return render_template('report_pdf.html', report=report_data, appointment=appt)

@app.route('/view_report/<int:appointment_id>')
@login_required
def view_report(appointment_id):
    appt = Appointment.query.get_or_404(appointment_id)
    # Ensure user owns this report or is the doctor
    if appt.patient_id != current_user.id and (not current_user.doctor_profile or appt.doctor_id != current_user.doctor_profile.id):
        flash('Unauthorized access to report!', 'danger')
        return redirect(url_for('reports'))
    
    report_data = generate_medical_report(appt)
    return render_template('view_report.html', appointment=appt, report=report_data)

@app.route('/send_test_email')
@login_required
def send_test_email():
    EmailService.send_otp_email(current_user.email, current_user.username, '123456')
    flash('Test email sent!', 'success')
    return redirect(url_for('email_settings'))

@app.route('/book_appointment_page')
@login_required
def book_appointment_page():
    return redirect(url_for('doctors'))

@app.route('/medicines')
def medicines():
    query = request.args.get('q', '')
    if query:
        # Prioritize "Starts With", then "Contains"
        starts_with = Medicine.query.filter(Medicine.name.ilike(f'{query}%')).all()
        contains = Medicine.query.filter(Medicine.name.ilike(f'%{query}%')).all()
        
        # Combine and remove duplicates, maintaining order
        meds_dict = {m.id: m for m in starts_with}
        for m in contains:
            if m.id not in meds_dict:
                meds_dict[m.id] = m
        meds = list(meds_dict.values())
    else:
        meds = Medicine.query.limit(20).all()
    return render_template('medicines.html', medicines=meds, query=query)

@app.route('/doctors')
@login_required
def doctors():
    query = request.args.get('q', '')
    
    if query:
        # Join with User to search by username
        doctors_list = DoctorProfile.query.join(User).filter(
            (User.username.ilike(f'%{query}%')) | 
            (DoctorProfile.specialization.ilike(f'%{query}%')) | 
            (DoctorProfile.hospital.ilike(f'%{query}%'))
        ).all()
        flash(f'Found {len(doctors_list)} results for "{query}"', 'info')
    else:
        doctors_list = DoctorProfile.query.all()
        
    # Group by specialization
    grouped = {}
    for d in doctors_list:
        if d.specialization not in grouped: grouped[d.specialization] = []
        grouped[d.specialization].append(d)
    return render_template('doctors.html', doctors_by_spec=grouped, search_query=query)

@app.route('/doctors/category/<category>')
@login_required
def doctors_by_category(category):
    doctors = DoctorProfile.query.filter_by(specialization=category).all()
    return render_template('doctors.html', doctors_by_spec={category: doctors}, selected_category=category)

@app.route('/search')
def search():
    query = request.args.get('q', '').strip()
    
    if not query:
        return redirect(url_for('index'))
    
    results = {
        'doctors': [],
        'medicines': [],
        'services': []
    }
    
    # 1. Search Doctors (Name, Specialization, Hospital)
    results['doctors'] = DoctorProfile.query.join(User).filter(
        (User.username.ilike(f'%{query}%')) | 
        (DoctorProfile.specialization.ilike(f'%{query}%')) | 
        (DoctorProfile.hospital.ilike(f'%{query}%'))
    ).all()
    
    # 2. Search Medicines (Name, Usage)
    results['medicines'] = Medicine.query.filter(
        (Medicine.name.ilike(f'%{query}%')) | 
        (Medicine.usage.ilike(f'%{query}%'))
    ).all()
    
    # 3. Search Static Services (Hardcoded)
    services_db = [
        {'name': 'Find Doctors', 'url': url_for('doctors'), 'description': 'Search and book appointments with specialists.', 'keywords': 'doctor appointment consult specialist'},
        {'name': 'Medicine Tracker', 'url': url_for('medicines'), 'description': 'Track your medicine stock and refills.', 'keywords': 'medicine pill stock refill pharmacy'},
        {'name': 'Dr. August AI', 'url': url_for('dr_august_ai'), 'description': 'Chat with our AI medical assistant.', 'keywords': 'chat ai bot help assistant'},

        {'name': 'Health Analytics', 'url': url_for('health_tracker'), 'description': 'Track your vitals and health metrics.', 'keywords': 'health tracker metrics weight bp heart'},
        {'name': 'Family Health Analysis', 'url': url_for('dependents'), 'description': 'Manage health records for your family.', 'keywords': 'family health dependents kids parents'},
    ]
    
    for service in services_db:
        if query.lower() in service['name'].lower() or query.lower() in service['keywords']:
            results['services'].append(service)
            
    total_results = len(results['doctors']) + len(results['medicines']) + len(results['services'])
    
    return render_template('search_results.html', query=query, results=results, total_results=total_results)



@app.route('/book_appointment/<int:doctor_id>', methods=['GET', 'POST'])
@login_required
def book_appointment(doctor_id):
    doctor = DoctorProfile.query.get_or_404(doctor_id)
    
    # Check for active subscription
    active_plan = UserSubscription.query.filter_by(user_id=current_user.id, status='Active').first()

    if request.method == 'POST':
        # Get form data
        consultation_type = request.form.get('consultation_type')
        appointment_date = request.form.get('appointment_date')
        time_slot = request.form.get('time_slot')
        payment_method = request.form.get('payment_method')
        patient_name = request.form.get('patient_name')
        
        # Calculate fee
        fees = {
            'video': 500,
            'clinic': 800,
            'home': 1500
        }
        base_fee = fees.get(consultation_type, 500)
        
        # Payment Logic
        payment_status = 'Pending'
        
        if payment_method == 'Health Plan':
            if active_plan:
                consultation_fee = 0.0
                payment_status = 'Covered by Plan'
            else:
                flash('❌ No active health plan found!', 'error')
                return redirect(url_for('book_appointment', doctor_id=doctor_id))
        else:
            # Standard Payment
            discount_applied = request.form.get('discount_applied') == 'true'
            consultation_fee = base_fee - 100 if discount_applied else base_fee
            payment_status = 'Paid' # Mock success
            
        # Parse date and time
        appt_datetime = datetime.strptime(f"{appointment_date} {time_slot}", "%Y-%m-%d %I:%M %p")
        
        # Check if slot is already booked
        existing_appt = Appointment.query.filter_by(
            doctor_id=doctor.id, 
            date_time=appt_datetime,
            status='Scheduled' 
        ).first()
        
        if existing_appt:
            flash('⚠️ This time slot is already booked! Please choose another time.', 'error')
            return redirect(url_for('book_appointment', doctor_id=doctor_id))

        # Prepare Notes
        notes = request.form.get('notes', '')
        if patient_name and patient_name.strip():
            notes = f"Patient: {patient_name} | " + notes

        # Create appointment
        appt = Appointment(
            patient_id=current_user.id,
            doctor_id=doctor.id,
            date_time=appt_datetime,
            consultation_type=consultation_type,
            time_slot=time_slot,
            consultation_fee=consultation_fee,
            payment_method=payment_method,
            payment_status=payment_status,
            transaction_id=f"TXN{random.randint(100000, 999999)}",
            notes=notes
        )
        db.session.add(appt)
        db.session.commit()
        
        # Send confirmation email
        try:
            EmailService.send_appointment_confirmation(
                current_user.email, current_user.username, 
                doctor.user.username, appt_datetime.strftime('%Y-%m-%d'), time_slot
            )
        except:
            pass
        
        flash(f'Appointment Booked Successfully! ID: {appt.transaction_id}', 'success')
        return redirect(url_for('appointments'))
    
    # GET request - show booking form
    return render_template('book_appointment.html', doctor=doctor, active_plan=active_plan)



@app.route('/appointments')
@login_required
def appointments():
    """View all appointments for current user"""
    user_appointments = Appointment.query.filter_by(patient_id=current_user.id).order_by(Appointment.date_time.desc()).all()
    return render_template('appointments.html', appointments=user_appointments)

@app.route('/appointment/details/<int:appointment_id>')
@login_required
def appointment_details(appointment_id):
    """View appointment details"""
    appt = Appointment.query.get_or_404(appointment_id)
    if appt.patient_id != current_user.id:
        flash('Unauthorized access', 'error')
        return redirect(url_for('appointments'))
    return render_template('view_report.html', appointment=appt)

@app.route('/appointment/reschedule/<int:appointment_id>', methods=['GET', 'POST'])
@login_required
def reschedule_appointment(appointment_id):
    """Reschedule an appointment"""
    appt = Appointment.query.get_or_404(appointment_id)
    if appt.patient_id != current_user.id:
        flash('Unauthorized access', 'error')
        return redirect(url_for('appointments'))
    
    if request.method == 'POST':
        new_date = request.form.get('new_date')
        new_time = request.form.get('new_time')
        if new_date and new_time:
            appt.date_time = datetime.strptime(f"{new_date} {new_time}", "%Y-%m-%d %H:%M")
            db.session.commit()
            flash('Appointment rescheduled successfully!', 'success')
            return redirect(url_for('appointments'))
    
    return render_template('reschedule_appointment.html', appointment=appt)

@app.route('/appointment/cancel/<int:appointment_id>')
@login_required
def cancel_appointment(appointment_id):
    """Cancel an appointment"""
    appt = Appointment.query.get_or_404(appointment_id)
    if appt.patient_id != current_user.id:
        flash('Unauthorized access', 'error')
        return redirect(url_for('appointments'))
    
    appt.status = 'Cancelled'
    db.session.commit()
    flash('Appointment cancelled successfully', 'success')
    return redirect(url_for('appointments'))

@app.route('/appointment/delete/<int:appointment_id>')
@login_required
def delete_appointment(appointment_id):
    """Delete an appointment (only if cancelled or completed)"""
    appt = Appointment.query.get_or_404(appointment_id)
    if appt.patient_id != current_user.id:
        flash('Unauthorized access', 'error')
        return redirect(url_for('appointments'))
    
    if appt.status not in ['Cancelled', 'Completed']:
         flash('Cannot delete active appointments. Cancel them first.', 'warning')
         return redirect(url_for('appointments'))

    try:
        db.session.delete(appt)
        db.session.commit()
        flash('Appointment deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting appointment: {str(e)}', 'error')
        
    return redirect(url_for('appointments'))

@app.route('/save-prescription', methods=['POST'])
@login_required
def save_prescription():
    if current_user.role != 'doctor':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    data = request.json
    try:
        appointment_id = data.get('appointmentId')
        diagnosis = data.get('diagnosis')
        medications = data.get('medications') # List of objects
        notes = data.get('notes')
        
        # Verify appointment belongs to doctor
        appt = Appointment.query.get(appointment_id)
        if not appt or appt.doctor_profile.user_id != current_user.id:
            return jsonify({'success': False, 'message': 'Invalid appointment'}), 400
            
        # Create or update prescription
        prescription = VideoPrescription.query.filter_by(appointment_id=appointment_id).first()
        if not prescription:
            prescription = VideoPrescription(appointment_id=appointment_id)
            db.session.add(prescription)
            
        prescription.diagnosis = diagnosis
        prescription.medications = json.dumps(medications)
        prescription.notes = notes
        prescription.created_at = datetime.utcnow()
        
        # Mark appointment as completed if not already
        if appt.status != 'Scheduled' and appt.status != 'Completed':
             pass # Don't change cancelled
        elif appt.status == 'Scheduled':
            appt.status = 'Completed'
            
        db.session.commit()
        
        # Send Email
        try:
            EmailService.send_prescription_email(
                appt.patient.email,
                appt.patient.username,
                current_user.username,
                diagnosis,
                medications,
                notes
            )
        except Exception as e:
            print(f"Failed to send email: {e}")
            
        return jsonify({'success': True})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

# --- Dependent & Stock Routes ---



@app.route('/dependents/<int:id>', methods=['GET', 'POST'])
@login_required
def dependent_detail(id):
    dep = Dependent.query.get_or_404(id)
    if dep.user_id != current_user.id: return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add_prescription':
            db.session.add(Prescription(
                dependent_id=dep.id,
                medicine_name=request.form.get('medicine_name'),
                dosage=request.form.get('dosage'),
                frequency_per_day=int(request.form.get('frequency', 1)),
                current_stock=int(request.form.get('current_stock', 0)),
                schedule_time=request.form.get('time_of_day')
            ))
            db.session.commit()
            flash('Prescription Added', 'success')
            
        elif action == 'update_history':
            dep.gender = request.form.get('gender')
            dep.blood_group = request.form.get('blood_group')
            date_of_birth = request.form.get('date_of_birth')
            if date_of_birth and date_of_birth.strip():
                try:
                    dep.date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
                except ValueError:
                    pass
            else:
                dep.date_of_birth = None
            
            dep.allergies = request.form.get('allergies')
            dep.current_medications = request.form.get('current_medications')
            dep.past_medications = request.form.get('past_medications')
            dep.chronic_diseases = request.form.get('chronic_diseases')
            dep.injuries = request.form.get('injuries')
            dep.surgeries = request.form.get('surgeries')
            
            db.session.commit()
            flash('Medical History Updated', 'success')
            
    return render_template('prescriptions.html', dependent=dep)

@app.route('/update_stock/<int:id>', methods=['POST'])
@login_required
def update_stock(id):
    script = Prescription.query.get_or_404(id)
    if script.dependent.user_id != current_user.id: return redirect(url_for('dashboard'))
    
    script.current_stock += int(request.form.get('added_stock', 0))
    script.last_refill_date = datetime.utcnow()
    db.session.commit()
    return redirect(url_for('dependent_detail', id=script.dependent_id))

# --- API Routes ---

@app.route('/api/send-otp', methods=['POST'])
def api_send_otp():
    try:
        data = request.get_json()
        email = data.get('email')
        create_if_missing = data.get('create_if_missing', False)
        
        user = User.query.filter_by(email=email).first()
        
        if not user:
            if create_if_missing:
                # Create a new user for Google Login flow
                username = email.split('@')[0].replace('.', ' ').title()
                user = User(
                    username=username, 
                    email=email, 
                    role='patient',
                    password_hash=generate_password_hash('google_dummy_' + generate_otp())
                )
                db.session.add(user)
                db.session.commit()
                
                # Create profile
                db.session.add(PatientProfile(user_id=user.id))
                db.session.commit()
            else:
                return jsonify({'success': False, 'message': 'User not found'}), 404
        
        otp = generate_otp()
        user.otp_code = otp
        user.otp_expiry = datetime.utcnow() + timedelta(minutes=10)
        db.session.commit()
        
        try:
            EmailService.send_otp_email(user.email, user.username, otp)
        except:
            # Console fallback
            # print(f"\n{'='*50}")
            # print(f"OTP for {user.email}: {otp}")
            # print(f"{'='*50}\n")
            pass
        
        return jsonify({'success': True, 'message': f'OTP sent. Code: {otp}'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Failed to send OTP: {str(e)}'}), 500

@app.route('/api/verify-otp', methods=['POST'])
def api_verify_otp():
    try:
        data = request.get_json()
        email = data.get('email')
        otp = data.get('otp')
        
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 400
            
        if user.otp_code == otp:
            login_user(user)
            user.otp_code = None
            db.session.commit()
            
            # Ensure patient profile exists
            if user.role == 'patient' and not user.patient_profile:
                try:
                    db.session.add(PatientProfile(user_id=user.id))
                    db.session.commit()
                except:
                    pass
            
            # Send welcome email if it was pending
            if session.get('pending_verification_email') == email:
                try:
                    EmailService.send_welcome_email(user.email, user.username)
                except:
                    pass
                session.pop('pending_verification_email', None)
            
            # Redirect based on role
            if user.role == 'patient':
                redirect_url = url_for('patient_dashboard')
            elif user.role == 'doctor':
                redirect_url = url_for('doctor_dashboard')
            elif user.role == 'admin':
                redirect_url = url_for('admin_dashboard')
            else:
                redirect_url = url_for('dashboard')
                
            return jsonify({'success': True, 'redirect': redirect_url})
            
        return jsonify({'success': False, 'message': 'Invalid OTP'}), 400
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Verification failed: {str(e)}'}), 500

# --- Admin Routes (Added to fix missing endpoints) ---

@app.route('/admin/users')
@login_required
def admin_view_users():
    if current_user.role != 'admin':
        flash('Unauthorized access', 'error')
        return redirect(url_for('dashboard'))
    users = User.query.all()
    return render_template('admin_view_users.html', users=users)

@app.route('/admin/patients')
@login_required
def admin_view_patients():
    if current_user.role != 'admin':
        flash('Unauthorized access', 'error')
        return redirect(url_for('dashboard'))
    patients = User.query.filter_by(role='patient').all()
    return render_template('admin_view_patients.html', patients=patients)

@app.route('/admin/doctors')
@login_required
def admin_manage_doctors():
    if current_user.role != 'admin':
        flash('Unauthorized access', 'error')
        return redirect(url_for('dashboard'))
    doctors = User.query.filter_by(role='doctor').all()
    return render_template('admin_manage_doctors.html', doctors=doctors)

@app.route('/admin/appointments')
@login_required
def admin_view_appointments():
    if current_user.role != 'admin':
        flash('Unauthorized access', 'error')
        return redirect(url_for('dashboard'))
    appointments = Appointment.query.order_by(Appointment.date_time.desc()).all()
    return render_template('admin_view_appointments.html', appointments=appointments)

@app.route('/admin/add_doctor', methods=['GET', 'POST'])
@login_required
def admin_add_doctor():
    if current_user.role != 'admin':
        flash('Unauthorized access', 'error')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        # Placeholder for adding doctor logic
        # For now, just a flash message. 
        # Ideally, this would create a User + DoctorProfile.
        flash('Doctor creation feature not fully implemented in this quick fix.', 'info')
        return redirect(url_for('admin_manage_doctors'))

    return render_template('admin_add_doctor.html')

@app.route('/api/recent-metrics', methods=['GET'])
@login_required
def api_recent_metrics():
    try:
        metrics = HealthMetric.query.filter_by(user_id=current_user.id).order_by(HealthMetric.recorded_date.desc()).limit(1).first()
        if metrics:
            return jsonify({
                'success': True,
                'heart_rate': metrics.heart_rate or '',
                'bp_systolic': metrics.blood_pressure_systolic or '',
                'bp_diastolic': metrics.blood_pressure_diastolic or '',
                'temperature': metrics.temperature or '',
                'weight': metrics.weight or '',
                'sleep_hours': metrics.sleep_hours or ''
            })
        return jsonify({
            'success': True,
            'heart_rate': '',
            'bp_systolic': '',
            'bp_diastolic': '',
            'temperature': '',
            'weight': '',
            'sleep_hours': ''
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/admin/add_offer', methods=['POST'])
@login_required
def admin_add_offer():
    if current_user.role != 'admin':
        flash('Unauthorized access', 'error')
        return redirect(url_for('dashboard'))
        
    try:
        expiry_str = request.form.get('expiry_date') # Format: YYYY-MM-DDTHH:MM
        expiry_date = datetime.strptime(expiry_str, '%Y-%m-%dT%H:%M') if expiry_str else None
        
        offer = Offer(
            title=request.form.get('title'),
            description=request.form.get('description'),
            price=request.form.get('price'),
            original_price=request.form.get('original_price'),
            discount_label=request.form.get('discount_label'),
            background_gradient=request.form.get('background_gradient'),
            expiry_date=expiry_date,
            status='active'
        )
        db.session.add(offer)
        db.session.commit()
        flash('New offer created successfully!', 'success')
    except Exception as e:
        flash(f'Error creating offer: {str(e)}', 'error')
        
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/edit_offer/<int:offer_id>', methods=['POST'])
@login_required
def admin_edit_offer(offer_id):
    if current_user.role != 'admin':
        flash('Unauthorized access', 'error')
        return redirect(url_for('dashboard'))
        
    offer = Offer.query.get_or_404(offer_id)
    try:
        offer.title = request.form.get('title')
        offer.description = request.form.get('description')
        offer.price = request.form.get('price')
        offer.original_price = request.form.get('original_price')
        offer.discount_label = request.form.get('discount_label')
        offer.background_gradient = request.form.get('background_gradient')
        
        expiry_str = request.form.get('expiry_date') # Format: YYYY-MM-DDTHH:MM
        if expiry_str:
             offer.expiry_date = datetime.strptime(expiry_str, '%Y-%m-%dT%H:%M')
             
        db.session.commit()
        flash('Offer updated successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating offer: {str(e)}', 'error')
        
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete_offer/<int:offer_id>', methods=['POST'])
@login_required
def admin_delete_offer(offer_id):
    if current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))
    
    offer = Offer.query.get_or_404(offer_id)
    try:
        db.session.delete(offer)
        db.session.commit()
        flash('Offer deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting offer: {str(e)}', 'danger')
        
    return redirect(url_for('admin_dashboard'))

# --- Wallet & Payment Routes ---

@app.route('/wallet')
@login_required
def wallet():
    return render_template('wallet.html')

@app.route('/api/wallet/topup', methods=['POST'])
@login_required
def wallet_topup():
    try:
        amount = float(request.form.get('amount', 0))
        if amount <= 0:
            return jsonify({'success': False, 'message': 'Invalid amount.'})
            
        current_user.wallet_balance += amount
        db.session.commit()
        
        flash(f'₹{amount} added to wallet successfully!', 'success')
        return jsonify({'success': True, 'new_balance': current_user.wallet_balance})
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/payment/process', methods=['POST'])
@login_required
def process_payment():
    try:
        data = request.json
        amount = float(data.get('amount', 0))
        description = data.get('description', 'Booking')
        
        if amount <= 0:
            return jsonify({'success': False, 'message': 'Invalid amount.'})
            
        if current_user.wallet_balance < amount:
            return jsonify({'success': False, 'message': 'Insufficient balance.'})
            
        # Deduct balance
        current_user.wallet_balance -= amount
        
        # Check if this is a Plan Purchase (Description matches an Offer)
        plan_subscription = None
        offer = Offer.query.filter_by(title=description).first()
        
        if offer:
            # Create Subscription
            new_sub = UserSubscription(
                user_id=current_user.id,
                offer_id=offer.id,
                plan_title=offer.title,
                price_paid=str(amount),
                status='Active'
            )
            db.session.add(new_sub)
            plan_subscription = {
                'title': offer.title,
                'price': str(amount),
                'date': datetime.utcnow().strftime('%b %d, %Y')
            }
        
        # Generate Reward
        reward_type = 'Better Luck Next Time'
        reward_desc = 'Try again next time!'
        reward_amount = 0
        
        # Simple random reward logic (30% chance of cashback)
        rand_val = random.random()
        if rand_val < 0.3:
            cashback = random.randint(10, 100)
            reward_type = 'Cashback'
            reward_desc = f'You won ₹{cashback} cashback!'
            reward_amount = cashback
            # Add cashback immediately
            current_user.wallet_balance += cashback
        elif rand_val < 0.5:
            reward_type = 'Coupon'
            reward_desc = 'Get 10% OFF on next medicine order.'
        
        new_reward = UserReward(
            user_id=current_user.id,
            reward_type=reward_type,
            description=reward_desc,
            amount=reward_amount
        )
        db.session.add(new_reward)
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': 'Payment successful!',
            'new_balance': current_user.wallet_balance,
            'reward': {
                'id': new_reward.id,
                'type': reward_type,
                'description': reward_desc,
                'amount': reward_amount
            },
            'subscription': plan_subscription
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/reward/scratch/<int:reward_id>', methods=['POST'])
@login_required
def scratch_reward(reward_id):
    try:
        reward = UserReward.query.get_or_404(reward_id)
        if reward.user_id != current_user.id:
            return jsonify({'success': False, 'message': 'Unauthorized'})
        
        reward.is_scratched = True
        db.session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/autosave', methods=['POST'])
@login_required
def api_autosave():
    data = request.get_json()
    # Autosave functionality - just return success
    return jsonify({'success': True})

@app.route('/api/save-metric', methods=['POST'])
@login_required
def api_save_metric():
    try:
        data = request.get_json()
        metric = HealthMetric(
            user_id=current_user.id,
            heart_rate=data.get('heart_rate') or None,
            blood_pressure_systolic=data.get('bp_systolic') or None,
            blood_pressure_diastolic=data.get('bp_diastolic') or None,
            temperature=data.get('temperature') or None,
            weight=data.get('weight') or None,
            sleep_hours=data.get('sleep_hours') or None
        )
        db.session.add(metric)
        db.session.commit()
        return jsonify({
            'success': True, 
            'message': 'Metrics saved successfully!',
            'data': {
                'heart_rate': metric.heart_rate,
                'bp_systolic': metric.blood_pressure_systolic,
                'bp_diastolic': metric.blood_pressure_diastolic,
                'temperature': metric.temperature,
                'weight': metric.weight,
                'sleep_hours': metric.sleep_hours
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# --- Video Consultation Routes ---

# Video consultation route already defined above

# --- Seeding Data ---

def seed_data():
    """Seed database with initial data including 20+ doctors"""
    if User.query.first(): return
    
    # Create Admin
    admin = User(username='Admin', email='admin@mediscan.com', role='admin')
    admin.set_password('admin123')
    db.session.add(admin)
    
    # Create 20+ Doctors with diverse specializations
    doctors_data = [
        # Cardiologists
        ('Dr. Rajesh Patel', 'Cardiologist', 'Apollo Hospital', 15, 'https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?w=400'),
        ('Dr. Priya Sharma', 'Cardiologist', 'Fortis Hospital', 12, 'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=400'),
        ('Dr. Vikram Singh', 'Cardiologist', 'Max Hospital', 18, 'https://images.unsplash.com/photo-1622253692010-333f2da6031d?w=400'),
        
        # Dermatologists
        ('Dr. Sneha Shah', 'Dermatologist', 'Zydus Hospital', 10, 'https://images.unsplash.com/photo-1594824476967-48c8b964273f?w=400'),
        ('Dr. Anjali Mehta', 'Dermatologist', 'Sterling Hospital', 8, 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=400'),
        
        # General Physicians
        ('Dr. Amit Gupta', 'General Physician', 'Sterling Hospital', 14, 'https://images.unsplash.com/photo-1537368910025-700350fe46c7?w=400'),
        ('Dr. Neha Desai', 'General Physician', 'Apollo Hospital', 9, 'https://images.unsplash.com/photo-1551836022-d5d88e9218df?w=400'),
        ('Dr. Karan Joshi', 'General Physician', 'Fortis Hospital', 11, 'https://images.unsplash.com/photo-1582750433449-648ed127bb54?w=400'),
        
        # Pediatricians
        ('Dr. Meera Iyer', 'Pediatrician', 'Rainbow Hospital', 13, 'https://images.unsplash.com/photo-1527613426441-4da17471b66d?w=400'),
        ('Dr. Rohan Kapoor', 'Pediatrician', 'Apollo Hospital', 10, 'https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?w=400'),
        
        # Orthopedic Surgeons
        ('Dr. Suresh Kumar', 'Orthopedic Surgeon', 'Max Hospital', 20, 'https://images.unsplash.com/photo-1622253692010-333f2da6031d?w=400'),
        ('Dr. Kavita Rao', 'Orthopedic Surgeon', 'Fortis Hospital', 16, 'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=400'),
        
        # Neurologists
        ('Dr. Arun Nair', 'Neurologist', 'Apollo Hospital', 17, 'https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?w=400'),
        ('Dr. Divya Reddy', 'Neurologist', 'Zydus Hospital', 12, 'https://images.unsplash.com/photo-1594824476967-48c8b964273f?w=400'),
        
        # Gynecologists
        ('Dr. Pooja Verma', 'Gynecologist', 'Fortis Hospital', 14, 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=400'),
        ('Dr. Shalini Pillai', 'Gynecologist', 'Apollo Hospital', 11, 'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=400'),
        
        # ENT Specialists
        ('Dr. Manish Agarwal', 'ENT Specialist', 'Sterling Hospital', 13, 'https://images.unsplash.com/photo-1537368910025-700350fe46c7?w=400'),
        ('Dr. Ritu Bansal', 'ENT Specialist', 'Max Hospital', 9, 'https://images.unsplash.com/photo-1527613426441-4da17471b66d?w=400'),
        
        # Psychiatrists
        ('Dr. Arjun Malhotra', 'Psychiatrist', 'Apollo Hospital', 15, 'https://images.unsplash.com/photo-1622253692010-333f2da6031d?w=400'),
        ('Dr. Nisha Chopra', 'Psychiatrist', 'Fortis Hospital', 10, 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=400'),
        
        # Ophthalmologists
        ('Dr. Sanjay Bhatia', 'Ophthalmologist', 'Zydus Hospital', 18, 'https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?w=400'),
        ('Dr. Lakshmi Menon', 'Ophthalmologist', 'Sterling Hospital', 12, 'https://images.unsplash.com/photo-1594824476967-48c8b964273f?w=400'),
    ]
    
    for name, spec, hosp, exp, img in doctors_data:
        # Create email from name
        email = name.lower().replace(' ', '').replace('dr.', '') + '@mediscan.com'
        
        # Create User account
        u = User(username=name, email=email, role='doctor')
        u.set_password('doctor123')
        db.session.add(u)
        db.session.flush()  # Get user ID
        
        # Create Doctor Profile
        db.session.add(DoctorProfile(
            user_id=u.id,
            specialization=spec,
            hospital=hosp,
            experience=exp,
            image_url=img,
            is_available=True
        ))
    
    # Seed Offers if none exist
    if not Offer.query.first():
        offer1 = Offer(
            title="Total Health Package",
            description="Includes 60+ Tests • Full Body Checkup",
            price="999",
            original_price="2999",
            discount_label="67% OFF",
            background_gradient="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
            status="active"
        )
        
        # Expires in 5 hours from now
        expiry = datetime.utcnow() + timedelta(hours=5)
        offer2 = Offer(
            title="Family Care Plus",
            description="Unlimited Consultations for 4 Members",
            price="1499",
            original_price="4999",
            discount_label="FLASH SALE",
            background_gradient="linear-gradient(135deg, #ff9a9e 0%, #fecfef 99%, #fecfef 100%)",
            expiry_date=expiry,
            status="active"
        )
        
        db.session.add(offer1)
        db.session.add(offer2)

    db.session.commit()
    # print("✅ Database Seeded Successfully with 22 Doctors!")

# --- Main Entry Point ---

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_data()
    app.run(debug=True, host='0.0.0.0', port=5001)
