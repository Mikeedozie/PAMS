"""
Time-series forecasting module using ARIMA, Prophet, and LSTM
Predicts demand, inventory levels, and stockout risk
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
import logging
from sklearn.preprocessing import MinMaxScaler

# Optional ML libraries - gracefully handle if not installed
try:
    from prophet import Prophet
    HAS_PROPHET = True
except ImportError:
    HAS_PROPHET = False

try:
    from statsmodels.tsa.statespace.sarimax import SARIMAX
    from pmdarima import auto_arima
    HAS_STATSMODELS = True
except ImportError:
    HAS_STATSMODELS = False

try:
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dense, Dropout
    from tensorflow.keras.callbacks import EarlyStopping
    HAS_TENSORFLOW = True
except ImportError:
    HAS_TENSORFLOW = False

logger = logging.getLogger(__name__)


class DemandForecaster:
    """Forecast product demand using multiple algorithms"""
    
    def __init__(self, model_type: str = "prophet"):
        """
        Args:
            model_type: 'prophet', 'arima', or 'lstm'
        """
        self.model_type = model_type
        self.model = None
        self.scaler = None
        
    def prepare_data(self, df: pd.DataFrame, target_col: str = 'demand') -> pd.DataFrame:
        """Prepare time-series data for forecasting"""
        df = df.copy()
        df['ds'] = pd.to_datetime(df['timestamp'])
        df['y'] = df[target_col]
        df = df.sort_values('ds')
        df = df[['ds', 'y']].dropna()
        return df
    
    def train_prophet(self, df: pd.DataFrame, seasonality_mode: str = 'multiplicative') -> Dict:
        """Train Prophet model"""
        if not HAS_PROPHET:
            raise ImportError("Prophet is required for prophet forecasting. Install with: pip install prophet")
        
        try:
            self.model = Prophet(
                seasonality_mode=seasonality_mode,
                yearly_seasonality=True,
                weekly_seasonality=True,
                daily_seasonality=False,
                changepoint_prior_scale=0.05
            )
            self.model.fit(df)
            return {"status": "success", "model": "prophet"}
        except Exception as e:
            logger.error(f"Prophet training failed: {e}")
            return {"status": "error", "message": str(e)}
    
    def train_arima(self, df: pd.DataFrame, seasonal: bool = True) -> Dict:
        """Train ARIMA/SARIMA model with auto parameter selection"""
        if not HAS_STATSMODELS:
            raise ImportError("statsmodels and pmdarima are required for ARIMA forecasting. Install with: pip install statsmodels pmdarima")
        
        try:
            # Auto ARIMA to find best parameters
            auto_model = auto_arima(
                df['y'],
                seasonal=seasonal,
                m=7 if seasonal else 1,  # Weekly seasonality
                suppress_warnings=True,
                stepwise=True,
                trace=False
            )
            
            self.model = auto_model
            return {
                "status": "success",
                "model": "arima",
                "order": auto_model.order,
                "seasonal_order": auto_model.seasonal_order if seasonal else None
            }
        except Exception as e:
            logger.error(f"ARIMA training failed: {e}")
            return {"status": "error", "message": str(e)}
    
    def train_lstm(self, df: pd.DataFrame, lookback: int = 14, epochs: int = 50) -> Dict:
        """Train LSTM neural network for time-series"""
        if not HAS_TENSORFLOW:
            raise ImportError("TensorFlow is required for LSTM forecasting. Install with: pip install tensorflow")
        
        try:
            # Scale data
            self.scaler = MinMaxScaler(feature_range=(0, 1))
            scaled_data = self.scaler.fit_transform(df[['y']].values)
            
            # Create sequences
            X, y = [], []
            for i in range(lookback, len(scaled_data)):
                X.append(scaled_data[i-lookback:i, 0])
                y.append(scaled_data[i, 0])
            
            X, y = np.array(X), np.array(y)
            X = X.reshape((X.shape[0], X.shape[1], 1))
            
            # Build LSTM model
            self.model = Sequential([
                LSTM(50, return_sequences=True, input_shape=(lookback, 1)),
                Dropout(0.2),
                LSTM(50, return_sequences=False),
                Dropout(0.2),
                Dense(25),
                Dense(1)
            ])
            
            self.model.compile(optimizer='adam', loss='mse')
            
            # Train
            early_stop = EarlyStopping(monitor='loss', patience=5)
            history = self.model.fit(
                X, y,
                epochs=epochs,
                batch_size=32,
                verbose=0,
                callbacks=[early_stop]
            )
            
            return {
                "status": "success",
                "model": "lstm",
                "final_loss": float(history.history['loss'][-1])
            }
        except Exception as e:
            logger.error(f"LSTM training failed: {e}")
            return {"status": "error", "message": str(e)}
    
    def predict(self, periods: int = 7) -> Dict:
        """Generate forecast for specified periods"""
        try:
            if self.model_type == "prophet":
                future = self.model.make_future_dataframe(periods=periods)
                forecast = self.model.predict(future)
                
                predictions = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(periods)
                return {
                    "status": "success",
                    "predictions": predictions.to_dict('records'),
                    "confidence_interval": True
                }
                
            elif self.model_type == "arima":
                forecast = self.model.predict(n_periods=periods, return_conf_int=True)
                predictions = forecast[0]
                conf_int = forecast[1]
                
                return {
                    "status": "success",
                    "predictions": predictions.tolist(),
                    "confidence_lower": conf_int[:, 0].tolist(),
                    "confidence_upper": conf_int[:, 1].tolist()
                }
                
            elif self.model_type == "lstm":
                # LSTM prediction (simplified - would need last sequence)
                return {
                    "status": "success",
                    "message": "LSTM prediction requires recent data sequence"
                }
                
        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            return {"status": "error", "message": str(e)}


class StockoutPredictor:
    """Predict stockout risk and timing"""
    
    def __init__(self):
        self.forecaster = DemandForecaster(model_type="prophet")
        
    def predict_stockout_risk(
        self,
        historical_data: pd.DataFrame,
        current_stock: int,
        reorder_point: int,
        forecast_days: int = 30
    ) -> Dict:
        """
        Predict when stockout will occur and risk level
        
        Returns:
            Dict with stockout_date, days_until_stockout, risk_level, confidence
        """
        try:
            # Prepare and train
            df = self.forecaster.prepare_data(historical_data, target_col='demand')
            self.forecaster.train_prophet(df)
            
            # Forecast demand
            forecast = self.forecaster.predict(periods=forecast_days)
            if forecast['status'] != 'success':
                return forecast
            
            predictions = forecast['predictions']
            
            # Simulate inventory depletion
            inventory = current_stock
            stockout_day = None
            
            for idx, pred in enumerate(predictions):
                daily_demand = max(0, pred['yhat'])
                inventory -= daily_demand
                
                if inventory <= reorder_point:
                    stockout_day = idx + 1
                    break
            
            # Calculate risk level
            if stockout_day is None:
                risk_level = "low"
                confidence = 0.9
            elif stockout_day <= 7:
                risk_level = "critical"
                confidence = 0.85
            elif stockout_day <= 14:
                risk_level = "high"
                confidence = 0.80
            elif stockout_day <= 21:
                risk_level = "medium"
                confidence = 0.75
            else:
                risk_level = "low"
                confidence = 0.70
            
            return {
                "status": "success",
                "stockout_day": stockout_day,
                "days_until_stockout": stockout_day,
                "risk_level": risk_level,
                "confidence": confidence,
                "current_stock": current_stock,
                "reorder_point": reorder_point,
                "forecast_horizon": forecast_days
            }
            
        except Exception as e:
            logger.error(f"Stockout prediction failed: {e}")
            return {"status": "error", "message": str(e)}


class DemandSurgeDetector:
    """Detect sudden demand spikes using statistical methods"""
    
    @staticmethod
    def detect_surge(
        historical_data: pd.DataFrame,
        threshold_std: float = 2.0
    ) -> Dict:
        """
        Detect demand surge using Z-score
        
        Args:
            historical_data: DataFrame with 'timestamp' and 'demand'
            threshold_std: Number of standard deviations for anomaly
        """
        try:
            df = historical_data.copy()
            df['demand_zscore'] = (df['demand'] - df['demand'].mean()) / df['demand'].std()
            
            # Find recent surge
            recent = df.tail(7)
            max_zscore = recent['demand_zscore'].max()
            
            if max_zscore > threshold_std:
                surge_detected = True
                severity = "high" if max_zscore > 3 else "medium"
            else:
                surge_detected = False
                severity = "low"
            
            return {
                "status": "success",
                "surge_detected": surge_detected,
                "severity": severity,
                "zscore": float(max_zscore),
                "avg_demand": float(df['demand'].mean()),
                "recent_avg": float(recent['demand'].mean())
            }
            
        except Exception as e:
            logger.error(f"Surge detection failed: {e}")
            return {"status": "error", "message": str(e)}
