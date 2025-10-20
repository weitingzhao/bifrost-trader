"""
Health monitoring API endpoints.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from ..models.service import ServiceHealth, ServiceStatus, HealthHistory, ServiceMetrics
from ..services.health_monitor import HealthMonitor
from ..utils.service_registry import ServiceRegistry


class HealthOverviewResponse(BaseModel):
    """Health overview response model."""
    total_services: int
    running_services: int
    stopped_services: int
    error_services: int
    last_updated: datetime
    services_by_category: Dict[str, int]


class ServiceHealthResponse(BaseModel):
    """Service health response model."""
    service_name: str
    health: ServiceHealth
    timestamp: datetime


class HealthHistoryResponse(BaseModel):
    """Health history response model."""
    service_name: str
    history: List[HealthHistory]
    total: int


class MetricsHistoryResponse(BaseModel):
    """Metrics history response model."""
    service_name: str
    metrics: List[ServiceMetrics]
    total: int


router = APIRouter()


def get_health_monitor() -> HealthMonitor:
    """Get health monitor instance."""
    service_registry = ServiceRegistry()
    return HealthMonitor(service_registry)


@router.get("/", response_model=HealthOverviewResponse)
async def get_health_overview():
    """Get overall system health overview."""
    health_monitor = get_health_monitor()
    
    overview = health_monitor.get_system_overview()
    
    return HealthOverviewResponse(
        total_services=overview["total_services"],
        running_services=overview["running_services"],
        stopped_services=overview["stopped_services"],
        error_services=overview["error_services"],
        last_updated=overview["last_updated"],
        services_by_category=overview["services_by_category"]
    )


@router.get("/services", response_model=Dict[str, ServiceHealth])
async def get_all_services_health():
    """Get health status of all services."""
    health_monitor = get_health_monitor()
    
    return health_monitor.get_all_health()


@router.get("/services/{service_name}", response_model=ServiceHealthResponse)
async def get_service_health(service_name: str):
    """Get health status of a specific service."""
    health_monitor = get_health_monitor()
    
    health = health_monitor.get_service_health(service_name)
    if not health:
        raise HTTPException(status_code=404, detail=f"Health data not found for service {service_name}")
    
    return ServiceHealthResponse(
        service_name=service_name,
        health=health,
        timestamp=datetime.now()
    )


@router.get("/services/{service_name}/history", response_model=HealthHistoryResponse)
async def get_service_health_history(
    service_name: str,
    hours: int = Query(24, description="Number of hours of history to retrieve")
):
    """Get health history for a specific service."""
    health_monitor = get_health_monitor()
    
    history = health_monitor.get_health_history(service_name, hours)
    
    return HealthHistoryResponse(
        service_name=service_name,
        history=history,
        total=len(history)
    )


@router.get("/services/{service_name}/metrics", response_model=MetricsHistoryResponse)
async def get_service_metrics_history(
    service_name: str,
    hours: int = Query(24, description="Number of hours of metrics to retrieve")
):
    """Get metrics history for a specific service."""
    health_monitor = get_health_monitor()
    
    metrics = health_monitor.get_metrics_history(service_name, hours)
    
    return MetricsHistoryResponse(
        service_name=service_name,
        metrics=metrics,
        total=len(metrics)
    )


@router.get("/history", response_model=List[HealthHistory])
async def get_all_health_history(
    hours: int = Query(24, description="Number of hours of history to retrieve"),
    service_name: Optional[str] = Query(None, description="Filter by service name")
):
    """Get health history for all services or a specific service."""
    health_monitor = get_health_monitor()
    
    history = health_monitor.get_health_history(service_name, hours)
    
    return history


@router.get("/metrics", response_model=List[ServiceMetrics])
async def get_all_metrics_history(
    hours: int = Query(24, description="Number of hours of metrics to retrieve"),
    service_name: Optional[str] = Query(None, description="Filter by service name")
):
    """Get metrics history for all services or a specific service."""
    health_monitor = get_health_monitor()
    
    metrics = health_monitor.get_metrics_history(service_name, hours)
    
    return metrics


@router.get("/status/summary")
async def get_health_status_summary():
    """Get a summary of health status across all services."""
    health_monitor = get_health_monitor()
    
    all_health = health_monitor.get_all_health()
    
    summary = {
        "total": len(all_health),
        "healthy": 0,
        "unhealthy": 0,
        "unknown": 0,
        "services": {}
    }
    
    for service_name, health in all_health.items():
        if health.status == ServiceStatus.RUNNING:
            summary["healthy"] += 1
        elif health.status == ServiceStatus.ERROR:
            summary["unhealthy"] += 1
        else:
            summary["unknown"] += 1
        
        summary["services"][service_name] = {
            "status": health.status.value,
            "response_time": health.response_time,
            "last_check": health.last_check.isoformat(),
            "error_message": health.error_message
        }
    
    return summary


@router.get("/alerts")
async def get_health_alerts():
    """Get current health alerts for services with issues."""
    health_monitor = get_health_monitor()
    
    all_health = health_monitor.get_all_health()
    alerts = []
    
    for service_name, health in all_health.items():
        if health.status == ServiceStatus.ERROR:
            alerts.append({
                "service_name": service_name,
                "severity": "error",
                "message": health.error_message or "Service is in error state",
                "timestamp": health.last_check.isoformat(),
                "response_time": health.response_time
            })
        elif health.status == ServiceStatus.STOPPED:
            alerts.append({
                "service_name": service_name,
                "severity": "warning",
                "message": "Service is stopped",
                "timestamp": health.last_check.isoformat(),
                "response_time": health.response_time
            })
        elif health.response_time and health.response_time > 5.0:
            alerts.append({
                "service_name": service_name,
                "severity": "warning",
                "message": f"High response time: {health.response_time:.2f}s",
                "timestamp": health.last_check.isoformat(),
                "response_time": health.response_time
            })
    
    return {
        "alerts": alerts,
        "total": len(alerts),
        "timestamp": datetime.now().isoformat()
    }


@router.post("/monitoring/start")
async def start_health_monitoring():
    """Start health monitoring."""
    health_monitor = get_health_monitor()
    
    await health_monitor.start_monitoring()
    
    return {
        "message": "Health monitoring started",
        "timestamp": datetime.now().isoformat()
    }


@router.post("/monitoring/stop")
async def stop_health_monitoring():
    """Stop health monitoring."""
    health_monitor = get_health_monitor()
    
    await health_monitor.stop_monitoring()
    
    return {
        "message": "Health monitoring stopped",
        "timestamp": datetime.now().isoformat()
    }
