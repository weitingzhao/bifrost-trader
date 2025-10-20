"""
Database Models Registry for Data Service

This module imports all SQLAlchemy models to ensure they are registered
with the Base metadata for proper table creation.
"""

# Import all models to register them with SQLAlchemy
from ..models.market_data import MarketDataModel
from ..models.market_reference import (
    MarketSymbol,
    MarketStockHistoricalBarsByMin,
    MarketStockHistoricalBarsByHour,
    MarketStockHistoricalBarsByDay,
    MarketStockHistoricalBarsByHourExt,
)

# Import Base from one of the model files
from ..models.market_reference import Base

__all__ = [
    "Base",
    "MarketSymbol",
    "MarketDataModel",
    "MarketStockHistoricalBarsByMin",
    "MarketStockHistoricalBarsByHour", 
    "MarketStockHistoricalBarsByDay",
    "MarketStockHistoricalBarsByHourExt",
]




