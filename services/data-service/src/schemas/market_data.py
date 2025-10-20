"""
Pydantic schemas for market data validation and serialization.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, validator


class MarketDataBase(BaseModel):
    """Base schema for market data."""
    
    symbol: str = Field(..., min_length=1, max_length=20, description="Symbol ticker")
    timestamp: datetime = Field(..., description="Data timestamp")
    open_price: float = Field(..., gt=0, description="Open price")
    high_price: float = Field(..., gt=0, description="High price")
    low_price: float = Field(..., gt=0, description="Low price")
    close_price: float = Field(..., gt=0, description="Close price")
    volume: int = Field(..., ge=0, description="Volume")
    adjusted_close: Optional[float] = Field(None, gt=0, description="Adjusted close price")

    @validator('high_price')
    def validate_high_price(cls, v, values):
        """Validate high price is the highest price."""
        if 'open_price' in values and 'low_price' in values and 'close_price' in values:
            prices = [values['open_price'], values['low_price'], values['close_price'], v]
            if v != max(prices):
                raise ValueError('High price must be the highest price')
        return v

    @validator('low_price')
    def validate_low_price(cls, v, values):
        """Validate low price is the lowest price."""
        if 'open_price' in values and 'high_price' in values and 'close_price' in values:
            prices = [values['open_price'], values['high_price'], values['close_price'], v]
            if v != min(prices):
                raise ValueError('Low price must be the lowest price')
        return v

    @validator('symbol')
    def validate_symbol(cls, v):
        """Validate symbol format."""
        if not v.isupper():
            v = v.upper()
        return v


class MarketDataCreate(MarketDataBase):
    """Schema for creating market data."""
    
    vwap: Optional[float] = Field(None, gt=0, description="Volume Weighted Average Price")
    dividend_amount: Optional[float] = Field(None, ge=0, description="Dividend amount")
    split_coefficient: Optional[float] = Field(None, gt=0, description="Stock split coefficient")


class MarketDataUpdate(BaseModel):
    """Schema for updating market data."""
    
    open_price: Optional[float] = Field(None, gt=0, description="Open price")
    high_price: Optional[float] = Field(None, gt=0, description="High price")
    low_price: Optional[float] = Field(None, gt=0, description="Low price")
    close_price: Optional[float] = Field(None, gt=0, description="Close price")
    volume: Optional[int] = Field(None, ge=0, description="Volume")
    adjusted_close: Optional[float] = Field(None, gt=0, description="Adjusted close price")
    vwap: Optional[float] = Field(None, gt=0, description="Volume Weighted Average Price")
    dividend_amount: Optional[float] = Field(None, ge=0, description="Dividend amount")
    split_coefficient: Optional[float] = Field(None, gt=0, description="Stock split coefficient")


class MarketDataResponse(MarketDataBase):
    """Schema for market data API responses."""
    
    id: int = Field(..., description="Record ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    uuid: str = Field(..., description="UUID for external references")
    vwap: Optional[float] = Field(None, description="Volume Weighted Average Price")
    dividend_amount: Optional[float] = Field(None, description="Dividend amount")
    split_coefficient: Optional[float] = Field(None, description="Stock split coefficient")

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class MarketDataListResponse(BaseModel):
    """Schema for market data list API responses."""
    
    data: List[MarketDataResponse] = Field(..., description="List of market data records")
    symbol: str = Field(..., description="Symbol ticker")
    start_timestamp: datetime = Field(..., description="Start timestamp of data range")
    end_timestamp: datetime = Field(..., description="End timestamp of data range")
    total_records: int = Field(..., description="Total number of records")
    page: int = Field(1, description="Current page number")
    page_size: int = Field(50, description="Page size")
    has_next: bool = Field(..., description="Has next page")
    has_previous: bool = Field(..., description="Has previous page")

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


# Common API Response Schemas
class APIResponse(BaseModel):
    """Standard API response format."""
    
    success: bool = Field(..., description="Request success status")
    data: Optional[dict] = Field(None, description="Response data")
    message: Optional[str] = Field(None, description="Response message")
    error: Optional[str] = Field(None, description="Error message")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")
    request_id: Optional[str] = Field(None, description="Request ID for tracking")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class PaginatedResponse(APIResponse):
    """Paginated API response."""
    
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Page size")
    total_pages: int = Field(..., description="Total number of pages")
    total_items: int = Field(..., description="Total number of items")
    has_next: bool = Field(..., description="Has next page")
    has_previous: bool = Field(..., description="Has previous page")


# Bulk Operations Schemas
class BulkMarketDataCreate(BaseModel):
    """Schema for bulk market data creation."""
    
    data: List[MarketDataCreate] = Field(..., min_items=1, max_items=1000, description="List of market data records")
    
    @validator('data')
    def validate_data_consistency(cls, v):
        """Validate data consistency within the bulk request."""
        if not v:
            raise ValueError('Data list cannot be empty')
        
        # Check for duplicate timestamps per symbol
        symbol_timestamps = {}
        for record in v:
            key = (record.symbol, record.timestamp)
            if key in symbol_timestamps:
                raise ValueError(f'Duplicate timestamp {record.timestamp} for symbol {record.symbol}')
            symbol_timestamps[key] = True
        
        return v


class BulkMarketDataResponse(BaseModel):
    """Schema for bulk market data creation response."""
    
    created_count: int = Field(..., description="Number of records created")
    updated_count: int = Field(..., description="Number of records updated")
    failed_count: int = Field(..., description="Number of records that failed")
    errors: List[str] = Field(default_factory=list, description="List of error messages")
    created_records: List[MarketDataResponse] = Field(default_factory=list, description="List of created records")
    
    class Config:
        from_attributes = True

