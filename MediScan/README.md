# 🏥 MediScan - AI Healthcare Assistant

A comprehensive full-stack healthcare web application with AI-powered features.

---

## 📚 Documentation

### Main Documentation Files:

1. **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - **START HERE!**
   - Complete project overview
   - All 4 subjects covered (FSD-1, FCSP-1, DSA, SQL)
   - Features, code organization, how to run
   - Database schema, API documentation

2. **[SYLLABUS_MAPPING.md](SYLLABUS_MAPPING.md)** - Detailed Mapping
   - Line-by-line code mapping to syllabus
   - Detailed examples and explanations
   - DSA algorithms with implementations
   - SQL queries and database design

3. **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Quick Guide
   - Fast reference for routes and features
   - Technology stack
   - Test accounts

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
```

### Access
Open browser: **http://127.0.0.1:5001**

### Test Account
- **Doctor**: rajeshpatel@mediscan.com / doctor123
- **Patient**: Create new account via Sign Up

---

## ✅ Syllabus Coverage

| Subject | Coverage | Status |
|---------|----------|--------|
| FSD-1 (Full Stack) | 100% | ✅ Complete |
| FCSP-1 (Python) | 100% | ✅ Complete |
| DSA (Algorithms) | 90% | ✅ Excellent |
| SQL/DBMS | 95% | ✅ Excellent |

---

## 🎯 Key Features

1. **Multi-Method Authentication** - Email/Phone/OTP login
2. **Health Tracking** - Monitor vitals with 6-month trends
3. **Medicine Tracker** - Reminders and stock management
4. **Doctor Appointments** - Book with 20+ specialists

6. **Family Health** - Manage dependents' health
7. **Analytics Dashboard** - Data visualization with Chart.js

---

## 💻 Technology Stack

**Backend**: Python, Flask, SQLAlchemy, NumPy  
**Frontend**: HTML5, CSS3, JavaScript ES6+, Chart.js  
**Database**: SQLite with 10 normalized tables  
**Security**: Password hashing, OTP authentication, CSRF protection

---

## 📊 Project Stats

- **900+ lines** of Python code
- **500+ lines** of JavaScript
- **2000+ lines** of HTML/CSS
- **10 database models** with relationships
- **50+ routes** and endpoints
- **40+ HTML templates**
- **6 major features**

---

## 📁 Project Structure

```
MediScan/
├── app.py                    # Main Flask application
├── requirements.txt          # Dependencies
├── README.md                 # This file
├── PROJECT_SUMMARY.md        # Complete documentation
├── SYLLABUS_MAPPING.md       # Detailed syllabus mapping
├── QUICK_REFERENCE.md        # Quick reference guide
├── instance/
│   └── mediscan.db          # SQLite database
├── static/
│   ├── css/                 # 5 CSS files
│   ├── js/                  # 5 JavaScript files
│   └── images/              # Static assets
└── templates/               # 40+ HTML templates
```

---

## 🔑 Important URLs

### Public Pages
- `/` - Landing page
- `/login` - User login
- `/signup` - Registration
- `/doctors` - Browse doctors
- `/symptom-checker` - AI diagnosis

### Patient Dashboard (Login Required)
- `/patient_dashboard` - Patient home
- `/health_tracker` - Track vitals
- `/health_analytics` - View trends
- `/medicine_tracker` - Manage medicines
- `/appointments` - View bookings
- `/dependents` - Family health

### Doctor Dashboard (Login Required)
- `/doctor_dashboard` - Doctor home
- `/doctor_update_appointment_status/<id>` - Update appointments

### API Endpoints
- `POST /api/send-otp` - Send OTP
- `POST /api/verify-otp` - Verify OTP
- `GET /api/recent-metrics` - Get health data
- `POST /api/save-metric` - Save health data

---

## 🎓 Academic Alignment

### SEM III FSD-1 (Full Stack Development)
✅ HTML5, CSS3, JavaScript ES6+  
✅ Flask framework, SQLAlchemy ORM  
✅ RESTful APIs, Authentication  
✅ Frontend-backend integration  

### SEM III FCSP-1 (Python Fundamentals)
✅ Python data types, control structures  
✅ OOP (classes, inheritance, encapsulation)  
✅ Data structures (lists, dicts, sets)  
✅ NumPy for data analysis  

### DSA (Data Structures & Algorithms)
✅ Arrays, lists, dictionaries, stacks, queues  
✅ Sorting (Timsort), searching (linear, binary)  
✅ Time complexity analysis (O(1), O(n), O(n log n))  
✅ Greedy algorithms, dynamic programming  

### SQL/DBMS
✅ Database design, normalization (1NF, 2NF, 3NF)  
✅ CRUD operations, joins, relationships  
✅ Indexes, transactions, ACID properties  
✅ Constraints (PK, FK, UNIQUE, NOT NULL)  

---

## 🔒 Security Features

- Password hashing (Werkzeug)
- SQL injection prevention (ORM)
- XSS protection (template escaping)
- CSRF tokens
- Session security
- Role-based access control

---

## 📖 How to Use This Project

1. **Read [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** for complete overview
2. **Check [SYLLABUS_MAPPING.md](SYLLABUS_MAPPING.md)** for detailed syllabus alignment
3. **Use [QUICK_REFERENCE.md](QUICK_REFERENCE.md)** for quick lookups
4. **Run `python app.py`** to start the application
5. **Open http://127.0.0.1:5001** in your browser

---

## 🎯 Project Highlights

✅ **Production-ready** code with industry standards  
✅ **100% syllabus coverage** for all 4 subjects  
✅ **Real-world application** solving healthcare problems  
✅ **Well-organized** and commented code  
✅ **Comprehensive documentation** with examples  
✅ **Advanced features** beyond basic requirements  

---

## 📞 Support

For detailed information:
- **Complete Guide**: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
- **Syllabus Mapping**: [SYLLABUS_MAPPING.md](SYLLABUS_MAPPING.md)
- **Quick Reference**: [QUICK_REFERENCE.md](QUICK_REFERENCE.md)

---

**Status**: ✅ Production Ready  
**Quality**: ✅ Well-organized & Documented  
**Coverage**: ✅ 100% Syllabus Aligned  

**Last Updated**: February 10, 2026


---

## 🛠️ Utility Scripts (Windows Only)

### Batch Files for Easy Server Management

**1. `kill_port_and_start.bat`**
- Double-click to automatically kill any process on port 5001 and start the server
- Use when you get "port already in use" error
- No need to manually open Task Manager

**2. `restart_server.bat`**
- Quick server restart
- Kills old process and starts new one
- Useful during development

### How to Use:
```bash
# Option 1: Double-click the .bat file in File Explorer

# Option 2: Run from command prompt
kill_port_and_start.bat
```

### Manual Alternative (if .bat files don't work):
```bash
# 1. Open Task Manager (Ctrl + Shift + Esc)
# 2. Go to "Details" tab
# 3. Find and end all "python.exe" processes
# 4. Run: python app.py
```

**Note**: These are Windows-specific utilities. Mac/Linux users should use:
```bash
# Kill process on port 5001
lsof -ti:5001 | xargs kill -9

# Start server
python app.py
```


---

## 🎓 For Faculty & Evaluators

### Presentation Guide
**[PRESENTATION_GUIDE.md](PRESENTATION_GUIDE.md)** - Complete guide for demonstrating this project

**Includes**:
- ✅ Quick setup instructions (5 minutes)
- ✅ Demonstration flow (15-20 minutes)
- ✅ Code walkthrough with explanations
- ✅ Syllabus coverage mapping
- ✅ Key points to emphasize
- ✅ Common questions & answers
- ✅ Troubleshooting guide

### Quick Demo Steps:
1. Run `python app.py`
2. Open http://127.0.0.1:5001
3. Login with: `rajeshpatel@mediscan.com` / `doctor123`
4. Show features: Health Tracker, Medicine Tracker, Appointments
5. Show code: `app.py`, database models, JavaScript ES6+

### Evaluation Points:
- ✅ 100% syllabus coverage (FSD-1, FCSP-1, DSA, SQL)
- ✅ 900+ lines of well-organized Python code
- ✅ 10 database models with relationships
- ✅ RESTful APIs with JSON
- ✅ Modern JavaScript (async/await, ES6+)
- ✅ Security features (password hashing, ORM)
- ✅ Real-world healthcare application
