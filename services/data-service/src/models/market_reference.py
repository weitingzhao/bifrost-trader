"""
Market Reference Models for Data Service - SQLAlchemy Implementation

This module contains SQLAlchemy models for market reference data,
replacing the Django ORM models with FastAPI-compatible async models.
"""

import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Index,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class MarketSymbol(Base):
    """Market symbol master table - SQLAlchemy implementation."""

    __tablename__ = "market_symbol"

    symbol = Column(String(20), primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    market = Column(String(50), nullable=False)
    asset_type = Column(String(50), nullable=False)
    ipo_date = Column(Date, nullable=True)
    delisting_date = Column(Date, nullable=True)
    status = Column(String(20), nullable=False, default="active")
    has_company_info = Column(Boolean, default=False, nullable=False)
    is_delisted = Column(Boolean, default=False, nullable=False)
    min_period_yfinance = Column(String(20), nullable=True)
    daily_period_yfinance = Column(String(20), nullable=True)
    
    # Metadata fields
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=False)

    # Relationships
    historical_bars_min = relationship(
        "MarketStockHistoricalBarsByMin", 
        back_populates="symbol_ref",
        cascade="all, delete-orphan"
    )
    historical_bars_hour = relationship(
        "MarketStockHistoricalBarsByHour", 
        back_populates="symbol_ref",
        cascade="all, delete-orphan"
    )
    historical_bars_day = relationship(
        "MarketStockHistoricalBarsByDay", 
        back_populates="symbol_ref",
        cascade="all, delete-orphan"
    )
    historical_bars_hour_ext = relationship(
        "MarketStockHistoricalBarsByHourExt", 
        back_populates="symbol_ref",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<MarketSymbol(symbol='{self.symbol}', name='{self.name}')>"

    def to_dict(self):
        """Convert model to dictionary for API responses."""
        return {
            "symbol": self.symbol,
            "name": self.name,
            "market": self.market,
            "asset_type": self.asset_type,
            "ipo_date": self.ipo_date.isoformat() if self.ipo_date is not None else None,
            "delisting_date": self.delisting_date.isoformat() if self.delisting_date is not None else None,
            "status": self.status,
            "has_company_info": self.has_company_info,
            "is_delisted": self.is_delisted,
            "min_period_yfinance": self.min_period_yfinance,
            "daily_period_yfinance": self.daily_period_yfinance,
            "created_at": self.created_at.isoformat() if self.created_at is not None else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at is not None else None,
            "uuid": str(self.uuid) if self.uuid is not None else None,
        }


class MarketStockHistoricalBarsByMin(Base):
    """Minute-level historical price data (TimescaleDB hypertable)."""

    __tablename__ = "market_stock_hist_bars_min_ts"

    symbol = Column(String(10), nullable=False, index=True)
    time = Column(DateTime, nullable=False, index=True)
    open = Column(Numeric(15, 4), nullable=False)
    high = Column(Numeric(15, 4), nullable=False)
    low = Column(Numeric(15, 4), nullable=False)
    close = Column(Numeric(15, 4), nullable=False)
    volume = Column(Numeric(20, 0), nullable=False)
    dividend = Column(Numeric(15, 4), nullable=True)
    stock_splits = Column(Numeric(15, 4), nullable=True)

    # TimescaleDB specific table arguments
    __table_args__ = (
        Index("idx_symbol_time_min", "symbol", "time"),
        UniqueConstraint("symbol", "time", name="symbol_timestamp_min_pk"),
        {"extend_existing": True}
    )

    # Relationships
    symbol_ref = relationship("MarketSymbol", back_populates="historical_bars_min")

    def __repr__(self):
        return f"<MarketStockHistoricalBarsByMin(symbol='{self.symbol}', time='{self.time}')>"

    def to_dict(self):
        """Convert model to dictionary for API responses."""
        return {
            "symbol": self.symbol,
            "time": self.time.isoformat() if self.time is not None else None,
            "open": float(self.open) if self.open is not None else None,
            "high": float(self.high) if self.high is not None else None,
            "low": float(self.low) if self.low is not None else None,
            "close": float(self.close) if self.close is not None else None,
            "volume": float(self.volume) if self.volume is not None else None,
            "dividend": float(self.dividend) if self.dividend is not None else None,
            "stock_splits": float(self.stock_splits) if self.stock_splits is not None else None,
        }


class MarketStockHistoricalBarsByDay(Base):
    """Daily historical price data (TimescaleDB hypertable)."""

    __tablename__ = "market_stock_hist_bars_day_ts"

    symbol = Column(String(10), nullable=False, index=True)
    time = Column(Date, nullable=False, index=True)  # Date field for daily data
    open = Column(Numeric(15, 4), nullable=False)
    high = Column(Numeric(15, 4), nullable=False)
    low = Column(Numeric(15, 4), nullable=False)
    close = Column(Numeric(15, 4), nullable=False)
    volume = Column(Numeric(20, 0), nullable=False)
    dividend = Column(Numeric(15, 4), nullable=True)
    stock_splits = Column(Numeric(15, 4), nullable=True)

    # TimescaleDB specific table arguments
    __table_args__ = (
        Index("idx_symbol_time_day", "symbol", "time"),
        UniqueConstraint("symbol", "time", name="symbol_timestamp_day_pk"),
        {"extend_existing": True}
    )

    # Relationships
    symbol_ref = relationship("MarketSymbol", back_populates="historical_bars_day")

    def __repr__(self):
        return f"<MarketStockHistoricalBarsByDay(symbol='{self.symbol}', time='{self.time}')>"

    def to_dict(self):
        """Convert model to dictionary for API responses."""
        return {
            "symbol": self.symbol,
            "time": self.time.isoformat() if self.time is not None else None,
            "open": float(self.open) if self.open is not None else None,
            "high": float(self.high) if self.high is not None else None,
            "low": float(self.low) if self.low is not None else None,
            "close": float(self.close) if self.close is not None else None,
            "volume": float(self.volume) if self.volume is not None else None,
            "dividend": float(self.dividend) if self.dividend is not None else None,
            "stock_splits": float(self.stock_splits) if self.stock_splits is not None else None,
        }


class MarketStockHistoricalBarsByHour(Base):
    """Hourly historical price data (TimescaleDB hypertable)."""

    __tablename__ = "market_stock_hist_bars_hour_ts"

    symbol = Column(String(10), nullable=False, index=True)
    time = Column(DateTime, nullable=False, index=True)
    open = Column(Numeric(15, 4), nullable=False)
    high = Column(Numeric(15, 4), nullable=False)
    low = Column(Numeric(15, 4), nullable=False)
    close = Column(Numeric(15, 4), nullable=False)
    volume = Column(Numeric(20, 0), nullable=False)
    # Note: dividend and stock_splits not included in hourly data

    # TimescaleDB specific table arguments
    __table_args__ = (
        Index("idx_symbol_time_hour", "symbol", "time"),
        UniqueConstraint("symbol", "time", name="symbol_timestamp_hour_pk"),
        {"extend_existing": True}
    )

    # Relationships
    symbol_ref = relationship("MarketSymbol", back_populates="historical_bars_hour")

    def __repr__(self):
        return f"<MarketStockHistoricalBarsByHour(symbol='{self.symbol}', time='{self.time}')>"

    def to_dict(self):
        """Convert model to dictionary for API responses."""
        return {
            "symbol": self.symbol,
            "time": self.time.isoformat() if self.time else None,
            "open": float(self.open) if self.open else None,
            "high": float(self.high) if self.high else None,
            "low": float(self.low) if self.low else None,
            "close": float(self.close) if self.close else None,
            "volume": float(self.volume) if self.volume else None,
        }


class MarketStockHistoricalBarsByHourExt(Base):
    """Extended hourly historical price data (TimescaleDB hypertable)."""

    __tablename__ = "market_stock_hist_bars_hour_ext_ts"

    symbol = Column(String(10), nullable=False, index=True)
    time = Column(DateTime, nullable=False, index=True)
    open = Column(Numeric(15, 4), nullable=False)
    high = Column(Numeric(15, 4), nullable=False)
    low = Column(Numeric(15, 4), nullable=False)
    close = Column(Numeric(15, 4), nullable=False)
    volume = Column(Numeric(20, 0), nullable=False)

    # TimescaleDB specific table arguments
    __table_args__ = (
        Index("idx_symbol_time_hour_ext", "symbol", "time"),
        UniqueConstraint("symbol", "time", name="symbol_timestamp_hour_extended_pk"),
        {"extend_existing": True}
    )

    # Relationships
    symbol_ref = relationship("MarketSymbol", back_populates="historical_bars_hour_ext")

    def __repr__(self):
        return f"<MarketStockHistoricalBarsByHourExt(symbol='{self.symbol}', time='{self.time}')>"

    def to_dict(self):
        """Convert model to dictionary for API responses."""
        return {
            "symbol": self.symbol,
            "time": self.time.isoformat() if self.time else None,
            "open": float(self.open) if self.open else None,
            "high": float(self.high) if self.high else None,
            "low": float(self.low) if self.low else None,
            "close": float(self.close) if self.close else None,
            "volume": float(self.volume) if self.volume else None,
        }
