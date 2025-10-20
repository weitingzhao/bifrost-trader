"""
Service registry for managing all Bifrost Trader services.
"""

import os
import yaml
from typing import Dict, List, Optional

from ..models.service import ServiceInfo, ServiceCategory


class ServiceRegistry:
    """Service registry for managing service configurations."""
    
    def __init__(self, config_path: str = "config/services.yaml"):
        """Initialize service registry with configuration."""
        self.config_path = config_path
        self.services: Dict[str, ServiceInfo] = {}
        self.categories: Dict[str, Dict] = {}
        self._load_config()
    
    def _load_config(self):
        """Load service configuration from YAML file."""
        try:
            config_file = os.path.join(
                os.path.dirname(__file__), 
                "..", "..", "..", 
                self.config_path
            )
            
            with open(config_file, 'r') as f:
                config = yaml.safe_load(f)
                
            # Load services
            for service_config in config.get('services', []):
                service = ServiceInfo(
                    name=service_config['name'],
                    port=service_config['port'],
                    category=ServiceCategory(service_config['category']),
                    description=service_config['description'],
                    has_ui=service_config['has_ui'],
                    management=service_config['management'],
                    health_endpoint=service_config['health_endpoint'],
                    docs_endpoint=service_config['docs_endpoint'],
                    url=service_config['url']
                )
                self.services[service.name] = service
            
            # Load categories
            self.categories = config.get('categories', {})
            
        except Exception as e:
            print(f"Error loading service configuration: {e}")
            # Load default services if config fails
            self._load_default_services()
    
    def _load_default_services(self):
        """Load default service configuration."""
        default_services = [
            ServiceInfo(
                name="api-gateway",
                port=8000,
                category=ServiceCategory.CORE,
                description="Central API Gateway",
                has_ui=False,
                management="uvicorn",
                health_endpoint="/health",
                docs_endpoint="/docs",
                url="http://localhost:8000"
            ),
            ServiceInfo(
                name="data-service",
                port=8001,
                category=ServiceCategory.CORE,
                description="Market Data Service",
                has_ui=False,
                management="uvicorn",
                health_endpoint="/health",
                docs_endpoint="/docs",
                url="http://localhost:8001"
            ),
            ServiceInfo(
                name="web-portal",
                port=8006,
                category=ServiceCategory.UI,
                description="Web Portal Dashboard",
                has_ui=True,
                management="uvicorn",
                health_endpoint="/health",
                docs_endpoint="/docs",
                url="http://localhost:8006"
            )
        ]
        
        for service in default_services:
            self.services[service.name] = service
    
    def get_service(self, name: str) -> Optional[ServiceInfo]:
        """Get service by name."""
        return self.services.get(name)
    
    def get_all_services(self) -> List[ServiceInfo]:
        """Get all services."""
        return list(self.services.values())
    
    def get_services_by_category(self, category: ServiceCategory) -> List[ServiceInfo]:
        """Get services by category."""
        return [
            service for service in self.services.values()
            if service.category == category
        ]
    
    def get_category_info(self, category: str) -> Optional[Dict]:
        """Get category information."""
        return self.categories.get(category)
    
    def get_all_categories(self) -> Dict[str, Dict]:
        """Get all categories."""
        return self.categories
    
    def get_service_url(self, name: str) -> Optional[str]:
        """Get service URL by name."""
        service = self.get_service(name)
        return service.url if service else None
    
    def get_health_endpoint(self, name: str) -> Optional[str]:
        """Get service health endpoint."""
        service = self.get_service(name)
        if service:
            return f"{service.url}{service.health_endpoint}"
        return None
    
    def get_docs_endpoint(self, name: str) -> Optional[str]:
        """Get service documentation endpoint."""
        service = self.get_service(name)
        if service:
            return f"{service.url}{service.docs_endpoint}"
        return None
    
    def is_service_ui_enabled(self, name: str) -> bool:
        """Check if service has UI."""
        service = self.get_service(name)
        return service.has_ui if service else False
    
    def get_services_with_ui(self) -> List[ServiceInfo]:
        """Get all services with UI."""
        return [
            service for service in self.services.values()
            if service.has_ui
        ]
    
    def reload_config(self):
        """Reload service configuration."""
        self.services.clear()
        self.categories.clear()
        self._load_config()
