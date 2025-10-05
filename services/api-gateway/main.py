"""
API Gateway for Bifrost Trader.
Central entry point for all service requests.
"""

from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import httpx
import os
import logging
from datetime import datetime
from typing import Dict, Any, Optional
import asyncio
from contextlib import asynccontextmanager

from shared.utils import ServiceRegistry, HealthChecker, setup_logging, load_environment
from shared.models import APIResponse, ServiceStatus


# Load environment variables
load_environment()

# Setup logging
logger = setup_logging("api-gateway")

# Service registry
service_registry = ServiceRegistry()

# Health checker
health_checker = HealthChecker("api-gateway")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    logger.info("Starting API Gateway...")
    yield
    logger.info("Shutting down API Gateway...")


# Create FastAPI app
app = FastAPI(
    title="Bifrost Trader API Gateway",
    version="1.0.0",
    description="Central API Gateway for Bifrost Trader microservices",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Trusted host middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # Configure appropriately for production
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time header to responses."""
    start_time = datetime.now()
    response = await call_next(request)
    process_time = (datetime.now() - start_time).total_seconds()
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests."""
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response


async def proxy_request(service_name: str, path: str, method: str = "GET", data: Optional[Dict] = None) -> Dict[str, Any]:
    """Proxy request to appropriate service."""
    service_url = service_registry.get_service_url(service_name)
    if not service_url:
        raise HTTPException(status_code=404, detail=f"Service {service_name} not found")
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            url = f"{service_url}{path}"
            
            if method.upper() == "GET":
                response = await client.get(url)
            elif method.upper() == "POST":
                response = await client.post(url, json=data)
            elif method.upper() == "PUT":
                response = await client.put(url, json=data)
            elif method.upper() == "DELETE":
                response = await client.delete(url)
            else:
                raise HTTPException(status_code=405, detail="Method not allowed")
            
            response.raise_for_status()
            return response.json()
    
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Service timeout")
    except httpx.HTTPError as e:
        logger.error(f"Service error: {e}")
        raise HTTPException(status_code=502, detail="Service error")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# Health check endpoints
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return health_checker.get_health_status()


@app.get("/ready")
async def readiness_check():
    """Readiness check endpoint."""
    return {"status": "ready", "service": "api-gateway"}


@app.get("/metrics")
async def metrics():
    """Metrics endpoint."""
    return {
        "service": "api-gateway",
        "uptime": health_checker.get_uptime(),
        "timestamp": datetime.now().isoformat(),
        "services": list(service_registry.services.keys())
    }


# Service status endpoint
@app.get("/services/status")
async def get_services_status():
    """Get status of all services."""
    services_status = []
    
    for service_name, service_url in service_registry.services.items():
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{service_url}/health")
                if response.status_code == 200:
                    services_status.append({
                        "service": service_name,
                        "status": "healthy",
                        "url": service_url,
                        "response_time": response.elapsed.total_seconds()
                    })
                else:
                    services_status.append({
                        "service": service_name,
                        "status": "unhealthy",
                        "url": service_url,
                        "error": f"HTTP {response.status_code}"
                    })
        except Exception as e:
            services_status.append({
                "service": service_name,
                "status": "unreachable",
                "url": service_url,
                "error": str(e)
            })
    
    return {
        "services": services_status,
        "timestamp": datetime.now().isoformat()
    }


# Data Service Routes
@app.get("/api/data/{path:path}")
async def proxy_data_service(path: str, request: Request):
    """Proxy requests to data service."""
    query_params = dict(request.query_params)
    return await proxy_request("data-service", f"/{path}", "GET")


@app.post("/api/data/{path:path}")
async def proxy_data_service_post(path: str, data: Dict[str, Any]):
    """Proxy POST requests to data service."""
    return await proxy_request("data-service", f"/{path}", "POST", data)


# Portfolio Service Routes
@app.get("/api/portfolio/{path:path}")
async def proxy_portfolio_service(path: str, request: Request):
    """Proxy requests to portfolio service."""
    query_params = dict(request.query_params)
    return await proxy_request("portfolio-service", f"/{path}", "GET")


@app.post("/api/portfolio/{path:path}")
async def proxy_portfolio_service_post(path: str, data: Dict[str, Any]):
    """Proxy POST requests to portfolio service."""
    return await proxy_request("portfolio-service", f"/{path}", "POST", data)


@app.put("/api/portfolio/{path:path}")
async def proxy_portfolio_service_put(path: str, data: Dict[str, Any]):
    """Proxy PUT requests to portfolio service."""
    return await proxy_request("portfolio-service", f"/{path}", "PUT", data)


@app.delete("/api/portfolio/{path:path}")
async def proxy_portfolio_service_delete(path: str):
    """Proxy DELETE requests to portfolio service."""
    return await proxy_request("portfolio-service", f"/{path}", "DELETE")


# Strategy Service Routes
@app.get("/api/strategy/{path:path}")
async def proxy_strategy_service(path: str, request: Request):
    """Proxy requests to strategy service."""
    return await proxy_request("strategy-service", f"/{path}", "GET")


@app.post("/api/strategy/{path:path}")
async def proxy_strategy_service_post(path: str, data: Dict[str, Any]):
    """Proxy POST requests to strategy service."""
    return await proxy_request("strategy-service", f"/{path}", "POST", data)


@app.put("/api/strategy/{path:path}")
async def proxy_strategy_service_put(path: str, data: Dict[str, Any]):
    """Proxy PUT requests to strategy service."""
    return await proxy_request("strategy-service", f"/{path}", "PUT", data)


@app.delete("/api/strategy/{path:path}")
async def proxy_strategy_service_delete(path: str):
    """Proxy DELETE requests to strategy service."""
    return await proxy_request("strategy-service", f"/{path}", "DELETE")


# Risk Service Routes
@app.get("/api/risk/{path:path}")
async def proxy_risk_service(path: str, request: Request):
    """Proxy requests to risk service."""
    return await proxy_request("risk-service", f"/{path}", "GET")


@app.post("/api/risk/{path:path}")
async def proxy_risk_service_post(path: str, data: Dict[str, Any]):
    """Proxy POST requests to risk service."""
    return await proxy_request("risk-service", f"/{path}", "POST", data)


# ML Service Routes
@app.get("/api/ml/{path:path}")
async def proxy_ml_service(path: str, request: Request):
    """Proxy requests to ML service."""
    return await proxy_request("ml-service", f"/{path}", "GET")


@app.post("/api/ml/{path:path}")
async def proxy_ml_service_post(path: str, data: Dict[str, Any]):
    """Proxy POST requests to ML service."""
    return await proxy_request("ml-service", f"/{path}", "POST", data)


# Analytics Service Routes
@app.get("/api/analytics/{path:path}")
async def proxy_analytics_service(path: str, request: Request):
    """Proxy requests to analytics service."""
    return await proxy_request("analytics-service", f"/{path}", "GET")


@app.post("/api/analytics/{path:path}")
async def proxy_analytics_service_post(path: str, data: Dict[str, Any]):
    """Proxy POST requests to analytics service."""
    return await proxy_request("analytics-service", f"/{path}", "POST", data)


# Compliance Service Routes
@app.get("/api/compliance/{path:path}")
async def proxy_compliance_service(path: str, request: Request):
    """Proxy requests to compliance service."""
    return await proxy_request("compliance-service", f"/{path}", "GET")


@app.post("/api/compliance/{path:path}")
async def proxy_compliance_service_post(path: str, data: Dict[str, Any]):
    """Proxy POST requests to compliance service."""
    return await proxy_request("compliance-service", f"/{path}", "POST", data)


# News Service Routes
@app.get("/api/news/{path:path}")
async def proxy_news_service(path: str, request: Request):
    """Proxy requests to news service."""
    return await proxy_request("news-service", f"/{path}", "GET")


@app.post("/api/news/{path:path}")
async def proxy_news_service_post(path: str, data: Dict[str, Any]):
    """Proxy POST requests to news service."""
    return await proxy_request("news-service", f"/{path}", "POST", data)


# Microstructure Service Routes
@app.get("/api/microstructure/{path:path}")
async def proxy_microstructure_service(path: str, request: Request):
    """Proxy requests to microstructure service."""
    return await proxy_request("microstructure-service", f"/{path}", "GET")


@app.post("/api/microstructure/{path:path}")
async def proxy_microstructure_service_post(path: str, data: Dict[str, Any]):
    """Proxy POST requests to microstructure service."""
    return await proxy_request("microstructure-service", f"/{path}", "POST", data)


# Web Portal Routes
@app.get("/api/web/{path:path}")
async def proxy_web_portal(path: str, request: Request):
    """Proxy requests to web portal."""
    return await proxy_request("web-portal", f"/{path}", "GET")


@app.post("/api/web/{path:path}")
async def proxy_web_portal_post(path: str, data: Dict[str, Any]):
    """Proxy POST requests to web portal."""
    return await proxy_request("web-portal", f"/{path}", "POST", data)


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail,
            "timestamp": datetime.now().isoformat(),
            "path": str(request.url)
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "timestamp": datetime.now().isoformat(),
            "path": str(request.url)
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )
