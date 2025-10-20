"""
API proxy endpoints for unified access to all services.
"""

from typing import Any, Dict, Optional

import httpx
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import Response

from ..utils.service_registry import ServiceRegistry

router = APIRouter()


def get_service_registry() -> ServiceRegistry:
    """Get service registry instance."""
    return ServiceRegistry()


@router.api_route("/{service_name}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"])
async def proxy_request(
    service_name: str,
    path: str,
    request: Request
):
    """Proxy requests to any service."""
    service_registry = get_service_registry()
    
    # Get service URL
    service_url = service_registry.get_service_url(service_name)
    if not service_url:
        raise HTTPException(status_code=404, detail=f"Service {service_name} not found")
    
    # Build target URL
    target_url = f"{service_url}/{path}"
    
    # Get request body if present
    body = None
    if request.method in ["POST", "PUT", "PATCH"]:
        try:
            body = await request.body()
        except:
            pass
    
    # Get query parameters
    query_params = dict(request.query_params)
    
    # Get headers (exclude host and connection headers)
    headers = dict(request.headers)
    headers.pop("host", None)
    headers.pop("connection", None)
    headers.pop("content-length", None)
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Make the request
            response = await client.request(
                method=request.method,
                url=target_url,
                params=query_params,
                headers=headers,
                content=body
            )
            
            # Get response content
            content = response.content
            
            # Get response headers
            response_headers = dict(response.headers)
            
            # Create response
            return Response(
                content=content,
                status_code=response.status_code,
                headers=response_headers,
                media_type=response.headers.get("content-type")
            )
            
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail=f"Service {service_name} timeout")
    except httpx.ConnectError:
        raise HTTPException(status_code=502, detail=f"Service {service_name} connection error")
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"Service {service_name} error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Proxy error: {str(e)}")


@router.get("/{service_name}/info")
async def get_service_info(service_name: str):
    """Get information about a service."""
    service_registry = get_service_registry()
    
    service = service_registry.get_service(service_name)
    if not service:
        raise HTTPException(status_code=404, detail=f"Service {service_name} not found")
    
    return {
        "name": service.name,
        "port": service.port,
        "category": service.category.value,
        "description": service.description,
        "has_ui": service.has_ui,
        "url": service.url,
        "docs_url": f"{service.url}{service.docs_endpoint}",
        "health_url": f"{service.url}{service.health_endpoint}",
        "management": service.management
    }


@router.get("/{service_name}/health")
async def proxy_health_check(service_name: str):
    """Proxy health check for a service."""
    service_registry = get_service_registry()
    
    health_endpoint = service_registry.get_health_endpoint(service_name)
    if not health_endpoint:
        raise HTTPException(status_code=404, detail=f"Health endpoint not found for service {service_name}")
    
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(health_endpoint)
            return response.json()
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail=f"Health check timeout for service {service_name}")
    except httpx.ConnectError:
        raise HTTPException(status_code=502, detail=f"Service {service_name} is not reachable")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check error: {str(e)}")


@router.get("/{service_name}/docs")
async def proxy_docs(service_name: str):
    """Get service documentation URL."""
    service_registry = get_service_registry()
    
    docs_url = service_registry.get_docs_endpoint(service_name)
    if not docs_url:
        raise HTTPException(status_code=404, detail=f"Documentation not found for service {service_name}")
    
    return {
        "service_name": service_name,
        "docs_url": docs_url,
        "message": f"Redirect to {docs_url} for service documentation"
    }


@router.get("/services/list")
async def list_available_services():
    """List all available services for proxying."""
    service_registry = get_service_registry()
    
    services = service_registry.get_all_services()
    
    service_list = []
    for service in services:
        service_info = {
            "name": service.name,
            "port": service.port,
            "category": service.category.value,
            "description": service.description,
            "has_ui": service.has_ui,
            "url": service.url,
            "proxy_url": f"/api/proxy/{service.name}",
            "health_url": f"/api/proxy/{service.name}/health",
            "docs_url": f"/api/proxy/{service.name}/docs"
        }
        service_list.append(service_info)
    
    return {
        "services": service_list,
        "total": len(service_list),
        "message": "Use /api/proxy/{service_name}/{path} to proxy requests to any service"
    }
