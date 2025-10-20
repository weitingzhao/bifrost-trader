"""
Service management for starting, stopping, and monitoring services.
"""

import asyncio
import os
import subprocess
import sys
from datetime import datetime
from typing import Dict, List, Optional, Tuple

import psutil

from ..models.service import ServiceAction, ServiceActionResponse, ServiceLog, ServiceStatus
from ..utils.service_registry import ServiceRegistry


class ServiceManager:
    """Service manager for controlling service lifecycle."""
    
    def __init__(self, service_registry: ServiceRegistry):
        """Initialize service manager."""
        self.service_registry = service_registry
        self.running_processes: Dict[str, subprocess.Popen] = {}
        self.service_logs: Dict[str, List[ServiceLog]] = {}
        
    async def start_service(self, service_name: str) -> ServiceActionResponse:
        """Start a service."""
        try:
            service = self.service_registry.get_service(service_name)
            if not service:
                return ServiceActionResponse(
                    success=False,
                    message=f"Service {service_name} not found",
                    service_name=service_name
                )
            
            # Check if service is already running
            if service_name in self.running_processes:
                process = self.running_processes[service_name]
                if process.poll() is None:  # Process is still running
                    return ServiceActionResponse(
                        success=False,
                        message=f"Service {service_name} is already running",
                        service_name=service_name
                    )
            
            # Start the service
            if service.management == "uvicorn":
                cmd = self._get_uvicorn_command(service)
            elif service.management == "docker":
                cmd = self._get_docker_command(service)
            else:
                cmd = self._get_default_command(service)
            
            # Start process
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=self._get_service_directory(service_name)
            )
            
            self.running_processes[service_name] = process
            
            # Log the action
            self._log_service_action(service_name, "INFO", f"Service {service_name} started")
            
            return ServiceActionResponse(
                success=True,
                message=f"Service {service_name} started successfully",
                service_name=service_name
            )
            
        except Exception as e:
            self._log_service_action(service_name, "ERROR", f"Failed to start service: {str(e)}")
            return ServiceActionResponse(
                success=False,
                message=f"Failed to start service: {str(e)}",
                service_name=service_name
            )
    
    async def stop_service(self, service_name: str) -> ServiceActionResponse:
        """Stop a service."""
        try:
            if service_name not in self.running_processes:
                return ServiceActionResponse(
                    success=False,
                    message=f"Service {service_name} is not running",
                    service_name=service_name
                )
            
            process = self.running_processes[service_name]
            
            # Try graceful shutdown first
            process.terminate()
            
            # Wait for process to terminate
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                # Force kill if graceful shutdown fails
                process.kill()
                process.wait()
            
            # Remove from running processes
            del self.running_processes[service_name]
            
            # Log the action
            self._log_service_action(service_name, "INFO", f"Service {service_name} stopped")
            
            return ServiceActionResponse(
                success=True,
                message=f"Service {service_name} stopped successfully",
                service_name=service_name
            )
            
        except Exception as e:
            self._log_service_action(service_name, "ERROR", f"Failed to stop service: {str(e)}")
            return ServiceActionResponse(
                success=False,
                message=f"Failed to stop service: {str(e)}",
                service_name=service_name
            )
    
    async def restart_service(self, service_name: str) -> ServiceActionResponse:
        """Restart a service."""
        try:
            # Stop the service first
            stop_result = await self.stop_service(service_name)
            if not stop_result.success and "not running" not in stop_result.message:
                return stop_result
            
            # Wait a moment
            await asyncio.sleep(2)
            
            # Start the service
            start_result = await self.start_service(service_name)
            return start_result
            
        except Exception as e:
            return ServiceActionResponse(
                success=False,
                message=f"Failed to restart service: {str(e)}",
                service_name=service_name
            )
    
    def get_service_status(self, service_name: str) -> ServiceStatus:
        """Get current status of a service."""
        if service_name not in self.running_processes:
            return ServiceStatus.STOPPED
        
        process = self.running_processes[service_name]
        if process.poll() is None:
            return ServiceStatus.RUNNING
        else:
            return ServiceStatus.STOPPED
    
    def get_all_service_status(self) -> Dict[str, ServiceStatus]:
        """Get status of all services."""
        status = {}
        for service in self.service_registry.get_all_services():
            status[service.name] = self.get_service_status(service.name)
        return status
    
    def get_service_logs(self, service_name: str, lines: int = 100) -> List[ServiceLog]:
        """Get service logs."""
        if service_name not in self.service_logs:
            return []
        
        logs = self.service_logs[service_name]
        return logs[-lines:] if lines > 0 else logs
    
    def get_service_metrics(self, service_name: str) -> Dict:
        """Get service metrics."""
        if service_name not in self.running_processes:
            return {}
        
        process = self.running_processes[service_name]
        try:
            ps_process = psutil.Process(process.pid)
            return {
                "pid": process.pid,
                "cpu_percent": ps_process.cpu_percent(),
                "memory_mb": ps_process.memory_info().rss / 1024 / 1024,
                "create_time": ps_process.create_time(),
                "status": ps_process.status()
            }
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return {}
    
    def _get_uvicorn_command(self, service) -> List[str]:
        """Get uvicorn command for service."""
        if service.name == "control-center":
            return [
                sys.executable, "-m", "uvicorn", 
                "src.main:app", 
                "--host", "0.0.0.0", 
                "--port", str(service.port),
                "--reload"
            ]
        elif service.name == "web-portal":
            return [
                sys.executable, "-m", "uvicorn", 
                "src.main:app", 
                "--host", "0.0.0.0", 
                "--port", str(service.port),
                "--reload"
            ]
        elif service.name == "data-service":
            return [
                sys.executable, "-m", "uvicorn", 
                "src.main:app", 
                "--host", "0.0.0.0", 
                "--port", str(service.port),
                "--reload"
            ]
        else:
            return [
                sys.executable, "-m", "uvicorn", 
                "main:app", 
                "--host", "0.0.0.0", 
                "--port", str(service.port),
                "--reload"
            ]
    
    def _get_docker_command(self, service) -> List[str]:
        """Get docker command for service."""
        return ["docker", "run", "--rm", "-p", f"{service.port}:{service.port}", service.name]
    
    def _get_default_command(self, service) -> List[str]:
        """Get default command for service."""
        return [sys.executable, "main.py"]
    
    def _get_service_directory(self, service_name: str) -> str:
        """Get service directory path."""
        if service_name == "control-center":
            return os.path.join(os.path.dirname(__file__), "..", "..", "..")
        else:
            return os.path.join(
                os.path.dirname(__file__), 
                "..", "..", "..", "..", 
                "services", service_name
            )
    
    def _log_service_action(self, service_name: str, level: str, message: str):
        """Log service action."""
        if service_name not in self.service_logs:
            self.service_logs[service_name] = []
        
        log_entry = ServiceLog(
            service_name=service_name,
            timestamp=datetime.now(),
            level=level,
            message=message,
            source="service_manager"
        )
        
        self.service_logs[service_name].append(log_entry)
        
        # Keep only last 1000 logs per service
        if len(self.service_logs[service_name]) > 1000:
            self.service_logs[service_name] = self.service_logs[service_name][-1000:]
    
    async def cleanup_stopped_processes(self):
        """Clean up stopped processes from registry."""
        stopped_services = []
        for service_name, process in self.running_processes.items():
            if process.poll() is not None:  # Process has terminated
                stopped_services.append(service_name)
        
        for service_name in stopped_services:
            del self.running_processes[service_name]
            self._log_service_action(service_name, "INFO", f"Service {service_name} process terminated")
    
    def get_running_services(self) -> List[str]:
        """Get list of running services."""
        return list(self.running_processes.keys())
    
    def get_service_process_info(self, service_name: str) -> Optional[Dict]:
        """Get process information for a service."""
        if service_name not in self.running_processes:
            return None
        
        process = self.running_processes[service_name]
        return {
            "pid": process.pid,
            "status": "running" if process.poll() is None else "stopped",
            "return_code": process.returncode
        }
