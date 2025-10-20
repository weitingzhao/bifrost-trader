"""
Market data API endpoints.

This module provides REST API endpoints for accessing and managing market data.
"""

from datetime import datetime
from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from ...repositories.market_data import MarketDataRepository
from ...schemas.market_data import (
    BulkMarketDataCreate,
    BulkMarketDataResponse,
    MarketDataCreate,
    MarketDataListResponse,
    MarketDataResponse,
)
from ..dependencies import get_db_session

router = APIRouter(prefix="/market-data", tags=["market-data"])


@router.get("/{symbol}/latest", response_model=MarketDataResponse)
async def get_latest_price(
    symbol: str,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Get the latest market data for a symbol.
    
    Args:
        symbol: Symbol ticker
        db: Database session
        
    Returns:
        Latest market data
        
    Raises:
        HTTPException: 404 if no data found
    """
    repo = MarketDataRepository(db)
    data = await repo.get_latest_data(symbol)
    
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No data found for symbol {symbol}"
        )
    
    return data


@router.get("/{symbol}", response_model=MarketDataListResponse)
async def get_market_data(
    symbol: str,
    start_date: Optional[datetime] = Query(None, description="Start date"),
    end_date: Optional[datetime] = Query(None, description="End date"),
    limit: int = Query(1000, ge=1, le=10000, description="Maximum records"),
    order_desc: bool = Query(True, description="Order by timestamp descending"),
    db: AsyncSession = Depends(get_db_session),
):
    """
    Get market data for a symbol within a date range.
    
    Args:
        symbol: Symbol ticker
        start_date: Start date for data range
        end_date: End date for data range
        limit: Maximum number of records
        order_desc: Order by timestamp descending
        db: Database session
        
    Returns:
        List of market data records
    """
    repo = MarketDataRepository(db)
    
    data = await repo.get_symbol_data(
        symbol=symbol,
        start_timestamp=start_date,
        end_timestamp=end_date,
        limit=limit,
        order_desc=order_desc
    )
    
    # Get data range
    data_range = await repo.get_symbol_data_range(symbol)
    
    return MarketDataListResponse(
        data=data,
        symbol=symbol,
        start_timestamp=data_range["start_timestamp"] if data_range else None,
        end_timestamp=data_range["end_timestamp"] if data_range else None,
        total_records=len(data),
        page=1,
        page_size=limit,
        has_next=False,  # TODO: Implement proper pagination
        has_previous=False
    )


@router.post("", response_model=MarketDataResponse, status_code=status.HTTP_201_CREATED)
async def create_market_data(
    data: MarketDataCreate,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Create a new market data record.
    
    Args:
        data: Market data to create
        db: Database session
        
    Returns:
        Created market data
    """
    repo = MarketDataRepository(db)
    
    # Create or update
    market_data = await repo.create_or_update(data)
    await repo.commit()
    
    return market_data


@router.post("/bulk", response_model=BulkMarketDataResponse)
async def bulk_create_market_data(
    bulk_data: BulkMarketDataCreate,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Bulk create or update market data records.
    
    Args:
        bulk_data: List of market data records
        db: Database session
        
    Returns:
        Bulk operation results
    """
    repo = MarketDataRepository(db)
    
    created_records = []
    failed_count = 0
    errors = []
    
    try:
        # Bulk create or update
        created_records = await repo.bulk_create_or_update(bulk_data.data)
        await repo.commit()
        
    except Exception as e:
        await repo.rollback()
        failed_count = len(bulk_data.data)
        errors.append(str(e))
    
    return BulkMarketDataResponse(
        created_count=len(created_records),
        updated_count=0,  # TODO: Track separately
        failed_count=failed_count,
        errors=errors,
        created_records=created_records
    )


@router.get("/{symbol}/range")
async def get_data_range(
    symbol: str,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Get the timestamp range of available data for a symbol.
    
    Args:
        symbol: Symbol ticker
        db: Database session
        
    Returns:
        Data range information
        
    Raises:
        HTTPException: 404 if no data found
    """
    repo = MarketDataRepository(db)
    
    data_range = await repo.get_symbol_data_range(symbol)
    if not data_range:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No data found for symbol {symbol}"
        )
    
    return data_range


@router.get("/statistics")
async def get_statistics(
    symbol: Optional[str] = Query(None, description="Symbol for statistics"),
    db: AsyncSession = Depends(get_db_session),
):
    """
    Get market data statistics.
    
    Args:
        symbol: Optional symbol ticker for symbol-specific statistics
        db: Database session
        
    Returns:
        Statistics about market data
    """
    repo = MarketDataRepository(db)
    stats = await repo.get_data_statistics(symbol=symbol)
    return stats


@router.get("/symbols/with-data", response_model=List[str])
async def get_symbols_with_data(
    limit: int = Query(100, ge=1, le=1000, description="Maximum symbols"),
    db: AsyncSession = Depends(get_db_session),
):
    """
    Get list of symbols that have market data.
    
    Args:
        limit: Maximum number of symbols
        db: Database session
        
    Returns:
        List of symbol tickers
    """
    repo = MarketDataRepository(db)
    symbols = await repo.get_symbols_with_data(limit=limit)
    return symbols


@router.get("/latest-prices", response_model=List[MarketDataResponse])
async def get_latest_prices(
    symbols: Optional[List[str]] = Query(None, description="List of symbols"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum symbols"),
    db: AsyncSession = Depends(get_db_session),
):
    """
    Get latest prices for multiple symbols.
    
    Args:
        symbols: Optional list of specific symbols
        limit: Maximum number of symbols if not specified
        db: Database session
        
    Returns:
        Latest prices for symbols
    """
    repo = MarketDataRepository(db)
    prices = await repo.get_latest_prices(symbols=symbols, limit=limit)
    return prices


@router.get("/multiple", response_model=Dict[str, List[MarketDataResponse]])
async def get_multiple_symbols_data(
    symbols: List[str] = Query(..., description="List of symbols"),
    start_date: Optional[datetime] = Query(None, description="Start date"),
    end_date: Optional[datetime] = Query(None, description="End date"),
    limit_per_symbol: int = Query(100, ge=1, le=1000, description="Records per symbol"),
    db: AsyncSession = Depends(get_db_session),
):
    """
    Get market data for multiple symbols.
    
    Args:
        symbols: List of symbol tickers
        start_date: Start date for data range
        end_date: End date for data range
        limit_per_symbol: Maximum records per symbol
        db: Database session
        
    Returns:
        Dictionary mapping symbol to list of market data
    """
    repo = MarketDataRepository(db)
    
    data = await repo.get_multiple_symbols_data(
        symbols=symbols,
        start_timestamp=start_date,
        end_timestamp=end_date,
        limit_per_symbol=limit_per_symbol
    )
    
    return data


@router.delete("/{symbol}/old-data")
async def delete_old_data(
    symbol: str,
    before_date: datetime = Query(..., description="Delete data before this date"),
    db: AsyncSession = Depends(get_db_session),
):
    """
    Delete old market data for a symbol.
    
    Args:
        symbol: Symbol ticker
        before_date: Delete data before this timestamp
        db: Database session
        
    Returns:
        Number of records deleted
    """
    repo = MarketDataRepository(db)
    
    count = await repo.delete_old_data(before_timestamp=before_date)
    await repo.commit()
    
    return {"deleted_count": count, "symbol": symbol}





