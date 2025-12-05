"""
Classification models for alert categorization, severity prediction, and risk assessment
Uses Random Forest, Gradient Boosting, and Neural Networks
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import logging

from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# Optional ML libraries - gracefully handle if not installed
try:
    import xgboost as xgb
    HAS_XGBOOST = True
except ImportError:
    HAS_XGBOOST = False
    
try:
    import lightgbm as lgb
    HAS_LIGHTGBM = True
except ImportError:
    HAS_LIGHTGBM = False

logger = logging.getLogger(__name__)


class AlertSeverityClassifier:
    """Predict alert severity based on features"""
    
    def __init__(self, model_type: str = "random_forest"):
        """
        Args:
            model_type: 'random_forest', 'xgboost', 'lightgbm', or 'gradient_boosting'
        """
        self.model_type = model_type
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.feature_names = []
        
    def _initialize_model(self):
        """Initialize the chosen model"""
        if self.model_type == "random_forest":
            self.model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                class_weight='balanced'
            )
        elif self.model_type == "xgboost" and HAS_XGBOOST:
            self.model = xgb.XGBClassifier(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=42
            )
        elif self.model_type == "lightgbm" and HAS_LIGHTGBM:
            self.model = lgb.LGBMClassifier(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=42
            )
        elif self.model_type == "gradient_boosting":
            self.model = GradientBoostingClassifier(
                n_estimators=100,
                max_depth=5,
                learning_rate=0.1,
                random_state=42
            )
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")
    
    def train(
        self,
        df: pd.DataFrame,
        feature_cols: List[str],
        target_col: str = 'severity',
        test_size: float = 0.2
    ) -> Dict:
        """
        Train severity classifier
        
        Args:
            df: Training data
            feature_cols: List of feature columns
            target_col: Target column name
            test_size: Test split ratio
        """
        try:
            self.feature_names = feature_cols
            
            # Prepare data
            X = df[feature_cols].values
            X = np.nan_to_num(X, nan=0.0)
            
            y = self.label_encoder.fit_transform(df[target_col])
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=42, stratify=y
            )
            
            # Scale features
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Initialize and train model
            self._initialize_model()
            self.model.fit(X_train_scaled, y_train)
            
            # Evaluate
            y_pred = self.model.predict(X_test_scaled)
            accuracy = accuracy_score(y_test, y_pred)
            
            # Cross-validation
            cv_scores = cross_val_score(self.model, X_train_scaled, y_train, cv=5)
            
            # Feature importance
            if hasattr(self.model, 'feature_importances_'):
                feature_importance = dict(zip(
                    feature_cols,
                    self.model.feature_importances_.tolist()
                ))
            else:
                feature_importance = {}
            
            return {
                "status": "success",
                "model_type": self.model_type,
                "accuracy": float(accuracy),
                "cv_mean": float(cv_scores.mean()),
                "cv_std": float(cv_scores.std()),
                "classes": self.label_encoder.classes_.tolist(),
                "feature_importance": feature_importance,
                "samples_trained": len(X_train)
            }
            
        except Exception as e:
            logger.error(f"Training failed: {e}")
            return {"status": "error", "message": str(e)}
    
    def predict(self, df: pd.DataFrame) -> Dict:
        """
        Predict severity for new alerts
        
        Returns:
            Dict with predictions and probabilities
        """
        try:
            X = df[self.feature_names].values
            X = np.nan_to_num(X, nan=0.0)
            X_scaled = self.scaler.transform(X)
            
            # Predict
            predictions = self.model.predict(X_scaled)
            probabilities = self.model.predict_proba(X_scaled)
            
            # Decode labels
            predicted_labels = self.label_encoder.inverse_transform(predictions)
            
            results = []
            for idx, (label, probs) in enumerate(zip(predicted_labels, probabilities)):
                class_probs = {
                    cls: float(prob)
                    for cls, prob in zip(self.label_encoder.classes_, probs)
                }
                
                results.append({
                    "index": idx,
                    "predicted_severity": label,
                    "confidence": float(max(probs)),
                    "probabilities": class_probs
                })
            
            return {
                "status": "success",
                "predictions": results
            }
            
        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            return {"status": "error", "message": str(e)}


class AlertCategoryClassifier:
    """Classify alerts into categories (quality, supply, demand, defect, etc.)"""
    
    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=150,
            max_depth=12,
            random_state=42,
            class_weight='balanced'
        )
        self.label_encoder = LabelEncoder()
        self.scaler = StandardScaler()
        
    def train(
        self,
        df: pd.DataFrame,
        feature_cols: List[str],
        target_col: str = 'category'
    ) -> Dict:
        """Train category classifier"""
        try:
            X = df[feature_cols].values
            X = np.nan_to_num(X, nan=0.0)
            y = self.label_encoder.fit_transform(df[target_col])
            
            X_scaled = self.scaler.fit_transform(X)
            self.model.fit(X_scaled, y)
            
            # Calculate accuracy
            accuracy = self.model.score(X_scaled, y)
            
            return {
                "status": "success",
                "accuracy": float(accuracy),
                "categories": self.label_encoder.classes_.tolist(),
                "samples": len(df)
            }
            
        except Exception as e:
            logger.error(f"Category classifier training failed: {e}")
            return {"status": "error", "message": str(e)}
    
    def predict(self, df: pd.DataFrame, feature_cols: List[str]) -> Dict:
        """Predict category for new data"""
        try:
            X = df[feature_cols].values
            X = np.nan_to_num(X, nan=0.0)
            X_scaled = self.scaler.transform(X)
            
            predictions = self.model.predict(X_scaled)
            probabilities = self.model.predict_proba(X_scaled)
            
            predicted_labels = self.label_encoder.inverse_transform(predictions)
            
            results = []
            for idx, (label, probs) in enumerate(zip(predicted_labels, probabilities)):
                results.append({
                    "index": idx,
                    "predicted_category": label,
                    "confidence": float(max(probs))
                })
            
            return {
                "status": "success",
                "predictions": results
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}


class RiskScoreCalculator:
    """Calculate comprehensive risk scores combining multiple factors"""
    
    @staticmethod
    def calculate_composite_risk(
        severity: str,
        likelihood: float,
        impact: float,
        confidence: float,
        time_sensitivity: float = 1.0
    ) -> Dict:
        """
        Calculate composite risk score
        
        Args:
            severity: 'critical', 'high', 'medium', 'low'
            likelihood: Probability of occurrence (0-1)
            impact: Business impact score (0-1)
            confidence: ML model confidence (0-1)
            time_sensitivity: Time decay factor (0-1, default 1.0)
        
        Returns:
            Dict with composite_score, priority_level, and components
        """
        # Severity weights
        severity_weights = {
            'critical': 1.0,
            'high': 0.75,
            'medium': 0.5,
            'low': 0.25
        }
        
        severity_score = severity_weights.get(severity.lower(), 0.5)
        
        # Composite score formula
        # Score = (Severity * 0.3) + (Likelihood * 0.25) + (Impact * 0.25) + (Confidence * 0.2)
        composite_score = (
            severity_score * 0.3 +
            likelihood * 0.25 +
            impact * 0.25 +
            confidence * 0.2
        ) * time_sensitivity
        
        # Determine priority
        if composite_score >= 0.8:
            priority = "p1"
            priority_label = "Critical - Immediate Action"
        elif composite_score >= 0.6:
            priority = "p2"
            priority_label = "High - Action Required"
        elif composite_score >= 0.4:
            priority = "p3"
            priority_label = "Medium - Monitor Closely"
        else:
            priority = "p4"
            priority_label = "Low - Routine Review"
        
        return {
            "composite_score": round(composite_score, 3),
            "priority": priority,
            "priority_label": priority_label,
            "components": {
                "severity": severity_score,
                "likelihood": likelihood,
                "impact": impact,
                "confidence": confidence,
                "time_sensitivity": time_sensitivity
            }
        }
    
    @staticmethod
    def calculate_supplier_risk(
        on_time_rate: float,
        quality_rating: float,
        lead_time_days: int,
        financial_health: str = "good",
        geopolitical_risk: float = 0.0
    ) -> Dict:
        """
        Calculate supplier risk score
        
        Returns:
            Dict with risk_score, risk_level, and breakdown
        """
        # Financial health scores
        financial_scores = {
            'excellent': 0.0,
            'good': 0.1,
            'fair': 0.3,
            'poor': 0.6,
            'critical': 0.9
        }
        
        financial_score = financial_scores.get(financial_health.lower(), 0.5)
        
        # On-time delivery risk (inverse)
        delivery_risk = 1.0 - on_time_rate
        
        # Quality risk (inverse)
        quality_risk = 1.0 - quality_rating
        
        # Lead time risk (normalize, assume 30 days is high risk)
        lead_time_risk = min(lead_time_days / 30.0, 1.0)
        
        # Composite supplier risk
        risk_score = (
            delivery_risk * 0.25 +
            quality_risk * 0.25 +
            lead_time_risk * 0.15 +
            financial_score * 0.20 +
            geopolitical_risk * 0.15
        )
        
        # Classify risk level
        if risk_score >= 0.7:
            risk_level = "critical"
        elif risk_score >= 0.5:
            risk_level = "high"
        elif risk_score >= 0.3:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        return {
            "risk_score": round(risk_score, 3),
            "risk_level": risk_level,
            "breakdown": {
                "delivery_risk": round(delivery_risk, 3),
                "quality_risk": round(quality_risk, 3),
                "lead_time_risk": round(lead_time_risk, 3),
                "financial_risk": financial_score,
                "geopolitical_risk": geopolitical_risk
            }
        }
