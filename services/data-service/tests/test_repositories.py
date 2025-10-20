"""
Integration tests for repositories.
"""

import pytest
from datetime import datetime

from src.schemas.market_reference import MarketSymbolCreate
from src.schemas.market_data import MarketDataCreate


@pytest.mark.asyncio
class TestMarketReferenceRepository:
    """Tests for MarketReferenceRepository."""
    
    async def test_create_symbol(self, market_reference_repo, sample_symbol_data):
        """Test creating a new symbol."""
        symbol_create = MarketSymbolCreate(**sample_symbol_data)
        
        symbol = await market_reference_repo.create(symbol_create)
        await market_reference_repo.commit()
        
        assert symbol.symbol == "AAPL"
        assert symbol.name == "Apple Inc."
        assert symbol.market == "NASDAQ"
    
    async def test_get_by_symbol(self, market_reference_repo, sample_symbol_data):
        """Test retrieving a symbol by ticker."""
        # Create symbol first
        symbol_create = MarketSymbolCreate(**sample_symbol_data)
        await market_reference_repo.create(symbol_create)
        await market_reference_repo.commit()
        
        # Retrieve symbol
        symbol = await market_reference_repo.get_by_symbol("AAPL")
        
        assert symbol is not None
        assert symbol.symbol == "AAPL"
        assert symbol.name == "Apple Inc."
    
    async def test_search_symbols(self, market_reference_repo, sample_symbol_data):
        """Test searching for symbols."""
        # Create symbol first
        symbol_create = MarketSymbolCreate(**sample_symbol_data)
        await market_reference_repo.create(symbol_create)
        await market_reference_repo.commit()
        
        # Search for symbols
        results = await market_reference_repo.search_symbols("Apple", limit=10)
        
        assert len(results) > 0
        assert results[0].name == "Apple Inc."
    
    async def test_get_active_symbols(self, market_reference_repo, sample_symbol_data):
        """Test getting active symbols."""
        # Create symbol first
        symbol_create = MarketSymbolCreate(**sample_symbol_data)
        await market_reference_repo.create(symbol_create)
        await market_reference_repo.commit()
        
        # Get active symbols
        symbols = await market_reference_repo.get_active_symbols(limit=10)
        
        assert len(symbols) > 0
        assert symbols[0].status == "active"
        assert symbols[0].is_delisted == False
    
    async def test_update_symbol_status(self, market_reference_repo, sample_symbol_data):
        """Test updating symbol status."""
        # Create symbol first
        symbol_create = MarketSymbolCreate(**sample_symbol_data)
        await market_reference_repo.create(symbol_create)
        await market_reference_repo.commit()
        
        # Update status
        updated = await market_reference_repo.update_symbol_status("AAPL", "delisted")
        await market_reference_repo.commit()
        
        assert updated is not None
        assert updated.status == "delisted"
    
    async def test_mark_as_delisted(self, market_reference_repo, sample_symbol_data):
        """Test marking a symbol as delisted."""
        # Create symbol first
        symbol_create = MarketSymbolCreate(**sample_symbol_data)
        await market_reference_repo.create(symbol_create)
        await market_reference_repo.commit()
        
        # Mark as delisted
        updated = await market_reference_repo.mark_as_delisted("AAPL")
        await market_reference_repo.commit()
        
        assert updated is not None
        assert updated.is_delisted == True
        assert updated.status == "delisted"
        assert updated.delisting_date is not None


@pytest.mark.asyncio
class TestMarketDataRepository:
    """Tests for MarketDataRepository."""
    
    async def test_create_market_data(self, market_data_repo, market_reference_repo, sample_symbol_data, sample_market_data):
        """Test creating market data."""
        # Create symbol first
        symbol_create = MarketSymbolCreate(**sample_symbol_data)
        await market_reference_repo.create(symbol_create)
        await market_reference_repo.commit()
        
        # Create market data
        data_create = MarketDataCreate(**sample_market_data)
        data = await market_data_repo.create(data_create)
        await market_data_repo.commit()
        
        assert data.symbol == "AAPL"
        assert data.open_price == 150.00
        assert data.close_price == 151.50
    
    async def test_get_latest_data(self, market_data_repo, market_reference_repo, sample_symbol_data, sample_market_data):
        """Test getting latest market data."""
        # Create symbol and data
        symbol_create = MarketSymbolCreate(**sample_symbol_data)
        await market_reference_repo.create(symbol_create)
        await market_reference_repo.commit()
        
        data_create = MarketDataCreate(**sample_market_data)
        await market_data_repo.create(data_create)
        await market_data_repo.commit()
        
        # Get latest data
        latest = await market_data_repo.get_latest_data("AAPL")
        
        assert latest is not None
        assert latest.symbol == "AAPL"
        assert latest.close_price == 151.50
    
    async def test_get_symbol_data_range(self, market_data_repo, market_reference_repo, sample_symbol_data, sample_market_data):
        """Test getting data range for a symbol."""
        # Create symbol and data
        symbol_create = MarketSymbolCreate(**sample_symbol_data)
        await market_reference_repo.create(symbol_create)
        await market_reference_repo.commit()
        
        data_create = MarketDataCreate(**sample_market_data)
        await market_data_repo.create(data_create)
        await market_data_repo.commit()
        
        # Get data range
        data_range = await market_data_repo.get_symbol_data_range("AAPL")
        
        assert data_range is not None
        assert data_range["symbol"] == "AAPL"
        assert "start_timestamp" in data_range
        assert "end_timestamp" in data_range
    
    async def test_get_symbols_with_data(self, market_data_repo, market_reference_repo, sample_symbol_data, sample_market_data):
        """Test getting symbols that have data."""
        # Create symbol and data
        symbol_create = MarketSymbolCreate(**sample_symbol_data)
        await market_reference_repo.create(symbol_create)
        await market_reference_repo.commit()
        
        data_create = MarketDataCreate(**sample_market_data)
        await market_data_repo.create(data_create)
        await market_data_repo.commit()
        
        # Get symbols with data
        symbols = await market_data_repo.get_symbols_with_data(limit=10)
        
        assert len(symbols) > 0
        assert "AAPL" in symbols
    
    async def test_create_or_update(self, market_data_repo, market_reference_repo, sample_symbol_data, sample_market_data):
        """Test create or update functionality."""
        # Create symbol first
        symbol_create = MarketSymbolCreate(**sample_symbol_data)
        await market_reference_repo.create(symbol_create)
        await market_reference_repo.commit()
        
        # First create
        data_create = MarketDataCreate(**sample_market_data)
        data1 = await market_data_repo.create_or_update(data_create)
        await market_data_repo.commit()
        
        # Update with same timestamp
        sample_market_data["close_price"] = 155.00
        data_create2 = MarketDataCreate(**sample_market_data)
        data2 = await market_data_repo.create_or_update(data_create2)
        await market_data_repo.commit()
        
        assert data2.close_price == 155.00
    
    async def test_get_data_statistics(self, market_data_repo, market_reference_repo, sample_symbol_data, sample_market_data):
        """Test getting data statistics."""
        # Create symbol and data
        symbol_create = MarketSymbolCreate(**sample_symbol_data)
        await market_reference_repo.create(symbol_create)
        await market_reference_repo.commit()
        
        data_create = MarketDataCreate(**sample_market_data)
        await market_data_repo.create(data_create)
        await market_data_repo.commit()
        
        # Get statistics
        stats = await market_data_repo.get_data_statistics(symbol="AAPL")
        
        assert stats is not None
        assert stats["symbol"] == "AAPL"
        assert stats["total_records"] > 0
        assert "start_timestamp" in stats
        assert "end_timestamp" in stats





