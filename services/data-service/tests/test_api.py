"""
API integration tests using httpx and TestClient.
"""

import pytest
from httpx import AsyncClient
from fastapi import status

from main_v2 import app


@pytest.mark.asyncio
class TestHealthEndpoints:
    """Tests for health check endpoints."""
    
    async def test_health_check(self):
        """Test health check endpoint."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/health")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "market-data-service"
    
    async def test_readiness_check(self):
        """Test readiness check endpoint."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/ready")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "status" in data
        assert data["service"] == "market-data-service"
    
    async def test_metrics(self):
        """Test metrics endpoint."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/metrics")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["service"] == "market-data-service"
        assert "database" in data


@pytest.mark.asyncio
class TestSymbolEndpoints:
    """Tests for symbol management endpoints."""
    
    async def test_create_symbol(self):
        """Test creating a new symbol."""
        symbol_data = {
            "symbol": "TSLA",
            "name": "Tesla Inc.",
            "market": "NASDAQ",
            "asset_type": "stock",
            "status": "active",
            "has_company_info": False,
            "is_delisted": False
        }
        
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post("/api/symbols", json=symbol_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["symbol"] == "TSLA"
        assert data["name"] == "Tesla Inc."
    
    async def test_get_symbol(self):
        """Test getting a symbol."""
        # First create a symbol
        symbol_data = {
            "symbol": "MSFT",
            "name": "Microsoft Corporation",
            "market": "NASDAQ",
            "asset_type": "stock",
            "status": "active"
        }
        
        async with AsyncClient(app=app, base_url="http://test") as client:
            await client.post("/api/symbols", json=symbol_data)
            
            # Now get it
            response = await client.get("/api/symbols/MSFT")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["symbol"] == "MSFT"
        assert data["name"] == "Microsoft Corporation"
    
    async def test_list_symbols(self):
        """Test listing symbols with pagination."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/api/symbols?limit=50&skip=0")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "symbols" in data
        assert "total" in data
        assert "page" in data
    
    async def test_search_symbols(self):
        """Test searching for symbols."""
        # Create a symbol first
        symbol_data = {
            "symbol": "GOOGL",
            "name": "Alphabet Inc.",
            "market": "NASDAQ",
            "asset_type": "stock",
            "status": "active"
        }
        
        async with AsyncClient(app=app, base_url="http://test") as client:
            await client.post("/api/symbols", json=symbol_data)
            
            # Search for it
            response = await client.get("/api/symbols/search?q=Alphabet")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
    
    async def test_update_symbol(self):
        """Test updating a symbol."""
        # First create
        symbol_data = {
            "symbol": "META",
            "name": "Meta Platforms Inc.",
            "market": "NASDAQ",
            "asset_type": "stock",
            "status": "active"
        }
        
        async with AsyncClient(app=app, base_url="http://test") as client:
            await client.post("/api/symbols", json=symbol_data)
            
            # Update
            update_data = {"name": "Meta Platforms, Inc."}
            response = await client.put("/api/symbols/META", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "Meta Platforms, Inc."
    
    async def test_delete_symbol(self):
        """Test deleting a symbol."""
        # First create
        symbol_data = {
            "symbol": "NFLX",
            "name": "Netflix Inc.",
            "market": "NASDAQ",
            "asset_type": "stock",
            "status": "active"
        }
        
        async with AsyncClient(app=app, base_url="http://test") as client:
            await client.post("/api/symbols", json=symbol_data)
            
            # Delete
            response = await client.delete("/api/symbols/NFLX")
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
    
    async def test_get_nonexistent_symbol(self):
        """Test getting a non-existent symbol."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/api/symbols/NONEXISTENT")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
class TestMarketDataEndpoints:
    """Tests for market data endpoints."""
    
    async def test_create_market_data(self):
        """Test creating market data."""
        from datetime import datetime
        
        # First create symbol
        symbol_data = {
            "symbol": "AAPL",
            "name": "Apple Inc.",
            "market": "NASDAQ",
            "asset_type": "stock",
            "status": "active"
        }
        
        market_data = {
            "symbol": "AAPL",
            "timestamp": datetime.now().isoformat(),
            "open_price": 150.00,
            "high_price": 152.00,
            "low_price": 149.00,
            "close_price": 151.50,
            "volume": 1000000
        }
        
        async with AsyncClient(app=app, base_url="http://test") as client:
            await client.post("/api/symbols", json=symbol_data)
            response = await client.post("/api/market-data", json=market_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["symbol"] == "AAPL"
        assert data["close_price"] == 151.50
    
    async def test_get_latest_price(self):
        """Test getting latest price."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/api/market-data/AAPL/latest")
        
        # May be 404 if no data exists, which is fine
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
    
    async def test_get_statistics(self):
        """Test getting market data statistics."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/api/market-data/statistics")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "total_records" in data





