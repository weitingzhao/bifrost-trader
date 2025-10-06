"""
Dashboard API endpoints
"""

from typing import Any, Dict

from fastapi import APIRouter, HTTPException, Query

from ..services.dashboard_service import DashboardService

router = APIRouter()
dashboard_service = DashboardService()


@router.get("/")
async def get_dashboard_data(
    user_id: str = Query(default="1", description="User ID")
) -> Dict[str, Any]:
    """Get comprehensive dashboard data."""
    try:
        data = await dashboard_service.get_dashboard_data(user_id)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/portfolio-summary")
async def get_portfolio_summary(
    user_id: str = Query(default="1", description="User ID")
) -> Dict[str, Any]:
    """Get portfolio summary data."""
    try:
        data = await dashboard_service.get_dashboard_data(user_id)
        return data.get("portfolio_summary", {})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/active-positions")
async def get_active_positions(
    user_id: str = Query(default="1", description="User ID")
) -> Dict[str, Any]:
    """Get active positions."""
    try:
        data = await dashboard_service.get_dashboard_data(user_id)
        return {"positions": data.get("active_positions", [])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/performance-metrics")
async def get_performance_metrics(
    user_id: str = Query(default="1", description="User ID")
) -> Dict[str, Any]:
    """Get performance metrics."""
    try:
        data = await dashboard_service.get_dashboard_data(user_id)
        return data.get("performance_metrics", {})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/risk-metrics")
async def get_risk_metrics(
    user_id: str = Query(default="1", description="User ID")
) -> Dict[str, Any]:
    """Get risk metrics."""
    try:
        data = await dashboard_service.get_dashboard_data(user_id)
        return data.get("risk_metrics", {})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/recent-activity")
async def get_recent_activity(
    user_id: str = Query(default="1", description="User ID")
) -> Dict[str, Any]:
    """Get recent trading activity."""
    try:
        data = await dashboard_service.get_dashboard_data(user_id)
        return {"activity": data.get("recent_activity", [])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/market-overview")
async def get_market_overview(
    user_id: str = Query(default="1", description="User ID")
) -> Dict[str, Any]:
    """Get market overview."""
    try:
        data = await dashboard_service.get_dashboard_data(user_id)
        return data.get("market_overview", {})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
