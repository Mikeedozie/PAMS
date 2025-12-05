# 🚀 ULTRA-SIMPLE SERVER STARTUP FOR SCREENSHOTS

## ⚠️ THE PROBLEM
WSL is 10-20x slower for Python packages due to cross-filesystem access. This makes servers take 60+ seconds to start.

## ✅ THE SOLUTION
Use **Windows PowerShell** or **CMD** natively (NOT WSL!)

---

## 🎯 FASTEST METHOD - Windows PowerShell

### Step 1: Open Windows PowerShell (as Administrator)
Press `Win + X`, select "Windows PowerShell (Admin)"

### Step 2: Navigate to Project
```powershell
cd C:\Users\Edozie\Downloads\MalwareIntel-ed\PAMS
```

### Step 3: Install Backend Dependencies (One-time)
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install fastapi uvicorn sqlalchemy pydantic python-jose passlib python-multipart bcrypt python-dotenv pydantic-settings email-validator
cd ..
```

### Step 4: Start Backend Server
```powershell
.\backend\venv\Scripts\Activate.ps1
python -m backend.main_screenshot
```

**Wait for:** `INFO:     Uvicorn running on http://0.0.0.0:8000`

### Step 5: Open NEW PowerShell Window for Frontend
```powershell
cd C:\Users\Edozie\Downloads\MalwareIntel-ed\PAMS\frontend
npm install
npm run dev
```

**Wait for:** `ready started server on [::]:3000`

---

## 📸 Take Screenshots

### Access URLs:
- **Backend API:** http://localhost:8000/docs
- **Frontend Landing:** http://localhost:3000/landing  
- **Frontend Dashboard:** http://localhost:3000/dashboard

### Login Credentials:
- **Admin:** `admin` / `Admin123!`
- **Analyst:** `analyst` / `Analyst123!`

### Screenshot Sequence:
1. **Fig 4.1 (Landing Page)**
   - Go to: http://localhost:3000/landing
   - Make sure you're logged OUT
   - Capture full page with hero, stats, features

2. **Fig 4.2 (Dashboard)**
   - Login as `analyst` / `Analyst123!`
   - Go to: http://localhost:3000/dashboard
   - Capture full dashboard with KPIs, charts, alerts

3. **Fig 4.5 (Alert Management)**
   - While on dashboard, scroll to alerts table
   - Capture the alerts section showing severity, scores

---

## 🔧 If PowerShell Gives Execution Policy Error

Run this ONCE in PowerShell (Admin):
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 🐛 Troubleshooting

### Backend Won't Start?
```powershell
# Reinstall with all dependencies
cd C:\Users\Edozie\Downloads\MalwareIntel-ed\PAMS\backend
Remove-Item -Recurse -Force venv
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install fastapi uvicorn sqlalchemy pydantic python-jose passlib python-multipart bcrypt python-dotenv pydantic-settings email-validator
cd ..
python -m backend.main_screenshot
```

### Frontend Won't Start?
```powershell
cd C:\Users\Edozie\Downloads\MalwareIntel-ed\PAMS\frontend
Remove-Item -Recurse -Force node_modules, .next
npm install
npm run dev
```

### Can't See Data?
```powershell
# Delete database and restart backend (will auto-reseed)
cd C:\Users\Edozie\Downloads\MalwareIntel-ed\PAMS
Remove-Item pams.db
.\backend\venv\Scripts\Activate.ps1
python -m backend.main_screenshot
```

---

## ⏱️ Expected Startup Times (Windows)
- ✅ Backend: 5-10 seconds
- ✅ Frontend: 10-15 seconds  
- ✅ Total: Under 30 seconds

vs WSL:
- ❌ Backend: 60+ seconds (pandas loading)
- ❌ Frontend: 15-20 seconds
- ❌ Total: 80+ seconds

---

## 📝 Summary

1. **Use Windows PowerShell** (not WSL!)
2. **Terminal 1:** Start backend (port 8000)
3. **Terminal 2:** Start frontend (port 3000)
4. **Browser:** Visit http://localhost:3000/landing
5. **Login:** analyst/Analyst123!
6. **Screenshot:** Follow SCREENSHOT_GUIDE.md

**Your servers should be running in under 30 seconds!** 🎉

---

## 🆘 Still Having Issues?

Try the **absolute minimal** approach:

```powershell
# Terminal 1 - Backend
cd C:\Users\Edozie\Downloads\MalwareIntel-ed\PAMS
python -m pip install --user fastapi uvicorn sqlalchemy pydantic python-jose passlib python-multipart bcrypt python-dotenv pydantic-settings email-validator
python -m backend.main_screenshot

# Terminal 2 - Frontend
cd C:\Users\Edozie\Downloads\MalwareIntel-ed\PAMS\frontend
npm install
npm run dev
```

This installs packages globally (no venv) which sometimes works better on Windows.
