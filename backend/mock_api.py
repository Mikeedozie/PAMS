"""
Simple mock API for screenshot purposes - no dependencies required
"""
from fastapi import FastAPI, Form, Header
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
import random
from typing import Optional

app = FastAPI(
    title="PAMS Mock API",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sample data
SAMPLE_ALERTS = [
    {
        "id": 1,
        "product_id": 1,
        "severity": "critical",
        "category": "quality",
        "description": "Battery failure rate increasing 15% week-over-week",
        "status": "open",
        "score": 0.89,
        "confidence": 0.89,
        "created_at": (datetime.now() - timedelta(hours=2)).isoformat()
    },
    {
        "id": 2,
        "product_id": 1,
        "severity": "high",
        "category": "supply",
        "description": "Supplier lead time extended by 3 weeks",
        "status": "open",
        "score": 0.72,
        "confidence": 0.72,
        "created_at": (datetime.now() - timedelta(hours=5)).isoformat()
    },
    {
        "id": 3,
        "product_id": 2,
        "severity": "medium",
        "category": "demand",
        "description": "Demand spike detected in Q4 forecast",
        "status": "in_progress",
        "score": 0.54,
        "confidence": 0.54,
        "created_at": (datetime.now() - timedelta(hours=12)).isoformat()
    },
    {
        "id": 4,
        "product_id": 3,
        "severity": "low",
        "category": "quality",
        "description": "Minor quality variations within acceptable range",
        "status": "resolved",
        "score": 0.35,
        "confidence": 0.35,
        "created_at": (datetime.now() - timedelta(days=1)).isoformat()
    },
]

SAMPLE_PRODUCTS = [
    {"id": 1, "sku": "ELEC-001", "name": "Smart Watch Pro", "category": "electronics"},
    {"id": 2, "sku": "MED-001", "name": "Blood Pressure Monitor", "category": "medical"},
    {"id": 3, "sku": "IND-001", "name": "Industrial Sensor", "category": "industrial"},
]

@app.get("/")
def root():
    return {"message": "PAMS Mock API for Screenshots", "status": "running"}

@app.get("/health")
def health():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}

@app.get("/api/alerts/dashboard/summary")
def get_summary():
    return {
        "total_alerts": len(SAMPLE_ALERTS),
        "open_alerts": len([a for a in SAMPLE_ALERTS if a["status"] == "open"]),
        "critical_alerts": len([a for a in SAMPLE_ALERTS if a["severity"] == "critical"]),
        "recent_24h": 3,
        "by_category": {
            "quality": 2,
            "supply": 1,
            "demand": 1
        }
    }

@app.get("/api/alerts/")
def list_alerts():
    return SAMPLE_ALERTS

@app.post("/api/alerts/")
def create_alert(alert_data: dict):
    """Create a new alert"""
    new_alert = {
        "id": len(SAMPLE_ALERTS) + 1,
        "product_id": alert_data.get("product_id", 1),
        "severity": alert_data.get("severity", "medium"),
        "category": alert_data.get("category", "quality"),
        "description": alert_data.get("description", "New alert"),
        "status": "open",
        "score": alert_data.get("score", 0.5),
        "confidence": alert_data.get("confidence", 0.5),
        "created_at": datetime.now().isoformat()
    }
    SAMPLE_ALERTS.append(new_alert)
    return new_alert

@app.put("/api/alerts/{alert_id}")
def update_alert(alert_id: int, alert_data: dict):
    """Update an existing alert"""
    for alert in SAMPLE_ALERTS:
        if alert["id"] == alert_id:
            alert.update({
                "severity": alert_data.get("severity", alert["severity"]),
                "category": alert_data.get("category", alert["category"]),
                "description": alert_data.get("description", alert["description"]),
                "status": alert_data.get("status", alert["status"]),
            })
            return alert
    return {"error": "Alert not found"}, 404

@app.delete("/api/alerts/{alert_id}")
def delete_alert(alert_id: int):
    """Delete an alert"""
    global SAMPLE_ALERTS
    SAMPLE_ALERTS = [a for a in SAMPLE_ALERTS if a["id"] != alert_id]
    return {"message": "Alert deleted", "id": alert_id}

@app.get("/api/products/")
def list_products():
    return SAMPLE_PRODUCTS

@app.post("/api/products/")
def create_product(product_data: dict):
    """Create a new product"""
    new_product = {
        "id": len(SAMPLE_PRODUCTS) + 1,
        "sku": product_data.get("sku", f"SKU-{random.randint(1000, 9999)}"),
        "name": product_data.get("name", "New Product"),
        "category": product_data.get("category", "general"),
        "description": product_data.get("description", ""),
        "price": product_data.get("price", 0.0),
        "stock_level": product_data.get("stock_level", 0),
        "reorder_point": product_data.get("reorder_point", 10),
        "supplier": product_data.get("supplier", "Unknown"),
        "created_at": datetime.now().isoformat()
    }
    SAMPLE_PRODUCTS.append(new_product)
    return new_product

@app.get("/api/products/{product_id}")
def get_product(product_id: int):
    """Get a specific product by ID"""
    for product in SAMPLE_PRODUCTS:
        if product["id"] == product_id:
            return product
    return {"error": "Product not found"}, 404

@app.put("/api/products/{product_id}")
def update_product(product_id: int, product_data: dict):
    """Update an existing product"""
    for product in SAMPLE_PRODUCTS:
        if product["id"] == product_id:
            product.update({
                "name": product_data.get("name", product["name"]),
                "sku": product_data.get("sku", product["sku"]),
                "category": product_data.get("category", product["category"]),
                "description": product_data.get("description", product.get("description", "")),
                "price": product_data.get("price", product.get("price", 0.0)),
                "stock_level": product_data.get("stock_level", product.get("stock_level", 0)),
            })
            return product
    return {"error": "Product not found"}, 404

@app.delete("/api/products/{product_id}")
def delete_product(product_id: int):
    """Delete a product"""
    global SAMPLE_PRODUCTS
    SAMPLE_PRODUCTS = [p for p in SAMPLE_PRODUCTS if p["id"] != product_id]
    return {"message": "Product deleted", "id": product_id}

@app.post("/api/auth/login")
def login(
    username: str = Form(...),
    password: str = Form(...),
    grant_type: Optional[str] = Form(None)
):
    """
    Accept form-encoded login data (username, password, grant_type)
    Always returns success for demo purposes
    """
    return {
        "access_token": "mock_token_" + str(random.randint(1000, 9999)),
        "token_type": "bearer",
        "user": {
            "id": 1,
            "username": username,
            "email": f"{username}@pams.com",
            "role": "admin",
            "full_name": username.capitalize() + " User"
        }
    }

@app.get("/api/auth/me")
def get_current_user(authorization: Optional[str] = Header(None)):
    """
    Returns the current user based on the token
    For demo purposes, always returns admin user
    """
    return {
        "id": 1,
        "username": "admin",
        "email": "admin@pams.com",
        "role": "admin",
        "full_name": "Admin User"
    }

@app.post("/api/auth/register")
def register(user_data: dict):
    return {
        "id": random.randint(100, 999),
        "username": user_data.get("username"),
        "email": user_data.get("email"),
        "message": "User registered successfully"
    }

if __name__ == "__main__":
    import uvicorn
    print("="*60)
    print("🚀 Starting PAMS Mock API for Screenshots")
    print("="*60)
    print("\n📊 API: http://localhost:8000")
    print("📚 Docs: http://localhost:8000/docs")
    print("="*60)
    uvicorn.run(app, host="0.0.0.0", port=8000)
