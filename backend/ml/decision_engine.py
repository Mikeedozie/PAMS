"""
Alert scoring, prioritization, deduplication, and decision engine
Central intelligence for PAMS alert management
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import hashlib
import logging

from ..ml.classification import RiskScoreCalculator
from ..ml.feature_engineering import FeatureEngineer

logger = logging.getLogger(__name__)


class AlertScorer:
    """Calculate priority scores for alerts"""
    
    def __init__(self):
        self.risk_calculator = RiskScoreCalculator()
        self.feature_engineer = FeatureEngineer()
    
    def calculate_alert_score(self, alert: Dict) -> Dict:
        """
        Calculate comprehensive alert score
        
        Args:
            alert: Alert dict with severity, category, confidence, impact, etc.
        
        Returns:
            Dict with composite_score, priority, and breakdown
        """
        try:
            severity = alert.get('severity', 'low')
            confidence = alert.get('confidence', 0.5)
            impact_score = alert.get('impact_score', 0.5)
            likelihood = alert.get('likelihood', 0.5)
            
            # Time sensitivity based on age
            created_at = alert.get('created_at', datetime.utcnow())
            if isinstance(created_at, str):
                created_at = datetime.fromisoformat(created_at)
            
            age_hours = (datetime.utcnow() - created_at).total_seconds() / 3600
            time_sensitivity = max(0.5, 1.0 - (age_hours / 168))  # Decay over 1 week
            
            # Calculate composite risk
            risk_result = self.risk_calculator.calculate_composite_risk(
                severity=severity,
                likelihood=likelihood,
                impact=impact_score,
                confidence=confidence,
                time_sensitivity=time_sensitivity
            )
            
            # Add additional context
            risk_result['age_hours'] = age_hours
            risk_result['category'] = alert.get('category', 'unknown')
            risk_result['source'] = alert.get('source', 'unknown')
            
            return risk_result
            
        except Exception as e:
            logger.error(f"Alert scoring failed: {e}")
            return {
                "composite_score": 0.5,
                "priority": "p3",
                "priority_label": "Error in scoring",
                "error": str(e)
            }
    
    def batch_score_alerts(self, alerts: List[Dict]) -> List[Dict]:
        """
        Score multiple alerts and sort by priority
        
        Returns:
            List of alerts with scores, sorted by priority (highest first)
        """
        scored_alerts = []
        
        for alert in alerts:
            score_result = self.calculate_alert_score(alert)
            
            # Merge score into alert
            alert_with_score = {**alert, **score_result}
            scored_alerts.append(alert_with_score)
        
        # Sort by composite score (descending)
        scored_alerts.sort(key=lambda x: x.get('composite_score', 0), reverse=True)
        
        return scored_alerts


class AlertDeduplicator:
    """Detect and merge duplicate/similar alerts"""
    
    @staticmethod
    def generate_alert_fingerprint(alert: Dict) -> str:
        """
        Create a fingerprint for alert similarity detection
        
        Uses: product_id, category, severity
        """
        product_id = alert.get('product_id', '')
        category = alert.get('category', '')
        severity = alert.get('severity', '')
        
        fingerprint_str = f"{product_id}:{category}:{severity}"
        return hashlib.md5(fingerprint_str.encode()).hexdigest()
    
    @staticmethod
    def calculate_similarity(alert1: Dict, alert2: Dict) -> float:
        """
        Calculate similarity score between two alerts (0-1)
        
        Returns:
            Similarity score (1.0 = identical, 0.0 = completely different)
        """
        score = 0.0
        
        # Product match (0.4 weight)
        if alert1.get('product_id') == alert2.get('product_id'):
            score += 0.4
        
        # Category match (0.3 weight)
        if alert1.get('category') == alert2.get('category'):
            score += 0.3
        
        # Severity match (0.2 weight)
        if alert1.get('severity') == alert2.get('severity'):
            score += 0.2
        
        # Time proximity (0.1 weight)
        created1 = alert1.get('created_at', datetime.utcnow())
        created2 = alert2.get('created_at', datetime.utcnow())
        
        if isinstance(created1, str):
            created1 = datetime.fromisoformat(created1)
        if isinstance(created2, str):
            created2 = datetime.fromisoformat(created2)
        
        time_diff_hours = abs((created1 - created2).total_seconds() / 3600)
        if time_diff_hours < 24:
            score += 0.1 * (1 - time_diff_hours / 24)
        
        return score
    
    @staticmethod
    def find_duplicates(
        alerts: List[Dict],
        similarity_threshold: float = 0.8
    ) -> List[Tuple[int, int, float]]:
        """
        Find duplicate alert pairs
        
        Returns:
            List of tuples (index1, index2, similarity_score)
        """
        duplicates = []
        
        for i in range(len(alerts)):
            for j in range(i + 1, len(alerts)):
                similarity = AlertDeduplicator.calculate_similarity(alerts[i], alerts[j])
                
                if similarity >= similarity_threshold:
                    duplicates.append((i, j, similarity))
        
        return duplicates
    
    @staticmethod
    def merge_alerts(primary: Dict, duplicate: Dict) -> Dict:
        """
        Merge duplicate alert into primary, keeping highest severity/confidence
        """
        merged = primary.copy()
        
        # Take highest severity
        severity_order = {'critical': 4, 'high': 3, 'medium': 2, 'low': 1}
        if severity_order.get(duplicate.get('severity', 'low'), 0) > \
           severity_order.get(primary.get('severity', 'low'), 0):
            merged['severity'] = duplicate['severity']
        
        # Take highest confidence
        if duplicate.get('confidence', 0) > primary.get('confidence', 0):
            merged['confidence'] = duplicate['confidence']
        
        # Merge descriptions
        if duplicate.get('description'):
            merged['description'] += f"\n[Merged] {duplicate['description']}"
        
        # Track merge
        merged['merged_alert_ids'] = merged.get('merged_alert_ids', []) + \
                                     [duplicate.get('id')]
        
        return merged


class AlertEnricher:
    """Enrich alerts with additional context and data"""
    
    @staticmethod
    def enrich_with_product_context(alert: Dict, product: Dict) -> Dict:
        """Add product information to alert"""
        enriched = alert.copy()
        
        enriched['product_name'] = product.get('name')
        enriched['product_sku'] = product.get('sku')
        enriched['product_category'] = product.get('category')
        enriched['current_stock'] = product.get('current_stock')
        enriched['reorder_point'] = product.get('reorder_point')
        
        # Add stock context to description
        if product.get('current_stock') and product.get('reorder_point'):
            stock_ratio = product['current_stock'] / (product['reorder_point'] + 0.01)
            enriched['stock_health'] = 'critical' if stock_ratio < 0.5 else \
                                      'warning' if stock_ratio < 1.0 else 'healthy'
        
        return enriched
    
    @staticmethod
    def enrich_with_historical_context(alert: Dict, history: List[Dict]) -> Dict:
        """Add historical alert context"""
        enriched = alert.copy()
        
        # Count similar past alerts
        similar_count = len([h for h in history 
                           if h.get('category') == alert.get('category')])
        
        enriched['similar_alerts_past_30_days'] = similar_count
        
        # Check if recurring
        enriched['is_recurring'] = similar_count > 2
        
        # Average resolution time for similar alerts
        resolved = [h for h in history 
                   if h.get('status') == 'resolved' and h.get('resolved_at')]
        
        if resolved:
            resolution_times = []
            for h in resolved:
                created = h.get('created_at')
                resolved_at = h.get('resolved_at')
                if created and resolved_at:
                    if isinstance(created, str):
                        created = datetime.fromisoformat(created)
                    if isinstance(resolved_at, str):
                        resolved_at = datetime.fromisoformat(resolved_at)
                    
                    resolution_times.append((resolved_at - created).total_seconds() / 3600)
            
            if resolution_times:
                enriched['avg_resolution_hours'] = sum(resolution_times) / len(resolution_times)
        
        return enriched


class SLAManager:
    """Manage SLA deadlines and escalation"""
    
    # SLA targets by priority (in hours)
    SLA_TARGETS = {
        'p1': 4,   # 4 hours
        'p2': 24,  # 1 day
        'p3': 72,  # 3 days
        'p4': 168  # 1 week
    }
    
    @staticmethod
    def calculate_sla_deadline(alert: Dict) -> datetime:
        """Calculate SLA deadline based on priority"""
        priority = alert.get('priority', 'p3')
        created_at = alert.get('created_at', datetime.utcnow())
        
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)
        
        sla_hours = SLAManager.SLA_TARGETS.get(priority, 72)
        deadline = created_at + timedelta(hours=sla_hours)
        
        return deadline
    
    @staticmethod
    def check_sla_breach(alert: Dict) -> Dict:
        """
        Check if alert is breaching SLA
        
        Returns:
            Dict with sla_status, time_remaining, breach_risk
        """
        deadline = SLAManager.calculate_sla_deadline(alert)
        now = datetime.utcnow()
        
        time_remaining = (deadline - now).total_seconds() / 3600  # hours
        
        if time_remaining < 0:
            sla_status = "breached"
            breach_risk = "high"
        elif time_remaining < 2:
            sla_status = "critical"
            breach_risk = "high"
        elif time_remaining < 12:
            sla_status = "warning"
            breach_risk = "medium"
        else:
            sla_status = "ok"
            breach_risk = "low"
        
        return {
            "sla_status": sla_status,
            "sla_deadline": deadline.isoformat(),
            "time_remaining_hours": round(time_remaining, 2),
            "breach_risk": breach_risk
        }
    
    @staticmethod
    def determine_escalation(alert: Dict) -> Optional[str]:
        """
        Determine if alert should be escalated
        
        Returns:
            Escalation level: 'manager', 'director', 'executive', or None
        """
        sla_check = SLAManager.check_sla_breach(alert)
        priority = alert.get('priority', 'p3')
        
        # Escalate critical priority immediately
        if priority == 'p1':
            if sla_check['sla_status'] == 'breached':
                return 'executive'
            elif sla_check['sla_status'] == 'critical':
                return 'director'
            else:
                return 'manager'
        
        # Escalate high priority if at risk
        elif priority == 'p2':
            if sla_check['breach_risk'] == 'high':
                return 'director'
            elif sla_check['breach_risk'] == 'medium':
                return 'manager'
        
        # Escalate medium priority only if breached
        elif priority == 'p3':
            if sla_check['sla_status'] == 'breached':
                return 'manager'
        
        return None


class DecisionEngine:
    """Central decision engine combining all alert intelligence"""
    
    def __init__(self):
        self.scorer = AlertScorer()
        self.deduplicator = AlertDeduplicator()
        self.enricher = AlertEnricher()
        self.sla_manager = SLAManager()
    
    def process_alert(
        self,
        alert: Dict,
        product: Optional[Dict] = None,
        history: Optional[List[Dict]] = None
    ) -> Dict:
        """
        Complete alert processing pipeline
        
        1. Score and prioritize
        2. Enrich with context
        3. Calculate SLA
        4. Determine assignment/escalation
        
        Returns:
            Fully processed alert ready for action
        """
        processed = alert.copy()
        
        # Step 1: Score
        score_result = self.scorer.calculate_alert_score(alert)
        processed.update(score_result)
        
        # Step 2: Enrich
        if product:
            processed = self.enricher.enrich_with_product_context(processed, product)
        
        if history:
            processed = self.enricher.enrich_with_historical_context(processed, history)
        
        # Step 3: SLA
        sla_deadline = self.sla_manager.calculate_sla_deadline(processed)
        sla_check = self.sla_manager.check_sla_breach(processed)
        processed['sla_deadline'] = sla_deadline
        processed.update(sla_check)
        
        # Step 4: Escalation
        escalation_level = self.sla_manager.determine_escalation(processed)
        processed['escalation_level'] = escalation_level
        processed['requires_escalation'] = escalation_level is not None
        
        # Step 5: Recommended actions
        processed['recommended_actions'] = self._generate_recommendations(processed)
        
        return processed
    
    def _generate_recommendations(self, alert: Dict) -> List[str]:
        """Generate action recommendations based on alert context"""
        recommendations = []
        
        priority = alert.get('priority', 'p3')
        category = alert.get('category', '')
        
        # Priority-based recommendations
        if priority == 'p1':
            recommendations.append("Immediate investigation required")
            recommendations.append("Notify relevant stakeholders")
        
        # Category-specific recommendations
        if category == 'quality':
            recommendations.append("Review recent quality inspection reports")
            recommendations.append("Check batch/lot numbers for affected products")
        
        elif category == 'supply':
            recommendations.append("Contact supplier for status update")
            recommendations.append("Identify alternative suppliers if needed")
        
        elif category == 'demand':
            recommendations.append("Adjust inventory orders")
            recommendations.append("Review demand forecast models")
        
        # Stock-specific
        if alert.get('stock_health') == 'critical':
            recommendations.append("Expedite reorder or switch to backup supplier")
        
        # Recurring alerts
        if alert.get('is_recurring'):
            recommendations.append("Investigate root cause (recurring issue)")
        
        return recommendations
