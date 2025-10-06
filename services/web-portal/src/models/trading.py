"""
Trading data models
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class AccountSummary(BaseModel):
    buying_power: float
    cash_balance: float
    margin_used: float
    equity: float
    day_trading_buying_power: float


class Order(BaseModel):
    order_id: str
    symbol: str
    side: str
    quantity: int
    order_type: str
    price: Optional[float] = None
    status: str
    timestamp: str


class MarketQuote(BaseModel):
    price: float
    change: float
    change_percent: float
    volume: int
    bid: float
    ask: float


class Strategy(BaseModel):
    id: str
    name: str
    description: str
    status: str


class TradingData(BaseModel):
    account_summary: AccountSummary
    active_orders: List[Order]
    market_data: Dict[str, MarketQuote]
    strategies: List[Strategy]
    last_updated: str
