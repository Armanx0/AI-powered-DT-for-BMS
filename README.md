# Intelligent Battery Digital Twin MVP

A production-grade backend system for real-time battery state estimation, health monitoring, and predictive maintenance using machine learning.

## 🎯 Overview

This system implements a complete battery intelligence platform with 7 core stages:

- **Stage 1**: Feature Engineering Pipeline
- **Stage 2**: State of Charge (SOC) Prediction
- **Stage 3**: State of Health (SOH) Prediction
- **Stage 4**: Hierarchical Integration Layer
- **Stage 5**: Digital Twin Engine
- **Stage 6**: Forecasting Engine
- **Stage 6.2**: Anomaly + Failure Intelligence

## 🛠 Tech Stack (Free & Production-Ready)

| Component | Technology | Why This Choice |
|-----------|------------|-----------------|
| **Framework** | FastAPI (Python) | Async, fast, perfect for ML pipelines |
| **Database** | PostgreSQL (Neon) | Serverless, 3GB free, scalable, JSONB support |
| **Cache/Queue** | Redis (optional) / Celery | Background ML inference tasks |
| **ML Models** | XGBoost | Fast, explainable, lightweight deployment |
| **Deployment** | Render + Docker | 750 hrs/mo free, GitHub integration, native FastAPI |
| **Storage** | AWS S3 / Backblaze B2 | ML model versioning & raw data |
| **Auth** | JWT + RBAC | Stateless, scalable authentication |

## 📁 Project Structure

```
AI-powered-DT-for-BMS/
├── app/
│   ├── main.py                          # FastAPI entry point
│   ├── config.py                        # Configuration & env vars
│   ├── database.py                      # Database connection
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── jwt.py                       # JWT token handling
│   │   └── rbac.py                      # Role-based access control
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py                      # POST /auth/signup, /auth/login
│   │   ├── upload.py                    # POST /upload/battery-data
│   │   ├── soc.py                       # POST /predict/soc
│   │   ├── soh.py                       # POST /predict/soh
│   │   ├── digital_twin.py              # GET /battery/{id}/digital-twin
│   │   ├── forecast.py                  # POST /forecast
│   │   ├── anomaly.py                   # POST /anomaly
│   │   └── dashboard.py                 # GET /fleet/overview, /fleet/alerts
│   ├── services/
│   │   ├── __init__.py
│   │   ├── feature_engineering.py       # ETL pipeline (dV/dt, dI/dt, etc.)
│   │   ├── soc_service.py               # SOC XGBoost inference
│   │   ├── soh_service.py               # SOH XGBoost inference
│   │   ├── twin_service.py              # Digital twin state management
│   │   ├── forecast_service.py          # Multi-horizon forecasting
│   │   ├── anomaly_service.py           # Hybrid anomaly detection
│   │   └── validation_service.py        # Data validation
│   ├── models/
│   │   ├── __init__.py
│   │   ├── db.py                        # SQLAlchemy ORM models
│   │   ├── schemas.py                   # Pydantic request/response schemas
│   │   └── ml/
│   │       ├── soc_model.pkl            # Trained SOC XGBoost
│   │       ├── soh_model.pkl            # Trained SOH XGBoost
│   │       └── forecast_model.pkl       # Trained Forecast XGBoost
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logger.py                    # Logging setup
│   │   ├── validators.py                # Data validation utilities
│   │   ├── constants.py                 # App constants
│   │   └── exceptions.py                # Custom exceptions
│   └── tasks/
│       ├── __init__.py
│       ├── celery_app.py                # Celery configuration (optional)
│       └── background_tasks.py          # Async task definitions
│
├── tests/
│   ├── __init__.py
│   ├── test_auth.py
│   ├── test_soc.py
│   ├── test_soh.py
│   ├── test_forecast.py
│   └── test_anomaly.py
│
├── migrations/                          # Alembic database migrations
├── .env.example                         # Environment template
├── .gitignore                           # Git ignore patterns
├── requirements.txt                     # Python dependencies
├── Dockerfile                           # Container image
├── docker-compose.yml                   # Multi-service orchestration
└── README.md                            # This file
```

## 🚀 Quick Start

### Local Development

```bash
# Clone repository
git clone https://github.com/Armanx0/AI-powered-DT-for-BMS.git
cd AI-powered-DT-for-BMS

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your DATABASE_URL and SECRET_KEY

# Run migrations
alembic upgrade head

# Start dev server
uvicorn app.main:app --reload
```

API available at: **http://localhost:8000**
Swagger docs: **http://localhost:8000/docs**

### Docker Deployment (Local)

```bash
# Build and run all services
docker-compose up --build

# Access API at http://localhost:8000
```

## 📡 API Endpoints

### Authentication
```
POST   /auth/signup              # Register new user
POST   /auth/login               # Login (returns JWT token)
```

### Data Management
```
POST   /upload/battery-data      # Upload raw CSV/JSON cycles
POST   /process/features         # Trigger feature engineering
```

### Real-Time Predictions
```
POST   /predict/soc              # SOC estimation
POST   /predict/soh              # SOH estimation
POST   /battery/state            # Unified battery state (SOC + SOH)
```

### Advanced Intelligence
```
POST   /forecast                 # Multi-horizon predictions
POST   /anomaly                  # Anomaly & failure detection
```

### Digital Twin & Monitoring
```
GET    /battery/{id}/digital-twin          # Digital twin state
GET    /battery/{id}/history               # Historical evolution
GET    /battery/{id}/report                # Detailed health report
GET    /fleet/overview                     # Fleet dashboard
GET    /fleet/alerts                       # Active anomalies
```

## 💾 Database Schema

```sql
-- Core tables
batteries                   -- Battery metadata & identification
raw_cycles                 -- Raw telemetry (V, I, T, time)
engineered_features        -- Processed feature vectors
soc_predictions            -- SOC estimation history
soh_predictions            -- SOH estimation history
digital_twin_states        -- Twin snapshots over time
forecasts                  -- Future predictions
anomaly_logs               -- Anomaly detection results
maintenance_actions        -- Maintenance recommendations
```

## 🔧 Environment Configuration

Create a `.env` file:

```env
# FastAPI
APP_NAME=Battery-Twin-MVP
APP_VERSION=1.0.0
DEBUG=False

# Database (Neon PostgreSQL)
DATABASE_URL=postgresql://user:password@ep-xxxxx.neon.tech/dbname

# JWT
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRY=3600

# Redis (Optional for Celery)
REDIS_URL=redis://localhost:6379/0

# ML Models Path
MODELS_PATH=./app/models/ml

# Logging
LOG_LEVEL=INFO
```

## 🌐 Free Deployment Guide (Render + Neon)

### Step 1: Database (Neon PostgreSQL)
```
1. Visit https://neon.tech
2. Sign up (free account)
3. Create project → Get DATABASE_URL
4. Copy to .env
```

### Step 2: Deploy on Render
```
1. Visit https://render.com
2. Connect your GitHub repo
3. Create New → Web Service
4. Select this repository
5. Add environment variables:
   - DATABASE_URL (from Neon)
   - SECRET_KEY (generate random string)
6. Deploy!
```

Your API will be live at: `https://your-service.onrender.com`

## 📊 Model Pipeline

```
Raw Battery Data
       ↓
Validation Layer
       ↓
Feature Engineering Pipeline
  ├─ dV/dt, dI/dt, dT/dt
  ├─ Power, Energy
  ├─ Capacity fraction
  └─ Resistance features
       ↓
Unified Feature Vector
       ↓
┌──────────────────┬──────────────────┐
│                  │                  │
↓                  ↓                  ↓
SOC Model    SOH Model      Integration Layer
(XGBoost)    (XGBoost)      (Unified State)
│                  │                  │
└──────────────────┬──────────────────┘
                   ↓
          Digital Twin State
          ├─ Current SOC
          ├─ Current SOH
          ├─ Resistance profile
          └─ Historical memory
                   ↓
        ┌──────────┬─────────┐
        ↓          ↓         ↓
    Forecast   Anomaly   Dashboard
    (XGBoost)  (Hybrid)   (Analytics)
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_soc.py -v

# Run with logging output
pytest -v -s
```

## 📈 Performance Targets

| Metric | Target |
|--------|--------|
| SOC Prediction Latency | < 100ms |
| SOH Prediction Latency | < 200ms |
| Anomaly Detection Latency | < 150ms |
| Database Query P95 | < 50ms |
| API Throughput | 1000+ req/sec |

## 🔐 Security

- ✅ JWT token-based authentication
- ✅ Role-based access control (RBAC)
- ✅ Password hashing (bcrypt)
- ✅ CORS middleware configured
- ✅ Input validation on all endpoints
- ✅ SQL injection protection (SQLAlchemy ORM)
- ✅ Environment variable secrets management

## 📝 Development Workflow

```bash
# Create feature branch
git checkout -b feature/your-feature

# Make changes, test locally
pytest

# Commit and push
git add .
git commit -m "feat: add SOC prediction enhancement"
git push origin feature/your-feature

# Open PR for review
# Deploy to Render on merge to main
```

## 🚦 Deployment Stages

| Stage | Status | Timeline |
|-------|--------|----------|
| Stage 1: Feature Engineering | ✅ Ready | Now |
| Stage 2: SOC Prediction | ✅ Ready | Now |
| Stage 3: SOH Prediction | ✅ Ready | Now |
| Stage 4: Integration Layer | ✅ Ready | Now |
| Stage 5: Digital Twin Engine | ✅ Ready | Now |
| Stage 6: Forecasting | ✅ Ready | Now |
| Stage 6.2: Anomaly Intelligence | ✅ Ready | Now |
| Stage 6.5: Federated Learning | 📋 Future | Q3 2026 |
| Stage 7: RL Optimization | 📋 Future | Q4 2026 |

## 📚 Documentation

- **API Docs**: `/docs` (Swagger UI)
- **ReDoc**: `/redoc` (Alternative docs)
- **Model Details**: See `/models/` documentation
- **Database Schema**: See `/migrations/` for Alembic schema

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/your-feature`
3. Write tests for new functionality
4. Commit with clear messages: `git commit -m "feat: description"`
5. Push and create Pull Request
6. CI/CD pipeline runs tests automatically
7. Merge after review

## 📞 Support

- **Issues**: GitHub Issues for bugs/features
- **Discussions**: GitHub Discussions for questions
- **API Docs**: Built-in Swagger at `/docs`

## 📄 License

MIT License - See LICENSE file

---

**Built for production-grade battery intelligence and predictive maintenance.**

Status: **MVP Ready for Deployment** 🚀
Last Updated: May 13, 2026
