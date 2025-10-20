"""
Pydantic schemas for Data Service API validation and serialization.

This module contains Pydantic models for request/response validation,
following FastAPI best practices with proper type hints and validation.
"""

from .market_data import *
from .market_reference import *

__all__ = [
    # Market Reference Schemas
    "MarketSymbolCreate",
    "MarketSymbolUpdate", 
    "MarketSymbolResponse",
    "MarketSymbolListResponse",
    
    # Market Data Schemas
    "MarketDataCreate",
    "MarketDataUpdate",
    "MarketDataResponse",
    "MarketDataListResponse",
    
    # Historical Data Schemas
    "HistoricalBarCreate",
    "HistoricalBarResponse",
    "HistoricalBarListResponse",
    
    # Common Schemas
    "APIResponse",
    "PaginatedResponse",
]

