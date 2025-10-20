"""
Individual service endpoints for each Bifrost Trader service.
Provides dedicated access points for each service under the Control Center.
"""

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from ..utils.service_registry import ServiceRegistry

router = APIRouter()
templates = Jinja2Templates(directory="templates")


def get_service_registry() -> ServiceRegistry:
    """Get service registry instance."""
    return ServiceRegistry()


# Analytics Service (Port 8008)
@router.get("/analytics", response_class=HTMLResponse)
async def analytics_service_page(request: Request):
    """Analytics Service dedicated page."""
    service_registry = get_service_registry()
    service = service_registry.get_service("analytics-service")
    
    if not service:
        raise HTTPException(status_code=404, detail="Analytics Service not found")
    
    return templates.TemplateResponse(
        "pages/service-page.html",
        {
            "request": request,
            "service": service,
            "service_name": "Analytics Service",
            "description": "Machine Learning and Data Analytics Service",
            "features": [
                "Data analysis and reporting",
                "Machine learning models",
                "Statistical analysis",
                "Performance metrics",
                "Risk analytics"
            ]
        }
    )


# API Gateway (Port 8000)
@router.get("/api-gateway", response_class=HTMLResponse)
async def api_gateway_page(request: Request):
    """API Gateway dedicated page."""
    service_registry = get_service_registry()
    service = service_registry.get_service("api-gateway")
    
    if not service:
        raise HTTPException(status_code=404, detail="API Gateway not found")
    
    return templates.TemplateResponse(
        "pages/service-page.html",
        {
            "request": request,
            "service": service,
            "service_name": "API Gateway",
            "description": "Central API Gateway for all microservices",
            "features": [
                "Request routing and load balancing",
                "Service discovery",
                "API rate limiting",
                "Authentication and authorization",
                "Request/response transformation"
            ]
        }
    )


# Compliance Service (Port 8010)
@router.get("/compliance", response_class=HTMLResponse)
async def compliance_service_page(request: Request):
    """Compliance Service dedicated page."""
    service_registry = get_service_registry()
    service = service_registry.get_service("compliance-service")
    
    if not service:
        raise HTTPException(status_code=404, detail="Compliance Service not found")
    
    return templates.TemplateResponse(
        "pages/service-page.html",
        {
            "request": request,
            "service": service,
            "service_name": "Compliance Service",
            "description": "Regulatory Compliance and Risk Management",
            "features": [
                "Regulatory compliance monitoring",
                "Risk assessment and reporting",
                "Audit trail management",
                "Compliance alerts",
                "Regulatory reporting"
            ]
        }
    )


# Data Service (Port 8001)
@router.get("/data", response_class=HTMLResponse)
async def data_service_page(request: Request):
    """Data Service dedicated page."""
    service_registry = get_service_registry()
    service = service_registry.get_service("data-service")
    
    if not service:
        raise HTTPException(status_code=404, detail="Data Service not found")
    
    return templates.TemplateResponse(
        "pages/service-page.html",
        {
            "request": request,
            "service": service,
            "service_name": "Data Service",
            "description": "Market Data Management with TimescaleDB",
            "features": [
                "Real-time market data ingestion",
                "Historical data storage",
                "Data validation and cleaning",
                "Time-series optimization",
                "Data API endpoints"
            ]
        }
    )


# Execution Service (Port 8004)
@router.get("/execution", response_class=HTMLResponse)
async def execution_service_page(request: Request):
    """Execution Service dedicated page."""
    service_registry = get_service_registry()
    service = service_registry.get_service("execution-service")
    
    if not service:
        raise HTTPException(status_code=404, detail="Execution Service not found")
    
    return templates.TemplateResponse(
        "pages/service-page.html",
        {
            "request": request,
            "service": service,
            "service_name": "Execution Service",
            "description": "Trade Execution and Order Management",
            "features": [
                "Order execution",
                "Trade management",
                "Execution algorithms",
                "Order routing",
                "Execution reporting"
            ]
        }
    )


# Microstructure Service (Port 8012)
@router.get("/microstructure", response_class=HTMLResponse)
async def microstructure_service_page(request: Request):
    """Microstructure Service dedicated page."""
    service_registry = get_service_registry()
    service = service_registry.get_service("microstructure-service")
    
    if not service:
        raise HTTPException(status_code=404, detail="Microstructure Service not found")
    
    return templates.TemplateResponse(
        "pages/service-page.html",
        {
            "request": request,
            "service": service,
            "service_name": "Microstructure Service",
            "description": "Market Microstructure Analysis",
            "features": [
                "Order book analysis",
                "Market microstructure metrics",
                "Liquidity analysis",
                "Market impact studies",
                "Trading pattern analysis"
            ]
        }
    )


# ML Service (Port 8008)
@router.get("/ml", response_class=HTMLResponse)
async def ml_service_page(request: Request):
    """ML Service dedicated page."""
    service_registry = get_service_registry()
    service = service_registry.get_service("ml-service")
    
    if not service:
        raise HTTPException(status_code=404, detail="ML Service not found")
    
    return templates.TemplateResponse(
        "pages/service-page.html",
        {
            "request": request,
            "service": service,
            "service_name": "ML Service",
            "description": "Machine Learning and AI Models",
            "features": [
                "Predictive models",
                "Pattern recognition",
                "Algorithm training",
                "Model deployment",
                "AI-powered insights"
            ]
        }
    )


# News Service (Port 8011)
@router.get("/news", response_class=HTMLResponse)
async def news_service_page(request: Request):
    """News Service dedicated page."""
    service_registry = get_service_registry()
    service = service_registry.get_service("news-service")
    
    if not service:
        raise HTTPException(status_code=404, detail="News Service not found")
    
    return templates.TemplateResponse(
        "pages/service-page.html",
        {
            "request": request,
            "service": service,
            "service_name": "News Service",
            "description": "Market News and Information Service",
            "features": [
                "Real-time news feeds",
                "News sentiment analysis",
                "Market impact assessment",
                "News filtering and categorization",
                "Historical news data"
            ]
        }
    )


# Portfolio Service (Port 8002)
@router.get("/portfolio", response_class=HTMLResponse)
async def portfolio_service_page(request: Request):
    """Portfolio Service dedicated page."""
    service_registry = get_service_registry()
    service = service_registry.get_service("portfolio-service")
    
    if not service:
        raise HTTPException(status_code=404, detail="Portfolio Service not found")
    
    return templates.TemplateResponse(
        "pages/service-page.html",
        {
            "request": request,
            "service": service,
            "service_name": "Portfolio Service",
            "description": "Portfolio Management and Tracking",
            "features": [
                "Portfolio tracking",
                "Position management",
                "P&L calculation",
                "Performance analytics",
                "Risk metrics"
            ]
        }
    )


# Risk Service (Port 8005)
@router.get("/risk", response_class=HTMLResponse)
async def risk_service_page(request: Request):
    """Risk Service dedicated page."""
    service_registry = get_service_registry()
    service = service_registry.get_service("risk-service")
    
    if not service:
        raise HTTPException(status_code=404, detail="Risk Service not found")
    
    return templates.TemplateResponse(
        "pages/service-page.html",
        {
            "request": request,
            "service": service,
            "service_name": "Risk Service",
            "description": "Risk Management and VaR Calculations",
            "features": [
                "Value at Risk (VaR) calculations",
                "Risk monitoring",
                "Stress testing",
                "Risk reporting",
                "Risk limits management"
            ]
        }
    )


# Strategy Service (Port 8003)
@router.get("/strategy", response_class=HTMLResponse)
async def strategy_service_page(request: Request):
    """Strategy Service dedicated page."""
    service_registry = get_service_registry()
    service = service_registry.get_service("strategy-service")
    
    if not service:
        raise HTTPException(status_code=404, detail="Strategy Service not found")
    
    return templates.TemplateResponse(
        "pages/service-page.html",
        {
            "request": request,
            "service": service,
            "service_name": "Strategy Service",
            "description": "Trading Strategies and Backtesting",
            "features": [
                "Strategy development",
                "Backtesting with Backtrader",
                "Strategy optimization",
                "Performance analysis",
                "Strategy deployment"
            ]
        }
    )


# Web Portal (Port 8006)
@router.get("/web-portal", response_class=HTMLResponse)
async def web_portal_page(request: Request):
    """Web Portal dedicated page."""
    service_registry = get_service_registry()
    service = service_registry.get_service("web-portal")
    
    if not service:
        raise HTTPException(status_code=404, detail="Web Portal not found")
    
    return templates.TemplateResponse(
        "pages/service-page.html",
        {
            "request": request,
            "service": service,
            "service_name": "Web Portal",
            "description": "Main Trading Dashboard and UI",
            "features": [
                "Trading dashboard",
                "Portfolio visualization",
                "Real-time data display",
                "Interactive charts",
                "User interface"
            ]
        }
    )


# Service List Page
@router.get("/services", response_class=HTMLResponse)
async def services_list_page(request: Request):
    """Services list page with all available services."""
    service_registry = get_service_registry()
    all_services = service_registry.get_all_services()
    categories = service_registry.get_all_categories()
    
    # Group services by category
    services_by_category = {}
    for service in all_services:
        category = service.category.value
        if category not in services_by_category:
            services_by_category[category] = []
        services_by_category[category].append(service)
    
    return templates.TemplateResponse(
        "pages/services-list.html",
        {
            "request": request,
            "services": all_services,
            "services_by_category": services_by_category,
            "categories": categories
        }
    )


# Service Endpoints Summary Page
@router.get("/endpoints", response_class=HTMLResponse)
async def service_endpoints_summary_page(request: Request):
    """Service endpoints summary page with all available endpoints."""
    return templates.TemplateResponse(
        "pages/service-endpoints-summary.html",
        {
            "request": request
        }
    )
