"""
Bifrost Trader Service Control Center

A centralized management interface for all Bifrost Trader microservices.
Provides service management, health monitoring, and unified API access.
"""

import asyncio
import json
import os
from contextlib import asynccontextmanager
from typing import Dict, List

from fastapi import Depends, FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.api import health, proxy, services, service_endpoints
from src.services.health_monitor import HealthMonitor
from src.services.service_manager import ServiceManager
from src.utils.service_registry import ServiceRegistry

# Service instances
service_registry = ServiceRegistry()
service_manager = ServiceManager(service_registry)
health_monitor = HealthMonitor(service_registry)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Start health monitoring
    await health_monitor.start_monitoring()
    print("🚀 Service Control Center Started")
    print("📊 Health monitoring active")
    print("🔧 Service management ready")
    
    yield
    
    # Cleanup
    await health_monitor.stop_monitoring()
    print("🛑 Service Control Center Stopped")


# Create FastAPI app
app = FastAPI(
    title="Bifrost Trader Service Control Center",
    version="1.0.0",
    description="Centralized management interface for all Bifrost Trader microservices",
    lifespan=lifespan,
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(services.router, prefix="/api/services", tags=["services"])
app.include_router(health.router, prefix="/api/health", tags=["health"])
app.include_router(proxy.router, prefix="/api/proxy", tags=["proxy"])
app.include_router(service_endpoints.router, tags=["service-pages"])


# WebSocket endpoint for real-time updates
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates."""
    await websocket.accept()
    
    # Add client to health monitor
    health_monitor.add_websocket_client(websocket)
    
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        health_monitor.remove_websocket_client(websocket)


# Template routes
@app.get("/", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    """Main control center dashboard."""
    try:
        # Get system overview
        overview = health_monitor.get_system_overview()
        
        # Get all services
        all_services = service_registry.get_all_services()
        service_statuses = service_manager.get_all_service_status()
        
        # Prepare service data
        services_data = []
        for service in all_services:
            status = service_statuses.get(service.name, "unknown")
            services_data.append({
                "name": service.name,
                "port": service.port,
                "category": service.category.value,
                "description": service.description,
                "has_ui": service.has_ui,
                "url": service.url,
                "status": status,
                "docs_url": f"{service.url}{service.docs_endpoint}",
                "health_url": f"{service.url}{service.health_endpoint}"
            })
        
        return templates.TemplateResponse(
            "pages/dashboard.html",
            {
                "request": request,
                "overview": overview,
                "services": services_data,
                "categories": service_registry.get_all_categories()
            }
        )
    except Exception as e:
        return HTMLResponse(f"<h1>Error loading dashboard</h1><p>{str(e)}</p>", status_code=500)


@app.get("/service/{service_name}", response_class=HTMLResponse)
async def service_detail_page(request: Request, service_name: str):
    """Service detail page."""
    try:
        service = service_registry.get_service(service_name)
        if not service:
            return HTMLResponse(f"<h1>Service {service_name} not found</h1>", status_code=404)
        
        # Get service status and metrics
        status = service_manager.get_service_status(service_name)
        metrics = service_manager.get_service_metrics(service_name)
        logs = service_manager.get_service_logs(service_name, lines=100)
        
        # Get health data
        health_data = health_monitor.get_service_health(service_name)
        
        return templates.TemplateResponse(
            "pages/service-detail.html",
            {
                "request": request,
                "service": service,
                "status": status,
                "metrics": metrics,
                "health": health_data,
                "logs": logs
            }
        )
    except Exception as e:
        return HTMLResponse(f"<h1>Error loading service details</h1><p>{str(e)}</p>", status_code=500)


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "control-center",
        "version": "1.0.0",
        "timestamp": "2024-01-01T00:00:00Z"
    }


# System status endpoint
@app.get("/status")
async def system_status():
    """Get overall system status."""
    overview = health_monitor.get_system_overview()
    all_health = health_monitor.get_all_health()
    
    return {
        "overview": overview,
        "services_health": all_health,
        "timestamp": "2024-01-01T00:00:00Z"
    }


# Service management endpoints
@app.post("/api/services/{service_name}/start")
async def start_service_api(service_name: str):
    """Start a service via API."""
    result = await service_manager.start_service(service_name)
    return result


@app.post("/api/services/{service_name}/stop")
async def stop_service_api(service_name: str):
    """Stop a service via API."""
    result = await service_manager.stop_service(service_name)
    return result


@app.post("/api/services/{service_name}/restart")
async def restart_service_api(service_name: str):
    """Restart a service via API."""
    result = await service_manager.restart_service(service_name)
    return result


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8007))
    host = os.getenv("HOST", "0.0.0.0")
    
    uvicorn.run("main:app", host=host, port=port, reload=True, log_level="info")
