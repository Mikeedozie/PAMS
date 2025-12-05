# PAMS Chapter 4 - Screenshot Guide

## Prerequisites

Before taking screenshots, ensure:

1. **Backend is running:**
   ```bash
   cd backend
   python main_simple.py
   # Should be accessible at http://localhost:8000
   ```

2. **Frontend is running:**
   ```bash
   cd frontend
   npm run dev
   # Should be accessible at http://localhost:3000
   ```

3. **Test credentials available:**
   - **Admin:** username: `admin`, password: `Admin123!`
   - **Analyst:** username: `analyst`, password: `Analyst123!`

4. **Browser preparation:**
   - Use Chrome or Edge in full-screen mode (F11)
   - Set zoom to 100%
   - Clear browser cache if needed
   - Use incognito/private mode for clean screenshots

---

## Fig. 4.1: System Landing Page

**Purpose:** Showcase the landing page with authentication controls, feature highlights, and marketing content.

### Steps:
1. Navigate to: `http://localhost:3000/landing`
2. Ensure you are **logged out** (if logged in, click user menu → Logout)
3. Scroll to show the full hero section with:
   - PAMS logo and navigation bar
   - "AI-Powered Product Alert Management" headline
   - "Login" and "Sign Up" buttons in top-right
   - Stats cards (Alerts Processed, Prediction Accuracy, etc.)
4. **Screenshot area:** Full page from top navigation to stats section

### What should be visible:
- ✓ Navigation bar with PAMS logo
- ✓ Login and Sign Up buttons (not logged in state)
- ✓ Large hero headline: "AI-Powered Product Alert Management"
- ✓ Subtext about predictive intelligence
- ✓ "Get Started" and "Admin Console" CTA buttons
- ✓ Four stats cards showing metrics

### Screenshot settings:
- **Resolution:** 1920x1080 or higher
- **Format:** PNG
- **Capture:** Full viewport or crop to show hero + stats
- **File name:** `fig_4_1_landing_page.png`

---

## Fig. 4.2: User Dashboard Overview

**Purpose:** Display the main operational dashboard with KPIs, charts, alerts table, and product inventory.

### Steps:
1. If not logged in, go to: `http://localhost:3000/auth/login`
2. Login with:
   - Username: `analyst`
   - Password: `Analyst123!`
3. You should be redirected to: `http://localhost:3000/dashboard`
4. Wait for all data to load (charts, alert cards, product cards)
5. Scroll to show:
   - Top KPI cards (Total Alerts, Open Alerts, Critical Issues, Last 24 Hours)
   - Two charts side-by-side (Alerts by Category bar chart, Alert Severity pie chart)
   - Recent Alerts table with at least 4-5 rows
   - Product Inventory cards at bottom

### What should be visible:
- ✓ Header with "User Dashboard" title
- ✓ User menu showing "analyst" username
- ✓ Four summary cards with icons and numbers
- ✓ Bar chart: "Alerts by Category"
- ✓ Pie chart: "Alert Severity" with color coding
- ✓ Alerts table with columns: Alert, Severity, Category, Score, Status, Actions
- ✓ Product inventory cards showing SKU, stock levels, status badges
- ✓ Color-coded severity badges (Critical=red, High=orange, Medium=yellow, Low=blue)

### Screenshot settings:
- **Capture method:** Full-page screenshot (use browser extension if needed)
- **File name:** `fig_4_2_user_dashboard.png`
- **Note:** May need multiple screenshots if one screen doesn't fit all sections

**Alternative - Two screenshots:**
- `fig_4_2a_dashboard_top.png` - KPIs + Charts
- `fig_4_2b_dashboard_alerts_products.png` - Alerts table + Products

---

## Fig. 4.3: System Subsystem Architecture

**Purpose:** System architecture diagram (create externally).

### This is a DIAGRAM, not a screenshot from the app.

**You need to create this using:**
- Draw.io (https://app.diagrams.net)
- Microsoft Visio
- Lucidchart
- PowerPoint with SmartArt

### Diagram content:
Create a layered architecture showing:

**Layer 1 - Frontend:**
- React/Next.js Web Dashboard
- Authentication UI
- Charts & Visualization

**Layer 2 - API Gateway:**
- FastAPI REST Endpoints
- JWT Authentication Middleware
- CORS Configuration

**Layer 3 - Business Logic:**
- Alert Generation Engine
- Predictive Analytics Module
- Feature Engineering
- Decision Engine

**Layer 4 - Machine Learning:**
- Anomaly Detection (Isolation Forest)
- Risk Classification (Random Forest)
- Demand Forecasting (ARIMA, Prophet, LSTM)

**Layer 5 - Data Layer:**
- SQLAlchemy ORM
- Database (SQLite/PostgreSQL)
- 15 interconnected tables

**External Systems (side):**
- ERP Integration
- IoT Sensors
- Quality Databases
- Supplier Feeds

### Visual style:
- Use boxes with different colors for each layer
- Show arrows indicating data flow
- Include technology names in each box
- Use professional color scheme (blues, purples, grays)

### File name: `fig_4_3_architecture_diagram.png`

---

## Fig. 4.4: Database Schema ERD

**Purpose:** Entity-Relationship Diagram showing all 15 tables and relationships.

### This is a DATABASE DIAGRAM, not a screenshot from the app.

**Option 1 - Generate from actual database:**

If you have DB Browser for SQLite installed:
1. Open `pams.db` file with DB Browser for SQLite
2. Go to "Database Structure" tab
3. Use "Export" → "Schema as image" or take screenshot

**Option 2 - Use online ERD tools:**
- dbdiagram.io
- QuickDBD
- Draw.io with database shapes

### Tables to include:
1. **users** - id, username, email, hashed_password, role, created_at
2. **products** - id, sku, name, category, current_stock, reorder_point, unit_cost
3. **alerts** - id, product_id (FK), severity, category, description, status, score, confidence, created_at
4. **predictions** - id, product_id (FK), model_name, prediction_type, confidence, predicted_value, created_at
5. **inventory_metrics** - id, product_id (FK), timestamp, stock_level, demand, turnover_rate
6. **quality_metrics** - id, product_id (FK), timestamp, defect_rate, inspection_count, quality_score
7. **supplier_risks** - id, supplier_name, risk_level, risk_score, lead_time_days
8. **workflow_cases** - id, alert_id (FK), case_number, status, priority, assigned_to (FK)
9. **notification_logs** - id, alert_id (FK), recipient_id (FK), channel, status, sent_at
10. **model_performance** - id, model_name, model_version, metric_name, metric_value
11. **feedback_loops** - id, prediction_id (FK), alert_id (FK), was_accurate, submitted_by (FK)
12. **audit_logs** - id, user_id (FK), action, resource_type, timestamp
13. **data_sources** - id, name, source_type, active, last_sync
14. Plus any additional supporting tables

### Relationships to show:
- products → alerts (one-to-many)
- products → predictions (one-to-many)
- products → inventory_metrics (one-to-many)
- products → quality_metrics (one-to-many)
- alerts → workflow_cases (one-to-many)
- alerts → notification_logs (one-to-many)
- users → alerts (assigned_to)
- users → workflow_cases (assigned_to)

### Visual requirements:
- Show primary keys (PK) with key icon
- Show foreign keys (FK) with arrows
- Use crow's foot notation for cardinality
- Color-code table groups (core entities, metrics, workflows, system)
- Include data types for key fields

### File name: `fig_4_4_database_erd.png`

---

## Fig. 4.5: Alert Dashboard Display

**Purpose:** Detailed view of alert management with filtering, prioritization, and comprehensive alert information.

### Steps:
1. Ensure logged in as `analyst` or `admin`
2. Navigate to: `http://localhost:3000/dashboard`
3. Scroll to the "Recent Alerts" table section
4. Focus on showing:
   - Alert table header with "Filter" and "Export" buttons
   - Multiple alert rows with different severities (critical, high, medium, low)
   - Severity badges in different colors
   - Alert scores shown as progress bars
   - Status icons (open, resolved, etc.)
   - "View Details" action buttons

### What should be visible:
- ✓ "Recent Alerts" heading
- ✓ Filter and Export buttons in header
- ✓ Table columns clearly labeled
- ✓ At least 5-8 alert rows
- ✓ Mix of severity levels with color-coded badges
- ✓ Alert scores displayed as percentage with visual progress bar
- ✓ Status icons (Clock for open, CheckCircle for resolved, etc.)
- ✓ Alert descriptions truncated if too long

### Enhanced view (optional):
If you want to show the "Create Alert" modal:
1. Click "+ New Alert" button in dashboard header
2. Modal should pop up showing form fields:
   - Product ID dropdown/input
   - Severity dropdown
   - Category dropdown
   - Description textarea
3. Take screenshot with modal open

### Screenshot settings:
- **Capture:** Table section prominently
- **File name:** `fig_4_5_alert_dashboard.png`
- **Alternative with modal:** `fig_4_5_alert_creation_modal.png`

---

## Fig. 4.6: System Flowchart

**Purpose:** Flowchart showing the complete workflow from data ingestion to alert notification.

### This is a FLOWCHART DIAGRAM, not a screenshot from the app.

**Create using:**
- Draw.io
- Microsoft Visio
- Lucidchart
- Mermaid diagrams

### Flowchart steps to include:

**Start:**
1. START

**Data Ingestion:**
2. Receive product data from ERP/IoT/sensors
3. Validate input data
   - Decision: Valid? → No → Error handling → Log error → END
   - Decision: Valid? → Yes → Continue

**Feature Engineering:**
4. Extract basic features (stock, reorder point, manufacturer)
5. Query historical metrics (inventory, quality, supplier)
6. Generate time-series features (lag, rolling mean, seasonality)
7. Normalize and encode features

**Parallel Processing:**
8. Split into three parallel paths:
   - Path A: Anomaly Detection (Isolation Forest)
   - Path B: Risk Classification (Random Forest)
   - Path C: Demand Forecasting (ARIMA/Prophet/LSTM)

**ML Processing:**
9. Load trained models
10. Generate predictions with confidence scores
11. Merge results from all three paths

**Alert Generation:**
12. Evaluate alert conditions (stockout, quality issues, anomalies)
13. Calculate composite alert score
14. Assign severity and priority (P1-P4)
15. Calculate SLA deadline
16. Check for duplicates
    - Decision: Duplicate exists? → Yes → Merge alerts
    - Decision: Duplicate exists? → No → Continue
17. Enrich with product context and recommendations

**Storage & Notification:**
18. Save alert to database
19. Log audit trail
20. Determine notification recipients based on severity/priority
21. Send notifications (email, SMS, in-app)

**Dashboard Update:**
22. Refresh dashboard with new alert
23. Update KPI metrics
24. END

### Visual style:
- Use standard flowchart shapes (rectangle=process, diamond=decision, parallelogram=input/output)
- Color code different sections (blue=input, green=processing, purple=ML, red=alerts, yellow=output)
- Show parallel processing with split/merge nodes
- Include error handling paths

### File name: `fig_4_6_system_flowchart.png`

---

## Fig. 4.7: Object Diagram

**Purpose:** UML object diagram showing runtime relationships during alert processing.

### This is a UML DIAGRAM, not a screenshot from the app.

**Create using:**
- StarUML
- Visual Paradigm
- Draw.io (UML shapes)
- PlantUML

### Objects to include:

**Object 1: Product**
```
:Product
-------------------------
id = 1
sku = "ELEC-001"
name = "Smart Watch Pro"
current_stock = 150
reorder_point = 30
status = "active"
```

**Object 2: InventoryMetric**
```
:InventoryMetric
-------------------------
id = 45
product_id = 1
timestamp = "2025-10-08T10:00:00Z"
stock_level = 150
demand = 25
turnover_rate = 8.5
```

**Object 3: FeatureExtractor**
```
:FeatureExtractor
-------------------------
product = :Product (link)
time_window = 30
features_generated = 35
```

**Object 4: AnomalyDetector**
```
:AnomalyDetector
-------------------------
model_version = "v1.0"
algorithm = "Isolation Forest"
anomaly_score = 0.15
is_anomaly = False
```

**Object 5: RiskClassifier**
```
:RiskClassifier
-------------------------
model_version = "v1.0"
algorithm = "Random Forest"
risk_score = 0.42
risk_level = "medium"
confidence = 0.89
```

**Object 6: AlertGenerator**
```
:AlertGenerator
-------------------------
product = :Product (link)
predictions = [:RiskClassifier]
severity = "medium"
alert_score = 54.3
priority = "P3"
```

**Object 7: Alert**
```
:Alert
-------------------------
id = 12
product_id = 1
title = "Stock declining trend"
severity = "medium"
category = "supply"
confidence_score = 0.89
alert_score = 54.3
status = "open"
created_at = "2025-10-08T10:30:00Z"
```

**Object 8: NotificationService**
```
:NotificationService
-------------------------
alert = :Alert (link)
recipients = ["analyst@pams.com"]
channel = "email"
status = "sent"
```

### Relationships (links):
- FeatureExtractor → Product (uses)
- FeatureExtractor → InventoryMetric (queries)
- AnomalyDetector → FeatureExtractor (receives features from)
- RiskClassifier → FeatureExtractor (receives features from)
- AlertGenerator → Product (references)
- AlertGenerator → RiskClassifier (uses predictions from)
- AlertGenerator → AnomalyDetector (uses detection from)
- Alert → AlertGenerator (created by)
- NotificationService → Alert (notifies about)

### Visual style:
- Use UML object notation (objectName:ClassName with underline)
- Show attributes with actual runtime values
- Draw links between objects with labels
- Group related objects visually
- Use consistent colors for similar object types

### File name: `fig_4_7_object_diagram.png`

---

## Additional Screenshots (Optional but Recommended)

### Admin Panel
**URL:** `http://localhost:3000/admin`
**Login:** admin / Admin123!

Shows:
- User management
- Product bulk operations
- System settings
- Model performance metrics

**File name:** `fig_extra_admin_panel.png`

---

### API Documentation (Swagger)
**URL:** `http://localhost:8000/docs`

Shows:
- All REST endpoints
- Request/response schemas
- Try-it-out functionality

**File name:** `fig_extra_api_docs.png`

---

### Login Page
**URL:** `http://localhost:3000/auth/login`

Shows:
- Clean login form
- Username and password fields
- "Login" button
- Link to registration

**File name:** `fig_extra_login_page.png`

---

## Screenshot Quality Checklist

Before submitting screenshots, verify:

- [ ] Resolution is at least 1920x1080
- [ ] No personal information visible (beyond test data)
- [ ] Browser UI is clean (no extra toolbars, bookmarks bar hidden)
- [ ] All text is legible (check zoom level)
- [ ] Colors are vibrant and clear
- [ ] No loading spinners or partial data
- [ ] Timestamps/data look realistic
- [ ] File names match figure numbers from Chapter 4

---

## Troubleshooting

**Problem:** Backend won't start
- Check if port 8000 is already in use
- Verify Python dependencies are installed: `pip install -r backend/requirements-minimal.txt`
- Check for database file `pams.db` - delete and restart to reseed

**Problem:** Frontend won't start
- Check if port 3000 is already in use
- Verify Node packages: `npm install` in frontend directory
- Clear .next folder: `rm -rf .next` and restart

**Problem:** Login fails
- Verify backend is running at http://localhost:8000
- Check backend logs for authentication errors
- Try reseeding database (restart backend server)

**Problem:** No data showing in dashboard
- Check browser console (F12) for API errors
- Verify CORS is enabled in backend
- Check network tab to see if API calls are returning data
- Backend might need reseeding

**Problem:** Charts not displaying
- Give page time to load (5-10 seconds)
- Check if data is present in alerts/products tables
- Refresh page (F5)

---

## Final Notes

- **Diagrams (Fig 4.3, 4.4, 4.6, 4.7)** must be created separately using diagramming tools
- **Screenshots (Fig 4.1, 4.2, 4.5)** must be taken from the running application
- Save all images in a dedicated folder: `Chapter4_Figures/`
- Use PNG format for better quality in Word documents
- Consider taking both full-page and cropped versions for flexibility
- Test print preview to ensure images fit well on A4/Letter pages

---

## Quick Command Reference

**Start backend:**
```bash
cd c:/Users/Edozie/Downloads/MalwareIntel-ed/PAMS/backend
python main_simple.py
```

**Start frontend:**
```bash
cd c:/Users/Edozie/Downloads/MalwareIntel-ed/PAMS/frontend
npm run dev
```

**Stop servers:** Press `Ctrl+C` in each terminal

**Test credentials:**
- Admin: `admin` / `Admin123!`
- Analyst: `analyst` / `Analyst123!`

---

**Good luck with your screenshots! 🎯📸**
