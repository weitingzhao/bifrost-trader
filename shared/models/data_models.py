"""
Database Models for Bifrost Trader Data Service

This module contains SQLAlchemy models for the data service microservice.
"""

from sqlalchemy import Column, Integer, String, DateTime, Decimal, Boolean, Text, Date, BigInteger, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime
import uuid

Base = declarative_base()

class MarketSymbol(Base):
    """Market symbol master table."""
    __tablename__ = 'market_symbol'
    
    symbol = Column(String(20), primary_key=True)
    name = Column(String(200), nullable=False)
    market = Column(String(50), nullable=False)
    asset_type = Column(String(50), nullable=False)
    ipo_date = Column(Date)
    delisting_date = Column(Date)
    status = Column(String(20), nullable=False)
    has_company_info = Column(Boolean, default=False)
    is_delisted = Column(Boolean, default=False)
    min_period_yfinance = Column(String(20))
    daily_period_yfinance = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    stock = relationship("MarketStock", back_populates="symbol_ref", uselist=False)
    historical_bars_min = relationship("MarketStockHistoricalBarsMin", back_populates="symbol_ref")
    historical_bars_hour = relationship("MarketStockHistoricalBarsHour", back_populates="symbol_ref")
    historical_bars_day = relationship("MarketStockHistoricalBarsDay", back_populates="symbol_ref")

class MarketStock(Base):
    """Detailed company information for stocks."""
    __tablename__ = 'market_stock'
    
    symbol = Column(String(20), ForeignKey('market_symbol.symbol'), primary_key=True)
    underlying_symbol = Column(String(10))
    short_name = Column(String(100))
    long_name = Column(String(200))
    address1 = Column(String(255))
    city = Column(String(100))
    state = Column(String(50))
    zip = Column(String(20))
    country = Column(String(100))
    phone = Column(String(20))
    website = Column(Text)
    industry = Column(String(100))
    sector = Column(String(100))
    long_business_summary = Column(Text)
    full_time_employees = Column(Integer)
    currency = Column(String(10))
    financial_currency = Column(String(10))
    exchange = Column(String(10))
    quote_type = Column(String(10))
    time_zone_full_name = Column(String(50))
    time_zone_short_name = Column(String(10))
    gmt_offset_milliseconds = Column(BigInteger)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    symbol_ref = relationship("MarketSymbol", back_populates="stock")
    risk_metrics = relationship("MarketStockRiskMetrics", back_populates="stock_ref", uselist=False)

class MarketStockRiskMetrics(Base):
    """Risk metrics for market stocks."""
    __tablename__ = 'market_stock_risk_metrics'
    
    symbol = Column(String(20), ForeignKey('market_stock.symbol'), primary_key=True)
    beta = Column(Decimal(10, 4))
    volatility = Column(Decimal(10, 4))
    sharpe_ratio = Column(Decimal(10, 4))
    max_drawdown = Column(Decimal(10, 4))
    var_95 = Column(Decimal(10, 4))
    var_99 = Column(Decimal(10, 4))
    expected_shortfall = Column(Decimal(10, 4))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    stock_ref = relationship("MarketStock", back_populates="risk_metrics")

class MarketStockHistoricalBarsMin(Base):
    """Minute-level historical price data (TimescaleDB)."""
    __tablename__ = 'market_stock_hist_bars_min_ts'
    
    symbol = Column(String(10), ForeignKey('market_symbol.symbol'), nullable=False)
    time = Column(DateTime, nullable=False)
    open = Column(Decimal(15, 4))
    high = Column(Decimal(15, 4))
    low = Column(Decimal(15, 4))
    close = Column(Decimal(15, 4))
    volume = Column(BigInteger)
    adj_close = Column(Decimal(15, 4))
    
    __table_args__ = (
        {'extend_existing': True}
    )
    
    # Relationships
    symbol_ref = relationship("MarketSymbol", back_populates="historical_bars_min")

class MarketStockHistoricalBarsHour(Base):
    """Hourly historical price data (TimescaleDB)."""
    __tablename__ = 'market_stock_hist_bars_hour_ts'
    
    symbol = Column(String(10), ForeignKey('market_symbol.symbol'), nullable=False)
    time = Column(DateTime, nullable=False)
    open = Column(Decimal(15, 4))
    high = Column(Decimal(15, 4))
    low = Column(Decimal(15, 4))
    close = Column(Decimal(15, 4))
    volume = Column(BigInteger)
    adj_close = Column(Decimal(15, 4))
    
    __table_args__ = (
        {'extend_existing': True}
    )
    
    # Relationships
    symbol_ref = relationship("MarketSymbol", back_populates="historical_bars_hour")

class MarketStockHistoricalBarsDay(Base):
    """Daily historical price data (TimescaleDB)."""
    __tablename__ = 'market_stock_hist_bars_day_ts'
    
    symbol = Column(String(10), ForeignKey('market_symbol.symbol'), nullable=False)
    time = Column(DateTime, nullable=False)
    open = Column(Decimal(15, 4))
    high = Column(Decimal(15, 4))
    low = Column(Decimal(15, 4))
    close = Column(Decimal(15, 4))
    volume = Column(BigInteger)
    adj_close = Column(Decimal(15, 4))
    
    __table_args__ = (
        {'extend_existing': True}
    )
    
    # Relationships
    symbol_ref = relationship("MarketSymbol", back_populates="historical_bars_day")

class SnapshotScreening(Base):
    """Screening snapshot data (TimescaleDB)."""
    __tablename__ = 'snapshot_screening'
    
    symbol = Column(String(20), ForeignKey('market_symbol.symbol'), nullable=False)
    time = Column(DateTime, nullable=False)
    screening_id = Column(Integer, nullable=False)
    price = Column(Decimal(15, 4))
    volume = Column(BigInteger)
    market_cap = Column(Decimal(20, 2))
    pe_ratio = Column(Decimal(10, 4))
    pb_ratio = Column(Decimal(10, 4))
    debt_to_equity = Column(Decimal(10, 4))
    roe = Column(Decimal(10, 4))
    roa = Column(Decimal(10, 4))
    current_ratio = Column(Decimal(10, 4))
    quick_ratio = Column(Decimal(10, 4))
    
    __table_args__ = (
        {'extend_existing': True}
    )

class SnapshotOverview(Base):
    """Overview snapshot data (TimescaleDB)."""
    __tablename__ = 'snapshot_overview'
    
    symbol = Column(String(20), ForeignKey('market_symbol.symbol'), nullable=False)
    time = Column(DateTime, nullable=False)
    name = Column(String(255))
    price = Column(Decimal(15, 4))
    change = Column(Decimal(15, 4))
    change_percent = Column(Decimal(10, 4))
    volume = Column(BigInteger)
    avg_volume = Column(BigInteger)
    market_cap = Column(Decimal(20, 2))
    pe_ratio = Column(Decimal(10, 4))
    eps = Column(Decimal(10, 4))
    dividend_yield = Column(Decimal(10, 4))
    beta = Column(Decimal(10, 4))
    
    __table_args__ = (
        {'extend_existing': True}
    )

class SnapshotTechnical(Base):
    """Technical analysis snapshot data (TimescaleDB)."""
    __tablename__ = 'snapshot_technical'
    
    symbol = Column(String(20), ForeignKey('market_symbol.symbol'), nullable=False)
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
        {'extend_existing': True}
    )

class SnapshotFundamental(Base):
    """Fundamental analysis snapshot data (TimescaleDB)."""
    __tablename__ = 'snapshot_fundamental'
    
    symbol = Column(String(20), ForeignKey('market_symbol.symbol'), nullable=False)
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
        {'extend_existing': True}
    )

class SnapshotSetup(Base):
    """Setup analysis snapshot data (TimescaleDB)."""
    __tablename__ = 'snapshot_setup'
    
    symbol = Column(String(20), ForeignKey('market_symbol.symbol'), nullable=False)
    time = Column(DateTime, nullable=False)
    setup_type = Column(String(50))
    setup_score = Column(Decimal(5, 2))
    setup_strength = Column(String(20))
    breakout_price = Column(Decimal(15, 4))
    stop_loss = Column(Decimal(15, 4))
    target_price = Column(Decimal(15, 4))
    risk_reward_ratio = Column(Decimal(10, 4))
    
    __table_args__ = (
        {'extend_existing': True}
    )

class SnapshotBullFlag(Base):
    """Bull flag pattern snapshot data (TimescaleDB)."""
    __tablename__ = 'snapshot_bull_flag'
    
    symbol = Column(String(20), ForeignKey('market_symbol.symbol'), nullable=False)
    time = Column(DateTime, nullable=False)
    flag_score = Column(Decimal(5, 2))
    flag_strength = Column(String(20))
    pole_height = Column(Decimal(15, 4))
    flag_height = Column(Decimal(15, 4))
    breakout_probability = Column(Decimal(5, 2))
    
    __table_args__ = (
        {'extend_existing': True}
    )

class SnapshotEarning(Base):
    """Earnings snapshot data (TimescaleDB)."""
    __tablename__ = 'snapshot_earning'
    
    symbol = Column(String(20), ForeignKey('market_symbol.symbol'), nullable=False)
    time = Column(DateTime, nullable=False)
    earnings_date = Column(Date)
    earnings_per_share = Column(Decimal(10, 4))
    revenue_estimate = Column(Decimal(20, 2))
    revenue_actual = Column(Decimal(20, 2))
    eps_estimate = Column(Decimal(10, 4))
    eps_actual = Column(Decimal(10, 4))
    surprise_percent = Column(Decimal(10, 4))
    
    __table_args__ = (
        {'extend_existing': True}
    )
