# 📱 Patient Video Call Guide - Where to Find "Join Call" Button

## 🎯 **Exact Locations for Video Call Access:**

### **Location 1: Patient Dashboard - Recent Appointments Section**

When you login as a patient and go to the dashboard, you'll see:

```
📊 Patient Dashboard
├── Quick Actions (Book Appointment, Symptom Checker, etc.)
├── Recent Appointments Section ⭐ **VIDEO CALL BUTTONS HERE**
│   ├── Dr. [Doctor Name]
│   │   ├── [Date] 
│   │   ├── Status Badge (Scheduled/Completed/etc.)
│   │   └── 🎥 "Join Call" Button ← **CLICK HERE FOR VIDEO CALL**
│   └── View All Appointments →
└── Notifications Section
```

### **Location 2: Full Appointments Page**

Click "View All Appointments" or go to `/appointments`:

```
📅 My Appointments
├── Filter Tabs (All, Scheduled, Completed, etc.)
└── Appointment Cards
    ├── Doctor Info & Status
    ├── Appointment Details
    └── Action Buttons:
        ├── 🎥 "Join Video Call" ← **MAIN VIDEO BUTTON**
        ├── 👁️ "View Details"
        ├── 📅 "Reschedule"
        └── ❌ "Cancel"
```

---

## 🔍 **Visual Identification:**

### **What to Look For:**
- **Green Button** with video camera icon 📹
- **Text**: "Join Call" (dashboard) or "Join Video Call" (appointments page)
- **Color**: Bright green background (#10b981)
- **Icon**: Video camera symbol
- **Only appears** when appointment status is "Scheduled"

### **Button Appearance:**
```
┌─────────────────┐
│ 🎥 Join Call    │  ← Dashboard version
└─────────────────┘

┌─────────────────────┐
│ 🎥 Join Video Call  │  ← Appointments page version
└─────────────────────┘
```

---

## 🧪 **Step-by-Step Test:**

### **Test with Demo Account:**
1. **Login**: Go to http://127.0.0.1:5001/login
2. **Email**: `patient@mediscan.com`
3. **Password**: `patient123`
4. **Dashboard**: You'll see "Recent Appointments" section
5. **Look for**: Green "Join Call" button next to scheduled appointments

### **If No Button Appears:**
- **Check appointment status**: Only "Scheduled" appointments show video buttons
- **Book new appointment**: Use "Book Appointment" to create a test appointment
- **Check appointments page**: Go to "View All Appointments" for more options

---

## 📋 **Current Status Check:**

Let me verify what appointments exist for the demo patient:

### **Demo Patient Account:**
- **Username**: Kriya
- **Email**: patient@mediscan.com
- **Password**: patient123

### **Expected Appointments:**
- Should have appointments with various doctors
- Status should be "Scheduled" to see video buttons
- If no appointments, book a new one first

---

## 🚨 **Troubleshooting:**

### **If "Join Call" Button is Missing:**

1. **Check Appointment Status**:
   - Only "Scheduled" appointments show video buttons
   - "Completed" or "Cancelled" appointments won't have video options

2. **Create Test Appointment**:
   - Click "Book Appointment" 
   - Select any doctor
   - Choose future date/time
   - Status will be "Scheduled" → Video button will appear

3. **Refresh Page**:
   - Sometimes browser cache needs refresh
   - Press F5 or Ctrl+R

4. **Check Different Locations**:
   - Dashboard → Recent Appointments
   - Full Appointments Page → Action buttons

---

## 🎯 **Quick Access Summary:**

### **Fastest Way to Join Video Call:**
1. **Login** as patient
2. **Dashboard** → Look at "Recent Appointments"
3. **Find scheduled appointment**
4. **Click green "Join Call" button** 🎥
5. **Video consultation opens** in new window/tab

### **Alternative Path:**
1. **Login** as patient  
2. **Click "View All Appointments"**
3. **Find scheduled appointment card**
4. **Click "Join Video Call" button** 🎥
5. **Video consultation starts**

---

## ✅ **Confirmation:**

The video call buttons are already implemented and should be visible on:
- ✅ Patient Dashboard (Recent Appointments)
- ✅ Full Appointments Page (Action buttons)
- ✅ Only for "Scheduled" status appointments
- ✅ Green color with video camera icon

**If you don't see them, the most likely reason is that there are no "Scheduled" appointments for the patient account.**