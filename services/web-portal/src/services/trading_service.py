"""
Trading Service

Handles trading operations and real-time trading data.
"""

import asyncio
import json
from datetime import datetime
from typing import Any, Dict, List, Optional

import httpx


class TradingService:
    def __init__(self):
        self.execution_service_url = "http://execution-service:8004"
        self.data_service_url = "http://data-service:8001"
        self.portfolio_service_url = "http://portfolio-service:8002"
        self.strategy_service_url = "http://strategy-service:8003"

    async def get_trading_data(self) -> Dict[str, Any]:
        """Get comprehensive trading data."""
        try:
            # Fetch data from multiple services concurrently
            tasks = [
                self._get_account_summary(),
                self._get_active_orders(),
                self._get_market_data(),
                self._get_strategies(),
            ]

            results = await asyncio.gather(*tasks, return_exceptions=True)

            return {
                "account_summary": results[0]
                if not isinstance(results[0], Exception)
                else {},
                "active_orders": results[1]
                if not isinstance(results[1], Exception)
                else [],
                "market_data": results[2]
                if not isinstance(results[2], Exception)
                else {},
                "strategies": results[3]
                if not isinstance(results[3], Exception)
                else [],
                "last_updated": datetime.now().isoformat(),
            }
        except Exception as e:
            print(f"Trading data error: {e}")
            return self._get_default_trading_data()

    async def _get_account_summary(self) -> Dict[str, Any]:
        """Get account summary."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.portfolio_service_url}/api/portfolio/account"
                )
                if response.status_code == 200:
                    return response.json()
        except Exception as e:
            print(f"Account summary error: {e}")

        # Return default data
        return {
            "buying_power": 100000.0,
            "cash_balance": 25000.0,
            "margin_used": 75000.0,
            "equity": 100000.0,
            "day_trading_buying_power": 200000.0,
        }

    async def _get_active_orders(self) -> List[Dict[str, Any]]:
        """Get active orders."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.execution_service_url}/api/execution/orders"
                )
                if response.status_code == 200:
                    return response.json()
        except Exception as e:
            print(f"Active orders error: {e}")

        # Return default data
        return [
            {
                "order_id": "ORD001",
                "symbol": "AAPL",
                "side": "BUY",
                "quantity": 100,
                "order_type": "LIMIT",
                "price": 175.00,
                "status": "PENDING",
                "timestamp": datetime.now().isoformat(),
            }
        ]

    async def _get_market_data(self) -> Dict[str, Any]:
        """Get market data for trading."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.data_service_url}/api/market/quotes"
                )
                if response.status_code == 200:
                    return response.json()
        except Exception as e:
            print(f"Market data error: {e}")

        # Return default data
        return {
            "AAPL": {
                "price": 175.50,
                "change": 2.25,
                "change_percent": 1.30,
                "volume": 45000000,
                "bid": 175.45,
                "ask": 175.55,
            },
            "MSFT": {
                "price": 380.25,
                "change": -1.50,
                "change_percent": -0.39,
                "volume": 25000000,
                "bid": 380.20,
                "ask": 380.30,
            },
        }

    async def _get_strategies(self) -> List[Dict[str, Any]]:
        """Get available strategies."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.strategy_service_url}/api/strategies"
                )
                if response.status_code == 200:
                    return response.json()
        except Exception as e:
            print(f"Strategies error: {e}")

        # Return default data
        return [
            {
                "id": "three_step",
                "name": "Three Step Strategy",
                "description": "Multi-timeframe momentum strategy",
                "status": "active",
            },
            {
                "id": "momentum",
                "name": "Momentum Strategy",
                "description": "Price momentum based strategy",
                "status": "inactive",
            },
        ]

    async def place_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """Place a trading order."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.execution_service_url}/api/execution/orders",
                    json=order_data,
                )
                if response.status_code == 200:
                    return response.json()
                else:
                    return {"error": f"Order failed: {response.status_code}"}
        except Exception as e:
            print(f"Place order error: {e}")
            return {"error": str(e)}

    async def cancel_order(self, order_id: str) -> Dict[str, Any]:
        """Cancel an order."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.delete(
                    f"{self.execution_service_url}/api/execution/orders/{order_id}"
                )
                if response.status_code == 200:
                    return response.json()
                else:
                    return {"error": f"Cancel failed: {response.status_code}"}
        except Exception as e:
            print(f"Cancel order error: {e}")
            return {"error": str(e)}

    def _get_default_trading_data(self) -> Dict[str, Any]:
        """Get default trading data when services are unavailable."""
        return {
            "account_summary": {
                "buying_power": 0.0,
                "cash_balance": 0.0,
                "margin_used": 0.0,
                "equity": 0.0,
                "day_trading_buying_power": 0.0,
            },
            "active_orders": [],
            "market_data": {},
            "strategies": [],
            "last_updated": datetime.now().isoformat(),
        }
