"""
Shared base models for Bifrost Trader services.
These models provide common functionality across all microservices.
"""

import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class BaseEntity(BaseModel):
    """Base entity with common fields for all models."""

    id: Optional[int] = Field(None, description="Unique identifier")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    uuid: Optional[str] = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="UUID for external references",
    )

    class Config:
        from_attributes = True
        json_encoders = {datetime: lambda v: v.isoformat()}


class MarketSymbol(BaseEntity):
    """Market symbol representation."""

    symbol: str = Field(..., description="Symbol ticker")
    name: str = Field(..., description="Company name")
    market: str = Field(..., description="Market exchange")
    asset_type: str = Field(..., description="Asset type (stock, etf, etc.)")
    ipo_date: Optional[datetime] = Field(None, description="IPO date")
    delisting_date: Optional[datetime] = Field(None, description="Delisting date")
    status: str = Field("active", description="Symbol status")
    has_company_info: bool = Field(False, description="Has company information")
    is_delisted: bool = Field(False, description="Is delisted")
    min_period_yfinance: Optional[str] = Field(
        None, description="Minimum period for yfinance"
    )
    daily_period_yfinance: Optional[str] = Field(
        None, description="Daily period for yfinance"
    )


class Portfolio(BaseEntity):
    """Portfolio representation."""

    user_id: int = Field(..., description="User ID")
    name: str = Field(..., description="Portfolio name")
    money_market: float = Field(0.0, description="Money market balance")
    cash: float = Field(0.0, description="Cash balance")
    investment: float = Field(0.0, description="Investment amount")
    total_value: float = Field(0.0, description="Total portfolio value")
    is_active: bool = Field(True, description="Is portfolio active")


class Holding(BaseEntity):
    """Portfolio holding representation."""

    portfolio_id: int = Field(..., description="Portfolio ID")
    symbol: str = Field(..., description="Symbol ticker")
    quantity: float = Field(..., description="Quantity held")
    average_price: float = Field(..., description="Average purchase price")
    current_price: float = Field(0.0, description="Current market price")
    market_value: float = Field(0.0, description="Current market value")
    unrealized_pnl: float = Field(0.0, description="Unrealized P&L")
    realized_pnl: float = Field(0.0, description="Realized P&L")


class Transaction(BaseEntity):
    """Transaction representation."""

    portfolio_id: int = Field(..., description="Portfolio ID")
    symbol: str = Field(..., description="Symbol ticker")
    transaction_type: str = Field(..., description="Transaction type (buy, sell)")
    quantity: float = Field(..., description="Transaction quantity")
    price: float = Field(..., description="Transaction price")
    total_amount: float = Field(..., description="Total transaction amount")
    commission: float = Field(0.0, description="Commission paid")
    transaction_date: datetime = Field(..., description="Transaction date")
    status: str = Field("completed", description="Transaction status")


class Strategy(BaseEntity):
    """Trading strategy representation."""

    user_id: int = Field(..., description="User ID")
    name: str = Field(..., description="Strategy name")
    description: Optional[str] = Field(None, description="Strategy description")
    strategy_type: str = Field(..., description="Strategy type")
    parameters: Dict[str, Any] = Field(
        default_factory=dict, description="Strategy parameters"
    )
    is_active: bool = Field(True, description="Is strategy active")
    is_live: bool = Field(False, description="Is strategy live trading")


class Order(BaseEntity):
    """Order representation."""

    portfolio_id: int = Field(..., description="Portfolio ID")
    symbol: str = Field(..., description="Symbol ticker")
    order_type: str = Field(..., description="Order type (market, limit, stop)")
    side: str = Field(..., description="Order side (buy, sell)")
    quantity: float = Field(..., description="Order quantity")
    price: Optional[float] = Field(None, description="Order price")
    stop_price: Optional[float] = Field(None, description="Stop price")
    status: str = Field("pending", description="Order status")
    filled_quantity: float = Field(0.0, description="Filled quantity")
    average_fill_price: Optional[float] = Field(None, description="Average fill price")
    order_date: datetime = Field(..., description="Order date")


class RiskSettings(BaseEntity):
    """Risk management settings."""

    user_id: int = Field(..., description="User ID")
    portfolio_id: int = Field(..., description="Portfolio ID")
    max_position_size: float = Field(..., description="Maximum position size")
    max_portfolio_risk: float = Field(..., description="Maximum portfolio risk")
    stop_loss_percentage: float = Field(..., description="Stop loss percentage")
    take_profit_percentage: float = Field(..., description="Take profit percentage")
    max_drawdown: float = Field(..., description="Maximum drawdown")
    is_active: bool = Field(True, description="Is risk settings active")


class MarketData(BaseEntity):
    """Market data representation."""

    symbol: str = Field(..., description="Symbol ticker")
    timestamp: datetime = Field(..., description="Data timestamp")
    open_price: float = Field(..., description="Open price")
    high_price: float = Field(..., description="High price")
    low_price: float = Field(..., description="Low price")
    close_price: float = Field(..., description="Close price")
    volume: int = Field(..., description="Volume")
    adjusted_close: Optional[float] = Field(None, description="Adjusted close price")


class ScreeningCriteria(BaseEntity):
    """Stock screening criteria."""

    user_id: int = Field(..., description="User ID")
    name: str = Field(..., description="Screening criteria name")
    criteria: Dict[str, Any] = Field(..., description="Screening criteria")
    is_active: bool = Field(True, description="Is criteria active")


class Notification(BaseEntity):
    """Notification representation."""

    user_id: int = Field(..., description="User ID")
    title: str = Field(..., description="Notification title")
    message: str = Field(..., description="Notification message")
    notification_type: str = Field(..., description="Notification type")
    is_read: bool = Field(False, description="Is notification read")
    priority: str = Field("normal", description="Notification priority")


class ServiceStatus(BaseModel):
    """Service status representation."""

    service_name: str = Field(..., description="Service name")
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="Service version")
    uptime: float = Field(..., description="Service uptime in seconds")
    last_health_check: datetime = Field(..., description="Last health check timestamp")
    dependencies: List[str] = Field(
        default_factory=list, description="Service dependencies"
    )


class APIResponse(BaseModel):
    """Standard API response format."""

    success: bool = Field(..., description="Request success status")
    data: Optional[Any] = Field(None, description="Response data")
    message: Optional[str] = Field(None, description="Response message")
    error: Optional[str] = Field(None, description="Error message")
    timestamp: datetime = Field(
        default_factory=datetime.now, description="Response timestamp"
    )
    request_id: Optional[str] = Field(None, description="Request ID for tracking")


class PaginatedResponse(APIResponse):
    """Paginated API response."""

    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Page size")
    total_pages: int = Field(..., description="Total number of pages")
    total_items: int = Field(..., description="Total number of items")
    has_next: bool = Field(..., description="Has next page")
    has_previous: bool = Field(..., description="Has previous page")


# Enums for common values
class OrderType(str, Enum):
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"


class OrderSide(str, Enum):
    BUY = "buy"
    SELL = "sell"


class OrderStatus(str, Enum):
    PENDING = "pending"
    FILLED = "filled"
    PARTIALLY_FILLED = "partially_filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"


class TransactionType(str, Enum):
    BUY = "buy"
    SELL = "sell"
    DIVIDEND = "dividend"
    SPLIT = "split"
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"


class AssetType(str, Enum):
    STOCK = "stock"
    ETF = "etf"
    OPTION = "option"
    FUTURE = "future"
    FOREX = "forex"
    CRYPTO = "crypto"
    BOND = "bond"


class StrategyType(str, Enum):
    MOMENTUM = "momentum"
    MEAN_REVERSION = "mean_reversion"
    ARBITRAGE = "arbitrage"
    MARKET_NEUTRAL = "market_neutral"
    TREND_FOLLOWING = "trend_following"
    SCALPING = "scalping"
    SWING = "swing"
    POSITION = "position"
