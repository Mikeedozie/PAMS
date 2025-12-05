# 🚀 PAMS - Modern Interface Quick Start

## ✨ New Features

Your PAMS platform now includes:

### 🎨 **Beautiful Landing Page**
- Professional hero section with gradient design
- Feature showcase with animations
- System statistics and metrics
- Call-to-action buttons

### 📊 **User Dashboard** 
- Real-time alert monitoring with charts
- Interactive data visualizations (bar charts, pie charts)
- Product inventory overview with low-stock warnings
- Smart alert table with scoring and status tracking
- Color-coded severity badges
- Easy filtering and export options

### ⚙️ **Admin Panel**
- Comprehensive system overview
- Product management (add, edit, delete)
- Alert management with bulk operations
- System health monitoring
- User management (coming soon)
- Settings and configuration (coming soon)

---

## 🎯 Quick Start (Easiest Method)

### Option 1: Double-Click Startup (Recommended)

1. **Double-click** `START_COMPLETE.bat` in the PAMS folder
2. Wait 10-20 seconds for both servers to start
3. Open your browser to: **http://localhost:3000/landing**

That's it! 🎉

---

## 🔧 Manual Startup (Alternative)

### Step 1: Start Backend Server

Open **Command Prompt** (not Git Bash) and run:

```cmd
cd C:\Users\Edozie\Downloads\MalwareIntel-ed\PAMS
python -m uvicorn backend.main_simple:app --reload --host 127.0.0.1 --port 8000
```

### Step 2: Start Frontend Server

Open a **NEW Command Prompt window** and run:

```cmd
cd C:\Users\Edozie\Downloads\MalwareIntel-ed\PAMS\frontend
npm install
npm run dev
```

---

## 🌐 Access Your Application

Once both servers are running, visit:

| Page | URL | Description |
|------|-----|-------------|
| **Landing Page** | http://localhost:3000/landing | Beautiful homepage with features |
| **User Dashboard** | http://localhost:3000/dashboard | Real-time monitoring & charts |
| **Admin Panel** | http://localhost:3000/admin | System management & configuration |
| **API Docs** | http://localhost:8000/docs | Interactive API documentation |

---

## 📱 What You'll See

### Landing Page (`/landing`)
- Modern gradient hero section
- Feature cards with icons and descriptions
- Statistics dashboard (10K+ alerts, 94% accuracy, etc.)
- "How It Works" section with 4-step process
- Call-to-action buttons to dashboard and admin panel

### User Dashboard (`/dashboard`)
- 4 summary cards: Total Alerts, Open Alerts, Critical Alerts, Last 24h
- Bar chart showing alerts by category
- Pie chart showing alert severity distribution
- Recent alerts table with:
  - Severity badges (color-coded)
  - Progress bars for alert scores
  - Status icons
  - View details buttons
- Product inventory cards showing:
  - SKU and product name
  - Current stock levels
  - Low-stock warnings

### Admin Panel (`/admin`)
- 5 tabs: Overview, Products, Alerts, Users, Settings
- **Overview Tab**:
  - 4 gradient stat cards
  - Alert status pie chart
  - Alert severity bar chart
  - System status indicators
- **Products Tab**:
  - Full product list with edit/delete actions
  - Add new product button
  - Import/export capabilities
- **Alerts Tab**:
  - Complete alert management
  - Create, edit, delete alerts
  - Export functionality

---

## 🎨 Design Features

- **Modern UI**: Gradient backgrounds, smooth animations, professional styling
- **Responsive**: Works on desktop, tablet, and mobile
- **Dark Theme**: Sleek dark mode with purple/pink accents
- **Interactive Charts**: Live data visualization with recharts
- **Icons**: 100+ beautiful icons from Lucide React
- **Color-Coded**: Red (Critical), Orange (High), Yellow (Medium), Blue (Low)
- **Easy Navigation**: Clear buttons and links between all pages

---

## 🔄 Sample Data Included

The system comes pre-loaded with:
- **3 Products**: Smart Watch Pro, MediKit Plus, Industrial Sensor X1
- **4 Alerts**: Various severities (Critical, High, Medium, Low)
- **2 Users**: Admin and viewer accounts

---

## 💡 For Non-Developers

### How to Add a Product:
1. Go to **Admin Panel** (http://localhost:3000/admin)
2. Click **Products** tab
3. Click **Add Product** button
4. Fill in the form (coming soon - currently view-only)

### How to View Alerts:
1. Go to **User Dashboard** (http://localhost:3000/dashboard)
2. Scroll to "Recent Alerts" section
3. Click "View Details" on any alert

### How to Monitor System Health:
1. Go to **Admin Panel** (http://localhost:3000/admin)
2. Click **Overview** tab
3. View system status at the bottom

---

## 🛑 Stopping the Servers

To stop the servers:
- Press `Ctrl+C` in each Command Prompt window
- Or simply close the Command Prompt windows

---

## 🐛 Troubleshooting

### Frontend won't start:
```cmd
cd frontend
npm install --force
npm run dev
```

### Backend won't start:
```cmd
python -m pip install --upgrade pip
python -m pip install fastapi uvicorn sqlalchemy pydantic pydantic-settings python-dotenv pandas numpy scikit-learn
python -m uvicorn backend.main_simple:app --reload --host 127.0.0.1 --port 8000
```

### Port already in use:
- Stop any other applications using port 3000 or 8000
- Or use different ports:
  ```cmd
  # Backend on port 8001
  python -m uvicorn backend.main_simple:app --reload --host 127.0.0.1 --port 8001
  
  # Frontend on port 3001
  npm run dev -- -p 3001
  ```

---

## 📦 What's Installed

### Frontend Dependencies:
- **Next.js 14**: React framework
- **Recharts**: Chart library for visualizations
- **Lucide React**: Beautiful icon library
- **Tailwind CSS**: Utility-first CSS framework

### Backend Dependencies:
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: Database ORM
- **Pydantic**: Data validation
- **Pandas/NumPy**: Data processing
- **Scikit-learn**: Machine learning (basic version)

---

## 🎯 Next Steps

1. Explore the landing page
2. Check out the user dashboard with live charts
3. Browse the admin panel
4. View the API documentation at /docs
5. Try the interactive API endpoints

Enjoy your modern PAMS interface! 🎉
