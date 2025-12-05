# PAMS Quick Start Guide (WSL/Linux)

## Step 1: Start Backend Server

Open a new terminal (WSL) and run:

```bash
cd /mnt/c/Users/Edozie/Downloads/MalwareIntel-ed/PAMS/backend

# Activate virtual environment (if already created)
source venv/bin/activate

# Start server
python main_simple.py
```

The backend will be available at:
- **API:** http://localhost:8000
- **Documentation:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

### Test Credentials:
- **Admin:** username: `admin`, password: `Admin123!`
- **Analyst:** username: `analyst`, password: `Analyst123!`

---

## Step 2: Start Frontend Server

Open a **second** terminal (WSL) and run:

```bash
cd /mnt/c/Users/Edozie/Downloads/MalwareIntel-ed/PAMS/frontend

# Install dependencies (first time only)
npm install

# Start development server
npm run dev
```

The frontend will be available at:
- **Landing Page:** http://localhost:3000/landing
- **Dashboard:** http://localhost:3000/dashboard  
- **Admin Panel:** http://localhost:3000/admin
- **Login:** http://localhost:3000/auth/login

---

## Taking Screenshots

Once both servers are running, follow the instructions in **SCREENSHOT_GUIDE.md** to capture figures for Chapter 4.

### Quick Screenshot Checklist:

**Fig 4.1 - Landing Page:**
1. Visit: http://localhost:3000/landing
2. Make sure you're logged OUT
3. Capture full page with hero section

**Fig 4.2 - User Dashboard:**
1. Visit: http://localhost:3000/auth/login
2. Login as: `analyst` / `Analyst123!`  
3. Auto-redirected to dashboard
4. Wait for charts to load
5. Capture full page

**Fig 4.5 - Alert Dashboard:**
1. On dashboard, scroll to "Recent Alerts" table
2. Capture the alert table section

---

## Troubleshooting

**Backend won't start:**
```bash
# Reinstall dependencies
cd /mnt/c/Users/Edozie/Downloads/MalwareIntel-ed/PAMS/backend
source venv/bin/activate
pip install -r requirements-minimal.txt
```

**Frontend won't start:**
```bash
# Clear and reinstall
cd /mnt/c/Users/Edozie/Downloads/MalwareIntel-ed/PAMS/frontend
rm -rf node_modules .next
npm install
npm run dev
```

**No data showing:**
- Delete `pams.db` file in backend folder
- Restart backend server (will reseed data automatically)

---

## Stop Servers

Press `Ctrl+C` in each terminal to stop the servers.

---

## Next Steps

After both servers are running successfully:
1. Test login at http://localhost:3000/auth/login
2. Verify dashboard loads with data
3. Follow SCREENSHOT_GUIDE.md for Chapter 4 figures
4. Create diagrams (Fig 4.3, 4.4, 4.6, 4.7) using Draw.io or similar tools
