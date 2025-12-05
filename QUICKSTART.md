# PAMS Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Option 1: Docker (Recommended)

**Prerequisites:** Docker and Docker Compose installed

```bash
# 1. Clone the repository
git clone https://github.com/Mikeedozie/PAMS.git
cd PAMS

# 2. Copy environment file
cp backend/.env.example backend/.env

# 3. Start all services
docker-compose up -d

# 4. Wait for services to be ready (30 seconds)
# Then access:
# - API Docs: http://localhost:8000/docs
# - Frontend: http://localhost:3000
```

### Option 2: Manual Setup

#### Backend Setup

```bash
# 1. Navigate to backend
cd backend

# 2. Create virtual environment
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Linux/Mac:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up database
# Install PostgreSQL 15+ first, then:
createdb pams

# Optional: Install TimescaleDB extension
psql -d pams -c "CREATE EXTENSION IF NOT EXISTS timescaledb;"

# 5. Copy and configure environment
cp .env.example .env
# Edit .env with your database credentials

# 6. Run migrations
alembic upgrade head

# 7. Start the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

```bash
# 1. Navigate to frontend (in new terminal)
cd frontend

# 2. Install dependencies
npm install

# 3. Set up environment
cp .env.local.example .env.local

# 4. Start development server
npm run dev

# Access: http://localhost:3000
```

---

## 📝 First Steps After Installation

### 1. Access API Documentation
Visit: http://localhost:8000/docs

### 2. Create Your First Product

```bash
curl -X POST "http://localhost:8000/api/products/" \
  -H "Content-Type: application/json" \
  -d '{
    "sku": "PROD-001",
    "name": "Sample Product",
    "category": "electronics",
    "current_stock": 100,
    "reorder_point": 20
  }'
```

### 3. Create an Alert

```bash
curl -X POST "http://localhost:8000/api/alerts/" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "severity": "high",
    "category": "quality",
    "description": "Quality issue detected",
    "confidence": 0.85
  }'
```

### 4. Run a Stockout Prediction

```bash
curl -X POST "http://localhost:8000/api/predictions/stockout/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "forecast_days": 30
  }'
```

---

## 🔑 Key Endpoints

### Products
- `GET /api/products/` - List all products
- `POST /api/products/` - Create product
- `GET /api/products/{id}` - Get product details

### Alerts
- `GET /api/alerts/` - List alerts (with filters)
- `POST /api/alerts/` - Create alert
- `GET /api/alerts/dashboard/summary` - Dashboard summary

### Predictions
- `POST /api/predictions/forecast/demand` - Forecast demand
- `POST /api/predictions/stockout/predict` - Predict stockout
- `POST /api/predictions/anomaly/detect` - Detect anomalies

---

## 🐛 Troubleshooting

### Database Connection Error
```bash
# Check PostgreSQL is running:
# Windows:
net start postgresql-x64-15

# Linux:
sudo systemctl status postgresql

# Mac:
brew services start postgresql@15
```

### Redis Connection Error
```bash
# Check Redis is running:
redis-cli ping
# Should return: PONG

# Start Redis:
# Windows: Install Redis from https://github.com/microsoftarchive/redis/releases
# Linux: sudo systemctl start redis
# Mac: brew services start redis
```

### Port Already in Use
```bash
# Backend (8000):
# Windows: netstat -ano | findstr :8000
# Linux/Mac: lsof -i :8000

# Frontend (3000):
# Windows: netstat -ano | findstr :3000
# Linux/Mac: lsof -i :3000

# Kill the process or change ports in .env files
```

### ML Dependencies Installation Issues
```bash
# If TensorFlow fails to install:
pip install tensorflow-cpu==2.15.0

# If Prophet fails:
# Windows: Download Visual C++ Build Tools first
# Linux: sudo apt-get install python3-dev
# Mac: brew install gcc
```

---

## 📊 Sample Data

To load sample data for testing:

```python
# Run this in Python shell after starting backend
from backend.database import SessionLocal
from backend import models
from datetime import datetime, timedelta
import random

db = SessionLocal()

# Create sample products
products = [
    models.Product(sku="ELEC-001", name="Smart Watch", category="electronics", 
                   current_stock=150, reorder_point=30),
    models.Product(sku="MED-001", name="Blood Pressure Monitor", category="medical",
                   current_stock=50, reorder_point=15),
]
db.add_all(products)
db.commit()

# Create sample inventory metrics
for product in products:
    for i in range(60):  # 60 days of data
        timestamp = datetime.utcnow() - timedelta(days=60-i)
        metric = models.InventoryMetric(
            product_id=product.id,
            timestamp=timestamp,
            stock_level=product.current_stock + random.randint(-20, 20),
            demand=random.randint(5, 20)
        )
        db.add(metric)

db.commit()
print("Sample data created successfully!")
```

---

## 🎯 Next Steps

1. **Explore the Dashboard**: http://localhost:3000
2. **Read API Docs**: http://localhost:8000/docs
3. **Configure Notifications**: Edit `backend/.env` SMTP settings
4. **Customize ML Models**: Check `backend/ml/` modules
5. **Set Up Monitoring**: Enable Prometheus with `docker-compose --profile monitoring up`

---

## 📚 Additional Resources

- **Full Documentation**: See README.md
- **API Reference**: http://localhost:8000/docs
- **GitHub Issues**: Report bugs or request features
- **Configuration Guide**: See `backend/.env.example`

---

**Need Help?** Open an issue on GitHub or check the troubleshooting section above.
