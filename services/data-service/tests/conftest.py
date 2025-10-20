"""
Pytest configuration and fixtures for Market Data Service tests.
"""

import asyncio
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.database.models import Base
from src.repositories.market_data import MarketDataRepository
from src.repositories.market_reference import MarketReferenceRepository

# Test database URL (use separate test database)
TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/bifrost_trader_test"


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def test_engine():
    """Create test database engine."""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        pool_pre_ping=True,
    )
    
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    # Drop all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create a new database session for a test."""
    async_session = sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
    async with async_session() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture
async def market_reference_repo(db_session):
    """Create MarketReferenceRepository instance for testing."""
    return MarketReferenceRepository(db_session)


@pytest_asyncio.fixture
async def market_data_repo(db_session):
    """Create MarketDataRepository instance for testing."""
    return MarketDataRepository(db_session)


@pytest.fixture
def sample_symbol_data():
    """Sample market symbol data for testing."""
    return {
        "symbol": "AAPL",
        "name": "Apple Inc.",
        "market": "NASDAQ",
        "asset_type": "stock",
        "status": "active",
        "has_company_info": True,
        "is_delisted": False,
    }


@pytest.fixture
def sample_market_data():
    """Sample market data for testing."""
    from datetime import datetime
    
    return {
        "symbol": "AAPL",
        "timestamp": datetime.now(),
        "open_price": 150.00,
        "high_price": 152.00,
        "low_price": 149.00,
        "close_price": 151.50,
        "volume": 1000000,
        "adjusted_close": 151.50,
    }





