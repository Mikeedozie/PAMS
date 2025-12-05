# PAMS Quick Start (Windows - FASTEST METHOD)

## Use Windows PowerShell or CMD for Best Performance!

WSL is very slow when accessing Windows files. Use native Windows terminals instead.

---

## Step 1: Start Backend (PowerShell)

Open PowerShell and run:

```powershell
cd C:\Users\Edozie\Downloads\MalwareIntel-ed\PAMS\backend

# Create & activate virtual environment
python -m venv venv
.\venv\Scripts\Activate

# Install dependencies
pip install -r requirements-minimal.txt

# Go back to parent directory and start server
cd ..
python -m backend.main_simple
```

**Expected output:** Server starts in ~5-10 seconds

---

## Step 2: Start Frontend (PowerShell - New Window)

Open a NEW PowerShell window:

```powershell
cd C:\Users\Edozie\Downloads\MalwareIntel-ed\PAMS\frontend

# Install dependencies (first time only)
npm install

# Start dev server
npm run dev
```

**Expected output:** Frontend ready in ~10-15 seconds

---

## Access Your Application

- Landing Page: http://localhost:3000/landing
- Dashboard: http://localhost:3000/dashboard
- Login: http://localhost:3000/auth/login
- API Docs: http://localhost:8000/docs

**Test Accounts:**
- Admin: `admin` / `Admin123!`
- Analyst: `analyst` / `Analyst123!`

---

## For Screenshots

Follow **SCREENSHOT_GUIDE.md** once both servers are running.

---

## Why Not WSL?

WSL accessing Windows files has 10-20x slower file I/O. This makes pandas/numpy load take 60+ seconds instead of 5 seconds.

If you must use WSL, expect long waits during startup.

