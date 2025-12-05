from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, ForeignKey, Integer, Text, Float, Boolean, JSON, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Try to import from database_simple first (SQLite), fall back to database (PostgreSQL)
try:
    from .database_simple import Base
except ImportError:
    from .database import Base

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    sku: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(128))
    category: Mapped[str] = mapped_column(String(64))
    status: Mapped[str] = mapped_column(String(32), default="active")
    manufacturer: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    current_stock: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    reorder_point: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    unit_cost: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    metadata_json: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    alerts: Mapped[list["Alert"]] = relationship(back_populates="product", cascade="all, delete-orphan")
    predictions: Mapped[list["Prediction"]] = relationship(back_populates="product", cascade="all, delete-orphan")
    inventory_metrics: Mapped[list["InventoryMetric"]] = relationship(back_populates="product", cascade="all, delete-orphan")
    quality_metrics: Mapped[list["QualityMetric"]] = relationship(back_populates="product", cascade="all, delete-orphan")

class Alert(Base):
    __tablename__ = "alerts"
    __table_args__ = (
        Index('ix_alerts_severity_status', 'severity', 'status'),
        Index('ix_alerts_created_at', 'created_at'),
    )
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    severity: Mapped[str] = mapped_column(String(16))  # critical, high, medium, low
    category: Mapped[str] = mapped_column(String(64))  # quality, supply, demand, expiration, defect
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(32), default="open")  # open, investigating, resolved, false_positive
    score: Mapped[float] = mapped_column(Float, default=0.0)  # 0-1 priority score
    confidence: Mapped[float] = mapped_column(Float, default=0.0)  # ML confidence
    impact_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # Business impact
    likelihood: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # Probability
    source: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)  # sensor, ml_model, manual, integration
    assigned_to: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    resolution_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    metadata_json: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    product: Mapped["Product"] = relationship(back_populates="alerts")
    assigned_user: Mapped[Optional["User"]] = relationship(foreign_keys=[assigned_to])
    workflow_cases: Mapped[list["WorkflowCase"]] = relationship(back_populates="alert", cascade="all, delete-orphan")
    notifications: Mapped[list["NotificationLog"]] = relationship(back_populates="alert", cascade="all, delete-orphan")

class Prediction(Base):
    __tablename__ = "predictions"
    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    model_name: Mapped[str] = mapped_column(String(64))  # arima, prophet, lstm, isolation_forest
    model_version: Mapped[str] = mapped_column(String(32), default="1.0")
    prediction_type: Mapped[str] = mapped_column(String(64))  # forecast, anomaly, classification, risk
    horizon_days: Mapped[int] = mapped_column(Integer, default=7)
    risk_level: Mapped[str] = mapped_column(String(16))  # critical, high, medium, low
    confidence: Mapped[float] = mapped_column(Float)
    predicted_value: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    payload: Mapped[dict] = mapped_column(JSON)  # Full prediction details
    features_used: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    valid_until: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Relationships
    product: Mapped["Product"] = relationship(back_populates="predictions")

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(128))
    role: Mapped[str] = mapped_column(String(32), default="analyst")  # admin, manager, analyst, operator
    department: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    notification_preferences: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # Authentication
    username: Mapped[Optional[str]] = mapped_column(String(64), unique=True, index=True, nullable=True)
    hashed_password: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

class DataSource(Base):
    """Track ingestion sources (ERP, IoT, CRM, social, supplier feeds)"""
    __tablename__ = "data_sources"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128), unique=True)
    source_type: Mapped[str] = mapped_column(String(64))  # iot, erp, crm, social, supplier, manual
    connection_config: Mapped[dict] = mapped_column(JSON)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_sync: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    sync_frequency: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # minutes
    status: Mapped[str] = mapped_column(String(32), default="pending")  # active, error, disabled
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class InventoryMetric(Base):
    """Time-series inventory data for forecasting"""
    __tablename__ = "inventory_metrics"
    __table_args__ = (
        Index('ix_inventory_product_timestamp', 'product_id', 'timestamp'),
    )
    
    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    timestamp: Mapped[datetime] = mapped_column(DateTime, index=True)
    stock_level: Mapped[int] = mapped_column(Integer)
    demand: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    supply: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    turnover_rate: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    days_on_hand: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    source_id: Mapped[Optional[int]] = mapped_column(ForeignKey("data_sources.id"), nullable=True)
    
    product: Mapped["Product"] = relationship(back_populates="inventory_metrics")

class QualityMetric(Base):
    """Quality control and defect tracking"""
    __tablename__ = "quality_metrics"
    __table_args__ = (
        Index('ix_quality_product_timestamp', 'product_id', 'timestamp'),
    )
    
    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    timestamp: Mapped[datetime] = mapped_column(DateTime, index=True)
    defect_rate: Mapped[float] = mapped_column(Float)  # 0-1
    inspection_count: Mapped[int] = mapped_column(Integer)
    failure_count: Mapped[int] = mapped_column(Integer)
    quality_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # 0-100
    defect_category: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    batch_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    source_id: Mapped[Optional[int]] = mapped_column(ForeignKey("data_sources.id"), nullable=True)
    
    product: Mapped["Product"] = relationship(back_populates="quality_metrics")

class SupplierRisk(Base):
    """Supplier performance and risk tracking"""
    __tablename__ = "supplier_risks"
    id: Mapped[int] = mapped_column(primary_key=True)
    supplier_name: Mapped[str] = mapped_column(String(128), index=True)
    risk_level: Mapped[str] = mapped_column(String(16))  # critical, high, medium, low
    risk_score: Mapped[float] = mapped_column(Float)  # 0-1
    lead_time_days: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    on_time_delivery_rate: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    quality_rating: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    financial_health: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    geopolitical_risk: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    last_assessment: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    metadata_json: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

class WorkflowCase(Base):
    """Investigation and case management"""
    __tablename__ = "workflow_cases"
    id: Mapped[int] = mapped_column(primary_key=True)
    alert_id: Mapped[int] = mapped_column(ForeignKey("alerts.id"))
    case_number: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    status: Mapped[str] = mapped_column(String(32), default="open")  # open, investigating, escalated, resolved, closed
    priority: Mapped[str] = mapped_column(String(16))  # p1, p2, p3, p4
    assigned_to: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    escalated_to: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    investigation_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    resolution: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    sla_deadline: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    alert: Mapped["Alert"] = relationship(back_populates="workflow_cases")
    assigned_user: Mapped[Optional["User"]] = relationship(foreign_keys=[assigned_to])
    escalated_user: Mapped[Optional["User"]] = relationship(foreign_keys=[escalated_to])

class NotificationLog(Base):
    """Track all notifications sent"""
    __tablename__ = "notification_logs"
    id: Mapped[int] = mapped_column(primary_key=True)
    alert_id: Mapped[Optional[int]] = mapped_column(ForeignKey("alerts.id"), nullable=True)
    recipient_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    channel: Mapped[str] = mapped_column(String(32))  # email, sms, push, api
    subject: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    message: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(32), default="pending")  # pending, sent, failed, delivered
    sent_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    delivered_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    metadata_json: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    alert: Mapped[Optional["Alert"]] = relationship(back_populates="notifications")
    recipient: Mapped["User"] = relationship()

class ModelPerformance(Base):
    """Track ML model accuracy and performance"""
    __tablename__ = "model_performance"
    id: Mapped[int] = mapped_column(primary_key=True)
    model_name: Mapped[str] = mapped_column(String(64))
    model_version: Mapped[str] = mapped_column(String(32))
    metric_name: Mapped[str] = mapped_column(String(64))  # accuracy, precision, recall, f1, mse, mae
    metric_value: Mapped[float] = mapped_column(Float)
    evaluation_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    sample_size: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    metadata_json: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

class FeedbackLoop(Base):
    """Capture feedback on predictions for continuous learning"""
    __tablename__ = "feedback_loops"
    id: Mapped[int] = mapped_column(primary_key=True)
    prediction_id: Mapped[Optional[int]] = mapped_column(ForeignKey("predictions.id"), nullable=True)
    alert_id: Mapped[Optional[int]] = mapped_column(ForeignKey("alerts.id"), nullable=True)
    feedback_type: Mapped[str] = mapped_column(String(32))  # accuracy, usefulness, false_positive, true_positive
    rating: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # 1-5
    was_accurate: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    actual_outcome: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    comments: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    submitted_by: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    submitter: Mapped["User"] = relationship()

class AuditLog(Base):
    """Security and compliance audit trail"""
    __tablename__ = "audit_logs"
    __table_args__ = (
        Index('ix_audit_user_action', 'user_id', 'action'),
        Index('ix_audit_timestamp', 'timestamp'),
    )
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    action: Mapped[str] = mapped_column(String(64))  # create, update, delete, login, export, view
    resource_type: Mapped[str] = mapped_column(String(64))  # alert, product, user, prediction
    resource_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    changes: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    
    user: Mapped[Optional["User"]] = relationship()
