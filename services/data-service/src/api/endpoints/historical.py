"""
Historical data API endpoints.

This module provides REST API endpoints for accessing historical price data
from TimescaleDB hypertables.
"""

from datetime import date, datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from ...repositories.market_reference import HistoricalDataRepository
from ...schemas.market_reference import (
    HistoricalBarCreate,
    HistoricalBarListResponse,
    HistoricalBarResponse,
)
from ..dependencies import get_db_session

router = APIRouter(prefix="/historical", tags=["historical-data"])


@router.get("/{symbol}/minute", response_model=HistoricalBarListResponse)
async def get_minute_bars(
    symbol: str,
    start_time: Optional[datetime] = Query(None, description="Start time"),
    end_time: Optional[datetime] = Query(None, description="End time"),
    limit: int = Query(1000, ge=1, le=10000, description="Maximum records"),
    db: AsyncSession = Depends(get_db_session),
):
    """
    Get minute-level historical bars for a symbol.
    
    Args:
        symbol: Symbol ticker
        start_time: Start datetime
        end_time: End datetime
        limit: Maximum number of records
        db: Database session
        
    Returns:
        List of minute bars
    """
    repo = HistoricalDataRepository(db)
    
    bars = await repo.get_historical_bars_min(
        symbol=symbol,
        start_time=start_time,
        end_time=end_time,
        limit=limit
    )
    
    # Get data range
    data_range = await repo.get_data_range(symbol, interval="min")
    
    return HistoricalBarListResponse(
        bars=bars,
        symbol=symbol,
        start_time=data_range["start_time"] if data_range else None,
        end_time=data_range["end_time"] if data_range else None,
        total_bars=len(bars),
        interval="minute"
    )


@router.get("/{symbol}/hour", response_model=HistoricalBarListResponse)
async def get_hour_bars(
    symbol: str,
    start_time: Optional[datetime] = Query(None, description="Start time"),
    end_time: Optional[datetime] = Query(None, description="End time"),
    limit: int = Query(1000, ge=1, le=10000, description="Maximum records"),
    db: AsyncSession = Depends(get_db_session),
):
    """
    Get hourly historical bars for a symbol.
    
    Args:
        symbol: Symbol ticker
        start_time: Start datetime
        end_time: End datetime
        limit: Maximum number of records
        db: Database session
        
    Returns:
        List of hourly bars
    """
    repo = HistoricalDataRepository(db)
    
    bars = await repo.get_historical_bars_hour(
        symbol=symbol,
        start_time=start_time,
        end_time=end_time,
        limit=limit
    )
    
    # Get data range
    data_range = await repo.get_data_range(symbol, interval="hour")
    
    return HistoricalBarListResponse(
        bars=bars,
        symbol=symbol,
        start_time=data_range["start_time"] if data_range else None,
        end_time=data_range["end_time"] if data_range else None,
        total_bars=len(bars),
        interval="hour"
    )


@router.get("/{symbol}/day", response_model=HistoricalBarListResponse)
async def get_day_bars(
    symbol: str,
    start_date: Optional[date] = Query(None, description="Start date"),
    end_date: Optional[date] = Query(None, description="End date"),
    limit: int = Query(1000, ge=1, le=10000, description="Maximum records"),
    db: AsyncSession = Depends(get_db_session),
):
    """
    Get daily historical bars for a symbol.
    
    Args:
        symbol: Symbol ticker
        start_date: Start date
        end_date: End date
        limit: Maximum number of records
        db: Database session
        
    Returns:
        List of daily bars
    """
    repo = HistoricalDataRepository(db)
    
    bars = await repo.get_historical_bars_day(
        symbol=symbol,
        start_date=start_date,
        end_date=end_date,
        limit=limit
    )
    
    # Get data range
    data_range = await repo.get_data_range(symbol, interval="day")
    
    return HistoricalBarListResponse(
        bars=bars,
        symbol=symbol,
        start_time=data_range["start_time"] if data_range else None,
        end_time=data_range["end_time"] if data_range else None,
        total_bars=len(bars),
        interval="day"
    )


@router.get("/{symbol}/latest")
async def get_latest_bar(
    symbol: str,
    interval: str = Query("day", regex="^(min|hour|day)$", description="Data interval"),
    db: AsyncSession = Depends(get_db_session),
):
    """
    Get the latest historical bar for a symbol.
    
    Args:
        symbol: Symbol ticker
        interval: Data interval (min, hour, day)
        db: Database session
        
    Returns:
        Latest historical bar
        
    Raises:
        HTTPException: 404 if no data found
    """
    repo = HistoricalDataRepository(db)
    
    bar = await repo.get_latest_bar(symbol=symbol, interval=interval)
    
    if not bar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No {interval} data found for symbol {symbol}"
        )
    
    return bar


@router.post("/ingest", status_code=status.HTTP_201_CREATED)
async def ingest_historical_data(
    bars: List[HistoricalBarCreate],
    interval: str = Query(..., regex="^(min|hour|day)$", description="Data interval"),
    db: AsyncSession = Depends(get_db_session),
):
    """
    Ingest historical bar data.
    
    Args:
        bars: List of historical bars to ingest
        interval: Data interval (min, hour, day)
        db: Database session
        
    Returns:
        Ingestion result
    """
    repo = HistoricalDataRepository(db)
    
    try:
        created_bars = await repo.create_historical_bars(bars=bars, interval=interval)
        await db.commit()
        
        return {
            "success": True,
            "message": f"Ingested {len(created_bars)} {interval} bars",
            "count": len(created_bars)
        }
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to ingest data: {str(e)}"
        )


@router.get("/{symbol}/range")
async def get_data_range(
    symbol: str,
    interval: str = Query("day", regex="^(min|hour|day)$", description="Data interval"),
    db: AsyncSession = Depends(get_db_session),
):
    """
    Get the date range of available data for a symbol.
    
    Args:
        symbol: Symbol ticker
        interval: Data interval (min, hour, day)
        db: Database session
        
    Returns:
        Data range information
        
    Raises:
        HTTPException: 404 if no data found
    """
    repo = HistoricalDataRepository(db)
    
    data_range = await repo.get_data_range(symbol=symbol, interval=interval)
    
    if not data_range:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No {interval} data found for symbol {symbol}"
        )
    
    return data_range


@router.get("/symbols-with-data", response_model=List[str])
async def get_symbols_with_data(
    interval: str = Query("day", regex="^(min|hour|day)$", description="Data interval"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum symbols"),
    db: AsyncSession = Depends(get_db_session),
):
    """
    Get list of symbols that have historical data.
    
    Args:
        interval: Data interval (min, hour, day)
        limit: Maximum number of symbols
        db: Database session
        
    Returns:
        List of symbol tickers
    """
    repo = HistoricalDataRepository(db)
    symbols = await repo.get_symbols_with_data(interval=interval, limit=limit)
    return symbols





