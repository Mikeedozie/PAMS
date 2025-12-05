# PAMS - Product Alert Management System

**AI-Driven Product Alert Management with Predictive Analytics**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-14+-black.svg)](https://nextjs.org)

## 🎯 Overview

PAMS is a cloud-based, AI-driven platform that transforms product and inventory management from **reactive firefighting to proactive prevention**. It leverages advanced machine learning, real-time data fusion, and intelligent automation to predict, prioritize, and manage product/inventory/quality issues across the entire lifecycle.

### Key Problems Solved

✅ **Alert Fatigue** → High signal-to-noise ratio with intelligent prioritization  
✅ **Late Detection** → Predictive analytics catch issues before they occur  
✅ **Manual Triage** → AI-powered scoring and automated workflows  
✅ **Siloed Data** → Centralized multi-source intelligence (ERP, IoT, CRM, social)  
✅ **Resource Constraints** → Optimized for low-bandwidth, emerging market environments  

---

## 🚀 Features

### Core Capabilities

#### 🔮 Predictive Analytics
- **Demand Forecasting**: ARIMA, Prophet, LSTM models for accurate demand prediction
- **Stockout Prediction**: Early warning system with risk scoring and timing
- **Anomaly Detection**: Isolation Forest and Autoencoders for quality/defect patterns
- **Supplier Risk Assessment**: Multi-factor supplier health scoring
- **Demand Surge Detection**: Statistical spike detection with severity classification

#### 🎯 Intelligent Alert Management
- **Smart Prioritization**: Composite scoring based on severity, likelihood, impact, confidence
- **Deduplication**: Fingerprint-based duplicate detection and merging
- **Context Enrichment**: Automatic addition of product, historical, and risk context
- **SLA Management**: Priority-based deadlines with breach detection
- **Auto-Escalation**: Rule-based escalation to managers/directors/executives

#### 📊 Analytics & Insights
- **Role-Based Dashboards**: Customized views for analysts, managers, executives
- **KPI Tracking**: MTTD, MTTR, false positive rates, prevention metrics
- **Trend Analysis**: Historical patterns and forecasting visualizations
- **Model Performance**: Continuous tracking of ML model accuracy

#### 🔔 Multi-Channel Notifications
- Email, SMS, Push, API webhooks
- Role-aware templated messaging
- Delivery tracking and confirmation

#### 🔄 Workflow Automation
- Investigation case management
- Assignment and routing logic
- Escalation paths and audit trails
- Resolution logging and feedback loops

#### 🔒 Security & Compliance
- Role-Based Access Control (RBAC)
- Comprehensive audit logging
- Data encryption and privacy safeguards

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (Next.js/React)                 │
│  Dashboards │ Analytics │ Alerts │ Workflows │ Reports      │
└────────────────────────────┬────────────────────────────────┘
                             │ REST API
┌────────────────────────────┴────────────────────────────────┐
│                    Backend (FastAPI)                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Alert Engine │  │ ML Predictor │  │ Workflow Mgr │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────┴────────────────────────────────┐
│                 Data Layer                                   │
│  PostgreSQL + TimescaleDB  │  Redis Cache  │  ML Models     │
└──────────────────────────────────────────────────────────────┘
```

### Technology Stack

**Backend:**
- FastAPI (Python 3.11+)
- SQLAlchemy 2.0 + PostgreSQL + TimescaleDB
- Redis (caching & pub/sub)
- Celery (background tasks)

**ML/AI:**
- Prophet, ARIMA, LSTM (forecasting)
- Isolation Forest, Autoencoders (anomaly detection)
- Random Forest, XGBoost, LightGBM (classification)
- scikit-learn, TensorFlow/Keras

**Frontend:**
- Next.js 14+ / React
- TypeScript
- Tailwind CSS (planned)

**Infrastructure:**
- Docker + Docker Compose
- Kubernetes-ready
- Prometheus + Grafana monitoring

---

## 📦 Installation

### Prerequisites

- **Python 3.11+**
- **Node.js 18+**
- **PostgreSQL 15+** (with TimescaleDB extension recommended)
- **Redis 7+**
- **Docker & Docker Compose** (optional, recommended)

### Quick Start with Docker

1. **Clone the repository**
```bash
git clone https://github.com/Mikeedozie/PAMS.git
cd PAMS
```

2. **Copy environment configuration**
```bash
cp backend/.env.example backend/.env
# Edit backend/.env with your configuration
```

3. **Start services**
```bash
docker-compose up -d
```

4. **Access the application**
- **API Documentation**: http://localhost:8000/docs
- **Frontend Dashboard**: http://localhost:3000
- **Prometheus**: http://localhost:9090 (with monitoring profile)
- **Grafana**: http://localhost:3001 (with monitoring profile)

### Manual Installation

#### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up database
createdb pams
psql -d pams -c "CREATE EXTENSION IF NOT EXISTS timescaledb;"

# Run migrations
alembic upgrade head

# Start the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

---

## 🔧 Configuration

Edit `backend/.env`:

```bash
# Database
DATABASE_URL=postgresql+psycopg2://user:pass@localhost:5432/pams

# Redis
REDIS_URL=redis://localhost:6379/0

# ML Settings
ML_ENABLE_GPU=False
ML_BATCH_SIZE=32

# Alert SLA Targets (hours)
ALERT_SLA_P1_HOURS=4    # Critical
ALERT_SLA_P2_HOURS=24   # High
ALERT_SLA_P3_HOURS=72   # Medium
ALERT_SLA_P4_HOURS=168  # Low

# Notifications
ENABLE_EMAIL_NOTIFICATIONS=True
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@example.com
SMTP_PASSWORD=your-password
```

---

## 📚 API Usage

### Create an Alert

```bash
curl -X POST "http://localhost:8000/api/alerts/" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "severity": "high",
    "category": "quality",
    "description": "Defect rate increasing 15% week-over-week",
    "confidence": 0.85,
    "impact_score": 0.8,
    "likelihood": 0.75
  }'
```

### Forecast Demand

```bash
curl -X POST "http://localhost:8000/api/predictions/forecast/demand" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "forecast_days": 30,
    "model_type": "prophet"
  }'
```

### Predict Stockout

```bash
curl -X POST "http://localhost:8000/api/predictions/stockout/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "forecast_days": 30
  }'
```

### Detect Anomalies

```bash
curl -X POST "http://localhost:8000/api/predictions/anomaly/detect" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "metric_type": "quality",
    "days": 30
  }'
```

**Full API documentation available at:** http://localhost:8000/docs

---

## 🎨 Dashboard Features

### Executive Dashboard
- Real-time alert summary
- Critical risk overview
- Prevention vs. reaction metrics
- Cost savings tracking

### Operations Dashboard
- Active alerts by priority
- SLA compliance tracking
- Workflow status
- Resource allocation

### Analytics Dashboard
- Demand forecasting charts
- Anomaly detection visualizations
- Model performance metrics
- Historical trend analysis

---

## 🧪 Machine Learning Models

### Forecasting Models
- **Prophet**: Additive time-series with seasonality
- **ARIMA/SARIMA**: Statistical forecasting with auto-parameter selection
- **LSTM**: Deep learning for complex patterns

### Anomaly Detection
- **Isolation Forest**: Quality metric anomalies
- **Autoencoders**: Multi-variate pattern detection
- **Statistical Methods**: Z-score, moving averages

### Classification
- **Random Forest**: Alert severity prediction
- **XGBoost**: Category classification
- **LightGBM**: Risk scoring

---

## 🔄 Workflow Example

1. **Data Ingestion**: IoT sensor reports quality metric drop
2. **Anomaly Detection**: ML model flags unusual pattern
3. **Alert Creation**: System generates alert with confidence score
4. **Intelligent Scoring**: Decision engine calculates priority (P1-P4)
5. **Context Enrichment**: Adds product, historical, supplier data
6. **SLA Calculation**: Sets deadline based on priority
7. **Auto-Assignment**: Routes to appropriate team member
8. **Notification**: Multi-channel alerts sent
9. **Workflow Tracking**: Investigation case created
10. **Resolution**: Issue resolved, feedback loop updates model

---

## 📊 Key Metrics Tracked

- **MTTD** (Mean Time To Detect): Average time to identify issues
- **MTTR** (Mean Time To Resolve): Average resolution time
- **False Positive Rate**: ML model accuracy
- **Prevention Rate**: Issues caught before impact
- **SLA Compliance**: % alerts resolved within SLA
- **Cost Savings**: Prevented recalls/stockouts/waste

---

## 🛣️ Roadmap

### Phase 1: Core Platform (Current)
- ✅ Database models and API routes
- ✅ ML prediction modules
- ✅ Alert scoring and decision engine
- ⏳ Frontend dashboard (in progress)

### Phase 2: Advanced Features
- 🔲 Real-time data streaming
- 🔲 Advanced NLP for social media sentiment
- 🔲 Explainable AI (XAI) for model interpretability
- 🔲 Mobile app (React Native)

### Phase 3: Enterprise Scale
- 🔲 Multi-tenant architecture
- 🔲 Advanced RBAC and SSO
- 🔲 Custom model training UI
- 🔲 API marketplace for integrations

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

- **Michael Edozie** - [@Mikeedozie](https://github.com/Mikeedozie)

---

## 🙏 Acknowledgments

- Built to address real-world challenges in product lifecycle management
- Designed for emerging market contexts with infrastructure constraints
- Inspired by research in predictive analytics and alert fatigue reduction

---

## 📞 Support

For issues, questions, or feature requests:
- **GitHub Issues**: [github.com/Mikeedozie/PAMS/issues](https://github.com/Mikeedozie/PAMS/issues)
- **Email**: support@pams.com

---

**PAMS** - From reactive to proactive. From chaos to clarity. 🚀

