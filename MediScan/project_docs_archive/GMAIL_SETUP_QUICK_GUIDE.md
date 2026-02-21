# 🚀 Quick Gmail Setup for Email OTP

## Current Status
✅ Email system is working with **console OTP** (fallback mode)  
⚠️ Gmail emails not being sent - **App Password needed**

## Why Emails Aren't Being Sent
Gmail requires a special **App Password** (not your regular password) for security. Without it, emails fail and the system falls back to console OTP.

---

## 📝 3-Step Setup (Takes 2 minutes)

### Step 1: Enable 2-Factor Authentication
1. Go to: https://myaccount.google.com/security
2. Find "2-Step Verification" and turn it ON
3. Follow the prompts (you'll need your phone)

### Step 2: Generate App Password
1. Go to: https://myaccount.google.com/apppasswords
2. You'll see "App passwords" section
3. Click "Select app" → Choose **Mail**
4. Click "Select device" → Choose **Other (Custom name)**
5. Type: **MediScan**
6. Click **Generate**
7. You'll see a 16-character password like: `abcd efgh ijkl mnop`
8. **Copy this password** (you can remove spaces)

### Step 3: Update email_service.py
1. Open `email_service.py` in your editor
2. Find line 13 that says:
   ```python
   SENDER_PASSWORD = 'YOUR_GMAIL_APP_PASSWORD_HERE'
   ```
3. Replace with your app password:
   ```python
   SENDER_PASSWORD = 'abcdefghijklmnop'  # Your 16-char password (no spaces)
   ```
4. Save the file
5. **Restart your Flask server** (stop and run again)

---

## ✅ Test It

Run this command to test:
```bash
python test_email.py
```

If successful, you'll see:
```
✅ OTP email sent successfully to test@example.com
```

---

## 🎯 What Happens After Setup

**Before Setup:**
- OTP prints to console: `🔑 Code: 123456`
- No email received

**After Setup:**
- Email sent to user's inbox
- Professional HTML email with OTP
- Console still shows confirmation

---

## 🔧 Troubleshooting

### "Username and Password not accepted"
- Make sure you enabled 2FA first
- Use the App Password, not your Gmail password
- Remove all spaces from the app password

### "App passwords" option not showing
- You need to enable 2-Factor Authentication first
- Wait a few minutes after enabling 2FA

### Still not working?
- Check if the email is in spam/junk folder
- Verify `SENDER_EMAIL` is `shethkriya2842@gmail.com` in `email_service.py`
- Make sure you restarted the Flask server after changes

---

## 📧 Current Configuration

File: `email_service.py`
- **Sender Email**: shethkriya2842@gmail.com ✅
- **Password**: Needs App Password ⚠️
- **SMTP Server**: smtp.gmail.com ✅
- **Port**: 587 ✅

---

## 💡 Important Notes

1. **Console OTP still works** - You can continue testing without Gmail setup
2. **App Password is safe** - It's specifically for this app, not your main password
3. **One-time setup** - You only need to do this once
4. **Restart required** - Always restart Flask server after changing email_service.py

---

## 🎉 Benefits After Setup

✅ Professional emails sent to users  
✅ Better user experience  
✅ No need to check console for OTP  
✅ Production-ready authentication  
✅ Automatic welcome emails  

---

## Need Help?

The system works perfectly with console OTP for now. Gmail setup is optional but recommended for production use.

**Current behavior:**
- Signup works ✅
- Login works ✅
- OTP verification works ✅
- Emails go to console instead of Gmail ⚠️

**After Gmail setup:**
- Everything above ✅
- Emails sent to user's inbox ✅
