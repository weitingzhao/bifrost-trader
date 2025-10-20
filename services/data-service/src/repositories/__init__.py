"""
Repository layer for Data Service - Data Access Pattern

This module implements the repository pattern for clean data access,
following FastAPI best practices with async support.
"""

from .base import BaseRepository
from .market_data import MarketDataRepository
from .market_reference import MarketReferenceRepository

__all__ = [
    "BaseRepository",
    "MarketDataRepository", 
    "MarketReferenceRepository",
]

