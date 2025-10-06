"""
Data Ingestion Service for Data Service.
Handles the complete data ingestion pipeline from external sources to database.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

from .yahoo_finance_service import YahooFinanceService
from ..models.market_symbol import MarketSymbolModel
from ..models.market_data import MarketDataModel

logger = logging.getLogger(__name__)


class DataIngestionService:
    """Service for ingesting data from external sources."""
    
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.yahoo_service = YahooFinanceService()
        self.executor = ThreadPoolExecutor(max_workers=5)
        self.logger = logger
    
    async def ingest_symbol_info(self, symbol: str) -> Dict[str, Any]:
        """Ingest company information for a symbol."""
        try:
            # Get company info from Yahoo Finance
            company_info = await self.yahoo_service.get_company_info(symbol)
            
            if not company_info:
                return {'error': f'No company info found for {symbol}'}
            
            # Create or update market symbol
            with self.SessionLocal() as session:
                # Check if symbol exists
                existing_symbol = session.query(MarketSymbolModel).filter(
                    MarketSymbolModel.symbol == symbol
                ).first()
                
                if existing_symbol:
                    # Update existing symbol
                    existing_symbol.name = company_info.get('name', existing_symbol.name)
                    existing_symbol.market = company_info.get('exchange', existing_symbol.market)
                    existing_symbol.asset_type = 'Stock'  # Default to Stock
                    existing_symbol.sector = company_info.get('sector', existing_symbol.sector)
                    existing_symbol.industry = company_info.get('industry', existing_symbol.industry)
                    existing_symbol.country = company_info.get('country', existing_symbol.country)
                    existing_symbol.currency = company_info.get('currency', existing_symbol.currency)
                    existing_symbol.description = company_info.get('description', existing_symbol.description)
                    existing_symbol.has_company_info = True
                    existing_symbol.updated_at = datetime.now()
                else:
                    # Create new symbol
                    new_symbol = MarketSymbolModel(
                        symbol=symbol,
                        name=company_info.get('name', ''),
                        market=company_info.get('exchange', ''),
                        asset_type='Stock',
                        sector=company_info.get('sector', ''),
                        industry=company_info.get('industry', ''),
                        country=company_info.get('country', ''),
                        currency=company_info.get('currency', ''),
                        description=company_info.get('description', ''),
                        has_company_info=True,
                        status='active'
                    )
                    session.add(new_symbol)
                
                session.commit()
                
                return {
                    'symbol': symbol,
                    'status': 'success',
                    'message': f'Symbol info ingested successfully for {symbol}'
                }
                
        except Exception as e:
            self.logger.error(f"Error ingesting symbol info for {symbol}: {e}")
            return {'error': str(e)}
    
    async def ingest_historical_data(self, symbol: str, period: str = "1y") -> Dict[str, Any]:
        """Ingest historical data for a symbol."""
        try:
            # Get historical data from Yahoo Finance
            historical_data = await self.yahoo_service.get_historical_data(symbol, period)
            
            if not historical_data or 'data' not in historical_data:
                return {'error': f'No historical data found for {symbol}'}
            
            # Prepare data for database insertion
            data_points = []
            for data_point in historical_data['data']:
                data_points.append({
                    'symbol': symbol,
                    'timestamp': datetime.fromisoformat(data_point['timestamp'].replace('Z', '+00:00')),
                    'open_price': data_point['open_price'],
                    'high_price': data_point['high_price'],
                    'low_price': data_point['low_price'],
                    'close_price': data_point['close_price'],
                    'volume': data_point['volume'],
                    'adjusted_close': data_point.get('adjusted_close')
                })
            
            # Insert data in batches
            batch_size = 1000
            total_inserted = 0
            
            with self.SessionLocal() as session:
                for i in range(0, len(data_points), batch_size):
                    batch = data_points[i:i + batch_size]
                    
                    # Use bulk insert for performance
                    session.bulk_insert_mappings(MarketDataModel, batch)
                    session.commit()
                    total_inserted += len(batch)
                    
                    self.logger.info(f"Inserted batch {i//batch_size + 1} for {symbol}: {len(batch)} records")
            
            return {
                'symbol': symbol,
                'status': 'success',
                'records_inserted': total_inserted,
                'period': period,
                'message': f'Historical data ingested successfully for {symbol}'
            }
            
        except Exception as e:
            self.logger.error(f"Error ingesting historical data for {symbol}: {e}")
            return {'error': str(e)}
    
    async def ingest_latest_price(self, symbol: str) -> Dict[str, Any]:
        """Ingest latest price data for a symbol."""
        try:
            # Get latest price from Yahoo Finance
            price_info = await self.yahoo_service.get_latest_price(symbol)
            
            if not price_info:
                return {'error': f'No price data found for {symbol}'}
            
            # Create market data record for latest price
            with self.SessionLocal() as session:
                # Check if we already have data for this timestamp
                latest_timestamp = datetime.now().replace(second=0, microsecond=0)
                
                existing_data = session.query(MarketDataModel).filter(
                    MarketDataModel.symbol == symbol,
                    MarketDataModel.timestamp >= latest_timestamp - timedelta(minutes=5)
                ).first()
                
                if not existing_data:
                    # Create new market data record
                    market_data = MarketDataModel(
                        symbol=symbol,
                        timestamp=latest_timestamp,
                        open_price=price_info.get('open', 0),
                        high_price=price_info.get('day_high', 0),
                        low_price=price_info.get('day_low', 0),
                        close_price=price_info.get('price', 0),
                        volume=price_info.get('volume', 0),
                        adjusted_close=price_info.get('price', 0)
                    )
                    session.add(market_data)
                    session.commit()
                    
                    return {
                        'symbol': symbol,
                        'status': 'success',
                        'price': price_info.get('price', 0),
                        'timestamp': latest_timestamp.isoformat(),
                        'message': f'Latest price ingested for {symbol}'
                    }
                else:
                    return {
                        'symbol': symbol,
                        'status': 'skipped',
                        'message': f'Price data already exists for {symbol}'
                    }
                    
        except Exception as e:
            self.logger.error(f"Error ingesting latest price for {symbol}: {e}")
            return {'error': str(e)}
    
    async def batch_ingest_symbols(self, symbols: List[str]) -> Dict[str, Any]:
        """Batch ingest multiple symbols."""
        try:
            results = {
                'symbols': symbols,
                'results': {},
                'errors': {},
                'summary': {
                    'total': len(symbols),
                    'success': 0,
                    'errors': 0
                }
            }
            
            # Process symbols in parallel
            tasks = []
            for symbol in symbols:
                # Ingest both symbol info and historical data
                tasks.append(self.ingest_symbol_info(symbol))
                tasks.append(self.ingest_historical_data(symbol))
            
            # Execute all tasks
            task_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results
            for i, result in enumerate(task_results):
                symbol_index = i // 2
                task_type = 'info' if i % 2 == 0 else 'historical'
                symbol = symbols[symbol_index]
                
                if isinstance(result, Exception):
                    results['errors'][f"{symbol}_{task_type}"] = str(result)
                    results['summary']['errors'] += 1
                else:
                    if symbol not in results['results']:
                        results['results'][symbol] = {}
                    results['results'][symbol][task_type] = result
                    if 'error' not in result:
                        results['summary']['success'] += 1
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error in batch_ingest_symbols: {e}")
            return {'error': str(e)}
    
    async def update_symbol_data(self, symbol: str) -> Dict[str, Any]:
        """Update all data for a symbol (info + historical + latest price)."""
        try:
            results = {
                'symbol': symbol,
                'tasks': {},
                'status': 'success'
            }
            
            # Update symbol info
            info_result = await self.ingest_symbol_info(symbol)
            results['tasks']['info'] = info_result
            
            # Update historical data
            historical_result = await self.ingest_historical_data(symbol)
            results['tasks']['historical'] = historical_result
            
            # Update latest price
            price_result = await self.ingest_latest_price(symbol)
            results['tasks']['price'] = price_result
            
            # Check for errors
            for task_name, task_result in results['tasks'].items():
                if 'error' in task_result:
                    results['status'] = 'partial_success'
                    break
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error updating symbol data for {symbol}: {e}")
            return {'error': str(e)}
    
    def get_ingestion_stats(self) -> Dict[str, Any]:
        """Get ingestion statistics."""
        try:
            with self.SessionLocal() as session:
                # Count symbols
                symbol_count = session.query(MarketSymbolModel).count()
                
                # Count market data records
                data_count = session.query(MarketDataModel).count()
                
                # Get latest data timestamp
                latest_data = session.query(MarketDataModel).order_by(
                    MarketDataModel.timestamp.desc()
                ).first()
                
                return {
                    'symbols_count': symbol_count,
                    'market_data_records': data_count,
                    'latest_data_timestamp': latest_data.timestamp.isoformat() if latest_data else None,
                    'last_updated': datetime.now().isoformat()
                }
                
        except Exception as e:
            self.logger.error(f"Error getting ingestion stats: {e}")
            return {'error': str(e)}
    
    def __del__(self):
        """Cleanup resources."""
        if hasattr(self, 'executor'):
            self.executor.shutdown(wait=False)
        if hasattr(self, 'engine'):
            self.engine.dispose()
