"""
Data Service for Bifrost Trader.
Handles market data ingestion, storage, and retrieval.
"""

from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import asyncio

# Import shared utilities (we'll create these locally for now)
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

try:
    from shared.utils import HealthChecker, setup_logging, load_environment, get_database_connection
    from shared.models import MarketSymbol, MarketData, APIResponse, PaginatedResponse
except ImportError:
    # Fallback to local implementations
    class HealthChecker:
        def __init__(self, service_name):
            self.service_name = service_name
        def get_health_status(self):
            return {"status": "healthy", "service": self.service_name}
    
    def setup_logging(service_name):
        import logging
        logging.basicConfig(level=logging.INFO)
        return logging.getLogger(service_name)
    
    def load_environment():
        pass
    
    class APIResponse:
        def __init__(self, success, data, message):
            self.success = success
            self.data = data
            self.message = message
from src.services.yahoo_finance_service import YahooFinanceService
from src.services.data_ingestion_service import DataIngestionService
from src.models.market_symbol import MarketSymbolModel
from src.models.market_data import MarketDataModel
import os


# Load environment variables
load_environment()

# Setup logging
logger = setup_logging("data-service")

# Health checker
health_checker = HealthChecker("data-service")

# Services
yahoo_service = YahooFinanceService()

# Database connection for ingestion service
database_url = f"postgresql://{os.getenv('DB_USERNAME', 'postgres')}:{os.getenv('DB_PASS', '')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '5432')}/{os.getenv('DB_NAME', 'bifrost_trader')}"
ingestion_service = DataIngestionService(database_url)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    logger.info("Starting Data Service...")
    yield
    logger.info("Shutting down Data Service...")


# Create FastAPI app
app = FastAPI(
    title="Bifrost Trader Data Service",
    version="1.0.0",
    description="Market data ingestion and retrieval service",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request, call_next):
    """Add processing time header to responses."""
    start_time = datetime.now()
    response = await call_next(request)
    process_time = (datetime.now() - start_time).total_seconds()
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Health check endpoints
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return health_checker.get_health_status()


@app.get("/ready")
async def readiness_check():
    """Readiness check endpoint."""
    return {"status": "ready", "service": "data-service"}


@app.get("/metrics")
async def metrics():
    """Metrics endpoint."""
    return {
        "service": "data-service",
        "uptime": health_checker.get_uptime(),
        "timestamp": datetime.now().isoformat(),
        "data_sources": ["yahoo_finance", "tradingview"],
        "symbols_tracked": await ingestion_service.get_symbol_count()
    }


# Market Symbol endpoints
@app.get("/symbols", response_model=PaginatedResponse)
async def get_symbols(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=1000),
    market: Optional[str] = Query(None),
    asset_type: Optional[str] = Query(None),
    status: Optional[str] = Query("active")
):
    """Get market symbols with pagination."""
    try:
        symbols = await ingestion_service.get_symbols(
            page=page,
            page_size=page_size,
            market=market,
            asset_type=asset_type,
            status=status
        )
        
        return PaginatedResponse(
            success=True,
            data=symbols["data"],
            page=page,
            page_size=page_size,
            total_pages=symbols["total_pages"],
            total_items=symbols["total_items"],
            has_next=symbols["has_next"],
            has_previous=symbols["has_previous"]
        )
    except Exception as e:
        logger.error(f"Error getting symbols: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/symbols/{symbol}", response_model=APIResponse)
async def get_symbol(symbol: str):
    """Get specific market symbol."""
    try:
        symbol_data = await ingestion_service.get_symbol(symbol)
        if not symbol_data:
            raise HTTPException(status_code=404, detail="Symbol not found")
        
        return APIResponse(
            success=True,
            data=symbol_data,
            message="Symbol retrieved successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting symbol {symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/symbols", response_model=APIResponse)
async def create_symbol(symbol: MarketSymbol):
    """Create new market symbol."""
    try:
        created_symbol = await ingestion_service.create_symbol(symbol)
        return APIResponse(
            success=True,
            data=created_symbol,
            message="Symbol created successfully"
        )
    except Exception as e:
        logger.error(f"Error creating symbol: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/symbols/{symbol}", response_model=APIResponse)
async def update_symbol(symbol: str, symbol_data: MarketSymbol):
    """Update market symbol."""
    try:
        updated_symbol = await ingestion_service.update_symbol(symbol, symbol_data)
        if not updated_symbol:
            raise HTTPException(status_code=404, detail="Symbol not found")
        
        return APIResponse(
            success=True,
            data=updated_symbol,
            message="Symbol updated successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating symbol {symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/symbols/{symbol}", response_model=APIResponse)
async def delete_symbol(symbol: str):
    """Delete market symbol."""
    try:
        success = await ingestion_service.delete_symbol(symbol)
        if not success:
            raise HTTPException(status_code=404, detail="Symbol not found")
        
        return APIResponse(
            success=True,
            message="Symbol deleted successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting symbol {symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Market Data endpoints
@app.get("/data/{symbol}/historical", response_model=APIResponse)
async def get_historical_data(
    symbol: str,
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    period: str = Query("1y", description="Period: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max")
):
    """Get historical market data for a symbol."""
    try:
        # Parse dates
        start_dt = None
        end_dt = None
        
        if start_date:
            start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        if end_date:
            end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        
        data = await ingestion_service.get_historical_data(
            symbol=symbol,
            start_date=start_dt,
            end_date=end_dt,
            period=period
        )
        
        if not data:
            raise HTTPException(status_code=404, detail="No data found for symbol")
        
        return APIResponse(
            success=True,
            data=data,
            message="Historical data retrieved successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting historical data for {symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/data/{symbol}/latest", response_model=APIResponse)
async def get_latest_data(symbol: str):
    """Get latest market data for a symbol."""
    try:
        data = await ingestion_service.get_latest_data(symbol)
        if not data:
            raise HTTPException(status_code=404, detail="No latest data found for symbol")
        
        return APIResponse(
            success=True,
            data=data,
            message="Latest data retrieved successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting latest data for {symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/data/{symbol}/fetch", response_model=APIResponse)
async def fetch_data(symbol: str, period: str = Query("1y")):
    """Fetch and store market data for a symbol."""
    try:
        result = await ingestion_service.fetch_and_store_data(symbol, period)
        return APIResponse(
            success=True,
            data=result,
            message="Data fetched and stored successfully"
        )
    except Exception as e:
        logger.error(f"Error fetching data for {symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/data/batch-fetch", response_model=APIResponse)
async def batch_fetch_data(symbols: List[str], period: str = Query("1y")):
    """Fetch and store market data for multiple symbols."""
    try:
        results = await ingestion_service.batch_fetch_and_store_data(symbols, period)
        return APIResponse(
            success=True,
            data=results,
            message="Batch data fetch completed"
        )
    except Exception as e:
        logger.error(f"Error batch fetching data: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Company Info endpoints
@app.get("/company/{symbol}", response_model=APIResponse)
async def get_company_info(symbol: str):
    """Get company information for a symbol."""
    try:
        info = await yahoo_service.get_company_info(symbol)
        if not info:
            raise HTTPException(status_code=404, detail="Company info not found")
        
        return APIResponse(
            success=True,
            data=info,
            message="Company info retrieved successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting company info for {symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Data validation endpoints
@app.get("/data/{symbol}/validate", response_model=APIResponse)
async def validate_data(symbol: str):
    """Validate data quality for a symbol."""
    try:
        validation_result = await ingestion_service.validate_data_quality(symbol)
        return APIResponse(
            success=True,
            data=validation_result,
            message="Data validation completed"
        )
    except Exception as e:
        logger.error(f"Error validating data for {symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Data statistics endpoints
@app.get("/stats/symbols", response_model=APIResponse)
async def get_symbol_stats():
    """Get symbol statistics."""
    try:
        stats = await ingestion_service.get_symbol_statistics()
        return APIResponse(
            success=True,
            data=stats,
            message="Symbol statistics retrieved successfully"
        )
    except Exception as e:
        logger.error(f"Error getting symbol stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats/data", response_model=APIResponse)
async def get_data_stats():
    """Get data statistics."""
    try:
        stats = ingestion_service.get_ingestion_stats()
        return APIResponse(
            success=True,
            data=stats,
            message="Data statistics retrieved successfully"
        )
    except Exception as e:
        logger.error(f"Error getting data stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# New enhanced endpoints

@app.post("/symbols/{symbol}/ingest")
async def ingest_symbol_data(symbol: str):
    """Ingest all data for a symbol (info + historical + latest price)."""
    try:
        result = await ingestion_service.update_symbol_data(symbol)
        
        if 'error' in result:
            raise HTTPException(status_code=400, detail=result['error'])
        
        return APIResponse(
            success=True,
            data=result,
            message=f"Symbol data ingested successfully for {symbol}"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error ingesting symbol data for {symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/symbols/batch-ingest")
async def batch_ingest_symbols(symbols: List[str]):
    """Batch ingest multiple symbols."""
    try:
        if len(symbols) > 50:  # Limit batch size
            raise HTTPException(status_code=400, detail="Batch size too large. Maximum 50 symbols.")
        
        result = await ingestion_service.batch_ingest_symbols(symbols)
        
        return APIResponse(
            success=True,
            data=result,
            message=f"Batch ingestion completed for {len(symbols)} symbols"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in batch ingestion: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/symbols/{symbol}/info")
async def get_symbol_info(symbol: str):
    """Get comprehensive symbol information."""
    try:
        info = await yahoo_service.get_company_info(symbol)
        
        if not info:
            raise HTTPException(status_code=404, detail=f"Symbol {symbol} not found")
        
        return APIResponse(
            success=True,
            data=info,
            message=f"Symbol info retrieved for {symbol}"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting symbol info for {symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/symbols/{symbol}/latest-price")
async def get_latest_price(symbol: str):
    """Get latest price information for a symbol."""
    try:
        price_info = await yahoo_service.get_latest_price(symbol)
        
        if not price_info:
            raise HTTPException(status_code=404, detail=f"Price data not found for {symbol}")
        
        return APIResponse(
            success=True,
            data=price_info,
            message=f"Latest price retrieved for {symbol}"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting latest price for {symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/symbols/search")
async def search_symbols(query: str = Query(..., min_length=1, max_length=50)):
    """Search for symbols by query."""
    try:
        results = await yahoo_service.search_symbols(query)
        
        return APIResponse(
            success=True,
            data=results,
            message=f"Search completed for query: {query}"
        )
    except Exception as e:
        logger.error(f"Error searching symbols: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/symbols/{symbol}/validate")
async def validate_symbol(symbol: str):
    """Validate if a symbol exists."""
    try:
        is_valid = yahoo_service.validate_symbol(symbol)
        
        return APIResponse(
            success=True,
            data={"symbol": symbol, "valid": is_valid},
            message=f"Symbol validation completed for {symbol}"
        )
    except Exception as e:
        logger.error(f"Error validating symbol {symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8001))
    host = os.getenv("HOST", "0.0.0.0")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )
