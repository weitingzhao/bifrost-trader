"""
Portfolio Service for Bifrost Trader Web Portal

Handles portfolio-related business logic and database operations.
"""

import os
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from sqlalchemy import text
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'shared'))

from database.connection import get_db_connection

class PortfolioService:
    def __init__(self):
        self.db = get_db_connection()
    
    async def get_portfolio_overview(self, user_id: int) -> Dict[str, Any]:
        """Get comprehensive portfolio overview for a user."""
        try:
            # Get user's portfolios
            portfolios_query = """
            SELECT 
                p.portfolio_id,
                p.name,
                p.initial_capital,
                p.current_value,
                p.cash_balance,
                p.is_active,
                p.created_at,
                p.updated_at
            FROM portfolio p
            WHERE p.user_id = :user_id AND p.is_active = true
            ORDER BY p.created_at DESC
            """
            
            portfolios = self.db.execute_query(portfolios_query, (user_id,))
            
            if not portfolios:
                return self._get_empty_portfolio_overview()
            
            # Get the primary portfolio (first active one)
            primary_portfolio = portfolios[0]
            portfolio_id = primary_portfolio['portfolio_id']
            
            # Get portfolio summary
            portfolio_summary = await self._get_portfolio_summary(portfolio_id)
            
            # Get active positions
            active_positions = await self._get_active_positions(portfolio_id)
            
            # Get performance metrics
            performance_metrics = await self._get_performance_metrics(portfolio_id)
            
            # Get risk metrics
            risk_metrics = await self._get_risk_metrics(portfolio_id)
            
            # Get recent activity
            recent_activity = await self._get_recent_activity(portfolio_id)
            
            return {
                "portfolio_summary": portfolio_summary,
                "active_positions": active_positions,
                "performance_metrics": performance_metrics,
                "risk_metrics": risk_metrics,
                "recent_activity": recent_activity,
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error getting portfolio overview: {e}")
            return self._get_empty_portfolio_overview()
    
    async def _get_portfolio_summary(self, portfolio_id: int) -> Dict[str, Any]:
        """Get portfolio summary data."""
        try:
            query = """
            SELECT 
                p.portfolio_id,
                p.name,
                p.initial_capital,
                p.current_value,
                p.cash_balance,
                COALESCE(SUM(h.market_value), 0) as total_holdings_value,
                COALESCE(SUM(h.unrealized_pnl), 0) as total_unrealized_pnl,
                CASE 
                    WHEN SUM(h.market_value) > 0 
                    THEN SUM(h.unrealized_pnl_percent * h.market_value) / SUM(h.market_value)
                    ELSE 0 
                END as weighted_unrealized_pnl_percent
            FROM portfolio p
            LEFT JOIN holding h ON p.portfolio_id = h.portfolio_id
            WHERE p.portfolio_id = :portfolio_id
            GROUP BY p.portfolio_id, p.name, p.initial_capital, p.current_value, p.cash_balance
            """
            
            result = self.db.execute_query(query, (portfolio_id,))
            
            if result:
                portfolio = result[0]
                total_value = float(portfolio['current_value'] or 0)
                initial_capital = float(portfolio['initial_capital'] or 0)
                total_pnl = total_value - initial_capital
                total_pnl_percent = (total_pnl / initial_capital * 100) if initial_capital > 0 else 0
                
                return {
                    "portfolio_id": portfolio['portfolio_id'],
                    "name": portfolio['name'],
                    "total_value": total_value,
                    "initial_capital": initial_capital,
                    "cash_balance": float(portfolio['cash_balance'] or 0),
                    "total_holdings_value": float(portfolio['total_holdings_value'] or 0),
                    "total_unrealized_pnl": float(portfolio['total_unrealized_pnl'] or 0),
                    "total_pnl": total_pnl,
                    "total_pnl_percent": round(total_pnl_percent, 2),
                    "weighted_unrealized_pnl_percent": float(portfolio['weighted_unrealized_pnl_percent'] or 0)
                }
            else:
                return self._get_empty_portfolio_summary()
                
        except Exception as e:
            print(f"Error getting portfolio summary: {e}")
            return self._get_empty_portfolio_summary()
    
    async def _get_active_positions(self, portfolio_id: int) -> List[Dict[str, Any]]:
        """Get active positions for a portfolio."""
        try:
            query = """
            SELECT 
                h.symbol,
                h.quantity,
                h.average_price,
                h.current_price,
                h.market_value,
                h.unrealized_pnl,
                h.unrealized_pnl_percent,
                ms.name as company_name,
                ms_stock.industry,
                ms_stock.sector
            FROM holding h
            LEFT JOIN market_symbol ms ON h.symbol = ms.symbol
            LEFT JOIN market_stock ms_stock ON h.symbol = ms_stock.symbol
            WHERE h.portfolio_id = :portfolio_id AND h.quantity > 0
            ORDER BY h.market_value DESC
            """
            
            results = self.db.execute_query(query, (portfolio_id,))
            
            positions = []
            for row in results:
                positions.append({
                    "symbol": row['symbol'],
                    "company_name": row['company_name'] or row['symbol'],
                    "quantity": row['quantity'],
                    "average_price": float(row['average_price'] or 0),
                    "current_price": float(row['current_price'] or 0),
                    "market_value": float(row['market_value'] or 0),
                    "unrealized_pnl": float(row['unrealized_pnl'] or 0),
                    "unrealized_pnl_percent": float(row['unrealized_pnl_percent'] or 0),
                    "industry": row['industry'],
                    "sector": row['sector']
                })
            
            return positions
            
        except Exception as e:
            print(f"Error getting active positions: {e}")
            return []
    
    async def _get_performance_metrics(self, portfolio_id: int) -> Dict[str, Any]:
        """Get performance metrics for a portfolio."""
        try:
            # Get basic portfolio info
            portfolio_query = """
            SELECT 
                initial_capital,
                current_value,
                created_at
            FROM portfolio 
            WHERE portfolio_id = :portfolio_id
            """
            
            portfolio_result = self.db.execute_query(portfolio_query, (portfolio_id,))
            
            if not portfolio_result:
                return self._get_empty_performance_metrics()
            
            portfolio = portfolio_result[0]
            initial_capital = float(portfolio['initial_capital'] or 0)
            current_value = float(portfolio['current_value'] or 0)
            created_at = portfolio['created_at']
            
            # Calculate basic metrics
            total_return = current_value - initial_capital
            total_return_percent = (total_return / initial_capital * 100) if initial_capital > 0 else 0
            
            # Calculate annualized return
            days_held = (datetime.now() - created_at).days
            annualized_return = 0
            if days_held > 0:
                annualized_return = ((current_value / initial_capital) ** (365 / days_held) - 1) * 100
            
            # Get trade statistics
            trades_query = """
            SELECT 
                COUNT(*) as total_trades,
                COUNT(CASE WHEN profit_actual > 0 THEN 1 END) as winning_trades,
                AVG(profit_actual) as avg_trade,
                MAX(profit_actual) as best_trade,
                MIN(profit_actual) as worst_trade,
                SUM(profit_actual) as total_profit
            FROM trade 
            WHERE portfolio_id = :portfolio_id AND status = 'CLOSED'
            """
            
            trades_result = self.db.execute_query(trades_query, (portfolio_id,))
            
            if trades_result:
                trades = trades_result[0]
                total_trades = trades['total_trades'] or 0
                winning_trades = trades['winning_trades'] or 0
                win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
                avg_trade = float(trades['avg_trade'] or 0)
            else:
                total_trades = 0
                win_rate = 0
                avg_trade = 0
            
            return {
                "total_return": round(total_return, 2),
                "total_return_percent": round(total_return_percent, 2),
                "annualized_return": round(annualized_return, 2),
                "total_trades": total_trades,
                "win_rate": round(win_rate, 2),
                "avg_trade": round(avg_trade, 2),
                "days_held": days_held
            }
            
        except Exception as e:
            print(f"Error getting performance metrics: {e}")
            return self._get_empty_performance_metrics()
    
    async def _get_risk_metrics(self, portfolio_id: int) -> Dict[str, Any]:
        """Get risk metrics for a portfolio."""
        try:
            # Get portfolio value history (simplified - would need actual historical data)
            portfolio_query = """
            SELECT 
                current_value,
                initial_capital
            FROM portfolio 
            WHERE portfolio_id = :portfolio_id
            """
            
            portfolio_result = self.db.execute_query(portfolio_query, (portfolio_id,))
            
            if not portfolio_result:
                return self._get_empty_risk_metrics()
            
            portfolio = portfolio_result[0]
            current_value = float(portfolio['current_value'] or 0)
            
            # Calculate basic risk metrics (simplified)
            # In a real implementation, you'd calculate these from historical data
            portfolio_var = current_value * 0.05  # 5% VaR (simplified)
            
            return {
                "portfolio_var": round(portfolio_var, 2),
                "var_percentile": 95,
                "beta": 1.0,  # Would be calculated from historical data
                "volatility": 0.15,  # Would be calculated from historical data
                "max_drawdown": -0.05,  # Would be calculated from historical data
                "sharpe_ratio": 1.2  # Would be calculated from historical data
            }
            
        except Exception as e:
            print(f"Error getting risk metrics: {e}")
            return self._get_empty_risk_metrics()
    
    async def _get_recent_activity(self, portfolio_id: int, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent trading activity for a portfolio."""
        try:
            query = """
            SELECT 
                t.transaction_id,
                t.symbol,
                t.transaction_type,
                t.quantity,
                t.price,
                t.total_amount,
                t.transaction_date,
                t.notes
            FROM transaction t
            WHERE t.portfolio_id = :portfolio_id
            ORDER BY t.transaction_date DESC
            LIMIT :limit
            """
            
            results = self.db.execute_query(query, (portfolio_id, limit))
            
            activities = []
            for row in results:
                activities.append({
                    "transaction_id": row['transaction_id'],
                    "symbol": row['symbol'],
                    "action": row['transaction_type'],
                    "quantity": row['quantity'],
                    "price": float(row['price'] or 0),
                    "total_amount": float(row['total_amount'] or 0),
                    "timestamp": row['transaction_date'].isoformat() if row['transaction_date'] else None,
                    "notes": row['notes']
                })
            
            return activities
            
        except Exception as e:
            print(f"Error getting recent activity: {e}")
            return []
    
    def _get_empty_portfolio_overview(self) -> Dict[str, Any]:
        """Return empty portfolio overview when no data is available."""
        return {
            "portfolio_summary": self._get_empty_portfolio_summary(),
            "active_positions": [],
            "performance_metrics": self._get_empty_performance_metrics(),
            "risk_metrics": self._get_empty_risk_metrics(),
            "recent_activity": [],
            "last_updated": datetime.now().isoformat()
        }
    
    def _get_empty_portfolio_summary(self) -> Dict[str, Any]:
        """Return empty portfolio summary."""
        return {
            "portfolio_id": None,
            "name": "No Portfolio",
            "total_value": 0.0,
            "initial_capital": 0.0,
            "cash_balance": 0.0,
            "total_holdings_value": 0.0,
            "total_unrealized_pnl": 0.0,
            "total_pnl": 0.0,
            "total_pnl_percent": 0.0,
            "weighted_unrealized_pnl_percent": 0.0
        }
    
    def _get_empty_performance_metrics(self) -> Dict[str, Any]:
        """Return empty performance metrics."""
        return {
            "total_return": 0.0,
            "total_return_percent": 0.0,
            "annualized_return": 0.0,
            "total_trades": 0,
            "win_rate": 0.0,
            "avg_trade": 0.0,
            "days_held": 0
        }
    
    def _get_empty_risk_metrics(self) -> Dict[str, Any]:
        """Return empty risk metrics."""
        return {
            "portfolio_var": 0.0,
            "var_percentile": 95,
            "beta": 0.0,
            "volatility": 0.0,
            "max_drawdown": 0.0,
            "sharpe_ratio": 0.0
        }
    
    async def get_portfolio_positions(self, user_id: int) -> List[Dict[str, Any]]:
        """Get all positions for a user's portfolios."""
        try:
            # Get user's active portfolios
            portfolios_query = """
            SELECT portfolio_id FROM portfolio 
            WHERE user_id = :user_id AND is_active = true
            """
            
            portfolios = self.db.execute_query(portfolios_query, (user_id,))
            
            if not portfolios:
                return []
            
            portfolio_ids = [p['portfolio_id'] for p in portfolios]
            
            # Get positions from all portfolios
            positions_query = """
            SELECT 
                h.portfolio_id,
                h.symbol,
                h.quantity,
                h.average_price,
                h.current_price,
                h.market_value,
                h.unrealized_pnl,
                h.unrealized_pnl_percent,
                ms.name as company_name,
                ms_stock.industry,
                ms_stock.sector,
                p.name as portfolio_name
            FROM holding h
            LEFT JOIN market_symbol ms ON h.symbol = ms.symbol
            LEFT JOIN market_stock ms_stock ON h.symbol = ms_stock.symbol
            LEFT JOIN portfolio p ON h.portfolio_id = p.portfolio_id
            WHERE h.portfolio_id = ANY(:portfolio_ids) AND h.quantity > 0
            ORDER BY h.market_value DESC
            """
            
            results = self.db.execute_query(positions_query, (portfolio_ids,))
            
            positions = []
            for row in results:
                positions.append({
                    "portfolio_id": row['portfolio_id'],
                    "portfolio_name": row['portfolio_name'],
                    "symbol": row['symbol'],
                    "company_name": row['company_name'] or row['symbol'],
                    "quantity": row['quantity'],
                    "average_price": float(row['average_price'] or 0),
                    "current_price": float(row['current_price'] or 0),
                    "market_value": float(row['market_value'] or 0),
                    "unrealized_pnl": float(row['unrealized_pnl'] or 0),
                    "unrealized_pnl_percent": float(row['unrealized_pnl_percent'] or 0),
                    "industry": row['industry'],
                    "sector": row['sector']
                })
            
            return positions
            
        except Exception as e:
            print(f"Error getting portfolio positions: {e}")
            return []
    
    async def get_trading_history(self, user_id: int, limit: int = 50) -> List[Dict[str, Any]]:
        """Get trading history for a user."""
        try:
            # Get user's portfolios
            portfolios_query = """
            SELECT portfolio_id FROM portfolio 
            WHERE user_id = :user_id AND is_active = true
            """
            
            portfolios = self.db.execute_query(portfolios_query, (user_id,))
            
            if not portfolios:
                return []
            
            portfolio_ids = [p['portfolio_id'] for p in portfolios]
            
            # Get trading history
            history_query = """
            SELECT 
                t.transaction_id,
                t.portfolio_id,
                t.symbol,
                t.transaction_type,
                t.quantity,
                t.price,
                t.total_amount,
                t.commission,
                t.tax,
                t.net_amount,
                t.transaction_date,
                t.notes,
                p.name as portfolio_name,
                ms.name as company_name
            FROM transaction t
            LEFT JOIN portfolio p ON t.portfolio_id = p.portfolio_id
            LEFT JOIN market_symbol ms ON t.symbol = ms.symbol
            WHERE t.portfolio_id = ANY(:portfolio_ids)
            ORDER BY t.transaction_date DESC
            LIMIT :limit
            """
            
            results = self.db.execute_query(history_query, (portfolio_ids, limit))
            
            history = []
            for row in results:
                history.append({
                    "transaction_id": row['transaction_id'],
                    "portfolio_id": row['portfolio_id'],
                    "portfolio_name": row['portfolio_name'],
                    "symbol": row['symbol'],
                    "company_name": row['company_name'] or row['symbol'],
                    "action": row['transaction_type'],
                    "quantity": row['quantity'],
                    "price": float(row['price'] or 0),
                    "total_amount": float(row['total_amount'] or 0),
                    "commission": float(row['commission'] or 0),
                    "tax": float(row['tax'] or 0),
                    "net_amount": float(row['net_amount'] or 0),
                    "timestamp": row['transaction_date'].isoformat() if row['transaction_date'] else None,
                    "notes": row['notes']
                })
            
            return history
            
        except Exception as e:
            print(f"Error getting trading history: {e}")
            return []
