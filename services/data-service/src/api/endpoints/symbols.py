"""
Symbol management API endpoints.

This module provides REST API endpoints for managing market symbols.
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from ...repositories.market_reference import MarketReferenceRepository
from ...schemas.market_reference import (
    MarketSymbolCreate,
    MarketSymbolListResponse,
    MarketSymbolResponse,
    MarketSymbolUpdate,
)
from ..dependencies import get_db_session

router = APIRouter(prefix="/symbols", tags=["symbols"])


@router.get("", response_model=MarketSymbolListResponse)
async def list_symbols(
    market: Optional[str] = Query(None, description="Filter by market exchange"),
    asset_type: Optional[str] = Query(None, description="Filter by asset type"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(50, ge=1, le=1000, description="Maximum records to return"),
    db: AsyncSession = Depends(get_db_session),
):
    """
    List all market symbols with optional filtering and pagination.
    
    Args:
        market: Filter by market exchange (e.g., "NASDAQ", "NYSE")
        asset_type: Filter by asset type (e.g., "stock", "etf")
        skip: Number of records to skip for pagination
        limit: Maximum number of records to return
        db: Database session
        
    Returns:
        List of market symbols with pagination metadata
    """
    repo = MarketReferenceRepository(db)
    
    symbols = await repo.get_active_symbols(
        market=market,
        asset_type=asset_type,
        skip=skip,
        limit=limit
    )
    
    # Get total count
    filters = {"is_delisted": False, "status": "active"}
    if market:
        filters["market"] = market
    if asset_type:
        filters["asset_type"] = asset_type
    
    total = await repo.count(filters)
    
    return MarketSymbolListResponse(
        symbols=symbols,
        total=total,
        page=skip // limit + 1,
        page_size=limit,
        has_next=(skip + limit) < total,
        has_previous=skip > 0
    )


@router.get("/search", response_model=List[MarketSymbolResponse])
async def search_symbols(
    q: str = Query(..., min_length=1, description="Search query"),
    limit: int = Query(50, ge=1, le=100, description="Maximum results"),
    db: AsyncSession = Depends(get_db_session),
):
    """
    Search symbols by name or symbol ticker.
    
    Args:
        q: Search query string
        limit: Maximum number of results
        db: Database session
        
    Returns:
        List of matching symbols
    """
    repo = MarketReferenceRepository(db)
    symbols = await repo.search_symbols(query=q, limit=limit)
    return symbols


@router.get("/{symbol}", response_model=MarketSymbolResponse)
async def get_symbol(
    symbol: str,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Get detailed information for a specific symbol.
    
    Args:
        symbol: Symbol ticker (e.g., "AAPL")
        db: Database session
        
    Returns:
        Symbol details
        
    Raises:
        HTTPException: 404 if symbol not found
    """
    repo = MarketReferenceRepository(db)
    symbol_obj = await repo.get_by_symbol(symbol)
    
    if not symbol_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Symbol {symbol} not found"
        )
    
    return symbol_obj


@router.post("", response_model=MarketSymbolResponse, status_code=status.HTTP_201_CREATED)
async def create_symbol(
    symbol_data: MarketSymbolCreate,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Create a new market symbol.
    
    Args:
        symbol_data: Symbol data to create
        db: Database session
        
    Returns:
        Created symbol
        
    Raises:
        HTTPException: 409 if symbol already exists
    """
    repo = MarketReferenceRepository(db)
    
    # Check if symbol already exists
    existing = await repo.get_by_symbol(symbol_data.symbol)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Symbol {symbol_data.symbol} already exists"
        )
    
    # Create symbol
    symbol = await repo.create(symbol_data)
    await repo.commit()
    
    return symbol


@router.put("/{symbol}", response_model=MarketSymbolResponse)
async def update_symbol(
    symbol: str,
    symbol_data: MarketSymbolUpdate,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Update an existing market symbol.
    
    Args:
        symbol: Symbol ticker
        symbol_data: Updated symbol data
        db: Database session
        
    Returns:
        Updated symbol
        
    Raises:
        HTTPException: 404 if symbol not found
    """
    repo = MarketReferenceRepository(db)
    
    # Get existing symbol
    symbol_obj = await repo.get_by_symbol(symbol)
    if not symbol_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Symbol {symbol} not found"
        )
    
    # Update symbol
    updated_symbol = await repo.update(symbol_obj, symbol_data)
    await repo.commit()
    
    return updated_symbol


@router.delete("/{symbol}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_symbol(
    symbol: str,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Delete a market symbol.
    
    Args:
        symbol: Symbol ticker
        db: Database session
        
    Raises:
        HTTPException: 404 if symbol not found
    """
    repo = MarketReferenceRepository(db)
    
    # Get existing symbol
    symbol_obj = await repo.get_by_symbol(symbol)
    if not symbol_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Symbol {symbol} not found"
        )
    
    # Delete symbol
    await repo.delete(symbol_obj)
    await repo.commit()


@router.patch("/{symbol}/status", response_model=MarketSymbolResponse)
async def update_symbol_status(
    symbol: str,
    status: str = Query(..., description="New status"),
    db: AsyncSession = Depends(get_db_session),
):
    """
    Update symbol status.
    
    Args:
        symbol: Symbol ticker
        status: New status (e.g., "active", "delisted")
        db: Database session
        
    Returns:
        Updated symbol
        
    Raises:
        HTTPException: 404 if symbol not found
    """
    repo = MarketReferenceRepository(db)
    
    updated_symbol = await repo.update_symbol_status(symbol, status)
    if not updated_symbol:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Symbol {symbol} not found"
        )
    
    await repo.commit()
    return updated_symbol


@router.get("/market/{market}", response_model=List[MarketSymbolResponse])
async def get_symbols_by_market(
    market: str,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Get all symbols for a specific market.
    
    Args:
        market: Market exchange name
        db: Database session
        
    Returns:
        List of symbols for the market
    """
    repo = MarketReferenceRepository(db)
    symbols = await repo.get_symbols_by_market(market)
    return symbols





