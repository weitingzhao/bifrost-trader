"""
Pydantic schemas for market reference data validation and serialization.
"""

from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, Field, validator


class MarketSymbolBase(BaseModel):
    """Base schema for market symbol data."""
    
    symbol: str = Field(..., min_length=1, max_length=20, description="Symbol ticker")
    name: str = Field(..., min_length=1, max_length=200, description="Company name")
    market: str = Field(..., min_length=1, max_length=50, description="Market exchange")
    asset_type: str = Field(..., min_length=1, max_length=50, description="Asset type")
    ipo_date: Optional[date] = Field(None, description="IPO date")
    delisting_date: Optional[date] = Field(None, description="Delisting date")
    status: str = Field("active", max_length=20, description="Symbol status")
    has_company_info: bool = Field(False, description="Has company information")
    is_delisted: bool = Field(False, description="Is delisted")
    min_period_yfinance: Optional[str] = Field(None, max_length=20, description="Min period for yfinance")
    daily_period_yfinance: Optional[str] = Field(None, max_length=20, description="Daily period for yfinance")

    @validator('symbol')
    def validate_symbol(cls, v):
        """Validate symbol format."""
        if not v.isupper():
            v = v.upper()
        return v

    @validator('delisting_date')
    def validate_delisting_date(cls, v, values):
        """Validate delisting date is after IPO date."""
        if v and 'ipo_date' in values and values['ipo_date']:
            if v <= values['ipo_date']:
                raise ValueError('Delisting date must be after IPO date')
        return v


class MarketSymbolCreate(MarketSymbolBase):
    """Schema for creating a new market symbol."""
    pass


class MarketSymbolUpdate(BaseModel):
    """Schema for updating a market symbol."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=200, description="Company name")
    market: Optional[str] = Field(None, min_length=1, max_length=50, description="Market exchange")
    asset_type: Optional[str] = Field(None, min_length=1, max_length=50, description="Asset type")
    ipo_date: Optional[date] = Field(None, description="IPO date")
    delisting_date: Optional[date] = Field(None, description="Delisting date")
    status: Optional[str] = Field(None, max_length=20, description="Symbol status")
    has_company_info: Optional[bool] = Field(None, description="Has company information")
    is_delisted: Optional[bool] = Field(None, description="Is delisted")
    min_period_yfinance: Optional[str] = Field(None, max_length=20, description="Min period for yfinance")
    daily_period_yfinance: Optional[str] = Field(None, max_length=20, description="Daily period for yfinance")


class MarketSymbolResponse(MarketSymbolBase):
    """Schema for market symbol API responses."""
    
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    uuid: str = Field(..., description="UUID for external references")

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            date: lambda v: v.isoformat()
        }


class MarketSymbolListResponse(BaseModel):
    """Schema for market symbol list API responses."""
    
    symbols: List[MarketSymbolResponse] = Field(..., description="List of market symbols")
    total: int = Field(..., description="Total number of symbols")
    page: int = Field(1, description="Current page number")
    page_size: int = Field(50, description="Page size")
    has_next: bool = Field(..., description="Has next page")
    has_previous: bool = Field(..., description="Has previous page")

    class Config:
        from_attributes = True


# Historical Data Schemas
class HistoricalBarBase(BaseModel):
    """Base schema for historical bar data."""
    
    symbol: str = Field(..., min_length=1, max_length=10, description="Symbol ticker")
    time: datetime = Field(..., description="Bar timestamp")
    open: float = Field(..., gt=0, description="Open price")
    high: float = Field(..., gt=0, description="High price")
    low: float = Field(..., gt=0, description="Low price")
    close: float = Field(..., gt=0, description="Close price")
    volume: float = Field(..., ge=0, description="Volume")

    @validator('high')
    def validate_high(cls, v, values):
        """Validate high is the highest price."""
        if 'open' in values and 'low' in values and 'close' in values:
            prices = [values['open'], values['low'], values['close'], v]
            if v != max(prices):
                raise ValueError('High price must be the highest price')
        return v

    @validator('low')
    def validate_low(cls, v, values):
        """Validate low is the lowest price."""
        if 'open' in values and 'high' in values and 'close' in values:
            prices = [values['open'], values['high'], values['close'], v]
            if v != min(prices):
                raise ValueError('Low price must be the lowest price')
        return v


class HistoricalBarCreate(HistoricalBarBase):
    """Schema for creating historical bar data."""
    
    dividend: Optional[float] = Field(None, ge=0, description="Dividend amount")
    stock_splits: Optional[float] = Field(None, gt=0, description="Stock split coefficient")


class HistoricalBarResponse(HistoricalBarBase):
    """Schema for historical bar API responses."""
    
    dividend: Optional[float] = Field(None, description="Dividend amount")
    stock_splits: Optional[float] = Field(None, description="Stock split coefficient")

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class HistoricalBarListResponse(BaseModel):
    """Schema for historical bar list API responses."""
    
    bars: List[HistoricalBarResponse] = Field(..., description="List of historical bars")
    symbol: str = Field(..., description="Symbol ticker")
    start_time: datetime = Field(..., description="Start time of data range")
    end_time: datetime = Field(..., description="End time of data range")
    total_bars: int = Field(..., description="Total number of bars")
    interval: str = Field(..., description="Data interval (min, hour, day)")

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

