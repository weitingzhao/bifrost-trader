"""
Market Data Models for Data Service - SQLAlchemy Implementation

This module contains SQLAlchemy models for market data,
following FastAPI best practices with async support.
"""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class MarketDataModel(Base):
    """Market Data SQLAlchemy model with enhanced features."""

    __tablename__ = "market_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(20), ForeignKey("market_symbol.symbol"), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    open_price = Column(Numeric(15, 4), nullable=False)
    high_price = Column(Numeric(15, 4), nullable=False)
    low_price = Column(Numeric(15, 4), nullable=False)
    close_price = Column(Numeric(15, 4), nullable=False)
    volume = Column(BigInteger, nullable=False)
    adjusted_close = Column(Numeric(15, 4), nullable=True)

    # Metadata
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=False)

    # Additional fields
    vwap = Column(Numeric(15, 4), nullable=True)  # Volume Weighted Average Price
    dividend_amount = Column(Numeric(15, 4), nullable=True)
    split_coefficient = Column(Numeric(15, 4), nullable=True)

    # Relationships
    symbol_ref = relationship("MarketSymbol", backref="market_data_records")

    # Indexes for performance
    __table_args__ = (
        Index("idx_symbol_timestamp", "symbol", "timestamp"),
        Index("idx_timestamp", "timestamp"),
        Index("idx_symbol_created", "symbol", "created_at"),
        UniqueConstraint("symbol", "timestamp", name="symbol_timestamp_unique"),
    )

    def __repr__(self):
        return f"<MarketData(symbol='{self.symbol}', timestamp='{self.timestamp}', close='{self.close_price}')>"

    def to_dict(self):
        """Convert model to dictionary for API responses."""
        return {
            "id": self.id,
            "symbol": self.symbol,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "open_price": float(self.open_price) if self.open_price else None,
            "high_price": float(self.high_price) if self.high_price else None,
            "low_price": float(self.low_price) if self.low_price else None,
            "close_price": float(self.close_price) if self.close_price else None,
            "volume": int(self.volume) if self.volume else None,
            "adjusted_close": float(self.adjusted_close) if self.adjusted_close else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "uuid": str(self.uuid) if self.uuid else None,
            "vwap": float(self.vwap) if self.vwap else None,
            "dividend_amount": float(self.dividend_amount) if self.dividend_amount else None,
            "split_coefficient": float(self.split_coefficient) if self.split_coefficient else None,
        }
