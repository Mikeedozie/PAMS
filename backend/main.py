import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routes import products, alerts, predictions

def init_db():
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    # Seed sample data
    from sqlalchemy.orm import Session
    from . import models
    db = Session(bind=engine)
    
    if db.query(models.Product).count() == 0:
        sample_products = [
            models.Product(sku="WIDG-001", name="Widget Pro 500", category="electronics"),
            models.Product(sku="PART-042", name="Supply Component X", category="industrial"),
            models.Product(sku="MED-789", name="Health Monitor", category="medical"),
        ]
        db.add_all(sample_products)
        db.commit()
        
        sample_alerts = [
            models.Alert(product_id=1, severity="critical", category="quality", 
                        description="Battery failure rate increasing 15% week-over-week", score=0.89),
            models.Alert(product_id=1, severity="high", category="supply",
                        description="Supplier lead time extended by 3 weeks", score=0.72),
            models.Alert(product_id=2, severity="medium", category="demand",
                        description="Demand spike detected in Q4 forecast", score=0.54),
        ]
        db.add_all(sample_alerts)
        db.commit()
    db.close()

app = FastAPI(title=os.getenv("API_TITLE", "PAMS API"), version=os.getenv("API_VERSION", "0.1.0"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

app.include_router(products.router)
app.include_router(alerts.router)
app.include_router(predictions.router)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.on_event("startup")
def startup():
    init_db()
