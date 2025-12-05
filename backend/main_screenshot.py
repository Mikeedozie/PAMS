"""
Simplified FastAPI app for screenshot generation - NO ML DEPENDENCIES
This version removes pandas/sklearn imports to avoid WSL performance issues
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database_simple import engine, SessionLocal
from backend.models import Base, Product, Alert, User
from datetime import datetime, timedelta
from passlib.context import CryptContext

# Initialize FastAPI app
app = FastAPI(
    title="PAMS - Product Alert Management System",
    description="AI-Driven Predictive Analytics for Product Management",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def init_db():
    """Initialize database with sample data"""
    try:
        # Drop all tables first to ensure clean state
        Base.metadata.drop_all(bind=engine)
    except Exception as e:
        print(f"Note: Could not drop tables (might not exist yet): {e}")
    
    # Create all tables fresh
    try:
        Base.metadata.create_all(bind=engine, checkfirst=True)
    except Exception as e:
        print(f"Note: Error creating tables: {e}")
        # Continue anyway - tables might already exist
    
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_users = db.query(User).count()
        if existing_users > 0:
            print(f"Database already initialized with {existing_users} users")
            return
        
        print("Initializing database with sample data...")
        
        # Create users
        admin = User(
            username="admin",
            email="admin@pams.com",
            name="System Administrator",
            hashed_password=pwd_context.hash("Admin123!"),
            role="admin",
            active=True
        )
        analyst = User(
            username="analyst",
            email="analyst@pams.com",
            name="Product Analyst",
            hashed_password=pwd_context.hash("Analyst123!"),
            role="analyst",
            active=True
        )
        db.add_all([admin, analyst])
        db.flush()
        
        # Create products
        products = [
            Product(
                sku="LAPTOP-001",
                name="Professional Laptop X1",
                category="Electronics",
                status="active",
                manufacturer="TechCorp",
                current_stock=45,
                reorder_point=20,
                unit_cost=1299.99
            ),
            Product(
                sku="PHONE-002",
                name="SmartPhone Pro 15",
                category="Electronics",
                status="active",
                manufacturer="PhoneTech",
                current_stock=12,
                reorder_point=25,
                unit_cost=899.99
            ),
            Product(
                sku="TABLET-003",
                name="Business Tablet Air",
                category="Electronics",
                status="active",
                manufacturer="TabletCo",
                current_stock=78,
                reorder_point=30,
                unit_cost=599.99
            ),
        ]
        db.add_all(products)
        db.flush()
        
        # Create alerts
        alerts = [
            Alert(
                product_id=products[1].id,  # Phone - low stock
                severity="critical",
                category="inventory",
                description="Critical: Low stock alert - only 12 units remaining. Stock level (12) is below reorder point (25). Immediate action required.",
                confidence=0.95,
                score=0.92,
                impact_score=0.85,
                source="ml_model",
                status="open",
                assigned_to=analyst.id
            ),
            Alert(
                product_id=products[0].id,  # Laptop
                severity="high",
                category="demand",
                description="High: Demand surge detected for Professional Laptop X1. 40% increase in demand predicted over next 7 days.",
                confidence=0.87,
                score=0.78,
                impact_score=0.70,
                source="ml_model",
                status="open",
                assigned_to=analyst.id
            ),
            Alert(
                product_id=products[2].id,  # Tablet
                severity="medium",
                category="quality",
                description="Medium: Quality anomaly detected in recent batch. Defect rate increased to 2.3% (normal: 0.5%).",
                confidence=0.82,
                score=0.65,
                impact_score=0.60,
                source="ml_model",
                status="in_progress",
                assigned_to=analyst.id
            ),
            Alert(
                product_id=products[0].id,
                severity="low",
                category="supply",
                description="Low: Price fluctuation detected. Supplier price increased by 5% in last 30 days.",
                confidence=0.75,
                score=0.45,
                impact_score=0.40,
                source="integration",
                status="open",
                assigned_to=admin.id
            ),
        ]
        db.add_all(alerts)
        db.commit()
        
        print(f"✅ Created {len(products)} products")
        print(f"✅ Created {len(alerts)} alerts")
        print(f"✅ Created 2 users (admin/Admin123!, analyst/Analyst123!)")
        print("Database initialization complete!")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()


@app.on_event("startup")
async def startup_event():
    """Run on app startup"""
    init_db()


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "PAMS API - Product Alert Management System",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "database": "connected"
    }


# Import routes (these don't use ML)
from backend.routes import auth

app.include_router(auth.router)  # Auth router already has /api/auth prefix


# Simple products endpoint (without ML dependencies)
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database_simple import get_db
from typing import List
from pydantic import BaseModel


class ProductResponse(BaseModel):
    id: int
    sku: str
    name: str
    category: str
    description: str | None
    unit_price: float
    stock_quantity: int
    reorder_point: int
    status: str
    
    class Config:
        from_attributes = True


class AlertResponse(BaseModel):
    id: int
    product_id: int
    alert_type: str
    severity: str
    category: str
    message: str
    description: str | None
    confidence_score: float
    priority_score: int
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True


@app.get("/products", response_model=List[ProductResponse])
async def get_products(db: Session = Depends(get_db)):
    """Get all products"""
    products = db.query(Product).all()
    return products


@app.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get product by ID"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.get("/alerts", response_model=List[AlertResponse])
async def get_alerts(
    status: str | None = None,
    severity: str | None = None,
    db: Session = Depends(get_db)
):
    """Get alerts with optional filtering"""
    query = db.query(Alert)
    
    if status:
        query = query.filter(Alert.status == status)
    if severity:
        query = query.filter(Alert.severity == severity)
    
    alerts = query.order_by(Alert.priority_score.desc()).all()
    return alerts


@app.get("/dashboard/summary")
async def dashboard_summary(db: Session = Depends(get_db)):
    """Get dashboard summary statistics"""
    total_alerts = db.query(Alert).count()
    open_alerts = db.query(Alert).filter(Alert.status == "open").count()
    critical_alerts = db.query(Alert).filter(Alert.severity == "critical").count()
    
    # Get recent alerts (last 24 hours)
    yesterday = datetime.utcnow() - timedelta(days=1)
    recent_alerts = db.query(Alert).filter(Alert.created_at >= yesterday).count()
    
    # Alerts by category
    categories = db.query(
        Alert.category,
        db.func.count(Alert.id).label('count')
    ).group_by(Alert.category).all()
    
    alerts_by_category = {cat: count for cat, count in categories}
    
    # Alerts by severity
    severities = db.query(
        Alert.severity,
        db.func.count(Alert.id).label('count')
    ).group_by(Alert.severity).all()
    
    alerts_by_severity = {sev: count for sev, count in severities}
    
    return {
        "total_alerts": total_alerts,
        "open_alerts": open_alerts,
        "critical_alerts": critical_alerts,
        "recent_alerts_24h": recent_alerts,
        "alerts_by_category": alerts_by_category,
        "alerts_by_severity": alerts_by_severity
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
