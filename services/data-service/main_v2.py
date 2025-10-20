"""
Market Data Service for Bifrost Trader - Version 2.0

This is the refactored version using SQLAlchemy, async operations,
and the repository pattern with FastAPI best practices.
"""

import logging
import os
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import API routers
from src.api.endpoints import historical, market_data, symbols
from src.database.connection import close_database, init_database

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    logger.info("Starting Market Data Service v2.0...")
    
    # Initialize database
    try:
        await init_database()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise
    
    yield
    
    # Cleanup
    logger.info("Shutting down Market Data Service...")
    await close_database()


# Create FastAPI app
app = FastAPI(
    title="Bifrost Trader - Market Data Service",
    version="2.0.0",
    description="Market data ingestion, storage, and retrieval service with TimescaleDB",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request, call_next):
    """Add processing time header to responses."""
    start_time = datetime.now()
    response = await call_next(request)
    process_time = (datetime.now() - start_time).total_seconds()
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Health check endpoints
@app.get("/health", tags=["health"])
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        Health status of the service
    """
    return {
        "status": "healthy",
        "service": "market-data-service",
        "version": "2.0.0",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/ready", tags=["health"])
async def readiness_check():
    """
    Readiness check endpoint.
    
    Returns:
        Readiness status of the service
    """
    from src.database.connection import db_manager
    
    # Test database connection
    is_ready = await db_manager.test_connection()
    
    return {
        "status": "ready" if is_ready else "not ready",
        "service": "market-data-service",
        "database": "connected" if is_ready else "disconnected"
    }


@app.get("/metrics", tags=["monitoring"])
async def metrics():
    """
    Metrics endpoint for monitoring.
    
    Returns:
        Service metrics
    """
    from src.database.connection import db_manager
    
    return {
        "service": "market-data-service",
        "version": "2.0.0",
        "timestamp": datetime.now().isoformat(),
        "database": {
            "type": "PostgreSQL with TimescaleDB",
            "connection_pool": {
                "size": db_manager.config.pool_size,
                "max_overflow": db_manager.config.max_overflow
            }
        }
    }


# Include API routers
app.include_router(
    symbols.router,
    prefix="/api",
    tags=["symbols"]
)

app.include_router(
    market_data.router,
    prefix="/api",
    tags=["market-data"]
)

app.include_router(
    historical.router,
    prefix="/api",
    tags=["historical"]
)


@app.get("/", tags=["root"])
async def root():
    """
    Root endpoint with service information.
    
    Returns:
        Service information and available endpoints
    """
    return {
        "service": "Bifrost Trader - Market Data Service",
        "version": "2.0.0",
        "description": "Market data ingestion, storage, and retrieval service",
        "documentation": "/docs",
        "health": "/health",
        "ready": "/ready",
        "metrics": "/metrics",
        "api": {
            "symbols": "/api/symbols",
            "market_data": "/api/market-data",
            "historical": "/api/historical"
        }
    }


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", "8001"))
    host = os.getenv("HOST", "0.0.0.0")
    reload = os.getenv("RELOAD", "true").lower() == "true"
    
    logger.info(f"Starting server on {host}:{port}")
    
    uvicorn.run(
        "main_v2:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info",
        access_log=True
    )





