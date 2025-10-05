"""
Dashboard Service

Handles dashboard data aggregation and business logic.
"""

import httpx
import asyncio
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import json

class DashboardService:
    def __init__(self):
        self.data_service_url = "http://data-service:8001"
        self.portfolio_service_url = "http://portfolio-service:8002"
        self.strategy_service_url = "http://strategy-service:8003"
        self.execution_service_url = "http://execution-service:8004"
        self.risk_service_url = "http://risk-service:8005"
        
    async def get_dashboard_data(self) -> Dict[str, Any]:
        """Get comprehensive dashboard data."""
        try:
            # Fetch data from multiple services concurrently
            tasks = [
                self._get_portfolio_summary(),
                self._get_active_positions(),
                self._get_performance_metrics(),
                self._get_risk_metrics(),
                self._get_recent_activity(),
                self._get_market_overview()
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            return {
                "portfolio_summary": results[0] if not isinstance(results[0], Exception) else {},
                "active_positions": results[1] if not isinstance(results[1], Exception) else [],
                "performance_metrics": results[2] if not isinstance(results[2], Exception) else {},
                "risk_metrics": results[3] if not isinstance(results[3], Exception) else {},
                "recent_activity": results[4] if not isinstance(results[4], Exception) else [],
                "market_overview": results[5] if not isinstance(results[5], Exception) else {},
                "last_updated": datetime.now().isoformat()
            }
        except Exception as e:
            print(f"Dashboard data error: {e}")
            return self._get_default_dashboard_data()
    
    async def _get_portfolio_summary(self) -> Dict[str, Any]:
        """Get portfolio summary data."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.portfolio_service_url}/api/portfolio/summary")
                if response.status_code == 200:
                    return response.json()
        except Exception as e:
            print(f"Portfolio summary error: {e}")
        
        # Return default data
        return {
            "total_value": 100000.0,
            "cash_balance": 25000.0,
            "buying_power": 100000.0,
            "daily_pnl": 1250.50,
            "daily_return": 1.25,
            "total_pnl": 5000.0,
            "total_return": 5.0
        }
    
    async def _get_active_positions(self) -> List[Dict[str, Any]]:
        """Get active positions."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.portfolio_service_url}/api/portfolio/positions")
                if response.status_code == 200:
                    return response.json()
        except Exception as e:
            print(f"Active positions error: {e}")
        
        # Return default data
        return [
            {
                "symbol": "AAPL",
                "quantity": 100,
                "current_price": 175.50,
                "current_value": 17550.0,
                "unrealized_pnl": 550.0,
                "weight": 17.55
            },
            {
                "symbol": "MSFT",
                "quantity": 50,
                "current_price": 380.25,
                "current_value": 19012.5,
                "unrealized_pnl": 1012.5,
                "weight": 19.01
            },
            {
                "symbol": "GOOGL",
                "quantity": 25,
                "current_price": 142.80,
                "current_value": 3570.0,
                "unrealized_pnl": 70.0,
                "weight": 3.57
            }
        ]
    
    async def _get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.strategy_service_url}/api/performance/metrics")
                if response.status_code == 200:
                    return response.json()
        except Exception as e:
            print(f"Performance metrics error: {e}")
        
        # Return default data
        return {
            "total_return": 5.0,
            "annualized_return": 12.5,
            "sharpe_ratio": 1.8,
            "max_drawdown": -8.5,
            "win_rate": 65.5,
            "avg_trade": 125.75,
            "total_trades": 45
        }
    
    async def _get_risk_metrics(self) -> Dict[str, Any]:
        """Get risk metrics."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.risk_service_url}/api/risk/metrics")
                if response.status_code == 200:
                    return response.json()
        except Exception as e:
            print(f"Risk metrics error: {e}")
        
        # Return default data
        return {
            "portfolio_var": 2500.0,
            "var_percentile": 95,
            "beta": 1.2,
            "volatility": 18.5,
            "correlation": 0.75
        }
    
    async def _get_recent_activity(self) -> List[Dict[str, Any]]:
        """Get recent trading activity."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.execution_service_url}/api/execution/recent")
                if response.status_code == 200:
                    return response.json()
        except Exception as e:
            print(f"Recent activity error: {e}")
        
        # Return default data
        return [
            {
                "timestamp": datetime.now().isoformat(),
                "action": "BUY",
                "symbol": "AAPL",
                "quantity": 100,
                "price": 175.50,
                "status": "FILLED"
            },
            {
                "timestamp": (datetime.now() - timedelta(minutes=5)).isoformat(),
                "action": "SELL",
                "symbol": "TSLA",
                "quantity": 50,
                "price": 245.80,
                "status": "FILLED"
            }
        ]
    
    async def _get_market_overview(self) -> Dict[str, Any]:
        """Get market overview."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.data_service_url}/api/market/overview")
                if response.status_code == 200:
                    return response.json()
        except Exception as e:
            print(f"Market overview error: {e}")
        
        # Return default data
        return {
            "sp500": {"price": 4567.89, "change": 12.34, "change_percent": 0.27},
            "nasdaq": {"price": 14234.56, "change": -45.67, "change_percent": -0.32},
            "dow": {"price": 34567.89, "change": 89.12, "change_percent": 0.26},
            "vix": {"price": 18.45, "change": -1.23, "change_percent": -6.25}
        }
    
    def _get_default_dashboard_data(self) -> Dict[str, Any]:
        """Get default dashboard data when services are unavailable."""
        return {
            "portfolio_summary": {
                "total_value": 100000.0,
                "cash_balance": 25000.0,
                "buying_power": 100000.0,
                "daily_pnl": 0.0,
                "daily_return": 0.0,
                "total_pnl": 0.0,
                "total_return": 0.0
            },
            "active_positions": [],
            "performance_metrics": {
                "total_return": 0.0,
                "annualized_return": 0.0,
                "sharpe_ratio": 0.0,
                "max_drawdown": 0.0,
                "win_rate": 0.0,
                "avg_trade": 0.0,
                "total_trades": 0
            },
            "risk_metrics": {
                "portfolio_var": 0.0,
                "var_percentile": 95,
                "beta": 0.0,
                "volatility": 0.0,
                "correlation": 0.0
            },
            "recent_activity": [],
            "market_overview": {
                "sp500": {"price": 0.0, "change": 0.0, "change_percent": 0.0},
                "nasdaq": {"price": 0.0, "change": 0.0, "change_percent": 0.0},
                "dow": {"price": 0.0, "change": 0.0, "change_percent": 0.0},
                "vix": {"price": 0.0, "change": 0.0, "change_percent": 0.0}
            },
            "last_updated": datetime.now().isoformat()
        }
