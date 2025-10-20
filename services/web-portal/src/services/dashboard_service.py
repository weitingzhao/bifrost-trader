"""
Dashboard Service

Handles dashboard data aggregation and business logic with PostgreSQL integration.
"""

import asyncio
import json
import os
import sys
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import httpx

sys.path.append(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "shared")
)

from database.connection import get_db_connection
# from services.portfolio_service import PortfolioService


class DashboardService:
    def __init__(self):
        self.data_service_url = "http://data-service:8001"
        self.portfolio_service_url = "http://portfolio-service:8002"
        self.strategy_service_url = "http://strategy-service:8003"
        self.execution_service_url = "http://execution-service:8004"
        self.risk_service_url = "http://risk-service:8005"
        self.db = get_db_connection()
        # self.portfolio_service = PortfolioService()

    async def get_dashboard_data(self, user_id: str = "1") -> Dict[str, Any]:
        """Get comprehensive dashboard data."""
        try:
            # Convert user_id to int
            user_id_int = int(user_id)

            # Get portfolio overview from database
            portfolio_overview = await self.portfolio_service.get_portfolio_overview(
                user_id_int
            )

            # Get market overview
            market_overview = await self._get_market_overview()

            return {
                "portfolio_summary": portfolio_overview.get("portfolio_summary", {}),
                "active_positions": portfolio_overview.get("active_positions", []),
                "performance_metrics": portfolio_overview.get(
                    "performance_metrics", {}
                ),
                "risk_metrics": portfolio_overview.get("risk_metrics", {}),
                "recent_activity": portfolio_overview.get("recent_activity", []),
                "market_overview": market_overview,
                "last_updated": datetime.now().isoformat(),
            }
        except Exception as e:
            print(f"Error getting dashboard data: {e}")
            return {
                "portfolio_summary": self._get_empty_portfolio_summary(),
                "active_positions": [],
                "performance_metrics": self._get_empty_performance_metrics(),
                "risk_metrics": self._get_empty_risk_metrics(),
                "recent_activity": [],
                "market_overview": self._get_empty_market_overview(),
                "last_updated": datetime.now().isoformat(),
            }

    async def _get_market_overview(self) -> Dict[str, Any]:
        """Fetches a summary of market data from database."""
        try:
            # Get market data from database
            query = """
            SELECT 
                symbol,
                name,
                status,
                ms_stock.industry,
                ms_stock.sector
            FROM market_symbol ms
            LEFT JOIN market_stock ms_stock ON ms.symbol = ms_stock.symbol
            WHERE ms.status = 'ACTIVE' AND ms.symbol IN ('SPY', 'QQQ', 'DIA', 'VIX')
            ORDER BY ms.symbol
            """

            results = self.db.execute_query(query)

            market_data = {}
            for row in results:
                symbol = row["symbol"]
                market_data[symbol] = {
                    "name": row["name"],
                    "status": row["status"],
                    "industry": row["industry"],
                    "sector": row["sector"],
                }

            # Add some mock price data (in real implementation, this would come from historical data)
            market_overview = {
                "SPY": {"price": 456.78, "change": 2.34, "change_percent": 0.51},
                "QQQ": {"price": 389.45, "change": -1.23, "change_percent": -0.31},
                "DIA": {"price": 34567.89, "change": 89.12, "change_percent": 0.26},
                "VIX": {"price": 18.45, "change": -1.23, "change_percent": -6.25},
            }

            return market_overview

        except Exception as e:
            print(f"Market overview error: {e}")
            return self._get_empty_market_overview()

    async def _get_portfolio_summary(self, user_id: int) -> Dict[str, Any]:
        """Fetches a summary of the user's portfolio from database."""
        try:
            portfolio_overview = await self.portfolio_service.get_portfolio_overview(
                user_id
            )
            return portfolio_overview.get("portfolio_summary", {})
        except Exception as e:
            print(f"Portfolio summary error: {e}")
            return self._get_empty_portfolio_summary()

    async def _get_active_positions(self, user_id: int) -> List[Dict[str, Any]]:
        """Fetches a list of active positions for the user from database."""
        try:
            portfolio_overview = await self.portfolio_service.get_portfolio_overview(
                user_id
            )
            return portfolio_overview.get("active_positions", [])
        except Exception as e:
            print(f"Active positions error: {e}")
            return []

    async def _get_recent_activity(self, user_id: int) -> List[Dict[str, Any]]:
        """Fetches recent trading activity from database."""
        try:
            portfolio_overview = await self.portfolio_service.get_portfolio_overview(
                user_id
            )
            return portfolio_overview.get("recent_activity", [])
        except Exception as e:
            print(f"Recent activity error: {e}")
            return []

    async def _get_performance_metrics(self, user_id: int) -> Dict[str, Any]:
        """Fetches key performance metrics for the portfolio from database."""
        try:
            portfolio_overview = await self.portfolio_service.get_portfolio_overview(
                user_id
            )
            return portfolio_overview.get("performance_metrics", {})
        except Exception as e:
            print(f"Performance metrics error: {e}")
            return self._get_empty_performance_metrics()

    async def _get_risk_metrics(self, user_id: int) -> Dict[str, Any]:
        """Fetches key risk metrics for the portfolio from database."""
        try:
            portfolio_overview = await self.portfolio_service.get_portfolio_overview(
                user_id
            )
            return portfolio_overview.get("risk_metrics", {})
        except Exception as e:
            print(f"Risk metrics error: {e}")
            return self._get_empty_risk_metrics()

    def _get_empty_portfolio_summary(self) -> Dict[str, Any]:
        """Return empty portfolio summary."""
        return {
            "portfolio_id": None,
            "name": "No Portfolio",
            "total_value": 0.0,
            "initial_capital": 0.0,
            "cash_balance": 0.0,
            "total_holdings_value": 0.0,
            "total_unrealized_pnl": 0.0,
            "total_pnl": 0.0,
            "total_pnl_percent": 0.0,
            "weighted_unrealized_pnl_percent": 0.0,
        }

    def _get_empty_performance_metrics(self) -> Dict[str, Any]:
        """Return empty performance metrics."""
        return {
            "total_return": 0.0,
            "total_return_percent": 0.0,
            "annualized_return": 0.0,
            "total_trades": 0,
            "win_rate": 0.0,
            "avg_trade": 0.0,
            "days_held": 0,
        }

    def _get_empty_risk_metrics(self) -> Dict[str, Any]:
        """Return empty risk metrics."""
        return {
            "portfolio_var": 0.0,
            "var_percentile": 95,
            "beta": 0.0,
            "volatility": 0.0,
            "max_drawdown": 0.0,
            "sharpe_ratio": 0.0,
        }

    def _get_empty_market_overview(self) -> Dict[str, Any]:
        """Return empty market overview."""
        return {
            "SPY": {"price": 0.0, "change": 0.0, "change_percent": 0.0},
            "QQQ": {"price": 0.0, "change": 0.0, "change_percent": 0.0},
            "DIA": {"price": 0.0, "change": 0.0, "change_percent": 0.0},
            "VIX": {"price": 0.0, "change": 0.0, "change_percent": 0.0},
        }
