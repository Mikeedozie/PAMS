"""
Alerts API routes with intelligent scoring and prioritization
"""
from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime, timedelta

from ..database_simple import get_db
from .. import models
from ..ml.decision_engine import DecisionEngine

router = APIRouter(prefix="/api/alerts", tags=["alerts"])

# Initialize decision engine
decision_engine = DecisionEngine()


# Pydantic schemas
class AlertCreate(BaseModel):
    product_id: int
    severity: str  # critical, high, medium, low
    category: str  # quality, supply, demand, expiration, defect, supplier
    description: str
    confidence: Optional[float] = 0.5
    impact_score: Optional[float] = 0.5
    likelihood: Optional[float] = 0.5
    source: Optional[str] = "manual"
    metadata_json: Optional[dict] = None


class AlertUpdate(BaseModel):
    severity: Optional[str] = None
    status: Optional[str] = None
    assigned_to: Optional[int] = None
    resolution_notes: Optional[str] = None
    metadata_json: Optional[dict] = None


class AlertResponse(BaseModel):
    id: int
    product_id: int
    severity: str
    category: str
    description: str
    status: str
    score: float
    confidence: float
    impact_score: Optional[float]
    likelihood: Optional[float]
    source: Optional[str]
    assigned_to: Optional[int]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


@router.get("/", response_model=List[AlertResponse])
def list_alerts(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    severity: Optional[str] = None,
    category: Optional[str] = None,
    product_id: Optional[int] = None,
    assigned_to: Optional[int] = None,
    sort_by: str = "score",  # score, created_at, severity
    db: Session = Depends(get_db)
):
    """List alerts with filtering and sorting"""
    query = db.query(models.Alert)
    
    # Apply filters
    if status:
        query = query.filter(models.Alert.status == status)
    if severity:
        query = query.filter(models.Alert.severity == severity)
    if category:
        query = query.filter(models.Alert.category == category)
    if product_id:
        query = query.filter(models.Alert.product_id == product_id)
    if assigned_to:
        query = query.filter(models.Alert.assigned_to == assigned_to)
    
    # Sort
    if sort_by == "score":
        query = query.order_by(desc(models.Alert.score))
    elif sort_by == "created_at":
        query = query.order_by(desc(models.Alert.created_at))
    elif sort_by == "severity":
        # Custom severity ordering
        severity_order = {
            'critical': 4,
            'high': 3,
            'medium': 2,
            'low': 1
        }
        query = query.order_by(desc(models.Alert.severity))
    
    alerts = query.offset(skip).limit(limit).all()
    return alerts


@router.get("/{alert_id}", response_model=AlertResponse)
def get_alert(alert_id: int, db: Session = Depends(get_db)):
    """Get a specific alert"""
    alert = db.query(models.Alert).filter(models.Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert


@router.post("/", response_model=AlertResponse, status_code=201)
def create_alert(
    alert: AlertCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Create a new alert with intelligent scoring"""
    # Verify product exists
    product = db.query(models.Product).filter(models.Product.id == alert.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Create alert dict for processing
    alert_dict = alert.model_dump()
    alert_dict['created_at'] = datetime.utcnow()
    
    # Get product dict
    product_dict = {
        'id': product.id,
        'sku': product.sku,
        'name': product.name,
        'category': product.category,
        'current_stock': product.current_stock,
        'reorder_point': product.reorder_point
    }
    
    # Get historical alerts for context
    history = db.query(models.Alert)\
        .filter(models.Alert.product_id == alert.product_id)\
        .order_by(desc(models.Alert.created_at))\
        .limit(10)\
        .all()
    
    history_dicts = [
        {
            'category': h.category,
            'severity': h.severity,
            'status': h.status,
            'created_at': h.created_at,
            'resolved_at': h.resolved_at
        }
        for h in history
    ]
    
    # Process alert through decision engine
    processed = decision_engine.process_alert(
        alert_dict,
        product=product_dict,
        history=history_dicts
    )
    
    # Create database alert
    db_alert = models.Alert(
        product_id=alert.product_id,
        severity=alert.severity,
        category=alert.category,
        description=alert.description,
        confidence=alert.confidence or 0.5,
        impact_score=alert.impact_score or 0.5,
        likelihood=alert.likelihood or 0.5,
        source=alert.source or "manual",
        metadata_json=alert.metadata_json,
        score=processed.get('composite_score', 0.5)
    )
    
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    
    # TODO: Send notifications in background
    # background_tasks.add_task(send_alert_notifications, db_alert.id)
    
    return db_alert


@router.put("/{alert_id}", response_model=AlertResponse)
def update_alert(
    alert_id: int,
    alert_update: AlertUpdate,
    db: Session = Depends(get_db)
):
    """Update an alert"""
    db_alert = db.query(models.Alert).filter(models.Alert.id == alert_id).first()
    if not db_alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    # Update fields
    update_data = alert_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_alert, field, value)
    
    # If resolving, set resolved_at
    if update_data.get('status') == 'resolved':
        db_alert.resolved_at = datetime.utcnow()
    
    db_alert.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_alert)
    
    return db_alert


@router.post("/{alert_id}/assign")
def assign_alert(alert_id: int, user_id: int, db: Session = Depends(get_db)):
    """Assign alert to a user"""
    db_alert = db.query(models.Alert).filter(models.Alert.id == alert_id).first()
    if not db_alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    # Verify user exists
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_alert.assigned_to = user_id
    db_alert.status = "investigating"
    db_alert.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(db_alert)
    
    return {"message": "Alert assigned successfully", "assigned_to": user.name}


@router.post("/{alert_id}/resolve")
def resolve_alert(
    alert_id: int,
    resolution_notes: str,
    db: Session = Depends(get_db)
):
    """Resolve an alert"""
    db_alert = db.query(models.Alert).filter(models.Alert.id == alert_id).first()
    if not db_alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    db_alert.status = "resolved"
    db_alert.resolution_notes = resolution_notes
    db_alert.resolved_at = datetime.utcnow()
    db_alert.updated_at = datetime.utcnow()
    
    db.commit()
    
    return {"message": "Alert resolved successfully"}


@router.post("/{alert_id}/escalate")
def escalate_alert(alert_id: int, db: Session = Depends(get_db)):
    """Escalate an alert"""
    db_alert = db.query(models.Alert).filter(models.Alert.id == alert_id).first()
    if not db_alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    # Increase severity if possible
    severity_escalation = {
        'low': 'medium',
        'medium': 'high',
        'high': 'critical',
        'critical': 'critical'
    }
    
    db_alert.severity = severity_escalation.get(db_alert.severity, 'high')
    db_alert.updated_at = datetime.utcnow()
    
    # TODO: Create workflow case for escalation
    # TODO: Send escalation notifications
    
    db.commit()
    
    return {"message": "Alert escalated", "new_severity": db_alert.severity}


@router.get("/dashboard/summary")
def get_alerts_summary(db: Session = Depends(get_db)):
    """Get alert dashboard summary"""
    total_alerts = db.query(models.Alert).count()
    open_alerts = db.query(models.Alert).filter(models.Alert.status == "open").count()
    critical_alerts = db.query(models.Alert).filter(
        and_(models.Alert.severity == "critical", models.Alert.status != "resolved")
    ).count()
    
    # Alerts by category
    categories = db.query(
        models.Alert.category,
        db.func.count(models.Alert.id)
    ).filter(
        models.Alert.status != "resolved"
    ).group_by(models.Alert.category).all()
    
    # Recent alerts (last 24h)
    cutoff = datetime.utcnow() - timedelta(hours=24)
    recent_count = db.query(models.Alert).filter(
        models.Alert.created_at >= cutoff
    ).count()
    
    return {
        "total_alerts": total_alerts,
        "open_alerts": open_alerts,
        "critical_alerts": critical_alerts,
        "recent_24h": recent_count,
        "by_category": dict(categories),
        "timestamp": datetime.utcnow()
    }


@router.get("/analytics/trends")
def get_alert_trends(days: int = 30, db: Session = Depends(get_db)):
    """Get alert trends over time"""
    cutoff = datetime.utcnow() - timedelta(days=days)
    
    # Daily alert counts
    daily_counts = db.query(
        db.func.date(models.Alert.created_at).label('date'),
        db.func.count(models.Alert.id).label('count')
    ).filter(
        models.Alert.created_at >= cutoff
    ).group_by(
        db.func.date(models.Alert.created_at)
    ).all()
    
    return {
        "period_days": days,
        "daily_counts": [
            {"date": str(date), "count": count}
            for date, count in daily_counts
        ]
    }
