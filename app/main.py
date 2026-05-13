"""Battery Digital Twin MVP - Main FastAPI Application"""

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.config import get_settings
from app.database import engine
from app.models.db import Base
from app.utils.logger import setup_logging

# Setup logging
logger = setup_logging()
settings = get_settings()

# Create database tables
Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown events"""
    # Startup
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug: {settings.DEBUG}")
    yield
    # Shutdown
    logger.info(f"Shutting down {settings.APP_NAME}")


# ============================================
# FastAPI Application Instance
# ============================================
app = FastAPI(
    title=settings.APP_NAME,
    description="Intelligent Battery Digital Twin MVP - Real-time battery state estimation and predictive maintenance",
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

# ============================================
# CORS Middleware
# ============================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)


# ============================================
# Health Check Endpoint
# ============================================
@app.get("/health", tags=["System"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
    }


@app.get("/", tags=["System"])
async def root():
    """Root endpoint with API information"""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": "Battery Digital Twin MVP",
        "docs_url": "/docs",
        "openapi_url": "/openapi.json",
    }


# ============================================
# Include Routers
# ============================================
# Auth routes
from app.routes import auth
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# Data upload routes
from app.routes import upload
app.include_router(upload.router, prefix="/upload", tags=["Data Management"])

# Prediction routes
from app.routes import soc, soh, forecast, anomaly
app.include_router(soc.router, prefix="/predict", tags=["Predictions"])
app.include_router(soh.router, prefix="/predict", tags=["Predictions"])
app.include_router(forecast.router, prefix="", tags=["Forecasting"])
app.include_router(anomaly.router, prefix="", tags=["Anomaly Detection"])

# Digital twin routes
from app.routes import digital_twin
app.include_router(digital_twin.router, prefix="/battery", tags=["Digital Twin"])

# Dashboard routes
from app.routes import dashboard
app.include_router(dashboard.router, prefix="/fleet", tags=["Dashboard"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.API_HOST,
        port=settings.API_PORT,
        log_level=settings.LOG_LEVEL.lower(),
    )
