# 📧 Email OTP Setup Guide for MediScan

## 🔐 Gmail App Password Setup

To enable OTP email functionality, you need to create a Gmail App Password:

### Step 1: Enable 2-Factor Authentication
1. Go to your Google Account: https://myaccount.google.com/
2. Click on **Security** in the left sidebar
3. Under "Signing in to Google", click on **2-Step Verification**
4. Follow the prompts to enable 2FA

### Step 2: Generate App Password
1. Go to: https://myaccount.google.com/apppasswords
2. Select app: **Mail**
3. Select device: **Other (Custom name)**
4. Enter name: **MediScan OTP**
5. Click **Generate**
6. Copy the 16-character password (remove spaces)

### Step 3: Configure Email Service
1. Open `email_service.py`
2. Find the line:
   ```python
   SENDER_PASSWORD = 'your_app_password_here'
   ```
3. Replace with your generated app password:
   ```python
   SENDER_PASSWORD = 'abcd efgh ijkl mnop'  # Your 16-char password
   ```

### Step 4: Update Sender Email (Optional)
If you want to use a different email:
```python
SENDER_EMAIL = 'your-email@gmail.com'
```

## 🧪 Testing the Email System

### Test OTP Email:
```python
python test_email.py
```

### Manual Test:
```python
from email_service import send_otp_email, generate_otp

otp = generate_otp()
send_otp_email('test@example.com', 'Test User', otp)
print(f"OTP sent: {otp}")
```

## 🔧 Troubleshooting

### Error: "Username and Password not accepted"
- Make sure 2FA is enabled
- Use App Password, not your regular Gmail password
- Remove spaces from the app password

### Error: "SMTPAuthenticationError"
- Verify the app password is correct
- Check if "Less secure app access" is enabled (if not using app password)

### Email not received:
- Check spam/junk folder
- Verify recipient email is correct
- Check Gmail sending limits (500 emails/day)

## 📝 Email Template Customization

Edit `email_service.py` to customize:
- Email subject
- HTML template
- Sender name
- OTP validity period

## 🚀 Production Deployment

For production, consider using:
- **SendGrid** - https://sendgrid.com/
- **AWS SES** - https://aws.amazon.com/ses/
- **Mailgun** - https://www.mailgun.com/

These services offer better deliverability and higher sending limits.

## 📊 Current Configuration

- **Sender Email**: shethkriya2842@gmail.com
- **SMTP Server**: smtp.gmail.com
- **SMTP Port**: 587
- **OTP Length**: 6 digits
- **OTP Validity**: 10 minutes
- **Email Format**: HTML + Plain Text

## 🔒 Security Best Practices

1. **Never commit** app passwords to version control
2. Use **environment variables** for sensitive data
3. Implement **rate limiting** for OTP requests
4. Add **CAPTCHA** to prevent abuse
5. Log all OTP attempts for security monitoring

## 📞 Support

If you encounter issues:
- Check the console for error messages
- Verify Gmail account settings
- Test with a simple SMTP client first
- Contact: shethkriya2842@gmail.com
