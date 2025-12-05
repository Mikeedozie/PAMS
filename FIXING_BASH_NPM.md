# 🛠️ FIXING NPM IN GIT BASH - Complete Guide

## ❌ Why Git Bash Can't Find npm

Git Bash is a **Linux-style terminal** for Windows. It doesn't automatically see Windows programs like:
- `npm` (Node Package Manager)
- `python` (sometimes)
- Other Windows executables

## ✅ SOLUTION 1: Use Command Prompt Instead (EASIEST)

### Step-by-Step Instructions:

1. **Press `Windows Key + R`** on your keyboard
2. **Type:** `cmd` and press Enter
3. A black Command Prompt window will open
4. **Copy and paste this command:**
   ```cmd
   cd C:\Users\Edozie\Downloads\MalwareIntel-ed\PAMS && START_COMPLETE.bat
   ```
5. Press **Enter**
6. Two new windows will open (backend and frontend servers)
7. Wait **20-30 seconds** for installation and startup
8. Open your browser to: **http://localhost:3000/landing**

### That's it! 🎉

---

## ✅ SOLUTION 2: Use PowerShell (ALSO EASY)

1. **Press `Windows Key + R`**
2. **Type:** `powershell` and press Enter
3. **Run:**
   ```powershell
   cd C:\Users\Edozie\Downloads\MalwareIntel-ed\PAMS
   .\START_COMPLETE.bat
   ```

---

## ✅ SOLUTION 3: Fix Git Bash Permanently

If you really want to use Git Bash, follow these steps:

### A. Find Node.js Installation Path

1. Open **Command Prompt** (not Git Bash)
2. Run: `where node`
3. You'll see something like: `C:\Program Files\nodejs\node.exe`
4. Remember this path!

### B. Add to Git Bash PATH

1. Open Git Bash
2. Run this command (replace the path if different):
   ```bash
   echo 'export PATH="/c/Program Files/nodejs:$PATH"' >> ~/.bashrc
   echo 'export PATH="$APPDATA/npm:$PATH"' >> ~/.bashrc
   source ~/.bashrc
   ```

3. Test if it works:
   ```bash
   npm --version
   ```

### C. If Still Doesn't Work

The Node.js installer might not have set up the PATH correctly. To fix:

1. **Press Windows Key + R**
2. Type: `sysdm.cpl` and press Enter
3. Click **"Advanced"** tab
4. Click **"Environment Variables"**
5. Under **"User variables"**, find **"Path"**
6. Click **"Edit"**
7. Click **"New"** and add:
   - `C:\Program Files\nodejs`
   - `%APPDATA%\npm`
8. Click **OK** three times
9. **Close and reopen Git Bash**

---

## 🚀 Quick Start Commands (Command Prompt)

### Start Everything:
```cmd
cd C:\Users\Edozie\Downloads\MalwareIntel-ed\PAMS
START_COMPLETE.bat
```

### Start Backend Only:
```cmd
cd C:\Users\Edozie\Downloads\MalwareIntel-ed\PAMS
python -m uvicorn backend.main_simple:app --reload --host 127.0.0.1 --port 8000
```

### Start Frontend Only (in new window):
```cmd
cd C:\Users\Edozie\Downloads\MalwareIntel-ed\PAMS\frontend
npm install
npm run dev
```

---

## 🐛 Common Issues

### "npm is not recognized"
**Cause:** Node.js is not installed or not in PATH
**Fix:** 
1. Download Node.js from: https://nodejs.org/
2. Install it (choose "Add to PATH" during installation)
3. Restart your terminal

### "python is not recognized" in Git Bash
**Cause:** Python not in Git Bash PATH
**Fix:** Use Command Prompt instead, or add Python to PATH like npm above

### Port 3000 already in use
**Cause:** Frontend already running or another app using port 3000
**Fix:**
```cmd
# Kill the process
taskkill /F /IM node.exe
# Or use a different port
npm run dev -- -p 3001
```

### Port 8000 already in use
**Cause:** Backend already running
**Fix:**
```cmd
# Kill the process
taskkill /F /IM python.exe
# Or use a different port
python -m uvicorn backend.main_simple:app --reload --port 8001
```

---

## 📝 Summary

**For the quickest setup:**
1. Don't use Git Bash - use Command Prompt
2. Double-click `START_COMPLETE.bat`
3. Wait 30 seconds
4. Open http://localhost:3000/landing

**Your Git Bash is fine for:**
- Git commands
- File operations
- Python scripts (if Python is in PATH)

**Use Command Prompt for:**
- npm commands
- Starting the PAMS frontend
- Any Windows-specific tools

---

## 🎯 What You Should Do Right Now

1. **Close Git Bash**
2. **Press Windows Key + R**
3. **Type:** `cmd`
4. **Press Enter**
5. **Run:** `cd C:\Users\Edozie\Downloads\MalwareIntel-ed\PAMS && START_COMPLETE.bat`
6. **Wait 30 seconds**
7. **Open browser:** http://localhost:3000/landing

Enjoy! 🎉
