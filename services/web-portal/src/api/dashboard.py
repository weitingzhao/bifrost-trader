"""
Dashboard API endpoints
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from ..services.dashboard_service import DashboardService

router = APIRouter()
dashboard_service = DashboardService()

@router.get("/")
async def get_dashboard_data() -> Dict[str, Any]:
    """Get comprehensive dashboard data."""
    try:
        data = await dashboard_service.get_dashboard_data()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/portfolio-summary")
async def get_portfolio_summary() -> Dict[str, Any]:
    """Get portfolio summary data."""
    try:
        data = await dashboard_service.get_dashboard_data()
        return data.get("portfolio_summary", {})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/active-positions")
async def get_active_positions() -> Dict[str, Any]:
    """Get active positions."""
    try:
        data = await dashboard_service.get_dashboard_data()
        return {"positions": data.get("active_positions", [])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/performance-metrics")
async def get_performance_metrics() -> Dict[str, Any]:
    """Get performance metrics."""
    try:
        data = await dashboard_service.get_dashboard_data()
        return data.get("performance_metrics", {})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/risk-metrics")
async def get_risk_metrics() -> Dict[str, Any]:
    """Get risk metrics."""
    try:
        data = await dashboard_service.get_dashboard_data()
        return data.get("risk_metrics", {})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recent-activity")
async def get_recent_activity() -> Dict[str, Any]:
    """Get recent trading activity."""
    try:
        data = await dashboard_service.get_dashboard_data()
        return {"activity": data.get("recent_activity", [])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/market-overview")
async def get_market_overview() -> Dict[str, Any]:
    """Get market overview."""
    try:
        data = await dashboard_service.get_dashboard_data()
        return data.get("market_overview", {})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
