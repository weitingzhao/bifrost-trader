"""
Yahoo Finance Service for Data Service.
Handles data fetching from Yahoo Finance API.
"""

import yfinance as yf
import pandas as pd
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime, timedelta
import asyncio
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)


class YahooFinanceService:
    """Service for fetching data from Yahoo Finance."""
    
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=10)
        self.logger = logger
    
    async def get_historical_data(self, symbol: str, period: str = "1y", 
                                 start_date: Optional[datetime] = None, 
                                 end_date: Optional[datetime] = None) -> Dict[str, Any]:
        """Get historical data for a symbol."""
        try:
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(
                self.executor,
                self._fetch_historical_data,
                symbol, period, start_date, end_date
            )
            return data
        except Exception as e:
            self.logger.error(f"Error fetching historical data for {symbol}: {e}")
            return {}
    
    def _fetch_historical_data(self, symbol: str, period: str = "1y",
                              start_date: Optional[datetime] = None,
                              end_date: Optional[datetime] = None) -> Dict[str, Any]:
        """Fetch historical data synchronously."""
        try:
            ticker = yf.Ticker(symbol)
            
            if start_date and end_date:
                data = ticker.history(start=start_date, end=end_date)
            else:
                data = ticker.history(period=period)
            
            if data.empty:
                return {}
            
            # Convert to dictionary format
            result = {
                'symbol': symbol,
                'data': [],
                'metadata': {
                    'period': period,
                    'start_date': start_date.isoformat() if start_date else None,
                    'end_date': end_date.isoformat() if end_date else None,
                    'data_points': len(data)
                }
            }
            
            for timestamp, row in data.iterrows():
                result['data'].append({
                    'timestamp': timestamp.isoformat(),
                    'open_price': float(row['Open']),
                    'high_price': float(row['High']),
                    'low_price': float(row['Low']),
                    'close_price': float(row['Close']),
                    'volume': int(row['Volume']),
                    'adjusted_close': float(row['Adj Close']) if 'Adj Close' in row else None
                })
            
            return result
        except Exception as e:
            self.logger.error(f"Error in _fetch_historical_data for {symbol}: {e}")
            return {}
    
    async def get_company_info(self, symbol: str) -> Dict[str, Any]:
        """Get company information."""
        try:
            loop = asyncio.get_event_loop()
            info = await loop.run_in_executor(
                self.executor,
                self._fetch_company_info,
                symbol
            )
            return info
        except Exception as e:
            self.logger.error(f"Error fetching company info for {symbol}: {e}")
            return {}
    
    def _fetch_company_info(self, symbol: str) -> Dict[str, Any]:
        """Fetch company info synchronously."""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            if not info:
                return {}
            
            # Filter and clean the info
            relevant_info = {
                'symbol': symbol,
                'name': info.get('longName', ''),
                'short_name': info.get('shortName', ''),
                'sector': info.get('sector', ''),
                'industry': info.get('industry', ''),
                'country': info.get('country', ''),
                'currency': info.get('currency', ''),
                'market_cap': info.get('marketCap', 0),
                'shares_outstanding': info.get('sharesOutstanding', 0),
                'float_shares': info.get('floatShares', 0),
                'regular_market_price': info.get('regularMarketPrice', 0),
                'previous_close': info.get('previousClose', 0),
                'open': info.get('open', 0),
                'day_low': info.get('dayLow', 0),
                'day_high': info.get('dayHigh', 0),
                'volume': info.get('volume', 0),
                'average_volume': info.get('averageVolume', 0),
                'beta': info.get('beta', 0),
                'pe_ratio': info.get('trailingPE', 0),
                'forward_pe': info.get('forwardPE', 0),
                'peg_ratio': info.get('pegRatio', 0),
                'price_to_book': info.get('priceToBook', 0),
                'dividend_yield': info.get('dividendYield', 0),
                'dividend_rate': info.get('dividendRate', 0),
                'ex_dividend_date': info.get('exDividendDate', 0),
                'payout_ratio': info.get('payoutRatio', 0),
                'earnings_growth': info.get('earningsGrowth', 0),
                'revenue_growth': info.get('revenueGrowth', 0),
                'profit_margins': info.get('profitMargins', 0),
                'operating_margins': info.get('operatingMargins', 0),
                'return_on_assets': info.get('returnOnAssets', 0),
                'return_on_equity': info.get('returnOnEquity', 0),
                'total_debt': info.get('totalDebt', 0),
                'debt_to_equity': info.get('debtToEquity', 0),
                'current_ratio': info.get('currentRatio', 0),
                'quick_ratio': info.get('quickRatio', 0),
                'cash_per_share': info.get('totalCashPerShare', 0),
                'book_value': info.get('bookValue', 0),
                'price_to_sales': info.get('priceToSalesTrailing12Months', 0),
                'enterprise_value': info.get('enterpriseValue', 0),
                'enterprise_to_revenue': info.get('enterpriseToRevenue', 0),
                'enterprise_to_ebitda': info.get('enterpriseToEbitda', 0),
                '52_week_low': info.get('fiftyTwoWeekLow', 0),
                '52_week_high': info.get('fiftyTwoWeekHigh', 0),
                'website': info.get('website', ''),
                'description': info.get('longBusinessSummary', ''),
                'employees': info.get('fullTimeEmployees', 0),
                'city': info.get('city', ''),
                'state': info.get('state', ''),
                'zip': info.get('zip', ''),
                'phone': info.get('phone', ''),
                'fax': info.get('fax', ''),
                'address': info.get('address1', ''),
                'exchange': info.get('exchange', ''),
                'quote_type': info.get('quoteType', ''),
                'market': info.get('market', ''),
                'timezone': info.get('timezone', ''),
                'currency_symbol': info.get('currencySymbol', ''),
                'last_update': datetime.now().isoformat()
            }
            
            return relevant_info
        except Exception as e:
            self.logger.error(f"Error in _fetch_company_info for {symbol}: {e}")
            return {}
    
    async def get_latest_price(self, symbol: str) -> Dict[str, Any]:
        """Get latest price information."""
        try:
            loop = asyncio.get_event_loop()
            price_info = await loop.run_in_executor(
                self.executor,
                self._fetch_latest_price,
                symbol
            )
            return price_info
        except Exception as e:
            self.logger.error(f"Error fetching latest price for {symbol}: {e}")
            return {}
    
    def _fetch_latest_price(self, symbol: str) -> Dict[str, Any]:
        """Fetch latest price synchronously."""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            if not info:
                return {}
            
            return {
                'symbol': symbol,
                'price': info.get('regularMarketPrice', 0),
                'previous_close': info.get('previousClose', 0),
                'open': info.get('open', 0),
                'day_low': info.get('dayLow', 0),
                'day_high': info.get('dayHigh', 0),
                'volume': info.get('volume', 0),
                'market_cap': info.get('marketCap', 0),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Error in _fetch_latest_price for {symbol}: {e}")
            return {}
    
    async def batch_get_data(self, symbols: List[str], period: str = "1y") -> Dict[str, Any]:
        """Get data for multiple symbols in batch."""
        try:
            tasks = [self.get_historical_data(symbol, period) for symbol in symbols]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            batch_result = {
                'symbols': symbols,
                'period': period,
                'results': {},
                'errors': {}
            }
            
            for i, result in enumerate(results):
                symbol = symbols[i]
                if isinstance(result, Exception):
                    batch_result['errors'][symbol] = str(result)
                else:
                    batch_result['results'][symbol] = result
            
            return batch_result
        except Exception as e:
            self.logger.error(f"Error in batch_get_data: {e}")
            return {'error': str(e)}
    
    def validate_symbol(self, symbol: str) -> bool:
        """Validate if symbol exists."""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            return bool(info and 'symbol' in info)
        except Exception:
            return False
    
    async def search_symbols(self, query: str) -> List[Dict[str, Any]]:
        """Search for symbols by query."""
        try:
            # This is a simplified search - in production, you might want to use
            # a more sophisticated search mechanism
            loop = asyncio.get_event_loop()
            results = await loop.run_in_executor(
                self.executor,
                self._search_symbols_sync,
                query
            )
            return results
        except Exception as e:
            self.logger.error(f"Error searching symbols: {e}")
            return []
    
    def _search_symbols_sync(self, query: str) -> List[Dict[str, Any]]:
        """Synchronous symbol search."""
        try:
            # Use yfinance's search functionality
            import yfinance as yf
            
            # Try to get suggestions from Yahoo Finance
            # This is a basic implementation - in production, you might want to use
            # a more sophisticated search mechanism or maintain a symbol database
            results = []
            
            # Common stock symbols to search through (this is a simplified approach)
            common_symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'NFLX', 'AMD', 'INTC']
            
            for symbol in common_symbols:
                if query.upper() in symbol.upper():
                    try:
                        ticker = yf.Ticker(symbol)
                        info = ticker.info
                        if info and 'longName' in info:
                            results.append({
                                'symbol': symbol,
                                'name': info.get('longName', ''),
                                'short_name': info.get('shortName', ''),
                                'exchange': info.get('exchange', ''),
                                'market': info.get('market', ''),
                                'currency': info.get('currency', '')
                            })
                    except Exception:
                        continue
            
            return results[:10]  # Limit to 10 results
        except Exception as e:
            self.logger.error(f"Error in _search_symbols_sync: {e}")
            return []
    
    def __del__(self):
        """Cleanup executor on deletion."""
        if hasattr(self, 'executor'):
            self.executor.shutdown(wait=False)
