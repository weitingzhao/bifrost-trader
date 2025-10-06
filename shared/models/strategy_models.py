"""
Database Models for Bifrost Trader Strategy Service

This module contains SQLAlchemy models for the strategy service microservice.
"""

import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    Date,
    DateTime,
    Decimal,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class StrategyCategory(Base):
    """Strategy categories."""

    __tablename__ = "strategy_category"

    strategy_category_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    strategies = relationship("StrategyStrategyCategory", back_populates="category_ref")


class Strategy(Base):
    """Trading strategies."""

    __tablename__ = "strategy"

    strategy_id = Column(Integer, primary_key=True)
    owner_user_id = Column(Integer)
    name = Column(String(255), nullable=False)
    short_name = Column(String(50))
    description = Column(Text)
    as_of_date = Column(Date, nullable=False)
    custom_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    categories = relationship(
        "StrategyStrategyCategory",
        back_populates="strategy_ref",
        cascade="all, delete-orphan",
    )
    ratings = relationship(
        "Rating", back_populates="strategy_ref", cascade="all, delete-orphan"
    )
    rating_indicator_results = relationship(
        "RatingIndicatorResult",
        back_populates="strategy_ref",
        cascade="all, delete-orphan",
    )


class StrategyStrategyCategory(Base):
    """Junction table for strategy categories."""

    __tablename__ = "strategy_strategy_category"

    strategy_id = Column(Integer, ForeignKey("strategy.strategy_id"), primary_key=True)
    strategy_category_id = Column(
        Integer, ForeignKey("strategy_category.strategy_category_id"), primary_key=True
    )

    # Relationships
    strategy_ref = relationship("Strategy", back_populates="categories")
    category_ref = relationship("StrategyCategory", back_populates="strategies")


class Screening(Base):
    """Stock screening configurations."""

    __tablename__ = "screening"

    screening_id = Column(Integer, primary_key=True)
    owner_user_id = Column(Integer)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    criteria = Column(JSONB)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    snapshot_screenings = relationship(
        "SnapshotScreening", back_populates="screening_ref"
    )


class Rating(Base):
    """Strategy ratings for symbols (TimescaleDB)."""

    __tablename__ = "rating"

    symbol = Column(String(20), nullable=False)
    time = Column(Date, nullable=False)
    strategy_id = Column(Integer, ForeignKey("strategy.strategy_id"), nullable=False)
    score = Column(Decimal(5, 2), nullable=False)

    # Relationships
    strategy_ref = relationship("Strategy", back_populates="ratings")

    __table_args__ = (
        CheckConstraint("symbol IS NOT NULL", name="rating_symbol_not_null"),
        CheckConstraint("time IS NOT NULL", name="rating_time_not_null"),
        CheckConstraint("strategy_id IS NOT NULL", name="rating_strategy_id_not_null"),
    )


class RatingIndicatorResult(Base):
    """Rating indicator results (TimescaleDB)."""

    __tablename__ = "rating_indicator_result"

    symbol = Column(String(20), nullable=False)
    time = Column(DateTime, nullable=False)
    strategy_id = Column(Integer, ForeignKey("strategy.strategy_id"), nullable=False)
    indicator_name = Column(String(100), nullable=False)
    indicator_value = Column(Decimal(15, 4))
    indicator_signal = Column(String(20))

    # Relationships
    strategy_ref = relationship("Strategy", back_populates="rating_indicator_results")

    __table_args__ = (
        CheckConstraint("symbol IS NOT NULL", name="rating_indicator_symbol_not_null"),
        CheckConstraint("time IS NOT NULL", name="rating_indicator_time_not_null"),
        CheckConstraint(
            "strategy_id IS NOT NULL", name="rating_indicator_strategy_id_not_null"
        ),
        CheckConstraint(
            "indicator_name IS NOT NULL", name="rating_indicator_name_not_null"
        ),
    )


class SnapshotScreening(Base):
    """Screening snapshot data (TimescaleDB)."""

    __tablename__ = "snapshot_screening"

    symbol = Column(String(20), nullable=False)
    time = Column(DateTime, nullable=False)
    screening_id = Column(Integer, ForeignKey("screening.screening_id"), nullable=False)
    price = Column(Decimal(15, 4))
    volume = Column(Integer)
    market_cap = Column(Decimal(20, 2))
    pe_ratio = Column(Decimal(10, 4))
    pb_ratio = Column(Decimal(10, 4))
    debt_to_equity = Column(Decimal(10, 4))
    roe = Column(Decimal(10, 4))
    roa = Column(Decimal(10, 4))
    current_ratio = Column(Decimal(10, 4))
    quick_ratio = Column(Decimal(10, 4))

    # Relationships
    screening_ref = relationship("Screening", back_populates="snapshot_screenings")

    __table_args__ = (
        CheckConstraint(
            "symbol IS NOT NULL", name="snapshot_screening_symbol_not_null"
        ),
        CheckConstraint("time IS NOT NULL", name="snapshot_screening_time_not_null"),
        CheckConstraint(
            "screening_id IS NOT NULL", name="snapshot_screening_screening_id_not_null"
        ),
    )


class SnapshotOverview(Base):
    """Overview snapshot data (TimescaleDB)."""

    __tablename__ = "snapshot_overview"

    symbol = Column(String(20), nullable=False)
    time = Column(DateTime, nullable=False)
    name = Column(String(255))
    price = Column(Decimal(15, 4))
    change = Column(Decimal(15, 4))
    change_percent = Column(Decimal(10, 4))
    volume = Column(Integer)
    avg_volume = Column(Integer)
    market_cap = Column(Decimal(20, 2))
    pe_ratio = Column(Decimal(10, 4))
    eps = Column(Decimal(10, 4))
    dividend_yield = Column(Decimal(10, 4))
    beta = Column(Decimal(10, 4))

    __table_args__ = (
        CheckConstraint("symbol IS NOT NULL", name="snapshot_overview_symbol_not_null"),
        CheckConstraint("time IS NOT NULL", name="snapshot_overview_time_not_null"),
    )


class SnapshotTechnical(Base):
    """Technical analysis snapshot data (TimescaleDB)."""

    __tablename__ = "snapshot_technical"

    symbol = Column(String(20), nullable=False)
    time = Column(DateTime, nullable=False)
    sma_20 = Column(Decimal(15, 4))
    sma_50 = Column(Decimal(15, 4))
    sma_200 = Column(Decimal(15, 4))
    ema_12 = Column(Decimal(15, 4))
    ema_26 = Column(Decimal(15, 4))
    macd = Column(Decimal(15, 4))
    macd_signal = Column(Decimal(15, 4))
    macd_histogram = Column(Decimal(15, 4))
    rsi = Column(Decimal(10, 4))
    bollinger_upper = Column(Decimal(15, 4))
    bollinger_middle = Column(Decimal(15, 4))
    bollinger_lower = Column(Decimal(15, 4))
    adx = Column(Decimal(10, 4))
    stochastic_k = Column(Decimal(10, 4))
    stochastic_d = Column(Decimal(10, 4))
    williams_r = Column(Decimal(10, 4))

    __table_args__ = (
        CheckConstraint(
            "symbol IS NOT NULL", name="snapshot_technical_symbol_not_null"
        ),
        CheckConstraint("time IS NOT NULL", name="snapshot_technical_time_not_null"),
    )


class SnapshotFundamental(Base):
    """Fundamental analysis snapshot data (TimescaleDB)."""

    __tablename__ = "snapshot_fundamental"

    symbol = Column(String(20), nullable=False)
    time = Column(DateTime, nullable=False)
    revenue = Column(Decimal(20, 2))
    net_income = Column(Decimal(20, 2))
    total_assets = Column(Decimal(20, 2))
    total_liabilities = Column(Decimal(20, 2))
    shareholders_equity = Column(Decimal(20, 2))
    cash_and_equivalents = Column(Decimal(20, 2))
    total_debt = Column(Decimal(20, 2))
    operating_cash_flow = Column(Decimal(20, 2))
    free_cash_flow = Column(Decimal(20, 2))

    __table_args__ = (
        CheckConstraint(
            "symbol IS NOT NULL", name="snapshot_fundamental_symbol_not_null"
        ),
        CheckConstraint("time IS NOT NULL", name="snapshot_fundamental_time_not_null"),
    )


class SnapshotSetup(Base):
    """Setup analysis snapshot data (TimescaleDB)."""

    __tablename__ = "snapshot_setup"

    symbol = Column(String(20), nullable=False)
    time = Column(DateTime, nullable=False)
    setup_type = Column(String(50))
    setup_score = Column(Decimal(5, 2))
    setup_strength = Column(String(20))
    breakout_price = Column(Decimal(15, 4))
    stop_loss = Column(Decimal(15, 4))
    target_price = Column(Decimal(15, 4))
    risk_reward_ratio = Column(Decimal(10, 4))

    __table_args__ = (
        CheckConstraint("symbol IS NOT NULL", name="snapshot_setup_symbol_not_null"),
        CheckConstraint("time IS NOT NULL", name="snapshot_setup_time_not_null"),
    )


class SnapshotBullFlag(Base):
    """Bull flag pattern snapshot data (TimescaleDB)."""

    __tablename__ = "snapshot_bull_flag"

    symbol = Column(String(20), nullable=False)
    time = Column(DateTime, nullable=False)
    flag_score = Column(Decimal(5, 2))
    flag_strength = Column(String(20))
    pole_height = Column(Decimal(15, 4))
    flag_height = Column(Decimal(15, 4))
    breakout_probability = Column(Decimal(5, 2))

    __table_args__ = (
        CheckConstraint(
            "symbol IS NOT NULL", name="snapshot_bull_flag_symbol_not_null"
        ),
        CheckConstraint("time IS NOT NULL", name="snapshot_bull_flag_time_not_null"),
    )


class SnapshotEarning(Base):
    """Earnings snapshot data (TimescaleDB)."""

    __tablename__ = "snapshot_earning"

    symbol = Column(String(20), nullable=False)
    time = Column(DateTime, nullable=False)
    earnings_date = Column(Date)
    earnings_per_share = Column(Decimal(10, 4))
    revenue_estimate = Column(Decimal(20, 2))
    revenue_actual = Column(Decimal(20, 2))
    eps_estimate = Column(Decimal(10, 4))
    eps_actual = Column(Decimal(10, 4))
    surprise_percent = Column(Decimal(10, 4))

    __table_args__ = (
        CheckConstraint("symbol IS NOT NULL", name="snapshot_earning_symbol_not_null"),
        CheckConstraint("time IS NOT NULL", name="snapshot_earning_time_not_null"),
    )
