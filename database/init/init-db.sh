#!/bin/bash
# Database initialization script for Bifrost Trader

set -e

echo "🚀 Initializing Bifrost Trader Database..."

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL to be ready..."
until pg_isready -h postgres -p 5432 -U ${DB_USERNAME:-postgres}; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 2
done

echo "✅ PostgreSQL is ready!"

# Create database if it doesn't exist
echo "📊 Creating database if it doesn't exist..."
psql -h postgres -U ${DB_USERNAME:-postgres} -d postgres -c "CREATE DATABASE ${DB_NAME:-bifrost_trader};" || echo "Database already exists"

# Run schema creation
echo "🏗️ Creating database schema..."
psql -h postgres -U ${DB_USERNAME:-postgres} -d ${DB_NAME:-bifrost_trader} -f /docker-entrypoint-initdb.d/bifrost_trader_schema.sql

# Create service users
echo "👥 Creating service users..."
psql -h postgres -U ${DB_USERNAME:-postgres} -d ${DB_NAME:-bifrost_trader} << EOF
-- Data Service User
CREATE USER IF NOT EXISTS bifrost_data_service WITH PASSWORD 'data_service_password';
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO bifrost_data_service;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO bifrost_data_service;

-- Portfolio Service User
CREATE USER IF NOT EXISTS bifrost_portfolio_service WITH PASSWORD 'portfolio_service_password';
GRANT SELECT, INSERT, UPDATE ON portfolio, holding, transaction, "order", trade, cash_balance, funding TO bifrost_portfolio_service;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO bifrost_portfolio_service;

-- Strategy Service User
CREATE USER IF NOT EXISTS bifrost_strategy_service WITH PASSWORD 'strategy_service_password';
GRANT SELECT, INSERT, UPDATE ON strategy, screening, rating, snapshot_screening, snapshot_overview, snapshot_technical, snapshot_fundamental, snapshot_setup, snapshot_bull_flag, snapshot_earning TO bifrost_strategy_service;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO bifrost_strategy_service;

-- Trading Service User
CREATE USER IF NOT EXISTS bifrost_trading_service WITH PASSWORD 'trading_service_password';
GRANT SELECT, INSERT, UPDATE ON "order", trade, transaction TO bifrost_trading_service;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO bifrost_trading_service;

-- Web Portal User (read-only)
CREATE USER IF NOT EXISTS bifrost_web_portal WITH PASSWORD 'web_portal_password';
GRANT SELECT ON ALL TABLES IN SCHEMA public TO bifrost_web_portal;
EOF

# Insert initial data
echo "📝 Inserting initial data..."
psql -h postgres -U ${DB_USERNAME:-postgres} -d ${DB_NAME:-bifrost_trader} << EOF
-- Insert sample market symbols
INSERT INTO market_symbol (symbol, name, market, asset_type, status) VALUES
('AAPL', 'Apple Inc.', 'NASDAQ', 'Stock', 'ACTIVE'),
('MSFT', 'Microsoft Corporation', 'NASDAQ', 'Stock', 'ACTIVE'),
('GOOGL', 'Alphabet Inc.', 'NASDAQ', 'Stock', 'ACTIVE'),
('AMZN', 'Amazon.com Inc.', 'NASDAQ', 'Stock', 'ACTIVE'),
('TSLA', 'Tesla Inc.', 'NASDAQ', 'Stock', 'ACTIVE'),
('META', 'Meta Platforms Inc.', 'NASDAQ', 'Stock', 'ACTIVE'),
('NVDA', 'NVIDIA Corporation', 'NASDAQ', 'Stock', 'ACTIVE'),
('NFLX', 'Netflix Inc.', 'NASDAQ', 'Stock', 'ACTIVE'),
('AMD', 'Advanced Micro Devices Inc.', 'NASDAQ', 'Stock', 'ACTIVE'),
('INTC', 'Intel Corporation', 'NASDAQ', 'Stock', 'ACTIVE')
ON CONFLICT (symbol) DO NOTHING;

-- Insert sample market stock data
INSERT INTO market_stock (symbol, short_name, long_name, industry, sector, exchange) VALUES
('AAPL', 'Apple', 'Apple Inc.', 'Consumer Electronics', 'Technology', 'NASDAQ'),
('MSFT', 'Microsoft', 'Microsoft Corporation', 'Software', 'Technology', 'NASDAQ'),
('GOOGL', 'Alphabet', 'Alphabet Inc.', 'Internet Content & Information', 'Technology', 'NASDAQ'),
('AMZN', 'Amazon', 'Amazon.com Inc.', 'E-commerce', 'Consumer Discretionary', 'NASDAQ'),
('TSLA', 'Tesla', 'Tesla Inc.', 'Electric Vehicles', 'Consumer Discretionary', 'NASDAQ')
ON CONFLICT (symbol) DO NOTHING;
EOF

echo "✅ Database initialization completed successfully!"

# Test connections
echo "🔍 Testing database connections..."
psql -h postgres -U ${DB_USERNAME:-postgres} -d ${DB_NAME:-bifrost_trader} -c "SELECT COUNT(*) as market_symbols FROM market_symbol;"
psql -h postgres -U ${DB_USERNAME:-postgres} -d ${DB_NAME:-bifrost_trader} -c "SELECT COUNT(*) as strategy_categories FROM strategy_category;"

echo "🎉 Bifrost Trader Database is ready!"
