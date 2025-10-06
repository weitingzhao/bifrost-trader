"""
Portfolio API endpoints
"""

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, Query

from ..services.portfolio_service import PortfolioService

router = APIRouter()
portfolio_service = PortfolioService()


@router.get("/")
async def get_portfolio_overview(
    user_id: int = Query(default=1, description="User ID")
) -> Dict[str, Any]:
    """Get comprehensive portfolio overview for a user."""
    try:
        return await portfolio_service.get_portfolio_overview(user_id)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting portfolio overview: {str(e)}"
        )


@router.get("/positions")
async def get_positions(
    user_id: int = Query(default=1, description="User ID")
) -> Dict[str, Any]:
    """Get all positions for a user's portfolios."""
    try:
        positions = await portfolio_service.get_portfolio_positions(user_id)
        return {"positions": positions}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting positions: {str(e)}"
        )


@router.get("/performance")
async def get_performance(
    user_id: int = Query(default=1, description="User ID")
) -> Dict[str, Any]:
    """Get performance metrics for a user's portfolio."""
    try:
        overview = await portfolio_service.get_portfolio_overview(user_id)
        return overview.get("performance_metrics", {})
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting performance metrics: {str(e)}"
        )


@router.get("/risk")
async def get_risk_metrics(
    user_id: int = Query(default=1, description="User ID")
) -> Dict[str, Any]:
    """Get risk metrics for a user's portfolio."""
    try:
        overview = await portfolio_service.get_portfolio_overview(user_id)
        return overview.get("risk_metrics", {})
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting risk metrics: {str(e)}"
        )


@router.get("/history")
async def get_trading_history(
    user_id: int = Query(default=1, description="User ID"),
    limit: int = Query(default=50, description="Number of records to return"),
) -> Dict[str, Any]:
    """Get trading history for a user."""
    try:
        history = await portfolio_service.get_trading_history(user_id, limit)
        return {"history": history}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting trading history: {str(e)}"
        )


@router.get("/summary")
async def get_portfolio_summary(
    user_id: int = Query(default=1, description="User ID")
) -> Dict[str, Any]:
    """Get portfolio summary data."""
    try:
        overview = await portfolio_service.get_portfolio_overview(user_id)
        return overview.get("portfolio_summary", {})
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting portfolio summary: {str(e)}"
        )


@router.get("/recent-activity")
async def get_recent_activity(
    user_id: int = Query(default=1, description="User ID")
) -> Dict[str, Any]:
    """Get recent trading activity for a user."""
    try:
        overview = await portfolio_service.get_portfolio_overview(user_id)
        return {"recent_activity": overview.get("recent_activity", [])}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting recent activity: {str(e)}"
        )
