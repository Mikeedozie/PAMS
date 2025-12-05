"""
Predictions API routes - Forecasting, anomaly detection, and risk assessment
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime, timedelta
import pandas as pd

from ..database_simple import get_db
from .. import models
from ..ml.forecasting import DemandForecaster, StockoutPredictor, DemandSurgeDetector
from ..ml.anomaly_detection import QualityAnomalyDetector, DefectPatternDetector
from ..ml.classification import AlertSeverityClassifier, RiskScoreCalculator

router = APIRouter(prefix="/api/predictions", tags=["predictions"])


# Pydantic schemas
class ForecastRequest(BaseModel):
    product_id: int
    forecast_days: int = 7
    model_type: str = "prophet"  # prophet, arima, lstm


class StockoutRequest(BaseModel):
    product_id: int
    forecast_days: int = 30


class AnomalyDetectionRequest(BaseModel):
    product_id: int
    metric_type: str = "quality"  # quality, inventory
    days: int = 30


class PredictionResponse(BaseModel):
    id: int
    product_id: int
    model_name: str
    prediction_type: str
    risk_level: str
    confidence: float
    payload: dict
    created_at: datetime
    
    class Config:
        from_attributes = True


@router.get("/", response_model=List[PredictionResponse])
def list_predictions(
    skip: int = 0,
    limit: int = 50,
    product_id: Optional[int] = None,
    prediction_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List predictions with filtering"""
    query = db.query(models.Prediction)
    
    if product_id:
        query = query.filter(models.Prediction.product_id == product_id)
    if prediction_type:
        query = query.filter(models.Prediction.prediction_type == prediction_type)
    
    predictions = query.order_by(desc(models.Prediction.created_at))\
        .offset(skip).limit(limit).all()
    
    return predictions


@router.post("/forecast/demand")
def forecast_demand(request: ForecastRequest, db: Session = Depends(get_db)):
    """
    Forecast product demand using time-series models
    
    Returns:
        Forecast for next N days with confidence intervals
    """
    # Get product
    product = db.query(models.Product).filter(models.Product.id == request.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Get historical inventory metrics
    cutoff_date = datetime.utcnow() - timedelta(days=90)
    metrics = db.query(models.InventoryMetric).filter(
        models.InventoryMetric.product_id == request.product_id,
        models.InventoryMetric.timestamp >= cutoff_date
    ).order_by(models.InventoryMetric.timestamp).all()
    
    if len(metrics) < 14:
        raise HTTPException(
            status_code=400,
            detail="Insufficient historical data (need at least 14 days)"
        )
    
    # Prepare DataFrame
    df = pd.DataFrame([
        {
            'timestamp': m.timestamp,
            'demand': m.demand or 0
        }
        for m in metrics
    ])
    
    # Create forecaster
    forecaster = DemandForecaster(model_type=request.model_type)
    prepared_df = forecaster.prepare_data(df, target_col='demand')
    
    # Train
    if request.model_type == "prophet":
        train_result = forecaster.train_prophet(prepared_df)
    elif request.model_type == "arima":
        train_result = forecaster.train_arima(prepared_df)
    else:
        raise HTTPException(status_code=400, detail="Invalid model_type")
    
    if train_result['status'] != 'success':
        raise HTTPException(status_code=500, detail=train_result.get('message'))
    
    # Predict
    forecast = forecaster.predict(periods=request.forecast_days)
    
    if forecast['status'] != 'success':
        raise HTTPException(status_code=500, detail=forecast.get('message'))
    
    # Save prediction to database
    db_prediction = models.Prediction(
        product_id=request.product_id,
        model_name=request.model_type,
        model_version="1.0",
        prediction_type="demand_forecast",
        horizon_days=request.forecast_days,
        risk_level="low",
        confidence=0.75,
        payload={
            "forecast": forecast['predictions'],
            "model_info": train_result
        },
        valid_until=datetime.utcnow() + timedelta(days=request.forecast_days)
    )
    
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)
    
    return {
        "prediction_id": db_prediction.id,
        "product_sku": product.sku,
        "product_name": product.name,
        "model_type": request.model_type,
        "forecast_days": request.forecast_days,
        "forecast": forecast['predictions'],
        "training_info": train_result
    }


@router.post("/stockout/predict")
def predict_stockout(request: StockoutRequest, db: Session = Depends(get_db)):
    """
    Predict stockout risk and timing
    
    Returns:
        Days until stockout, risk level, and confidence
    """
    # Get product
    product = db.query(models.Product).filter(models.Product.id == request.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if not product.current_stock or not product.reorder_point:
        raise HTTPException(
            status_code=400,
            detail="Product missing current_stock or reorder_point"
        )
    
    # Get historical demand data
    cutoff_date = datetime.utcnow() - timedelta(days=90)
    metrics = db.query(models.InventoryMetric).filter(
        models.InventoryMetric.product_id == request.product_id,
        models.InventoryMetric.timestamp >= cutoff_date
    ).order_by(models.InventoryMetric.timestamp).all()
    
    if len(metrics) < 14:
        raise HTTPException(
            status_code=400,
            detail="Insufficient historical data"
        )
    
    # Prepare DataFrame
    df = pd.DataFrame([
        {
            'timestamp': m.timestamp,
            'demand': m.demand or 0
        }
        for m in metrics
    ])
    
    # Predict stockout
    predictor = StockoutPredictor()
    result = predictor.predict_stockout_risk(
        historical_data=df,
        current_stock=product.current_stock,
        reorder_point=product.reorder_point,
        forecast_days=request.forecast_days
    )
    
    if result['status'] != 'success':
        raise HTTPException(status_code=500, detail=result.get('message'))
    
    # Save prediction
    db_prediction = models.Prediction(
        product_id=request.product_id,
        model_name="prophet_stockout",
        model_version="1.0",
        prediction_type="stockout_risk",
        horizon_days=request.forecast_days,
        risk_level=result['risk_level'],
        confidence=result['confidence'],
        payload=result,
        valid_until=datetime.utcnow() + timedelta(days=request.forecast_days)
    )
    
    db.add(db_prediction)
    db.commit()
    
    # Create alert if high risk
    if result['risk_level'] in ['critical', 'high']:
        alert = models.Alert(
            product_id=request.product_id,
            severity=result['risk_level'],
            category="supply",
            description=f"Stockout predicted in {result['days_until_stockout']} days. "
                       f"Current stock: {product.current_stock}, Reorder point: {product.reorder_point}",
            confidence=result['confidence'],
            impact_score=0.8,
            likelihood=result['confidence'],
            source="ml_model",
            score=0.75 if result['risk_level'] == 'critical' else 0.6
        )
        db.add(alert)
        db.commit()
    
    return result


@router.post("/anomaly/detect")
def detect_anomalies(request: AnomalyDetectionRequest, db: Session = Depends(get_db)):
    """
    Detect anomalies in quality or inventory metrics
    
    Returns:
        Detected anomalies with severity and scores
    """
    product = db.query(models.Product).filter(models.Product.id == request.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    cutoff_date = datetime.utcnow() - timedelta(days=request.days)
    
    if request.metric_type == "quality":
        # Get quality metrics
        metrics = db.query(models.QualityMetric).filter(
            models.QualityMetric.product_id == request.product_id,
            models.QualityMetric.timestamp >= cutoff_date
        ).order_by(models.QualityMetric.timestamp).all()
        
        if len(metrics) < 10:
            raise HTTPException(status_code=400, detail="Insufficient data")
        
        # Prepare DataFrame
        df = pd.DataFrame([
            {
                'timestamp': m.timestamp,
                'defect_rate': m.defect_rate,
                'quality_score': m.quality_score or 0,
                'failure_count': m.failure_count
            }
            for m in metrics
        ])
        
        # Train and detect
        detector = QualityAnomalyDetector(contamination=0.1)
        feature_cols = ['defect_rate', 'quality_score', 'failure_count']
        
        # Use first 80% for training
        train_size = int(len(df) * 0.8)
        train_df = df.head(train_size)
        test_df = df.tail(len(df) - train_size)
        
        train_result = detector.train(train_df, feature_cols)
        if train_result['status'] != 'success':
            raise HTTPException(status_code=500, detail="Training failed")
        
        # Detect anomalies in recent data
        detection_result = detector.predict(test_df)
        
    else:
        raise HTTPException(status_code=400, detail="Invalid metric_type")
    
    # Create alerts for detected anomalies
    if detection_result['anomalies_detected'] > 0:
        for anomaly in detection_result['anomalies'][:5]:  # Limit to top 5
            alert = models.Alert(
                product_id=request.product_id,
                severity=anomaly['severity'],
                category="quality",
                description=f"Quality anomaly detected: defect_rate={anomaly['features'].get('defect_rate', 0):.3f}, "
                           f"anomaly_score={anomaly['anomaly_score']:.3f}",
                confidence=anomaly['anomaly_score'],
                impact_score=0.7,
                likelihood=anomaly['anomaly_score'],
                source="ml_model",
                score=anomaly['anomaly_score']
            )
            db.add(alert)
        
        db.commit()
    
    return detection_result


@router.post("/demand/surge")
def detect_demand_surge(product_id: int, db: Session = Depends(get_db)):
    """Detect demand surge/spike"""
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Get recent demand data
    cutoff = datetime.utcnow() - timedelta(days=60)
    metrics = db.query(models.InventoryMetric).filter(
        models.InventoryMetric.product_id == product_id,
        models.InventoryMetric.timestamp >= cutoff
    ).order_by(models.InventoryMetric.timestamp).all()
    
    if len(metrics) < 30:
        raise HTTPException(status_code=400, detail="Insufficient data")
    
    df = pd.DataFrame([
        {'timestamp': m.timestamp, 'demand': m.demand or 0}
        for m in metrics
    ])
    
    # Detect surge
    result = DemandSurgeDetector.detect_surge(df, threshold_std=2.0)
    
    # Create alert if surge detected
    if result.get('surge_detected'):
        alert = models.Alert(
            product_id=product_id,
            severity=result['severity'],
            category="demand",
            description=f"Demand surge detected! Recent avg: {result['recent_avg']:.1f}, "
                       f"Baseline avg: {result['avg_demand']:.1f}, Z-score: {result['zscore']:.2f}",
            confidence=min(0.9, abs(result['zscore']) / 3.0),
            impact_score=0.7,
            likelihood=0.8,
            source="ml_model",
            score=0.7
        )
        db.add(alert)
        db.commit()
    
    return result


@router.get("/analytics/performance")
def get_prediction_performance(db: Session = Depends(get_db)):
    """Get ML model performance metrics"""
    # Get model performance records
    performance = db.query(models.ModelPerformance)\
        .order_by(desc(models.ModelPerformance.evaluation_date))\
        .limit(50)\
        .all()
    
    # Group by model
    models_dict = {}
    for perf in performance:
        if perf.model_name not in models_dict:
            models_dict[perf.model_name] = []
        
        models_dict[perf.model_name].append({
            "metric_name": perf.metric_name,
            "metric_value": perf.metric_value,
            "evaluation_date": perf.evaluation_date,
            "version": perf.model_version
        })
    
    return {
        "models": models_dict,
        "total_evaluations": len(performance)
    }


@router.get("/dashboard/risk_overview")
def get_risk_overview(db: Session = Depends(get_db)):
    """Get overall risk dashboard"""
    # Recent predictions by risk level
    cutoff = datetime.utcnow() - timedelta(days=7)
    
    predictions = db.query(
        models.Prediction.risk_level,
        db.func.count(models.Prediction.id)
    ).filter(
        models.Prediction.created_at >= cutoff
    ).group_by(models.Prediction.risk_level).all()
    
    # Products at risk
    high_risk_predictions = db.query(models.Prediction)\
        .filter(
            models.Prediction.risk_level.in_(['critical', 'high']),
            models.Prediction.created_at >= cutoff
        ).order_by(desc(models.Prediction.confidence)).limit(10).all()
    
    return {
        "risk_distribution": dict(predictions),
        "high_risk_products": [
            {
                "product_id": p.product_id,
                "prediction_type": p.prediction_type,
                "risk_level": p.risk_level,
                "confidence": p.confidence
            }
            for p in high_risk_predictions
        ],
        "period": "last_7_days"
    }
