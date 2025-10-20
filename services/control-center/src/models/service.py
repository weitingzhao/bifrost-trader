"""
Service data models for the Control Center.
"""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class ServiceStatus(str, Enum):
    """Service status enumeration."""
    RUNNING = "running"
    STOPPED = "stopped"
    ERROR = "error"
    STARTING = "starting"
    STOPPING = "stopping"
    UNKNOWN = "unknown"


class ServiceCategory(str, Enum):
    """Service category enumeration."""
    CORE = "core"
    TRADING = "trading"
    ANALYTICS = "analytics"
    SUPPORTING = "supporting"
    UI = "ui"
    MANAGEMENT = "management"


class ServiceHealth(BaseModel):
    """Service health status model."""
    status: ServiceStatus
    response_time: Optional[float] = None
    last_check: datetime
    error_message: Optional[str] = None
    uptime: Optional[float] = None
    memory_usage: Optional[float] = None
    cpu_usage: Optional[float] = None


class ServiceInfo(BaseModel):
    """Service information model."""
    name: str
    port: int
    category: ServiceCategory
    description: str
    has_ui: bool
    management: str
    health_endpoint: str
    docs_endpoint: str
    url: str
    health: Optional[ServiceHealth] = None


class ServiceMetrics(BaseModel):
    """Service metrics model."""
    service_name: str
    timestamp: datetime
    response_time: float
    memory_usage: float
    cpu_usage: float
    request_count: int = 0
    error_count: int = 0


class ServiceLog(BaseModel):
    """Service log entry model."""
    service_name: str
    timestamp: datetime
    level: str
    message: str
    source: str = "service"


class ServiceAction(BaseModel):
    """Service action request model."""
    action: str  # start, stop, restart
    service_name: str
    timestamp: datetime = Field(default_factory=datetime.now)


class ServiceActionResponse(BaseModel):
    """Service action response model."""
    success: bool
    message: str
    service_name: str
    timestamp: datetime = Field(default_factory=datetime.now)


class SystemOverview(BaseModel):
    """System overview model."""
    total_services: int
    running_services: int
    stopped_services: int
    error_services: int
    last_updated: datetime
    services_by_category: Dict[str, int]


class HealthHistory(BaseModel):
    """Health history model."""
    service_name: str
    timestamp: datetime
    status: ServiceStatus
    response_time: Optional[float] = None
    error_message: Optional[str] = None
