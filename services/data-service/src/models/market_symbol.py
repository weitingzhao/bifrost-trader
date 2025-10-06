"""
Market Symbol Model for Data Service.
SQLAlchemy model for market symbols.
"""

from datetime import datetime

from sqlalchemy import Boolean, Column, Date, DateTime, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class MarketSymbolModel(Base):
    """Market Symbol SQLAlchemy model."""

    __tablename__ = "market_symbol"

    symbol = Column(String(20), primary_key=True)
    name = Column(String(200), nullable=False)
    market = Column(String(50), nullable=False)
    asset_type = Column(String(50), nullable=False)
    ipo_date = Column(Date, nullable=True)
    delisting_date = Column(Date, nullable=True)
    status = Column(String(20), default="active")
    has_company_info = Column(Boolean, default=False)
    is_delisted = Column(Boolean, default=False)
    min_period_yfinance = Column(String(20), nullable=True)
    daily_period_yfinance = Column(String(20), nullable=True)

    # Metadata
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Additional fields
    description = Column(Text, nullable=True)
    sector = Column(String(100), nullable=True)
    industry = Column(String(100), nullable=True)
    country = Column(String(50), nullable=True)
    currency = Column(String(10), nullable=True)

    def __repr__(self):
        return f"<MarketSymbol(symbol='{self.symbol}', name='{self.name}', market='{self.market}')>"

    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "symbol": self.symbol,
            "name": self.name,
            "market": self.market,
            "asset_type": self.asset_type,
            "ipo_date": self.ipo_date.isoformat() if self.ipo_date else None,
            "delisting_date": self.delisting_date.isoformat()
            if self.delisting_date
            else None,
            "status": self.status,
            "has_company_info": self.has_company_info,
            "is_delisted": self.is_delisted,
            "min_period_yfinance": self.min_period_yfinance,
            "daily_period_yfinance": self.daily_period_yfinance,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "description": self.description,
            "sector": self.sector,
            "industry": self.industry,
            "country": self.country,
            "currency": self.currency,
        }
