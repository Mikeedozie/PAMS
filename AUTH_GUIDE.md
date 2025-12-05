# 🔐 PAMS Authentication Guide

## ⚠️ IMPORTANT: Login vs Signup

### Default Test Accounts (Already Created)
These accounts are **pre-created** in the database. Use them to **LOGIN**, not signup:

1. **Admin Account:**
   - Username: `admin`
   - Password: `Admin123!`
   - Role: Administrator

2. **Analyst Account:**
   - Username: `analyst`
   - Password: `Analyst123!`
   - Role: Product Analyst

---

## 🚨 Common Errors & Solutions

### Error: "Registration failed (username/email may be taken)"
**Cause:** You're trying to signup with `admin` or `analyst` - these already exist!

**Solutions:**
1. **Use different credentials** for signup:
   - Username: `testuser` (or any unique name)
   - Email: `test@example.com` (or any unique email)
   - Password: `Test123!`

2. **Or just LOGIN** with the existing accounts above

---

### Error: "Invalid credentials" when logging in
**Causes & Fixes:**

#### 1. Backend not running
```bash
# Check if backend is running
curl http://localhost:8000/health

# If no response, start backend:
cd C:\Users\Edozie\Downloads\MalwareIntel-ed\PAMS
python -m backend.main_screenshot
```

#### 2. Database schema mismatch
```bash
# Delete old database and restart (Windows PowerShell):
cd C:\Users\Edozie\Downloads\MalwareIntel-ed\PAMS
Remove-Item pams.db -Force
python -m backend.main_screenshot
```

#### 3. Wrong password format
- Make sure to use `Admin123!` (capital A, exclamation mark)
- Don't add extra spaces

---

## ✅ How to Test Authentication

### Option 1: Use API Directly (cURL)
```bash
# Test login
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=Admin123%21&grant_type=password"

# Should return:
# {"access_token":"eyJ...","token_type":"bearer","expires_in":21600}
```

### Option 2: Use Frontend
1. Start frontend: `npm run dev` in `/frontend` directory
2. Visit http://localhost:3000/auth/login
3. Enter `admin` / `Admin123!`
4. Click "Sign In"
5. Should redirect to dashboard

### Option 3: Use Swagger UI
1. Visit http://localhost:8000/docs
2. Click "Authorize" button (top right)
3. Enter username: `admin`, password: `Admin123!`
4. Click "Authorize"
5. Test any endpoint

---

## 🔄 Reset Database (Fresh Start)

### Windows PowerShell:
```powershell
cd C:\Users\Edozie\Downloads\MalwareIntel-ed\PAMS

# Stop backend (Ctrl+C in terminal or close window)

# Delete database
Remove-Item pams.db -Force -ErrorAction SilentlyContinue

# Restart backend
python -m backend.main_screenshot
```

### WSL/Linux:
```bash
cd /mnt/c/Users/Edozie/Downloads/MalwareIntel-ed/PAMS

# Stop backend
pkill -f "python3 -m backend.main_screenshot"

# Delete database (use Windows path)
rm -f /mnt/c/Users/Edozie/Downloads/MalwareIntel-ed/PAMS/pams.db

# Restart backend
source backend/venv/bin/activate
python3 -m backend.main_screenshot
```

---

## 📝 Creating New Accounts

### Via API (cURL):
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "newuser@example.com",
    "password": "NewPass123!",
    "full_name": "New User"
  }'
```

### Via Frontend:
1. Visit http://localhost:3000/auth/register
2. Fill in the form with **unique** username and email
3. Click "Create Account"
4. Will auto-login after successful registration

---

## 🔍 Troubleshooting Checklist

- [ ] Backend running on port 8000?
  - Test: `curl http://localhost:8000/health`
  
- [ ] Frontend running on port 3000?
  - Test: Visit `http://localhost:3000`
  
- [ ] Using correct credentials?
  - `admin` / `Admin123!` (case-sensitive!)
  
- [ ] Database initialized?
  - Check: `pams.db` file exists
  - Check backend logs for "Created 3 products, 4 alerts, 2 users"
  
- [ ] API path correct?
  - Should be: `/api/auth/login` (not `/auth/api/auth/login`)
  
- [ ] No CORS errors in browser console?
  - Press F12, check Console tab

---

## 🎯 Quick Test Script

Save this as `test_auth.sh` and run it:

```bash
#!/bin/bash

echo "=== Testing PAMS Authentication ==="

echo -e "\n1. Testing backend health..."
curl -s http://localhost:8000/health | jq '.' || echo "❌ Backend not running!"

echo -e "\n\n2. Testing admin login..."
curl -s -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=Admin123%21&grant_type=password" | jq '.' || echo "❌ Login failed!"

echo -e "\n\n3. Testing analyst login..."
curl -s -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=analyst&password=Analyst123%21&grant_type=password" | jq '.' || echo "❌ Login failed!"

echo -e "\n\n=== Test complete! ==="
```

---

## 📚 Additional Resources

- **Backend API Docs:** http://localhost:8000/docs
- **Backend Health:** http://localhost:8000/health
- **Frontend Landing:** http://localhost:3000/landing
- **Frontend Login:** http://localhost:3000/auth/login
- **Frontend Signup:** http://localhost:3000/auth/register

---

**Remember:** The default accounts are for **testing only**. In production, you would:
1. Remove or disable default accounts
2. Implement password complexity requirements
3. Add rate limiting on login attempts
4. Enable two-factor authentication
5. Use environment variables for sensitive data
