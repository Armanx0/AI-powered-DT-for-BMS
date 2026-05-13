# Quick Start & Deployment Guide

## 🚀 Part 1: Local Development Setup

### Prerequisites
- Python 3.11+ installed
- Git installed
- PostgreSQL (or use Docker)
- pip or conda package manager

### Step 1: Clone Repository

```bash
git clone https://github.com/Armanx0/AI-powered-DT-for-BMS.git
cd AI-powered-DT-for-BMS
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Linux/macOS)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Setup Environment Variables

```bash
# Copy example file
cp .env.example .env

# Edit .env file with your settings
# For local development:
# DATABASE_URL=postgresql://battery_user:battery_password@localhost:5432/battery_twin
# SECRET_KEY=dev-secret-key-change-in-production
# ENABLE_MOCK_MODELS=True  # Use mock predictions for testing
```

### Step 5: Create Database

#### Option A: Using Docker Compose (Recommended)

```bash
# Start PostgreSQL, Redis, and other services
docker-compose up -d postgres redis

# Wait for services to be ready (30 seconds)
sleep 30
```

#### Option B: Local PostgreSQL

```bash
# Create database
psql -U postgres -c "CREATE DATABASE battery_twin;"
psql -U postgres -c "CREATE USER battery_user WITH PASSWORD 'battery_password';"
psql -U postgres -c "ALTER ROLE battery_user SET client_encoding TO 'utf8';"
psql -U postgres -c "ALTER ROLE battery_user SET default_transaction_isolation TO 'read committed';"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE battery_twin TO battery_user;"
```

### Step 6: Run Database Migrations

```bash
alembic upgrade head
```

### Step 7: Start Development Server

```bash
# Option A: Using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Option B: Using Python
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

✅ **API is now running at: http://localhost:8000**

---

## 📚 Part 2: Test the API

### Access API Documentation

```
Swagger UI:  http://localhost:8000/docs
ReDoc:       http://localhost:8000/redoc
OpenAPI:     http://localhost:8000/openapi.json
```

### Health Check

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "app": "Battery-Twin-MVP",
  "version": "1.0.0",
  "environment": "development"
}
```

### 1. User Registration

```bash
curl -X POST "http://localhost:8000/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "TestPassword123!"
  }'
```

Expected response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

### 2. Create a Battery

First, add a battery to the database (use Swagger UI or database insert):

```bash
curl -X POST "http://localhost:8000/battery/create" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "battery_id": "BATT_001",
    "battery_type": "LiPo",
    "nominal_voltage": 12.0,
    "nominal_capacity": 100.0,
    "max_charge_current": 50.0,
    "max_discharge_current": 100.0
  }'
```

### 3. Predict SOC

```bash
curl -X POST "http://localhost:8000/predict/soc?battery_id=BATT_001&voltage=3.8&current=25.0&temperature=25.0" \
  -H "Content-Type: application/json"
```

Expected response:
```json
{
  "soc": 76.5,
  "confidence": 0.95,
  "timestamp": "2026-05-13T15:45:00Z",
  "model_version": null
}
```

### 4. Predict SOH

```bash
curl -X POST "http://localhost:8000/predict/soh?battery_id=BATT_001&cycle_count=100&internal_resistance=0.05" \
  -H "Content-Type: application/json"
```

Expected response:
```json
{
  "soh": 99.5,
  "degradation_rate": 0.5,
  "timestamp": "2026-05-13T15:45:00Z",
  "model_version": null
}
```

### 5. Generate Forecast

```bash
curl -X POST "http://localhost:8000/forecast?battery_id=BATT_001&current_soc=0.765&current_soh=0.995&horizon_hours=24" \
  -H "Content-Type: application/json"
```

Expected response:
```json
{
  "future_soc": [0.76, 0.74, 0.72, ...],
  "future_soh": [0.995, 0.994, 0.993, ...],
  "future_resistance": [0.05, 0.051, 0.052, ...],
  "confidence": 0.85,
  "horizon_hours": 24,
  "timestamp": "2026-05-13T15:45:00Z"
}
```

### 6. Detect Anomalies

```bash
curl -X POST "http://localhost:8000/anomaly?battery_id=BATT_001&soc=0.765&soh=0.995&temperature=25.0&internal_resistance=0.05" \
  -H "Content-Type: application/json"
```

Expected response:
```json
{
  "status": "normal",
  "severity": "none"
}
```

### 7. Get Digital Twin State

```bash
curl http://localhost:8000/battery/BATT_001/digital-twin
```

### 8. Get Fleet Overview

```bash
curl http://localhost:8000/fleet/overview
```

### 9. Get Fleet Alerts

```bash
curl http://localhost:8000/fleet/alerts
```

---

## 🐳 Part 3: Docker Deployment (Local)

### Run Full Stack with Docker Compose

```bash
# Start all services (backend, PostgreSQL, Redis, pgAdmin)
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### Access Services

- **API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **pgAdmin**: http://localhost:5050 (admin@battreytwim.local / admin)
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

---

## ☁️ Part 4: Free Cloud Deployment (Render + Neon)

### Step 1: Create Neon PostgreSQL Database

1. Go to https://neon.tech
2. Sign up (free account - 3GB storage)
3. Create new project
4. Copy the connection string (looks like: `postgresql://user:password@ep-xxxxx.neon.tech/database`)
5. Save it for later

### Step 2: Deploy on Render

1. Go to https://render.com
2. Sign up with GitHub
3. Create new **Web Service**
4. Select "Connect a Repository"
5. Choose `AI-powered-DT-for-BMS`
6. Configure:
   - **Name**: `battery-twin-backend`
   - **Runtime**: Python 3.11
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 app.main:app`
7. Add environment variables:
   ```
   DATABASE_URL=postgresql://user:password@ep-xxxxx.neon.tech/battery_twin
   SECRET_KEY=generate-random-string-here
   ENVIRONMENT=production
   DEBUG=False
   ENABLE_MOCK_MODELS=True
   ```
8. Click **Deploy**

✅ **Your API is live at**: `https://battery-twin-backend.onrender.com`

### Step 3: Verify Cloud Deployment

```bash
# Health check
curl https://battery-twin-backend.onrender.com/health

# Access Swagger docs
https://battery-twin-backend.onrender.com/docs
```

---

## 🛠️ Part 5: Train & Add Your Models

### Current Setup

The backend is currently using **mock models** for testing. To add your trained XGBoost models:

### Step 1: Train Models (Optional)

```python
import joblib
import xgboost as xgb
import numpy as np

# Example: Train SOC model
X_train = np.random.rand(1000, 3)  # voltage, current, temperature
y_train = np.random.rand(1000)     # SOC values

model = xgb.XGBRegressor(
    n_estimators=100,
    max_depth=5,
    learning_rate=0.1
)
model.fit(X_train, y_train)

# Save model
joblib.dump(model, 'app/models/ml/soc_model.pkl')
joblib.dump(model, 'app/models/ml/soh_model.pkl')
joblib.dump(model, 'app/models/ml/forecast_model.pkl')
```

### Step 2: Add Models to Repository

```bash
# Create models directory
mkdir -p app/models/ml

# Copy your trained models
cp soc_model.pkl app/models/ml/
cp soh_model.pkl app/models/ml/
cp forecast_model.pkl app/models/ml/

# Update .env
# Set ENABLE_MOCK_MODELS=False
```

### Step 3: Restart Backend

```bash
# Local
uvicorn app.main:app --reload

# Docker
docker-compose restart backend

# Render - Push to GitHub (auto-deploys)
git push origin main
```

---

## 🧪 Part 6: Testing

### Run Unit Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_soc.py -v

# Run with output
pytest -v -s
```

### Load Testing

```bash
# Install locust
pip install locust

# Create locustfile.py (see below)
# Run load test
locust -f locustfile.py --host http://localhost:8000
```

**Example locustfile.py:**
```python
from locust import HttpUser, task, between

class BatteryUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def health_check(self):
        self.client.get("/health")

    @task
    def predict_soc(self):
        self.client.post(
            "/predict/soc?battery_id=BATT_001&voltage=3.8&current=25.0&temperature=25.0"
        )
```

---

## 📊 Part 7: Monitoring & Troubleshooting

### Check Logs

```bash
# Local development
UVICORN_LOG_LEVEL=DEBUG uvicorn app.main:app --reload

# Docker
docker-compose logs -f backend

# Render
# View in Render dashboard → Logs
```

### Database Debugging

```bash
# Connect to PostgreSQL
psql -h localhost -U battery_user -d battery_twin

# List tables
\dt

# Query batteries
SELECT * FROM batteries;

# View predictions
SELECT * FROM soc_predictions ORDER BY timestamp DESC LIMIT 10;
```

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'app'` | Run from project root: `cd AI-powered-DT-for-BMS` |
| `psycopg2.OperationalError: could not connect` | Check DATABASE_URL in .env, ensure PostgreSQL is running |
| `CORS error in browser` | Check CORS_ORIGINS in .env matches your frontend URL |
| `Models not loading` | Set `ENABLE_MOCK_MODELS=True` in .env to use mock predictions |
| `Port 8000 already in use` | `lsof -i :8000` then `kill -9 PID` or use different port |

---

## ✅ Verification Checklist

- [ ] Repository cloned
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file configured
- [ ] Database created and migrations applied
- [ ] Development server running on http://localhost:8000
- [ ] Health check endpoint returns 200
- [ ] Swagger docs accessible at `/docs`
- [ ] Can register user via `/auth/signup`
- [ ] Can predict SOC via `/predict/soc`
- [ ] Can predict SOH via `/predict/soh`
- [ ] Can get fleet overview via `/fleet/overview`

---

## 📝 Next Steps

1. **Add your trained ML models** to `app/models/ml/`
2. **Configure production database** (Neon PostgreSQL)
3. **Deploy to Render** for free cloud hosting
4. **Set up monitoring** with Sentry or DataDog (optional)
5. **Add frontend** (React/Vue) to consume API
6. **Configure CI/CD** with GitHub Actions

---

## 🎯 Production Checklist

- [ ] `DEBUG=False` in .env
- [ ] `SECRET_KEY` is strong and random
- [ ] Database backups configured
- [ ] Environment variables secure (use Render secrets)
- [ ] HTTPS/SSL enabled (Render handles this)
- [ ] Logging configured
- [ ] Database indexed
- [ ] Rate limiting configured
- [ ] CORS restricted to known origins

---

## 📞 Support & Resources

- **API Documentation**: http://localhost:8000/docs
- **Repository**: https://github.com/Armanx0/AI-powered-DT-for-BMS
- **Issues**: GitHub Issues tab
- **Neon Docs**: https://neon.tech/docs
- **Render Docs**: https://render.com/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com

---

**Status**: Ready for MVP Deployment 🚀
