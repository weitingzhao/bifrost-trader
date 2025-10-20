"""
Service management API endpoints.
"""

from datetime import datetime
from typing import Dict, List, Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from ..models.service import ServiceAction, ServiceActionResponse, ServiceLog, ServiceStatus
from ..services.service_manager import ServiceManager
from ..utils.service_registry import ServiceRegistry


class ServiceListResponse(BaseModel):
    """Service list response model."""
    services: List[Dict]
    total: int
    running: int
    stopped: int
    errors: int


class ServiceDetailResponse(BaseModel):
    """Service detail response model."""
    service: Dict
    status: ServiceStatus
    health: Optional[Dict] = None
    metrics: Optional[Dict] = None
    logs: List[ServiceLog] = []


router = APIRouter()


def get_service_manager() -> ServiceManager:
    """Get service manager instance."""
    # This would be injected via dependency injection in a real app
    service_registry = ServiceRegistry()
    return ServiceManager(service_registry)


def get_service_registry() -> ServiceRegistry:
    """Get service registry instance."""
    return ServiceRegistry()


@router.get("/", response_model=ServiceListResponse)
async def list_services(
    category: Optional[str] = Query(None, description="Filter by service category"),
    status: Optional[ServiceStatus] = Query(None, description="Filter by service status")
):
    """List all services with optional filtering."""
    service_registry = get_service_registry()
    service_manager = get_service_manager()
    
    services = service_registry.get_all_services()
    
    # Filter by category if specified
    if category:
        from ..models.service import ServiceCategory
        try:
            category_enum = ServiceCategory(category)
            services = [s for s in services if s.category == category_enum]
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid category: {category}")
    
    # Get service statuses
    service_statuses = service_manager.get_all_service_status()
    
    # Build response
    service_list = []
    running_count = 0
    stopped_count = 0
    error_count = 0
    
    for service in services:
        service_status = service_statuses.get(service.name, ServiceStatus.UNKNOWN)
        
        # Filter by status if specified
        if status and service_status != status:
            continue
        
        service_info = {
            "name": service.name,
            "port": service.port,
            "category": service.category.value,
            "description": service.description,
            "has_ui": service.has_ui,
            "url": service.url,
            "status": service_status.value,
            "docs_url": f"{service.url}{service.docs_endpoint}",
            "health_url": f"{service.url}{service.health_endpoint}"
        }
        
        service_list.append(service_info)
        
        # Count statuses
        if service_status == ServiceStatus.RUNNING:
            running_count += 1
        elif service_status == ServiceStatus.STOPPED:
            stopped_count += 1
        elif service_status == ServiceStatus.ERROR:
            error_count += 1
    
    return ServiceListResponse(
        services=service_list,
        total=len(service_list),
        running=running_count,
        stopped=stopped_count,
        errors=error_count
    )


@router.get("/{service_name}", response_model=ServiceDetailResponse)
async def get_service_detail(service_name: str):
    """Get detailed information about a specific service."""
    service_registry = get_service_registry()
    service_manager = get_service_manager()
    
    service = service_registry.get_service(service_name)
    if not service:
        raise HTTPException(status_code=404, detail=f"Service {service_name} not found")
    
    # Get service status
    status = service_manager.get_service_status(service_name)
    
    # Get service metrics
    metrics = service_manager.get_service_metrics(service_name)
    
    # Get recent logs
    logs = service_manager.get_service_logs(service_name, lines=50)
    
    # Build service info
    service_info = {
        "name": service.name,
        "port": service.port,
        "category": service.category.value,
        "description": service.description,
        "has_ui": service.has_ui,
        "management": service.management,
        "url": service.url,
        "docs_url": f"{service.url}{service.docs_endpoint}",
        "health_url": f"{service.url}{service.health_endpoint}"
    }
    
    return ServiceDetailResponse(
        service=service_info,
        status=status,
        metrics=metrics,
        logs=logs
    )


@router.post("/{service_name}/start", response_model=ServiceActionResponse)
async def start_service(service_name: str):
    """Start a service."""
    service_manager = get_service_manager()
    
    result = await service_manager.start_service(service_name)
    
    if not result.success:
        raise HTTPException(status_code=400, detail=result.message)
    
    return result


@router.post("/{service_name}/stop", response_model=ServiceActionResponse)
async def stop_service(service_name: str):
    """Stop a service."""
    service_manager = get_service_manager()
    
    result = await service_manager.stop_service(service_name)
    
    if not result.success:
        raise HTTPException(status_code=400, detail=result.message)
    
    return result


@router.post("/{service_name}/restart", response_model=ServiceActionResponse)
async def restart_service(service_name: str):
    """Restart a service."""
    service_manager = get_service_manager()
    
    result = await service_manager.restart_service(service_name)
    
    if not result.success:
        raise HTTPException(status_code=400, detail=result.message)
    
    return result


@router.get("/{service_name}/logs")
async def get_service_logs(
    service_name: str,
    lines: int = Query(100, description="Number of log lines to return")
):
    """Get service logs."""
    service_manager = get_service_manager()
    
    logs = service_manager.get_service_logs(service_name, lines)
    
    return {
        "service_name": service_name,
        "logs": [log.dict() for log in logs],
        "total": len(logs)
    }


@router.get("/{service_name}/metrics")
async def get_service_metrics(service_name: str):
    """Get service metrics."""
    service_manager = get_service_manager()
    
    metrics = service_manager.get_service_metrics(service_name)
    
    if not metrics:
        raise HTTPException(status_code=404, detail=f"No metrics available for service {service_name}")
    
    return {
        "service_name": service_name,
        "metrics": metrics,
        "timestamp": datetime.now().isoformat()
    }


@router.get("/{service_name}/status")
async def get_service_status(service_name: str):
    """Get service status."""
    service_manager = get_service_manager()
    
    status = service_manager.get_service_status(service_name)
    
    return {
        "service_name": service_name,
        "status": status.value,
        "timestamp": datetime.now().isoformat()
    }


@router.get("/categories/list")
async def list_categories():
    """List all service categories."""
    service_registry = get_service_registry()
    categories = service_registry.get_all_categories()
    
    return {
        "categories": categories,
        "total": len(categories)
    }


@router.get("/categories/{category}/services")
async def get_services_by_category(category: str):
    """Get services by category."""
    from ..models.service import ServiceCategory
    
    try:
        category_enum = ServiceCategory(category)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid category: {category}")
    
    service_registry = get_service_registry()
    services = service_registry.get_services_by_category(category_enum)
    
    service_list = []
    for service in services:
        service_info = {
            "name": service.name,
            "port": service.port,
            "description": service.description,
            "has_ui": service.has_ui,
            "url": service.url
        }
        service_list.append(service_info)
    
    return {
        "category": category,
        "services": service_list,
        "total": len(service_list)
    }
