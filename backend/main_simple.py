"""
Simplified main.py for quick start - uses SQLite, no Redis/Celery
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import random

from backend.routes import products, alerts, predictions, auth
from backend.auth import get_password_hash
# Use simple database
from backend.database_simple import engine, Base
from backend import models

def init_db():
    """Create tables and seed sample data"""
    Base.metadata.create_all(bind=engine)
    
    from backend.database_simple import SessionLocal
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(models.Product).count() == 0:
            print("Seeding database with sample data...")
            
            # Create sample products
            sample_products = [
                models.Product(
                    sku="ELEC-001", 
                    name="Smart Watch Pro", 
                    category="electronics",
                    manufacturer="TechCorp",
                    current_stock=150,
                    reorder_point=30,
                    unit_cost=299.99
                ),
                models.Product(
                    sku="MED-001", 
                    name="Blood Pressure Monitor", 
                    category="medical",
                    manufacturer="HealthTech",
                    current_stock=50,
                    reorder_point=15,
                    unit_cost=89.99
                ),
                models.Product(
                    sku="IND-001", 
                    name="Industrial Sensor", 
                    category="industrial",
                    manufacturer="IndustrialCo",
                    current_stock=200,
                    reorder_point=40,
                    unit_cost=149.99
                ),
            ]
            db.add_all(sample_products)
            db.commit()
            
            # Create sample alerts
            sample_alerts = [
                models.Alert(
                    product_id=1, 
                    severity="critical", 
                    category="quality", 
                    description="Battery failure rate increasing 15% week-over-week. Immediate investigation required.",
                    confidence=0.89,
                    impact_score=0.85,
                    likelihood=0.80,
                    source="ml_model",
                    score=0.89
                ),
                models.Alert(
                    product_id=1, 
                    severity="high", 
                    category="supply",
                    description="Supplier lead time extended by 3 weeks due to material shortage.",
                    confidence=0.72,
                    impact_score=0.70,
                    likelihood=0.65,
                    source="integration",
                    score=0.72
                ),
                models.Alert(
                    product_id=2, 
                    severity="medium", 
                    category="demand",
                    description="Demand spike detected in Q4 forecast - consider increasing inventory.",
                    confidence=0.54,
                    impact_score=0.50,
                    likelihood=0.60,
                    source="ml_model",
                    score=0.54
                ),
                models.Alert(
                    product_id=3, 
                    severity="low", 
                    category="quality",
                    description="Minor quality variations detected within acceptable range.",
                    confidence=0.35,
                    impact_score=0.30,
                    likelihood=0.40,
                    source="sensor",
                    score=0.35
                ),
            ]
            db.add_all(sample_alerts)
            db.commit()
            # Create sample users
            sample_users = [
                models.User(
                    email="admin@pams.com",
                    username="admin",
                    name="Admin User",
                    role="admin",
                    department="Operations",
                    phone="+1234567890",
                    active=True,
                    hashed_password=get_password_hash("Admin123!")
                ),
                models.User(
                    email="analyst@pams.com",
                    username="analyst",
                    name="Data Analyst",
                    role="analyst",
                    department="Analytics",
                    active=True,
                    hashed_password=get_password_hash("Analyst123!")
                ),
            ]
            db.add_all(sample_users)
            db.commit()
            
            print(f"✓ Created {len(sample_products)} products")
            print(f"✓ Created {len(sample_alerts)} alerts")
            print(f"✓ Created {len(sample_users)} users")
            
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

# Create FastAPI app
app = FastAPI(
    title="PAMS - Product Alert Management System",
    version="1.0.0",
    description="AI-driven Product Alert Management with Predictive Analytics"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
# Import routes
from backend.routes import products, alerts, predictions

app.include_router(products.router)
app.include_router(alerts.router)
app.include_router(predictions.router)

@app.get("/")
def root():
    return {
        "message": "Welcome to PAMS - Product Alert Management System",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
def health():
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "database": "connected"
    }

@app.on_event("startup")
def startup():
    print("="*60)
    print("🚀 Starting PAMS - Product Alert Management System")
    print("="*60)
    init_db()
    print("\n✓ Database initialized successfully")
    print("\n📊 API Documentation: http://localhost:8000/docs")
    print("🏠 Home: http://localhost:8000")
    print("❤️  Health: http://localhost:8000/health")
    print("="*60)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
