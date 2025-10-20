"""
Health monitoring service for real-time service status tracking.
"""

import asyncio
import json
import psutil
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set

import httpx
from websockets import WebSocketServerProtocol

from ..models.service import ServiceHealth, ServiceStatus, ServiceMetrics, HealthHistory
from ..utils.service_registry import ServiceRegistry


class HealthMonitor:
    """Health monitoring service for tracking service status."""
    
    def __init__(self, service_registry: ServiceRegistry):
        """Initialize health monitor."""
        self.service_registry = service_registry
        self.health_data: Dict[str, ServiceHealth] = {}
        self.metrics_history: List[ServiceMetrics] = []
        self.health_history: List[HealthHistory] = []
        self.websocket_clients: Set[WebSocketServerProtocol] = set()
        self.monitoring = False
        self.monitor_task: Optional[asyncio.Task] = None
        
    async def start_monitoring(self):
        """Start health monitoring."""
        if not self.monitoring:
            self.monitoring = True
            self.monitor_task = asyncio.create_task(self._monitor_loop())
            print("🔍 Health monitoring started")
    
    async def stop_monitoring(self):
        """Stop health monitoring."""
        self.monitoring = False
        if self.monitor_task:
            self.monitor_task.cancel()
            try:
                await self.monitor_task
            except asyncio.CancelledError:
                pass
        print("🛑 Health monitoring stopped")
    
    async def _monitor_loop(self):
        """Main monitoring loop."""
        while self.monitoring:
            try:
                await self._check_all_services()
                await self._broadcast_updates()
                await asyncio.sleep(30)  # Check every 30 seconds
            except Exception as e:
                print(f"Error in monitoring loop: {e}")
                await asyncio.sleep(5)
    
    async def _check_all_services(self):
        """Check health of all services."""
        tasks = []
        for service in self.service_registry.get_all_services():
            task = asyncio.create_task(self._check_service_health(service.name))
            tasks.append(task)
        
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _check_service_health(self, service_name: str):
        """Check health of a specific service."""
        service = self.service_registry.get_service(service_name)
        if not service:
            return
        
        health_endpoint = self.service_registry.get_health_endpoint(service_name)
        if not health_endpoint:
            return
        
        start_time = datetime.now()
        
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(health_endpoint)
                response_time = (datetime.now() - start_time).total_seconds()
                
                if response.status_code == 200:
                    health_data = response.json()
                    status = ServiceStatus.RUNNING
                    error_message = None
                    uptime = health_data.get('uptime')
                else:
                    status = ServiceStatus.ERROR
                    error_message = f"HTTP {response.status_code}"
                    uptime = None
                    response_time = None
                    
        except httpx.TimeoutException:
            status = ServiceStatus.ERROR
            error_message = "Request timeout"
            response_time = None
            uptime = None
            
        except Exception as e:
            status = ServiceStatus.ERROR
            error_message = str(e)
            response_time = None
            uptime = None
        
        # Get system metrics
        try:
            process = psutil.Process()
            memory_usage = process.memory_info().rss / 1024 / 1024  # MB
            cpu_usage = process.cpu_percent()
        except:
            memory_usage = None
            cpu_usage = None
        
        # Create health record
        health = ServiceHealth(
            status=status,
            response_time=response_time,
            last_check=datetime.now(),
            error_message=error_message,
            uptime=uptime,
            memory_usage=memory_usage,
            cpu_usage=cpu_usage
        )
        
        self.health_data[service_name] = health
        
        # Store metrics
        if response_time is not None:
            metrics = ServiceMetrics(
                service_name=service_name,
                timestamp=datetime.now(),
                response_time=response_time,
                memory_usage=memory_usage or 0,
                cpu_usage=cpu_usage or 0
            )
            self.metrics_history.append(metrics)
            
            # Keep only last 1000 metrics
            if len(self.metrics_history) > 1000:
                self.metrics_history = self.metrics_history[-1000:]
        
        # Store health history
        history = HealthHistory(
            service_name=service_name,
            timestamp=datetime.now(),
            status=status,
            response_time=response_time,
            error_message=error_message
        )
        self.health_history.append(history)
        
        # Keep only last 24 hours of history
        cutoff_time = datetime.now() - timedelta(hours=24)
        self.health_history = [
            h for h in self.health_history 
            if h.timestamp > cutoff_time
        ]
    
    async def _broadcast_updates(self):
        """Broadcast updates to WebSocket clients."""
        if not self.websocket_clients:
            return
        
        update_data = {
            "type": "health_update",
            "timestamp": datetime.now().isoformat(),
            "services": {}
        }
        
        for service_name, health in self.health_data.items():
            update_data["services"][service_name] = {
                "status": health.status,
                "response_time": health.response_time,
                "last_check": health.last_check.isoformat(),
                "error_message": health.error_message,
                "uptime": health.uptime,
                "memory_usage": health.memory_usage,
                "cpu_usage": health.cpu_usage
            }
        
        message = json.dumps(update_data)
        
        # Send to all connected clients
        disconnected = set()
        for client in self.websocket_clients:
            try:
                await client.send(message)
            except:
                disconnected.add(client)
        
        # Remove disconnected clients
        self.websocket_clients -= disconnected
    
    def add_websocket_client(self, client: WebSocketServerProtocol):
        """Add WebSocket client for real-time updates."""
        self.websocket_clients.add(client)
    
    def remove_websocket_client(self, client: WebSocketServerProtocol):
        """Remove WebSocket client."""
        self.websocket_clients.discard(client)
    
    def get_service_health(self, service_name: str) -> Optional[ServiceHealth]:
        """Get health status of a specific service."""
        return self.health_data.get(service_name)
    
    def get_all_health(self) -> Dict[str, ServiceHealth]:
        """Get health status of all services."""
        return self.health_data.copy()
    
    def get_health_history(self, service_name: Optional[str] = None, hours: int = 24) -> List[HealthHistory]:
        """Get health history for a service or all services."""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        history = [
            h for h in self.health_history 
            if h.timestamp > cutoff_time
        ]
        
        if service_name:
            history = [h for h in history if h.service_name == service_name]
        
        return sorted(history, key=lambda x: x.timestamp)
    
    def get_metrics_history(self, service_name: Optional[str] = None, hours: int = 24) -> List[ServiceMetrics]:
        """Get metrics history for a service or all services."""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        metrics = [
            m for m in self.metrics_history 
            if m.timestamp > cutoff_time
        ]
        
        if service_name:
            metrics = [m for m in metrics if m.service_name == service_name]
        
        return sorted(metrics, key=lambda x: x.timestamp)
    
    def get_system_overview(self) -> Dict:
        """Get system overview statistics."""
        total_services = len(self.service_registry.get_all_services())
        running_services = sum(
            1 for health in self.health_data.values() 
            if health.status == ServiceStatus.RUNNING
        )
        stopped_services = sum(
            1 for health in self.health_data.values() 
            if health.status == ServiceStatus.STOPPED
        )
        error_services = sum(
            1 for health in self.health_data.values() 
            if health.status == ServiceStatus.ERROR
        )
        
        # Services by category
        services_by_category = {}
        for service in self.service_registry.get_all_services():
            category = service.category.value
            services_by_category[category] = services_by_category.get(category, 0) + 1
        
        return {
            "total_services": total_services,
            "running_services": running_services,
            "stopped_services": stopped_services,
            "error_services": error_services,
            "last_updated": datetime.now(),
            "services_by_category": services_by_category
        }
