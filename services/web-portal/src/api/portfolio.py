"""
Portfolio API endpoints
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
from ..services.dashboard_service import DashboardService

router = APIRouter()
dashboard_service = DashboardService()

@router.get("/")
async def get_portfolio_overview() -> Dict[str, Any]:
    """Get portfolio overview."""
    try:
        data = await dashboard_service.get_dashboard_data()
        return {
            "portfolio_summary": data.get("portfolio_summary", {}),
            "active_positions": data.get("active_positions", []),
            "performance_metrics": data.get("performance_metrics", {}),
            "risk_metrics": data.get("risk_metrics", {})
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/positions")
async def get_positions() -> Dict[str, Any]:
    """Get all positions."""
    try:
        data = await dashboard_service.get_dashboard_data()
        return {"positions": data.get("active_positions", [])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/performance")
async def get_performance() -> Dict[str, Any]:
    """Get performance metrics."""
    try:
        data = await dashboard_service.get_dashboard_data()
        return data.get("performance_metrics", {})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/risk")
async def get_risk_metrics() -> Dict[str, Any]:
    """Get risk metrics."""
    try:
        data = await dashboard_service.get_dashboard_data()
        return data.get("risk_metrics", {})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history")
async def get_trading_history() -> Dict[str, Any]:
    """Get trading history."""
    try:
        data = await dashboard_service.get_dashboard_data()
        return {"history": data.get("recent_activity", [])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
