"""
Trading API endpoints
"""

from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..services.trading_service import TradingService

router = APIRouter()
trading_service = TradingService()


class OrderRequest(BaseModel):
    symbol: str
    side: str  # BUY or SELL
    quantity: int
    order_type: str  # MARKET, LIMIT, STOP
    price: float = None
    stop_price: float = None


@router.get("/")
async def get_trading_data() -> Dict[str, Any]:
    """Get comprehensive trading data."""
    try:
        data = await trading_service.get_trading_data()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/account-summary")
async def get_account_summary() -> Dict[str, Any]:
    """Get account summary."""
    try:
        data = await trading_service.get_trading_data()
        return data.get("account_summary", {})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/active-orders")
async def get_active_orders() -> Dict[str, Any]:
    """Get active orders."""
    try:
        data = await trading_service.get_trading_data()
        return {"orders": data.get("active_orders", [])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/market-data")
async def get_market_data() -> Dict[str, Any]:
    """Get market data for trading."""
    try:
        data = await trading_service.get_trading_data()
        return data.get("market_data", {})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/strategies")
async def get_strategies() -> Dict[str, Any]:
    """Get available strategies."""
    try:
        data = await trading_service.get_trading_data()
        return {"strategies": data.get("strategies", [])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/orders")
async def place_order(order: OrderRequest) -> Dict[str, Any]:
    """Place a trading order."""
    try:
        order_data = order.dict()
        result = await trading_service.place_order(order_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/orders/{order_id}")
async def cancel_order(order_id: str) -> Dict[str, Any]:
    """Cancel an order."""
    try:
        result = await trading_service.cancel_order(order_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/quotes/{symbol}")
async def get_quote(symbol: str) -> Dict[str, Any]:
    """Get quote for a specific symbol."""
    try:
        data = await trading_service.get_trading_data()
        market_data = data.get("market_data", {})
        quote = market_data.get(symbol.upper())
        if quote:
            return {"symbol": symbol.upper(), "quote": quote}
        else:
            raise HTTPException(status_code=404, detail=f"Quote not found for {symbol}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
