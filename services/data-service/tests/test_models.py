"""
Unit tests for SQLAlchemy models.
"""

import pytest
from datetime import datetime, date

from src.models.market_reference import (
    MarketSymbol,
    MarketStockHistoricalBarsByMin,
    MarketStockHistoricalBarsByDay,
)
from src.models.market_data import MarketDataModel


class TestMarketSymbol:
    """Tests for MarketSymbol model."""
    
    def test_market_symbol_creation(self):
        """Test creating a MarketSymbol instance."""
        symbol = MarketSymbol(
            symbol="AAPL",
            name="Apple Inc.",
            market="NASDAQ",
            asset_type="stock",
            status="active"
        )
        
        assert symbol.symbol == "AAPL"
        assert symbol.name == "Apple Inc."
        assert symbol.market == "NASDAQ"
        assert symbol.asset_type == "stock"
        assert symbol.status == "active"
        assert symbol.is_delisted == False
    
    def test_market_symbol_repr(self):
        """Test MarketSymbol __repr__ method."""
        symbol = MarketSymbol(
            symbol="AAPL",
            name="Apple Inc.",
            market="NASDAQ",
            asset_type="stock",
            status="active"
        )
        
        repr_str = repr(symbol)
        assert "AAPL" in repr_str
        assert "Apple Inc." in repr_str
    
    def test_market_symbol_to_dict(self):
        """Test MarketSymbol to_dict method."""
        symbol = MarketSymbol(
            symbol="AAPL",
            name="Apple Inc.",
            market="NASDAQ",
            asset_type="stock",
            status="active",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        symbol_dict = symbol.to_dict()
        
        assert symbol_dict["symbol"] == "AAPL"
        assert symbol_dict["name"] == "Apple Inc."
        assert symbol_dict["market"] == "NASDAQ"
        assert "created_at" in symbol_dict
        assert "updated_at" in symbol_dict


class TestMarketData:
    """Tests for MarketDataModel."""
    
    def test_market_data_creation(self):
        """Test creating a MarketDataModel instance."""
        data = MarketDataModel(
            symbol="AAPL",
            timestamp=datetime.now(),
            open_price=150.00,
            high_price=152.00,
            low_price=149.00,
            close_price=151.50,
            volume=1000000
        )
        
        assert data.symbol == "AAPL"
        assert data.open_price == 150.00
        assert data.high_price == 152.00
        assert data.low_price == 149.00
        assert data.close_price == 151.50
        assert data.volume == 1000000
    
    def test_market_data_to_dict(self):
        """Test MarketDataModel to_dict method."""
        data = MarketDataModel(
            symbol="AAPL",
            timestamp=datetime.now(),
            open_price=150.00,
            high_price=152.00,
            low_price=149.00,
            close_price=151.50,
            volume=1000000,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        data_dict = data.to_dict()
        
        assert data_dict["symbol"] == "AAPL"
        assert data_dict["open_price"] == 150.00
        assert "timestamp" in data_dict
        assert "created_at" in data_dict


class TestHistoricalData:
    """Tests for Historical data models."""
    
    def test_historical_bars_min_creation(self):
        """Test creating a minute bar instance."""
        bar = MarketStockHistoricalBarsByMin(
            symbol="AAPL",
            time=datetime.now(),
            open=150.00,
            high=152.00,
            low=149.00,
            close=151.50,
            volume=1000000
        )
        
        assert bar.symbol == "AAPL"
        assert bar.open == 150.00
        assert bar.high == 152.00
        assert bar.low == 149.00
        assert bar.close == 151.50
    
    def test_historical_bars_day_creation(self):
        """Test creating a daily bar instance."""
        bar = MarketStockHistoricalBarsByDay(
            symbol="AAPL",
            time=date.today(),
            open=150.00,
            high=152.00,
            low=149.00,
            close=151.50,
            volume=1000000
        )
        
        assert bar.symbol == "AAPL"
        assert bar.open == 150.00
        assert isinstance(bar.time, date)
    
    def test_historical_bar_to_dict(self):
        """Test historical bar to_dict method."""
        bar = MarketStockHistoricalBarsByMin(
            symbol="AAPL",
            time=datetime.now(),
            open=150.00,
            high=152.00,
            low=149.00,
            close=151.50,
            volume=1000000
        )
        
        bar_dict = bar.to_dict()
        
        assert bar_dict["symbol"] == "AAPL"
        assert bar_dict["open"] == 150.00
        assert "time" in bar_dict





