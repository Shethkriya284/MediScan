# 🚀 Gmail Setup - Follow These Exact Steps

## Why Emails Aren't Coming

Gmail requires a special **App Password** for security. Your current password in `email_service.py` is just a placeholder: `YOUR_GMAIL_APP_PASSWORD_HERE`

Without the real App Password, emails fail and the system uses console OTP instead.

---

## ✅ Step-by-Step Setup

### STEP 1: Enable 2-Factor Authentication (2FA)

1. **Open this link**: https://myaccount.google.com/signinoptions/two-step-verification

2. **Sign in** with your Gmail account: `shethkriya2842@gmail.com`

3. Click **"Get Started"** button

4. **Enter your password** when prompted

5. **Add your phone number** for verification

6. **Enter the verification code** you receive via SMS

7. Click **"Turn On"** to enable 2FA

✅ **Done!** You should see "2-Step Verification is on"

---

### STEP 2: Generate App Password

1. **Open this link**: https://myaccount.google.com/apppasswords

   ⚠️ **Note**: If you don't see "App passwords" option:
   - Make sure 2FA is enabled (Step 1)
   - Wait 5 minutes after enabling 2FA
   - Refresh the page

2. You'll see two dropdown menus:
   - **Select app**: Choose **"Mail"**
   - **Select device**: Choose **"Other (Custom name)"**

3. **Type**: `MediScan` (or any name you want)

4. Click **"Generate"**

5. You'll see a **yellow box** with a 16-character password like:
   ```
   abcd efgh ijkl mnop
   ```

6. **COPY THIS PASSWORD** (you can copy with or without spaces)

✅ **Done!** Keep this password - you'll need it in the next step

---

### STEP 3: Update email_service.py

1. **Open** the file `email_service.py` in your editor

2. **Find line 13** that looks like this:
   ```python
   SENDER_PASSWORD = 'YOUR_GMAIL_APP_PASSWORD_HERE'
   ```

3. **Replace** with your App Password (remove spaces):
   ```python
   SENDER_PASSWORD = 'abcdefghijklmnop'
   ```

   **Example with your actual password:**
   ```python
   SENDER_PASSWORD = 'xyzw abcd efgh ijkl'  # If your password is: xyzw abcd efgh ijkl
   ```
   
   **Should become:**
   ```python
   SENDER_PASSWORD = 'xyzwabcdefghijkl'  # Remove all spaces!
   ```

4. **Save** the file (Ctrl+S or Cmd+S)

✅ **Done!** Password is now configured

---

### STEP 4: Restart Flask Server

1. **Stop** the current Flask server:
   - Press `Ctrl + C` in the terminal where Flask is running

2. **Start** it again:
   ```bash
   python app.py
   ```

3. Wait for the server to start (you'll see "Running on http://...")

✅ **Done!** Server is now using Gmail

---

### STEP 5: Test It

**Option A: Use test script**
```bash
python quick_email_test.py
```

**Option B: Try signup/login**
1. Go to: http://localhost:5001/auth
2. Click "Sign Up" or "Sign In with OTP"
3. Enter your email
4. **Check your Gmail inbox** for the OTP email

✅ **Success!** If you receive the email, setup is complete!

---

## 🔍 How to Verify It's Working

### Before Setup (Console OTP):
Terminal shows:
```
❌ Failed to send OTP email: (535, b'5.7.8 Username and Password not accepted')
==================================================
📧 OTP for user@example.com
🔑 Code: 123456
==================================================
```

### After Setup (Gmail Working):
Terminal shows:
```
✅ OTP email sent successfully to user@example.com
```

And user receives email in their Gmail inbox!

---

## 🔧 Troubleshooting

### Problem: "App passwords" option not showing
**Solution:**
- Enable 2FA first (Step 1)
- Wait 5-10 minutes
- Refresh the page
- Try this direct link: https://myaccount.google.com/apppasswords

### Problem: "Username and Password not accepted"
**Solution:**
- Make sure you're using the App Password, not your regular Gmail password
- Remove ALL spaces from the password
- Check if 2FA is enabled
- Verify the password is correct in email_service.py

### Problem: Still showing console OTP
**Solution:**
- Confirm password is updated in email_service.py line 13
- Make sure you saved the file
- Restart Flask server (Ctrl+C then python app.py)
- Check terminal for error messages

### Problem: Email not received after setup
**Solution:**
- Check spam/junk folder
- Verify sender email is `shethkriya2842@gmail.com` in email_service.py
- Look for "✅ OTP email sent successfully" in terminal
- Try sending to a different email address

---

## 📋 Quick Checklist

- [ ] 2FA enabled on Gmail account
- [ ] App Password generated (16 characters)
- [ ] email_service.py updated with App Password (line 13)
- [ ] All spaces removed from password
- [ ] File saved
- [ ] Flask server restarted
- [ ] Test email sent
- [ ] Email received in Gmail inbox

---

## 💡 Important Notes

1. **App Password is NOT your Gmail password**
   - It's a special 16-character code
   - Only works for this app
   - Can be revoked anytime

2. **Remove spaces from password**
   - Google shows: `abcd efgh ijkl mnop`
   - You type: `abcdefghijklmnop`

3. **Restart server after changes**
   - Changes only take effect after restart
   - Always restart: Ctrl+C then python app.py

4. **Keep password secure**
   - Don't share it
   - Don't commit to GitHub
   - Save it somewhere safe

---

## 🎯 Current Configuration

**File**: `email_service.py`

**Line 12**: `SENDER_EMAIL = 'shethkriya2842@gmail.com'` ✅ Correct

**Line 13**: `SENDER_PASSWORD = 'YOUR_GMAIL_APP_PASSWORD_HERE'` ⚠️ **UPDATE THIS**

**Line 14**: `SENDER_NAME = 'MediScan Team'` ✅ Correct

---

## 🚀 After Setup

Once configured, your system will:
- ✅ Send professional HTML emails
- ✅ Deliver OTP to user's inbox
- ✅ Send welcome emails after signup
- ✅ Work like a production app
- ✅ No more console dependency

---

## 📞 Need Help?

If you're stuck:
1. Check which step you're on
2. Read the troubleshooting section
3. Look for error messages in terminal
4. Make sure each step is completed

**Remember**: The system works fine with console OTP for testing. Gmail setup is for production use!

---

**Estimated Time**: 5 minutes  
**Difficulty**: Easy  
**Required**: Gmail account + Phone for 2FA
