"""
Database module for Data Service - Async SQLAlchemy Integration

This module provides async database connection management and utilities
for the data service, following FastAPI best practices.
"""

from .connection import DatabaseManager, get_db_session
from .models import Base

__all__ = [
    "DatabaseManager",
    "get_db_session", 
    "Base",
]




