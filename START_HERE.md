# 🚀 Quick Start Guide - Get PAMS Running Now!

## Option 1: Automatic Start (Windows - Recommended)

### Using PowerShell (Best for Windows):

1. **Open PowerShell** (Right-click Start menu → Windows PowerShell)

2. **Navigate to project**:
   ```powershell
   cd C:\Users\Edozie\Downloads\MalwareIntel-ed\PAMS
   ```

3. **Run the start script**:
   ```powershell
   .\start-simple.ps1
   ```

   If you get a security error, first run:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
   Then try again.

---

## Option 2: Manual Start (Step-by-Step)

### Step 1: Install Dependencies

Open Command Prompt or PowerShell and run:

```bash
cd C:\Users\Edozie\Downloads\MalwareIntel-ed\PAMS

python -m pip install --upgrade pip
python -m pip install fastapi uvicorn sqlalchemy pydantic pydantic-settings python-dotenv pandas numpy scikit-learn
```

### Step 2: Start the Backend Server

```bash
python -m uvicorn backend.main_simple:app --reload --host 0.0.0.0 --port 8000
```

### Step 3: Open Your Browser

Once you see "Application startup complete", open your browser and visit:

- **📊 API Documentation**: http://localhost:8000/docs
- **🏠 Home Page**: http://localhost:8000
- **❤️ Health Check**: http://localhost:8000/health

---

## ✅ What You'll See

### In the Terminal:
```
🚀 Starting PAMS - Product Alert Management System
✓ Database initialized successfully
✓ Created 3 products
✓ Created 4 alerts
✓ Created 2 users

📊 API Documentation: http://localhost:8000/docs
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### In Your Browser (http://localhost:8000/docs):
- Interactive API documentation
- Try out all endpoints
- See request/response examples

---

## 🎯 Quick Test - Try These API Calls

### 1. Get All Alerts
Visit: http://localhost:8000/api/alerts/

### 2. Get Dashboard Summary
Visit: http://localhost:8000/api/alerts/dashboard/summary

### 3. Get All Products
Visit: http://localhost:8000/api/products/

### 4. Interactive Testing
Visit: http://localhost:8000/docs
- Click on any endpoint
- Click "Try it out"
- Click "Execute"
- See live results!

---

## 🔧 Troubleshooting

### "python: command not found"
- Make sure Python 3.11+ is installed
- Try using `py` instead of `python`
- Or use full path: `C:\Python311\python.exe`

### Port 8000 already in use
- Change port: `--port 8001` in the command
- Or kill the process using port 8000

### Import errors
- Reinstall dependencies:
  ```bash
  python -m pip install --force-reinstall fastapi uvicorn sqlalchemy pydantic pydantic-settings python-dotenv
  ```

---

## 📱 Frontend (Optional - For Full Dashboard)

The backend API is now running! To see the full dashboard:

1. **Install Node.js** from https://nodejs.org/ (if not installed)

2. **In a new terminal**:
   ```bash
   cd C:\Users\Edozie\Downloads\MalwareIntel-ed\PAMS\frontend
   npm install
   npm run dev
   ```

3. **Visit**: http://localhost:3000

---

## 🎉 Success!

If you see the PAMS API docs at http://localhost:8000/docs, you're all set!

**Sample Data Included:**
- ✅ 3 Products (Smart Watch, BP Monitor, Industrial Sensor)
- ✅ 4 Alerts (Critical to Low severity)
- ✅ 2 Users (Admin & Analyst)
- ✅ All API endpoints ready to test

---

## 💡 Next Steps

1. **Explore the API**: http://localhost:8000/docs
2. **Test predictions**: Try the `/api/predictions/` endpoints
3. **View alerts dashboard**: `/api/alerts/dashboard/summary`
4. **Read full docs**: See README.md

---

## 🆘 Need Help?

Still having issues? Here's what to check:

1. **Python version**: Run `python --version` (should be 3.11+)
2. **Dependencies installed**: Run `python -m pip list | findstr fastapi`
3. **Port available**: Make sure port 8000 is free
4. **Path correct**: Make sure you're in the PAMS directory

**Quick Fix Command:**
```bash
cd C:\Users\Edozie\Downloads\MalwareIntel-ed\PAMS && python -m pip install fastapi uvicorn sqlalchemy pydantic pydantic-settings python-dotenv pandas numpy scikit-learn && python -m uvicorn backend.main_simple:app --reload
```

Just copy and paste this entire command!

---

**Ready to go? Open your browser to http://localhost:8000/docs and start exploring!** 🚀
