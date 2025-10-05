#!/usr/bin/env python3
"""
Database initialization script for Bifrost Trader Web Portal

This script initializes the database with sample data for testing the web portal.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'shared'))

from database.connection import get_db_connection
from datetime import datetime, timedelta
import random

def init_sample_data():
    """Initialize database with sample data."""
    db = get_db_connection()
    
    print("🚀 Initializing Bifrost Trader database with sample data...")
    
    try:
        # Test database connection
        if not db.test_connection():
            print("❌ Database connection failed!")
            return False
        
        print("✅ Database connection successful!")
        
        # Insert sample market symbols
        print("📊 Inserting sample market symbols...")
        symbols_data = [
            ('AAPL', 'Apple Inc.', 'NASDAQ', 'Stock', 'ACTIVE'),
            ('MSFT', 'Microsoft Corporation', 'NASDAQ', 'Stock', 'ACTIVE'),
            ('GOOGL', 'Alphabet Inc.', 'NASDAQ', 'Stock', 'ACTIVE'),
            ('AMZN', 'Amazon.com Inc.', 'NASDAQ', 'Stock', 'ACTIVE'),
            ('TSLA', 'Tesla Inc.', 'NASDAQ', 'Stock', 'ACTIVE'),
            ('META', 'Meta Platforms Inc.', 'NASDAQ', 'Stock', 'ACTIVE'),
            ('NVDA', 'NVIDIA Corporation', 'NASDAQ', 'Stock', 'ACTIVE'),
            ('NFLX', 'Netflix Inc.', 'NASDAQ', 'Stock', 'ACTIVE'),
            ('AMD', 'Advanced Micro Devices Inc.', 'NASDAQ', 'Stock', 'ACTIVE'),
            ('INTC', 'Intel Corporation', 'NASDAQ', 'Stock', 'ACTIVE'),
            ('SPY', 'SPDR S&P 500 ETF Trust', 'NYSE', 'ETF', 'ACTIVE'),
            ('QQQ', 'Invesco QQQ Trust', 'NASDAQ', 'ETF', 'ACTIVE'),
            ('DIA', 'SPDR Dow Jones Industrial Average ETF', 'NYSE', 'ETF', 'ACTIVE'),
            ('VIX', 'CBOE Volatility Index', 'CBOE', 'Index', 'ACTIVE')
        ]
        
        for symbol, name, market, asset_type, status in symbols_data:
            query = """
            INSERT INTO market_symbol (symbol, name, market, asset_type, status, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (symbol) DO NOTHING
            """
            db.execute_insert(query, (symbol, name, market, asset_type, status, datetime.now(), datetime.now()))
        
        print(f"✅ Inserted {len(symbols_data)} market symbols")
        
        # Insert sample market stock data
        print("🏢 Inserting sample market stock data...")
        stock_data = [
            ('AAPL', 'Apple', 'Apple Inc.', 'Consumer Electronics', 'Technology', 'NASDAQ'),
            ('MSFT', 'Microsoft', 'Microsoft Corporation', 'Software', 'Technology', 'NASDAQ'),
            ('GOOGL', 'Alphabet', 'Alphabet Inc.', 'Internet Content & Information', 'Technology', 'NASDAQ'),
            ('AMZN', 'Amazon', 'Amazon.com Inc.', 'E-commerce', 'Consumer Discretionary', 'NASDAQ'),
            ('TSLA', 'Tesla', 'Tesla Inc.', 'Electric Vehicles', 'Consumer Discretionary', 'NASDAQ'),
            ('META', 'Meta', 'Meta Platforms Inc.', 'Social Media', 'Technology', 'NASDAQ'),
            ('NVDA', 'NVIDIA', 'NVIDIA Corporation', 'Semiconductors', 'Technology', 'NASDAQ'),
            ('NFLX', 'Netflix', 'Netflix Inc.', 'Streaming Services', 'Consumer Discretionary', 'NASDAQ'),
            ('AMD', 'AMD', 'Advanced Micro Devices Inc.', 'Semiconductors', 'Technology', 'NASDAQ'),
            ('INTC', 'Intel', 'Intel Corporation', 'Semiconductors', 'Technology', 'NASDAQ')
        ]
        
        for symbol, short_name, long_name, industry, sector, exchange in stock_data:
            query = """
            INSERT INTO market_stock (symbol, short_name, long_name, industry, sector, exchange, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (symbol) DO NOTHING
            """
            db.execute_insert(query, (symbol, short_name, long_name, industry, sector, exchange, datetime.now(), datetime.now()))
        
        print(f"✅ Inserted {len(stock_data)} market stock records")
        
        # Insert sample portfolio
        print("💼 Inserting sample portfolio...")
        portfolio_query = """
        INSERT INTO portfolio (user_id, name, description, initial_capital, current_value, cash_balance, is_active, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING
        RETURNING portfolio_id
        """
        
        portfolio_result = db.execute_query(portfolio_query, (1, 'Main Portfolio', 'Primary trading portfolio', 100000.00, 105000.00, 25000.00, True, datetime.now(), datetime.now()))
        
        if portfolio_result:
            portfolio_id = portfolio_result[0]['portfolio_id']
            print(f"✅ Created portfolio with ID: {portfolio_id}")
            
            # Insert sample holdings
            print("📈 Inserting sample holdings...")
            holdings_data = [
                ('AAPL', 100, 170.00, 175.50),
                ('MSFT', 50, 380.00, 385.25),
                ('GOOGL', 25, 140.00, 142.80),
                ('TSLA', 20, 200.00, 195.75),
                ('NVDA', 30, 450.00, 465.20)
            ]
            
            for symbol, quantity, avg_price, current_price in holdings_data:
                market_value = quantity * current_price
                unrealized_pnl = market_value - (quantity * avg_price)
                unrealized_pnl_percent = (unrealized_pnl / (quantity * avg_price)) * 100
                
                query = """
                INSERT INTO holding (portfolio_id, symbol, quantity, average_price, current_price, market_value, unrealized_pnl, unrealized_pnl_percent, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (portfolio_id, symbol) DO UPDATE SET
                    quantity = EXCLUDED.quantity,
                    current_price = EXCLUDED.current_price,
                    market_value = EXCLUDED.market_value,
                    unrealized_pnl = EXCLUDED.unrealized_pnl,
                    unrealized_pnl_percent = EXCLUDED.unrealized_pnl_percent,
                    updated_at = EXCLUDED.updated_at
                """
                db.execute_insert(query, (portfolio_id, symbol, quantity, avg_price, current_price, market_value, unrealized_pnl, unrealized_pnl_percent, datetime.now(), datetime.now()))
            
            print(f"✅ Inserted {len(holdings_data)} holdings")
            
            # Insert sample transactions
            print("💱 Inserting sample transactions...")
            transactions_data = [
                ('AAPL', 'BUY', 100, 170.00, 17000.00, 0.00, 0.00, 17000.00),
                ('MSFT', 'BUY', 50, 380.00, 19000.00, 0.00, 0.00, 19000.00),
                ('GOOGL', 'BUY', 25, 140.00, 3500.00, 0.00, 0.00, 3500.00),
                ('TSLA', 'BUY', 20, 200.00, 4000.00, 0.00, 0.00, 4000.00),
                ('NVDA', 'BUY', 30, 450.00, 13500.00, 0.00, 0.00, 13500.00)
            ]
            
            for symbol, transaction_type, quantity, price, total_amount, commission, tax, net_amount in transactions_data:
                query = """
                INSERT INTO transaction (portfolio_id, symbol, transaction_type, quantity, price, total_amount, commission, tax, net_amount, transaction_date, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                db.execute_insert(query, (portfolio_id, symbol, transaction_type, quantity, price, total_amount, commission, tax, net_amount, datetime.now() - timedelta(days=random.randint(1, 30)), datetime.now()))
            
            print(f"✅ Inserted {len(transactions_data)} transactions")
            
            # Insert sample trades
            print("📊 Inserting sample trades...")
            trades_data = [
                ('AAPL', datetime.now() - timedelta(days=30), None, 170.00, None, 100, 0.00, 0.00, 0.00, 0.00, 0.00, 'OPEN'),
                ('MSFT', datetime.now() - timedelta(days=25), None, 380.00, None, 50, 0.00, 0.00, 0.00, 0.00, 0.00, 'OPEN'),
                ('GOOGL', datetime.now() - timedelta(days=20), None, 140.00, None, 25, 0.00, 0.00, 0.00, 0.00, 0.00, 'OPEN'),
                ('TSLA', datetime.now() - timedelta(days=15), None, 200.00, None, 20, 0.00, 0.00, 0.00, 0.00, 0.00, 'OPEN'),
                ('NVDA', datetime.now() - timedelta(days=10), None, 450.00, None, 30, 0.00, 0.00, 0.00, 0.00, 0.00, 'OPEN')
            ]
            
            for symbol, entry_date, exit_date, entry_price, exit_price, quantity, profit_actual, profit_actual_ratio, commission, tax, net_profit, status in trades_data:
                query = """
                INSERT INTO trade (portfolio_id, symbol, entry_date, exit_date, entry_price, exit_price, quantity, profit_actual, profit_actual_ratio, commission, tax, net_profit, status, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                db.execute_insert(query, (portfolio_id, symbol, entry_date, exit_date, entry_price, exit_price, quantity, profit_actual, profit_actual_ratio, commission, tax, net_profit, status, datetime.now(), datetime.now()))
            
            print(f"✅ Inserted {len(trades_data)} trades")
            
            # Insert cash balance
            print("💰 Inserting cash balance...")
            cash_query = """
            INSERT INTO cash_balance (portfolio_id, balance, currency, balance_date, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
            """
            db.execute_insert(cash_query, (portfolio_id, 25000.00, 'USD', datetime.now(), datetime.now(), datetime.now()))
            print("✅ Inserted cash balance")
        
        print("🎉 Database initialization completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        return False

if __name__ == "__main__":
    success = init_sample_data()
    if success:
        print("\n✅ Bifrost Trader database is ready with sample data!")
        print("🌐 You can now test the web portal at http://localhost:8006")
    else:
        print("\n❌ Database initialization failed!")
        sys.exit(1)
