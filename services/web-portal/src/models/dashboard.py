"""
Dashboard data models
"""

from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from datetime import datetime

class PortfolioSummary(BaseModel):
    total_value: float
    cash_balance: float
    buying_power: float
    daily_pnl: float
    daily_return: float
    total_pnl: float
    total_return: float

class Position(BaseModel):
    symbol: str
    quantity: int
    current_price: float
    current_value: float
    unrealized_pnl: float
    weight: float

class PerformanceMetrics(BaseModel):
    total_return: float
    annualized_return: float
    sharpe_ratio: float
    max_drawdown: float
    win_rate: float
    avg_trade: float
    total_trades: int

class RiskMetrics(BaseModel):
    portfolio_var: float
    var_percentile: int
    beta: float
    volatility: float
    correlation: float

class Activity(BaseModel):
    timestamp: str
    action: str
    symbol: str
    quantity: int
    price: float
    status: str

class MarketIndex(BaseModel):
    price: float
    change: float
    change_percent: float

class MarketOverview(BaseModel):
    sp500: MarketIndex
    nasdaq: MarketIndex
    dow: MarketIndex
    vix: MarketIndex

class DashboardData(BaseModel):
    portfolio_summary: PortfolioSummary
    active_positions: List[Position]
    performance_metrics: PerformanceMetrics
    risk_metrics: RiskMetrics
    recent_activity: List[Activity]
    market_overview: MarketOverview
    last_updated: str
