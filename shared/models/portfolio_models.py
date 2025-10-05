"""
Database Models for Bifrost Trader Portfolio Service

This module contains SQLAlchemy models for the portfolio service microservice.
"""

from sqlalchemy import Column, Integer, String, DateTime, Decimal, Boolean, Text, Date, ForeignKey, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
import uuid

Base = declarative_base()

class UserStaticSetting(Base):
    """User static settings for trading preferences."""
    __tablename__ = 'user_static_setting'
    
    user_id = Column(Integer, primary_key=True)
    capital = Column(Decimal(15, 2), default=10000.00)
    risk = Column(Decimal(5, 2), default=0.50)
    rounding = Column(Integer, default=2)
    commission = Column(Decimal(10, 2), default=0.00)
    tax = Column(Decimal(10, 2), default=0.00)
    expect_gain_risk_ratio = Column(Decimal(5, 2), default=2.00)
    position_min = Column(Integer, default=2)
    position_max = Column(Integer, default=2)
    total_risk_cap = Column(Decimal(5, 2), default=10.00)
    net_risk_cap = Column(Decimal(5, 2), default=5.00)
    performance_tracking_date = Column(Date)
    single_max_drawdown = Column(Decimal(5, 2), default=0.10)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Portfolio(Base):
    """User portfolios."""
    __tablename__ = 'portfolio'
    
    portfolio_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    initial_capital = Column(Decimal(15, 2), default=0.00)
    current_value = Column(Decimal(15, 2), default=0.00)
    cash_balance = Column(Decimal(15, 2), default=0.00)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    holdings = relationship("Holding", back_populates="portfolio_ref", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="portfolio_ref", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="portfolio_ref", cascade="all, delete-orphan")
    trades = relationship("Trade", back_populates="portfolio_ref", cascade="all, delete-orphan")
    cash_balances = relationship("CashBalance", back_populates="portfolio_ref", cascade="all, delete-orphan")
    fundings = relationship("Funding", back_populates="portfolio_ref", cascade="all, delete-orphan")
    
    __table_args__ = (
        CheckConstraint('user_id IS NOT NULL', name='portfolio_user_id_not_null'),
    )

class Holding(Base):
    """Stock holdings in portfolios."""
    __tablename__ = 'holding'
    
    holding_id = Column(Integer, primary_key=True)
    portfolio_id = Column(Integer, ForeignKey('portfolio.portfolio_id'), nullable=False)
    symbol = Column(String(20), nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    average_price = Column(Decimal(15, 4), nullable=False, default=0.0000)
    current_price = Column(Decimal(15, 4), default=0.0000)
    market_value = Column(Decimal(15, 2), default=0.00)
    unrealized_pnl = Column(Decimal(15, 2), default=0.00)
    unrealized_pnl_percent = Column(Decimal(10, 4), default=0.0000)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    portfolio_ref = relationship("Portfolio", back_populates="holdings")
    
    __table_args__ = (
        CheckConstraint('portfolio_id IS NOT NULL', name='holding_portfolio_id_not_null'),
        CheckConstraint('symbol IS NOT NULL', name='holding_symbol_not_null'),
    )

class Transaction(Base):
    """Buy/sell transactions."""
    __tablename__ = 'transaction'
    
    transaction_id = Column(Integer, primary_key=True)
    portfolio_id = Column(Integer, ForeignKey('portfolio.portfolio_id'), nullable=False)
    symbol = Column(String(20), nullable=False)
    transaction_type = Column(String(10), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Decimal(15, 4), nullable=False)
    total_amount = Column(Decimal(15, 2), nullable=False)
    commission = Column(Decimal(10, 2), default=0.00)
    tax = Column(Decimal(10, 2), default=0.00)
    net_amount = Column(Decimal(15, 2), nullable=False)
    transaction_date = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    portfolio_ref = relationship("Portfolio", back_populates="transactions")
    
    __table_args__ = (
        CheckConstraint("transaction_type IN ('BUY', 'SELL')", name='transaction_type_check'),
        CheckConstraint('portfolio_id IS NOT NULL', name='transaction_portfolio_id_not_null'),
        CheckConstraint('symbol IS NOT NULL', name='transaction_symbol_not_null'),
    )

class Order(Base):
    """Trading orders."""
    __tablename__ = 'order'
    
    order_id = Column(Integer, primary_key=True)
    portfolio_id = Column(Integer, ForeignKey('portfolio.portfolio_id'), nullable=False)
    symbol = Column(String(20), nullable=False)
    order_type = Column(String(20), nullable=False)
    side = Column(String(10), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Decimal(15, 4))
    stop_price = Column(Decimal(15, 4))
    status = Column(String(20), nullable=False, default='PENDING')
    filled_quantity = Column(Integer, default=0)
    filled_price = Column(Decimal(15, 4))
    time_in_force = Column(String(10), default='GTC')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    filled_at = Column(DateTime)
    
    # Relationships
    portfolio_ref = relationship("Portfolio", back_populates="orders")
    
    __table_args__ = (
        CheckConstraint("order_type IN ('MARKET', 'LIMIT', 'STOP', 'STOP_LIMIT')", name='order_type_check'),
        CheckConstraint("side IN ('BUY', 'SELL')", name='order_side_check'),
        CheckConstraint("status IN ('PENDING', 'FILLED', 'PARTIALLY_FILLED', 'CANCELLED', 'REJECTED')", name='order_status_check'),
        CheckConstraint("time_in_force IN ('GTC', 'IOC', 'FOK', 'DAY')", name='order_time_in_force_check'),
        CheckConstraint('portfolio_id IS NOT NULL', name='order_portfolio_id_not_null'),
        CheckConstraint('symbol IS NOT NULL', name='order_symbol_not_null'),
    )

class Trade(Base):
    """Trade records."""
    __tablename__ = 'trade'
    
    trade_id = Column(Integer, primary_key=True)
    portfolio_id = Column(Integer, ForeignKey('portfolio.portfolio_id'), nullable=False)
    symbol = Column(String(20), nullable=False)
    entry_date = Column(DateTime, nullable=False)
    exit_date = Column(DateTime)
    entry_price = Column(Decimal(15, 4), nullable=False)
    exit_price = Column(Decimal(15, 4))
    quantity = Column(Integer, nullable=False)
    profit_actual = Column(Decimal(15, 2), default=0.00)
    profit_actual_ratio = Column(Decimal(10, 4), default=0.0000)
    commission = Column(Decimal(10, 2), default=0.00)
    tax = Column(Decimal(10, 2), default=0.00)
    net_profit = Column(Decimal(15, 2), default=0.00)
    status = Column(String(20), default='OPEN')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    portfolio_ref = relationship("Portfolio", back_populates="trades")
    
    __table_args__ = (
        CheckConstraint("status IN ('OPEN', 'CLOSED', 'PARTIALLY_CLOSED')", name='trade_status_check'),
        CheckConstraint('portfolio_id IS NOT NULL', name='trade_portfolio_id_not_null'),
        CheckConstraint('symbol IS NOT NULL', name='trade_symbol_not_null'),
    )

class CashBalance(Base):
    """Cash balance tracking."""
    __tablename__ = 'cash_balance'
    
    cash_balance_id = Column(Integer, primary_key=True)
    portfolio_id = Column(Integer, ForeignKey('portfolio.portfolio_id'), nullable=False)
    balance = Column(Decimal(15, 2), nullable=False, default=0.00)
    currency = Column(String(10), default='USD')
    balance_date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    portfolio_ref = relationship("Portfolio", back_populates="cash_balances")
    
    __table_args__ = (
        CheckConstraint('portfolio_id IS NOT NULL', name='cash_balance_portfolio_id_not_null'),
    )

class Funding(Base):
    """Portfolio funding records."""
    __tablename__ = 'funding'
    
    funding_id = Column(Integer, primary_key=True)
    portfolio_id = Column(Integer, ForeignKey('portfolio.portfolio_id'), nullable=False)
    amount = Column(Decimal(15, 2), nullable=False)
    funding_type = Column(String(20), nullable=False)
    funding_date = Column(DateTime, default=datetime.utcnow)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    portfolio_ref = relationship("Portfolio", back_populates="fundings")
    
    __table_args__ = (
        CheckConstraint("funding_type IN ('DEPOSIT', 'WITHDRAWAL', 'DIVIDEND', 'INTEREST')", name='funding_type_check'),
        CheckConstraint('portfolio_id IS NOT NULL', name='funding_portfolio_id_not_null'),
    )

class Wishlist(Base):
    """User watchlists."""
    __tablename__ = 'wishlist'
    
    wishlist_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    symbol = Column(String(20), nullable=False)
    quantity = Column(Integer, default=1)
    target_price = Column(Decimal(15, 4))
    purpose = Column(String(20))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        CheckConstraint("purpose IN ('WATCH', 'BUY', 'EARNING')", name='wishlist_purpose_check'),
        CheckConstraint('user_id IS NOT NULL', name='wishlist_user_id_not_null'),
        CheckConstraint('symbol IS NOT NULL', name='wishlist_symbol_not_null'),
    )
