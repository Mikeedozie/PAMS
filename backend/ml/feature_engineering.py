"""
Feature engineering for alert prioritization and prediction
Extracts meaningful features from raw data
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class FeatureEngineer:
    """Extract and engineer features for ML models"""
    
    @staticmethod
    def extract_inventory_features(df: pd.DataFrame) -> pd.DataFrame:
        """
        Extract features from inventory time-series
        
        Args:
            df: DataFrame with columns: timestamp, stock_level, demand, supply
        
        Returns:
            DataFrame with engineered features
        """
        df = df.copy().sort_values('timestamp')
        
        # Rolling statistics
        df['stock_ma_7'] = df['stock_level'].rolling(window=7, min_periods=1).mean()
        df['stock_ma_14'] = df['stock_level'].rolling(window=14, min_periods=1).mean()
        df['stock_std_7'] = df['stock_level'].rolling(window=7, min_periods=1).std()
        
        # Demand features
        if 'demand' in df.columns:
            df['demand_ma_7'] = df['demand'].rolling(window=7, min_periods=1).mean()
            df['demand_std_7'] = df['demand'].rolling(window=7, min_periods=1).std()
            df['demand_trend'] = df['demand'].diff(periods=7)
        
        # Stock velocity (rate of change)
        df['stock_velocity'] = df['stock_level'].diff()
        df['stock_acceleration'] = df['stock_velocity'].diff()
        
        # Days of inventory on hand (if demand available)
        if 'demand' in df.columns:
            df['days_on_hand'] = df['stock_level'] / (df['demand_ma_7'] + 0.01)
        
        # Volatility
        df['stock_volatility'] = df['stock_level'].rolling(window=14, min_periods=1).std() / \
                                 (df['stock_level'].rolling(window=14, min_periods=1).mean() + 0.01)
        
        # Fill NaN with 0
        df = df.fillna(0)
        
        return df
    
    @staticmethod
    def extract_quality_features(df: pd.DataFrame) -> pd.DataFrame:
        """
        Extract features from quality metrics
        
        Args:
            df: DataFrame with columns: timestamp, defect_rate, inspection_count, failure_count
        """
        df = df.copy().sort_values('timestamp')
        
        # Defect rate statistics
        df['defect_ma_7'] = df['defect_rate'].rolling(window=7, min_periods=1).mean()
        df['defect_ma_30'] = df['defect_rate'].rolling(window=30, min_periods=1).mean()
        df['defect_std_7'] = df['defect_rate'].rolling(window=7, min_periods=1).std()
        
        # Defect rate trend
        df['defect_trend'] = df['defect_rate'].diff(periods=7)
        df['defect_acceleration'] = df['defect_trend'].diff()
        
        # Inspection statistics
        if 'inspection_count' in df.columns:
            df['inspection_ma_7'] = df['inspection_count'].rolling(window=7, min_periods=1).mean()
        
        # Failure rate
        if 'failure_count' in df.columns and 'inspection_count' in df.columns:
            df['failure_rate'] = df['failure_count'] / (df['inspection_count'] + 0.01)
            df['failure_ma_7'] = df['failure_rate'].rolling(window=7, min_periods=1).mean()
        
        # Volatility
        df['defect_volatility'] = df['defect_rate'].rolling(window=14, min_periods=1).std()
        
        df = df.fillna(0)
        return df
    
    @staticmethod
    def extract_temporal_features(timestamp: datetime) -> Dict:
        """
        Extract time-based features
        
        Returns:
            Dict with day_of_week, hour, is_weekend, is_business_hours, etc.
        """
        return {
            'hour': timestamp.hour,
            'day_of_week': timestamp.weekday(),
            'day_of_month': timestamp.day,
            'month': timestamp.month,
            'quarter': (timestamp.month - 1) // 3 + 1,
            'is_weekend': int(timestamp.weekday() >= 5),
            'is_business_hours': int(9 <= timestamp.hour <= 17),
            'week_of_year': timestamp.isocalendar()[1]
        }
    
    @staticmethod
    def calculate_lag_features(
        df: pd.DataFrame,
        target_col: str,
        lags: List[int] = [1, 7, 14, 30]
    ) -> pd.DataFrame:
        """
        Create lagged features for time-series
        
        Args:
            df: DataFrame sorted by time
            target_col: Column to create lags for
            lags: List of lag periods
        """
        df = df.copy()
        
        for lag in lags:
            df[f'{target_col}_lag_{lag}'] = df[target_col].shift(lag)
        
        df = df.fillna(0)
        return df
    
    @staticmethod
    def create_alert_features(alert_data: Dict) -> Dict:
        """
        Create features from alert metadata for scoring
        
        Args:
            alert_data: Dict with alert information
        
        Returns:
            Feature dict for classification/scoring
        """
        features = {}
        
        # Severity encoding
        severity_map = {'critical': 4, 'high': 3, 'medium': 2, 'low': 1}
        features['severity_encoded'] = severity_map.get(alert_data.get('severity', 'low'), 1)
        
        # Category encoding (one-hot)
        category = alert_data.get('category', 'unknown')
        categories = ['quality', 'supply', 'demand', 'expiration', 'defect', 'supplier']
        for cat in categories:
            features[f'category_{cat}'] = 1 if category == cat else 0
        
        # Source encoding
        source = alert_data.get('source', 'manual')
        sources = ['sensor', 'ml_model', 'manual', 'integration']
        for src in sources:
            features[f'source_{src}'] = 1 if source == src else 0
        
        # Time-based features
        created_at = alert_data.get('created_at', datetime.utcnow())
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)
        
        temporal = FeatureEngineer.extract_temporal_features(created_at)
        features.update(temporal)
        
        # Confidence and scores
        features['confidence'] = alert_data.get('confidence', 0.5)
        features['impact_score'] = alert_data.get('impact_score', 0.5)
        features['likelihood'] = alert_data.get('likelihood', 0.5)
        
        return features
    
    @staticmethod
    def normalize_features(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """
        Min-max normalization for specified columns
        
        Args:
            df: DataFrame
            columns: Columns to normalize
        """
        df = df.copy()
        
        for col in columns:
            if col in df.columns:
                min_val = df[col].min()
                max_val = df[col].max()
                
                if max_val > min_val:
                    df[col] = (df[col] - min_val) / (max_val - min_val)
                else:
                    df[col] = 0
        
        return df
    
    @staticmethod
    def create_interaction_features(df: pd.DataFrame, col_pairs: List[tuple]) -> pd.DataFrame:
        """
        Create interaction features (multiplication of feature pairs)
        
        Args:
            df: DataFrame
            col_pairs: List of tuples with column pairs to interact
        """
        df = df.copy()
        
        for col1, col2 in col_pairs:
            if col1 in df.columns and col2 in df.columns:
                df[f'{col1}_x_{col2}'] = df[col1] * df[col2]
        
        return df
    
    @staticmethod
    def extract_product_features(product_data: Dict) -> Dict:
        """
        Extract features from product metadata
        
        Returns:
            Product feature dict
        """
        features = {}
        
        # Stock features
        current_stock = product_data.get('current_stock', 0)
        reorder_point = product_data.get('reorder_point', 0)
        
        features['stock_level'] = current_stock
        features['reorder_point'] = reorder_point
        features['stock_reorder_ratio'] = current_stock / (reorder_point + 0.01)
        features['below_reorder_point'] = 1 if current_stock < reorder_point else 0
        
        # Cost features
        features['unit_cost'] = product_data.get('unit_cost', 0)
        
        # Category encoding
        category = product_data.get('category', 'unknown')
        categories = ['electronics', 'industrial', 'medical', 'food', 'chemical']
        for cat in categories:
            features[f'category_{cat}'] = 1 if category == cat else 0
        
        # Status
        status = product_data.get('status', 'active')
        features['is_active'] = 1 if status == 'active' else 0
        
        return features
