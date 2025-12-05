"""
Anomaly detection for quality metrics, defects, and unusual patterns
Uses Isolation Forest, Autoencoders, and statistical methods
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime
import logging

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# Optional TensorFlow for Autoencoder
try:
    from tensorflow.keras.models import Model, Sequential
    from tensorflow.keras.layers import Input, Dense
    from tensorflow.keras.callbacks import EarlyStopping
    HAS_TENSORFLOW = True
except ImportError:
    HAS_TENSORFLOW = False

logger = logging.getLogger(__name__)


class QualityAnomalyDetector:
    """Detect quality anomalies using Isolation Forest"""
    
    def __init__(self, contamination: float = 0.1):
        """
        Args:
            contamination: Expected proportion of outliers (0.01 - 0.5)
        """
        self.model = IsolationForest(
            contamination=contamination,
            random_state=42,
            n_estimators=100
        )
        self.scaler = StandardScaler()
        self.feature_names = []
        
    def train(self, df: pd.DataFrame, feature_cols: List[str]) -> Dict:
        """
        Train anomaly detector on quality metrics
        
        Args:
            df: DataFrame with quality metrics
            feature_cols: List of feature column names
        """
        try:
            self.feature_names = feature_cols
            X = df[feature_cols].values
            
            # Handle missing values
            X = np.nan_to_num(X, nan=0.0)
            
            # Scale features
            X_scaled = self.scaler.fit_transform(X)
            
            # Train model
            self.model.fit(X_scaled)
            
            return {
                "status": "success",
                "samples_trained": len(df),
                "features": feature_cols
            }
            
        except Exception as e:
            logger.error(f"Training failed: {e}")
            return {"status": "error", "message": str(e)}
    
    def predict(self, df: pd.DataFrame) -> Dict:
        """
        Detect anomalies in new data
        
        Returns:
            Dict with anomaly flags, scores, and severity
        """
        try:
            X = df[self.feature_names].values
            X = np.nan_to_num(X, nan=0.0)
            X_scaled = self.scaler.transform(X)
            
            # Predict (-1 = anomaly, 1 = normal)
            predictions = self.model.predict(X_scaled)
            
            # Get anomaly scores (lower = more anomalous)
            scores = self.model.score_samples(X_scaled)
            
            # Normalize scores to 0-1 (1 = most anomalous)
            scores_normalized = 1 - ((scores - scores.min()) / (scores.max() - scores.min() + 1e-10))
            
            anomalies = []
            for idx, (pred, score) in enumerate(zip(predictions, scores_normalized)):
                if pred == -1:
                    # Determine severity
                    if score > 0.8:
                        severity = "critical"
                    elif score > 0.6:
                        severity = "high"
                    else:
                        severity = "medium"
                    
                    anomalies.append({
                        "index": idx,
                        "anomaly_score": float(score),
                        "severity": severity,
                        "features": {k: float(v) for k, v in zip(self.feature_names, X[idx])}
                    })
            
            return {
                "status": "success",
                "total_samples": len(df),
                "anomalies_detected": len(anomalies),
                "anomalies": anomalies
            }
            
        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            return {"status": "error", "message": str(e)}


class DefectPatternDetector:
    """Detect defect patterns and trends"""
    
    @staticmethod
    def detect_increasing_defects(
        df: pd.DataFrame,
        window: int = 7,
        threshold: float = 0.15
    ) -> Dict:
        """
        Detect increasing defect rate trend
        
        Args:
            df: DataFrame with 'timestamp' and 'defect_rate'
            window: Moving average window
            threshold: Minimum increase rate to trigger alert (0.15 = 15%)
        """
        try:
            df = df.sort_values('timestamp')
            df['defect_ma'] = df['defect_rate'].rolling(window=window).mean()
            
            # Compare recent to baseline
            recent = df.tail(window)['defect_ma'].mean()
            baseline = df.head(len(df) - window)['defect_ma'].mean()
            
            if baseline == 0:
                increase_rate = 0
            else:
                increase_rate = (recent - baseline) / baseline
            
            trend_detected = increase_rate > threshold
            
            if increase_rate > 0.3:
                severity = "critical"
            elif increase_rate > 0.2:
                severity = "high"
            elif increase_rate > threshold:
                severity = "medium"
            else:
                severity = "low"
            
            return {
                "status": "success",
                "trend_detected": trend_detected,
                "severity": severity,
                "increase_rate": float(increase_rate),
                "recent_avg": float(recent),
                "baseline_avg": float(baseline)
            }
            
        except Exception as e:
            logger.error(f"Defect pattern detection failed: {e}")
            return {"status": "error", "message": str(e)}


class AutoencoderAnomalyDetector:
    """Deep learning anomaly detection using Autoencoder"""
    
    def __init__(self, encoding_dim: int = 8):
        """
        Args:
            encoding_dim: Size of encoded representation
        """
        self.encoding_dim = encoding_dim
        self.model = None
        self.scaler = StandardScaler()
        self.threshold = None
        
    def build_model(self, input_dim: int):
        """Build autoencoder architecture"""
        if not HAS_TENSORFLOW:
            raise ImportError("TensorFlow is required for AutoencoderAnomalyDetector. Install with: pip install tensorflow")
        
        # Encoder
        input_layer = Input(shape=(input_dim,))
        encoded = Dense(input_dim // 2, activation='relu')(input_layer)
        encoded = Dense(self.encoding_dim, activation='relu')(encoded)
        
        # Decoder
        decoded = Dense(input_dim // 2, activation='relu')(encoded)
        decoded = Dense(input_dim, activation='sigmoid')(decoded)
        
        # Autoencoder model
        self.model = Model(input_layer, decoded)
        self.model.compile(optimizer='adam', loss='mse')
        
    def train(self, df: pd.DataFrame, feature_cols: List[str], epochs: int = 50) -> Dict:
        """
        Train autoencoder on normal data
        
        Args:
            df: Training data (should be mostly normal)
            feature_cols: Features to use
            epochs: Training epochs
        """
        try:
            X = df[feature_cols].values
            X = np.nan_to_num(X, nan=0.0)
            
            # Scale
            X_scaled = self.scaler.fit_transform(X)
            
            # Build model
            self.build_model(X_scaled.shape[1])
            
            # Train
            early_stop = EarlyStopping(monitor='loss', patience=5, restore_best_weights=True)
            history = self.model.fit(
                X_scaled, X_scaled,
                epochs=epochs,
                batch_size=32,
                shuffle=True,
                validation_split=0.1,
                verbose=0,
                callbacks=[early_stop]
            )
            
            # Calculate reconstruction error threshold
            reconstructions = self.model.predict(X_scaled)
            mse = np.mean(np.power(X_scaled - reconstructions, 2), axis=1)
            self.threshold = np.percentile(mse, 95)  # 95th percentile
            
            return {
                "status": "success",
                "samples_trained": len(df),
                "final_loss": float(history.history['loss'][-1]),
                "threshold": float(self.threshold)
            }
            
        except Exception as e:
            logger.error(f"Autoencoder training failed: {e}")
            return {"status": "error", "message": str(e)}
    
    def detect(self, df: pd.DataFrame, feature_cols: List[str]) -> Dict:
        """Detect anomalies using reconstruction error"""
        try:
            X = df[feature_cols].values
            X = np.nan_to_num(X, nan=0.0)
            X_scaled = self.scaler.transform(X)
            
            # Reconstruct
            reconstructions = self.model.predict(X_scaled)
            
            # Calculate reconstruction error
            mse = np.mean(np.power(X_scaled - reconstructions, 2), axis=1)
            
            # Detect anomalies
            anomalies = []
            for idx, error in enumerate(mse):
                if error > self.threshold:
                    # Calculate severity based on how much it exceeds threshold
                    excess = (error - self.threshold) / self.threshold
                    
                    if excess > 1.0:
                        severity = "critical"
                    elif excess > 0.5:
                        severity = "high"
                    else:
                        severity = "medium"
                    
                    anomalies.append({
                        "index": idx,
                        "reconstruction_error": float(error),
                        "severity": severity,
                        "features": {k: float(v) for k, v in zip(feature_cols, X[idx])}
                    })
            
            return {
                "status": "success",
                "total_samples": len(df),
                "anomalies_detected": len(anomalies),
                "anomalies": anomalies,
                "threshold": float(self.threshold)
            }
            
        except Exception as e:
            logger.error(f"Anomaly detection failed: {e}")
            return {"status": "error", "message": str(e)}


class MultiVariateAnomalyDetector:
    """Combined approach using multiple methods"""
    
    def __init__(self):
        self.isolation_forest = QualityAnomalyDetector(contamination=0.1)
        self.autoencoder = None
        
    def detect_anomalies(
        self,
        df: pd.DataFrame,
        feature_cols: List[str],
        method: str = "isolation_forest"
    ) -> Dict:
        """
        Detect anomalies using specified method
        
        Args:
            df: Data to analyze
            feature_cols: Features to use
            method: 'isolation_forest', 'autoencoder', or 'ensemble'
        """
        if method == "isolation_forest":
            return self.isolation_forest.predict(df)
        elif method == "autoencoder":
            if self.autoencoder is None:
                return {"status": "error", "message": "Autoencoder not trained"}
            return self.autoencoder.detect(df, feature_cols)
        else:
            return {"status": "error", "message": f"Unknown method: {method}"}
