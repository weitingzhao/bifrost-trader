-- Bifrost Trader Database Schema
-- Extracted from Smart Trader project
-- PostgreSQL with TimescaleDB extension

-- Enable TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- ==============================================
-- MARKET DATA TABLES
-- ==============================================

-- Market Symbol Master Table
CREATE TABLE market_symbol (
    symbol VARCHAR(20) PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    market VARCHAR(50) NOT NULL,
    asset_type VARCHAR(50) NOT NULL,
    ipo_date DATE,
    delisting_date DATE,
    status VARCHAR(20) NOT NULL,
    has_company_info BOOLEAN DEFAULT FALSE,
    is_delisted BOOLEAN DEFAULT FALSE,
    min_period_yfinance VARCHAR(20),
    daily_period_yfinance VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Market Stock Details
CREATE TABLE market_stock (
    symbol VARCHAR(20) PRIMARY KEY REFERENCES market_symbol(symbol) ON DELETE CASCADE,
    underlying_symbol VARCHAR(10),
    short_name VARCHAR(100),
    long_name VARCHAR(200),
    address1 VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(50),
    zip VARCHAR(20),
    country VARCHAR(100),
    phone VARCHAR(20),
    website TEXT,
    industry VARCHAR(100),
    sector VARCHAR(100),
    long_business_summary TEXT,
    full_time_employees INTEGER,
    currency VARCHAR(10),
    financial_currency VARCHAR(10),
    exchange VARCHAR(10),
    quote_type VARCHAR(10),
    time_zone_full_name VARCHAR(50),
    time_zone_short_name VARCHAR(10),
    gmt_offset_milliseconds BIGINT,
    uuid UUID,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Market Stock Risk Metrics
CREATE TABLE market_stock_risk_metrics (
    symbol VARCHAR(20) PRIMARY KEY REFERENCES market_symbol(symbol) ON DELETE CASCADE,
    beta DECIMAL(10,4),
    volatility DECIMAL(10,4),
    sharpe_ratio DECIMAL(10,4),
    max_drawdown DECIMAL(10,4),
    var_95 DECIMAL(10,4),
    var_99 DECIMAL(10,4),
    expected_shortfall DECIMAL(10,4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Historical Price Data (TimescaleDB Hypertables)
CREATE TABLE market_stock_hist_bars_min_ts (
    symbol VARCHAR(10) NOT NULL,
    time TIMESTAMP NOT NULL,
    open DECIMAL(15,4),
    high DECIMAL(15,4),
    low DECIMAL(15,4),
    close DECIMAL(15,4),
    volume BIGINT,
    adj_close DECIMAL(15,4),
    PRIMARY KEY (symbol, time)
);

CREATE TABLE market_stock_hist_bars_hour_ts (
    symbol VARCHAR(10) NOT NULL,
    time TIMESTAMP NOT NULL,
    open DECIMAL(15,4),
    high DECIMAL(15,4),
    low DECIMAL(15,4),
    close DECIMAL(15,4),
    volume BIGINT,
    adj_close DECIMAL(15,4),
    PRIMARY KEY (symbol, time)
);

CREATE TABLE market_stock_hist_bars_day_ts (
    symbol VARCHAR(10) NOT NULL,
    time TIMESTAMP NOT NULL,
    open DECIMAL(15,4),
    high DECIMAL(15,4),
    low DECIMAL(15,4),
    close DECIMAL(15,4),
    volume BIGINT,
    adj_close DECIMAL(15,4),
    PRIMARY KEY (symbol, time)
);

-- ==============================================
-- PORTFOLIO MANAGEMENT TABLES
-- ==============================================

-- User Static Settings
CREATE TABLE user_static_setting (
    user_id INTEGER PRIMARY KEY REFERENCES auth_user(id) ON DELETE CASCADE,
    capital DECIMAL(15,2) DEFAULT 10000.00,
    risk DECIMAL(5,2) DEFAULT 0.50,
    rounding INTEGER DEFAULT 2,
    commission DECIMAL(10,2) DEFAULT 0.00,
    tax DECIMAL(10,2) DEFAULT 0.00,
    expect_gain_risk_ratio DECIMAL(5,2) DEFAULT 2.00,
    position_min INTEGER DEFAULT 2,
    position_max INTEGER DEFAULT 2,
    total_risk_cap DECIMAL(5,2) DEFAULT 10.00,
    net_risk_cap DECIMAL(5,2) DEFAULT 5.00,
    performance_tracking_date DATE,
    single_max_drawdown DECIMAL(5,2) DEFAULT 0.10,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Portfolio
CREATE TABLE portfolio (
    portfolio_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    initial_capital DECIMAL(15,2) DEFAULT 0.00,
    current_value DECIMAL(15,2) DEFAULT 0.00,
    cash_balance DECIMAL(15,2) DEFAULT 0.00,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, name)
);

-- Holdings
CREATE TABLE holding (
    holding_id SERIAL PRIMARY KEY,
    portfolio_id INTEGER NOT NULL REFERENCES portfolio(portfolio_id) ON DELETE CASCADE,
    symbol VARCHAR(20) NOT NULL REFERENCES market_symbol(symbol) ON DELETE CASCADE,
    quantity INTEGER NOT NULL DEFAULT 0,
    average_price DECIMAL(15,4) NOT NULL DEFAULT 0.0000,
    current_price DECIMAL(15,4) DEFAULT 0.0000,
    market_value DECIMAL(15,2) DEFAULT 0.00,
    unrealized_pnl DECIMAL(15,2) DEFAULT 0.00,
    unrealized_pnl_percent DECIMAL(10,4) DEFAULT 0.0000,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(portfolio_id, symbol)
);

-- Transactions
CREATE TABLE transaction (
    transaction_id SERIAL PRIMARY KEY,
    portfolio_id INTEGER NOT NULL REFERENCES portfolio(portfolio_id) ON DELETE CASCADE,
    symbol VARCHAR(20) NOT NULL REFERENCES market_symbol(symbol) ON DELETE CASCADE,
    transaction_type VARCHAR(10) NOT NULL CHECK (transaction_type IN ('BUY', 'SELL')),
    quantity INTEGER NOT NULL,
    price DECIMAL(15,4) NOT NULL,
    total_amount DECIMAL(15,2) NOT NULL,
    commission DECIMAL(10,2) DEFAULT 0.00,
    tax DECIMAL(10,2) DEFAULT 0.00,
    net_amount DECIMAL(15,2) NOT NULL,
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Orders
CREATE TABLE "order" (
    order_id SERIAL PRIMARY KEY,
    portfolio_id INTEGER NOT NULL REFERENCES portfolio(portfolio_id) ON DELETE CASCADE,
    symbol VARCHAR(20) NOT NULL REFERENCES market_symbol(symbol) ON DELETE CASCADE,
    order_type VARCHAR(20) NOT NULL CHECK (order_type IN ('MARKET', 'LIMIT', 'STOP', 'STOP_LIMIT')),
    side VARCHAR(10) NOT NULL CHECK (side IN ('BUY', 'SELL')),
    quantity INTEGER NOT NULL,
    price DECIMAL(15,4),
    stop_price DECIMAL(15,4),
    status VARCHAR(20) NOT NULL DEFAULT 'PENDING' CHECK (status IN ('PENDING', 'FILLED', 'PARTIALLY_FILLED', 'CANCELLED', 'REJECTED')),
    filled_quantity INTEGER DEFAULT 0,
    filled_price DECIMAL(15,4),
    time_in_force VARCHAR(10) DEFAULT 'GTC' CHECK (time_in_force IN ('GTC', 'IOC', 'FOK', 'DAY')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    filled_at TIMESTAMP
);

-- Trades
CREATE TABLE trade (
    trade_id SERIAL PRIMARY KEY,
    portfolio_id INTEGER NOT NULL REFERENCES portfolio(portfolio_id) ON DELETE CASCADE,
    symbol VARCHAR(20) NOT NULL REFERENCES market_symbol(symbol) ON DELETE CASCADE,
    entry_date TIMESTAMP NOT NULL,
    exit_date TIMESTAMP,
    entry_price DECIMAL(15,4) NOT NULL,
    exit_price DECIMAL(15,4),
    quantity INTEGER NOT NULL,
    profit_actual DECIMAL(15,2) DEFAULT 0.00,
    profit_actual_ratio DECIMAL(10,4) DEFAULT 0.0000,
    commission DECIMAL(10,2) DEFAULT 0.00,
    tax DECIMAL(10,2) DEFAULT 0.00,
    net_profit DECIMAL(15,2) DEFAULT 0.00,
    status VARCHAR(20) DEFAULT 'OPEN' CHECK (status IN ('OPEN', 'CLOSED', 'PARTIALLY_CLOSED')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Cash Balance
CREATE TABLE cash_balance (
    cash_balance_id SERIAL PRIMARY KEY,
    portfolio_id INTEGER NOT NULL REFERENCES portfolio(portfolio_id) ON DELETE CASCADE,
    balance DECIMAL(15,2) NOT NULL DEFAULT 0.00,
    currency VARCHAR(10) DEFAULT 'USD',
    balance_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Funding
CREATE TABLE funding (
    funding_id SERIAL PRIMARY KEY,
    portfolio_id INTEGER NOT NULL REFERENCES portfolio(portfolio_id) ON DELETE CASCADE,
    amount DECIMAL(15,2) NOT NULL,
    funding_type VARCHAR(20) NOT NULL CHECK (funding_type IN ('DEPOSIT', 'WITHDRAWAL', 'DIVIDEND', 'INTEREST')),
    funding_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==============================================
-- STRATEGY & ANALYSIS TABLES
-- ==============================================

-- Strategy Categories
CREATE TABLE strategy_category (
    strategy_category_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Strategies
CREATE TABLE strategy (
    strategy_id SERIAL PRIMARY KEY,
    owner_user_id INTEGER REFERENCES auth_user(id) ON DELETE SET NULL,
    name VARCHAR(255) NOT NULL,
    short_name VARCHAR(50),
    description TEXT,
    as_of_date DATE NOT NULL,
    custom_order INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Strategy Categories Junction
CREATE TABLE strategy_strategy_category (
    strategy_id INTEGER NOT NULL REFERENCES strategy(strategy_id) ON DELETE CASCADE,
    strategy_category_id INTEGER NOT NULL REFERENCES strategy_category(strategy_category_id) ON DELETE CASCADE,
    PRIMARY KEY (strategy_id, strategy_category_id)
);

-- Screening
CREATE TABLE screening (
    screening_id SERIAL PRIMARY KEY,
    owner_user_id INTEGER REFERENCES auth_user(id) ON DELETE SET NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    criteria JSONB,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Ratings (TimescaleDB)
CREATE TABLE rating (
    symbol VARCHAR(20) NOT NULL REFERENCES market_symbol(symbol) ON DELETE CASCADE,
    time DATE NOT NULL,
    strategy_id INTEGER NOT NULL REFERENCES strategy(strategy_id) ON DELETE CASCADE,
    score DECIMAL(5,2) NOT NULL,
    PRIMARY KEY (symbol, time, strategy_id)
);

-- Rating Indicator Results (TimescaleDB)
CREATE TABLE rating_indicator_result (
    symbol VARCHAR(20) NOT NULL REFERENCES market_symbol(symbol) ON DELETE CASCADE,
    time TIMESTAMP NOT NULL,
    strategy_id INTEGER NOT NULL REFERENCES strategy(strategy_id) ON DELETE CASCADE,
    indicator_name VARCHAR(100) NOT NULL,
    indicator_value DECIMAL(15,4),
    indicator_signal VARCHAR(20),
    PRIMARY KEY (symbol, time, strategy_id, indicator_name)
);

-- ==============================================
-- SNAPSHOT TABLES (TimescaleDB)
-- ==============================================

-- Snapshot Screening
CREATE TABLE snapshot_screening (
    symbol VARCHAR(20) NOT NULL REFERENCES market_symbol(symbol) ON DELETE CASCADE,
    time TIMESTAMP NOT NULL,
    screening_id INTEGER NOT NULL REFERENCES screening(screening_id) ON DELETE CASCADE,
    price DECIMAL(15,4),
    volume BIGINT,
    market_cap DECIMAL(20,2),
    pe_ratio DECIMAL(10,4),
    pb_ratio DECIMAL(10,4),
    debt_to_equity DECIMAL(10,4),
    roe DECIMAL(10,4),
    roa DECIMAL(10,4),
    current_ratio DECIMAL(10,4),
    quick_ratio DECIMAL(10,4),
    PRIMARY KEY (symbol, time, screening_id)
);

-- Snapshot Overview
CREATE TABLE snapshot_overview (
    symbol VARCHAR(20) NOT NULL REFERENCES market_symbol(symbol) ON DELETE CASCADE,
    time TIMESTAMP NOT NULL,
    name VARCHAR(255),
    price DECIMAL(15,4),
    change DECIMAL(15,4),
    change_percent DECIMAL(10,4),
    volume BIGINT,
    avg_volume BIGINT,
    market_cap DECIMAL(20,2),
    pe_ratio DECIMAL(10,4),
    eps DECIMAL(10,4),
    dividend_yield DECIMAL(10,4),
    beta DECIMAL(10,4),
    PRIMARY KEY (symbol, time)
);

-- Snapshot Technical
CREATE TABLE snapshot_technical (
    symbol VARCHAR(20) NOT NULL REFERENCES market_symbol(symbol) ON DELETE CASCADE,
    time TIMESTAMP NOT NULL,
    sma_20 DECIMAL(15,4),
    sma_50 DECIMAL(15,4),
    sma_200 DECIMAL(15,4),
    ema_12 DECIMAL(15,4),
    ema_26 DECIMAL(15,4),
    macd DECIMAL(15,4),
    macd_signal DECIMAL(15,4),
    macd_histogram DECIMAL(15,4),
    rsi DECIMAL(10,4),
    bollinger_upper DECIMAL(15,4),
    bollinger_middle DECIMAL(15,4),
    bollinger_lower DECIMAL(15,4),
    adx DECIMAL(10,4),
    stochastic_k DECIMAL(10,4),
    stochastic_d DECIMAL(10,4),
    williams_r DECIMAL(10,4),
    PRIMARY KEY (symbol, time)
);

-- Snapshot Fundamental
CREATE TABLE snapshot_fundamental (
    symbol VARCHAR(20) NOT NULL REFERENCES market_symbol(symbol) ON DELETE CASCADE,
    time TIMESTAMP NOT NULL,
    revenue DECIMAL(20,2),
    net_income DECIMAL(20,2),
    total_assets DECIMAL(20,2),
    total_liabilities DECIMAL(20,2),
    shareholders_equity DECIMAL(20,2),
    cash_and_equivalents DECIMAL(20,2),
    total_debt DECIMAL(20,2),
    operating_cash_flow DECIMAL(20,2),
    free_cash_flow DECIMAL(20,2),
    PRIMARY KEY (symbol, time)
);

-- Snapshot Setup
CREATE TABLE snapshot_setup (
    symbol VARCHAR(20) NOT NULL REFERENCES market_symbol(symbol) ON DELETE CASCADE,
    time TIMESTAMP NOT NULL,
    setup_type VARCHAR(50),
    setup_score DECIMAL(5,2),
    setup_strength VARCHAR(20),
    breakout_price DECIMAL(15,4),
    stop_loss DECIMAL(15,4),
    target_price DECIMAL(15,4),
    risk_reward_ratio DECIMAL(10,4),
    PRIMARY KEY (symbol, time)
);

-- Snapshot Bull Flag
CREATE TABLE snapshot_bull_flag (
    symbol VARCHAR(20) NOT NULL REFERENCES market_symbol(symbol) ON DELETE CASCADE,
    time TIMESTAMP NOT NULL,
    flag_score DECIMAL(5,2),
    flag_strength VARCHAR(20),
    pole_height DECIMAL(15,4),
    flag_height DECIMAL(15,4),
    breakout_probability DECIMAL(5,2),
    PRIMARY KEY (symbol, time)
);

-- Snapshot Earning
CREATE TABLE snapshot_earning (
    symbol VARCHAR(20) NOT NULL REFERENCES market_symbol(symbol) ON DELETE CASCADE,
    time TIMESTAMP NOT NULL,
    earnings_date DATE,
    earnings_per_share DECIMAL(10,4),
    revenue_estimate DECIMAL(20,2),
    revenue_actual DECIMAL(20,2),
    eps_estimate DECIMAL(10,4),
    eps_actual DECIMAL(10,4),
    surprise_percent DECIMAL(10,4),
    PRIMARY KEY (symbol, time)
);

-- ==============================================
-- UTILITY TABLES
-- ==============================================

-- Utilities Lookup
CREATE TABLE utilities_lookup (
    category VARCHAR(255) NOT NULL,
    key VARCHAR(255) NOT NULL,
    value TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (category, key)
);

-- Wishlist
CREATE TABLE wishlist (
    wishlist_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    symbol VARCHAR(20) NOT NULL REFERENCES market_symbol(symbol) ON DELETE CASCADE,
    quantity INTEGER DEFAULT 1,
    target_price DECIMAL(15,4),
    purpose VARCHAR(20) CHECK (purpose IN ('WATCH', 'BUY', 'EARNING')),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, symbol)
);

-- ==============================================
-- TIMESCALEDB HYPERTABLES
-- ==============================================

-- Create hypertables for time-series data
SELECT create_hypertable('market_stock_hist_bars_min_ts', 'time', chunk_time_interval => INTERVAL '1 day');
SELECT create_hypertable('market_stock_hist_bars_hour_ts', 'time', chunk_time_interval => INTERVAL '1 day');
SELECT create_hypertable('market_stock_hist_bars_day_ts', 'time', chunk_time_interval => INTERVAL '1 week');

SELECT create_hypertable('rating', 'time', chunk_time_interval => INTERVAL '1 day');
SELECT create_hypertable('rating_indicator_result', 'time', chunk_time_interval => INTERVAL '1 day');

SELECT create_hypertable('snapshot_screening', 'time', chunk_time_interval => INTERVAL '1 day');
SELECT create_hypertable('snapshot_overview', 'time', chunk_time_interval => INTERVAL '1 day');
SELECT create_hypertable('snapshot_technical', 'time', chunk_time_interval => INTERVAL '1 day');
SELECT create_hypertable('snapshot_fundamental', 'time', chunk_time_interval => INTERVAL '1 day');
SELECT create_hypertable('snapshot_setup', 'time', chunk_time_interval => INTERVAL '1 day');
SELECT create_hypertable('snapshot_bull_flag', 'time', chunk_time_interval => INTERVAL '1 day');
SELECT create_hypertable('snapshot_earning', 'time', chunk_time_interval => INTERVAL '1 day');

-- ==============================================
-- INDEXES
-- ==============================================

-- Market data indexes
CREATE INDEX idx_market_symbol_name ON market_symbol(name);
CREATE INDEX idx_market_symbol_market ON market_symbol(market);
CREATE INDEX idx_market_symbol_asset_type ON market_symbol(asset_type);
CREATE INDEX idx_market_symbol_status ON market_symbol(status);

CREATE INDEX idx_market_stock_industry ON market_stock(industry);
CREATE INDEX idx_market_stock_sector ON market_stock(sector);
CREATE INDEX idx_market_stock_exchange ON market_stock(exchange);

-- Portfolio indexes
CREATE INDEX idx_portfolio_user_id ON portfolio(user_id);
CREATE INDEX idx_portfolio_name ON portfolio(name);
CREATE INDEX idx_portfolio_active ON portfolio(is_active);

CREATE INDEX idx_holding_portfolio_id ON holding(portfolio_id);
CREATE INDEX idx_holding_symbol ON holding(symbol);
CREATE INDEX idx_holding_portfolio_symbol ON holding(portfolio_id, symbol);

CREATE INDEX idx_transaction_portfolio_id ON transaction(portfolio_id);
CREATE INDEX idx_transaction_symbol ON transaction(symbol);
CREATE INDEX idx_transaction_date ON transaction(transaction_date);
CREATE INDEX idx_transaction_type ON transaction(transaction_type);

CREATE INDEX idx_order_portfolio_id ON "order"(portfolio_id);
CREATE INDEX idx_order_symbol ON "order"(symbol);
CREATE INDEX idx_order_status ON "order"(status);
CREATE INDEX idx_order_created_at ON "order"(created_at);

CREATE INDEX idx_trade_portfolio_id ON trade(portfolio_id);
CREATE INDEX idx_trade_symbol ON trade(symbol);
CREATE INDEX idx_trade_entry_date ON trade(entry_date);
CREATE INDEX idx_trade_status ON trade(status);

-- Strategy indexes
CREATE INDEX idx_strategy_owner ON strategy(owner_user_id);
CREATE INDEX idx_strategy_name ON strategy(name);
CREATE INDEX idx_strategy_active ON strategy(is_active);

CREATE INDEX idx_screening_owner ON screening(owner_user_id);
CREATE INDEX idx_screening_name ON screening(name);
CREATE INDEX idx_screening_active ON screening(is_active);

CREATE INDEX idx_rating_symbol ON rating(symbol);
CREATE INDEX idx_rating_strategy ON rating(strategy_id);
CREATE INDEX idx_rating_time ON rating(time);

-- Snapshot indexes
CREATE INDEX idx_snapshot_screening_symbol ON snapshot_screening(symbol);
CREATE INDEX idx_snapshot_screening_screening ON snapshot_screening(screening_id);
CREATE INDEX idx_snapshot_screening_time ON snapshot_screening(time);

CREATE INDEX idx_snapshot_overview_symbol ON snapshot_overview(symbol);
CREATE INDEX idx_snapshot_overview_time ON snapshot_overview(time);

CREATE INDEX idx_snapshot_technical_symbol ON snapshot_technical(symbol);
CREATE INDEX idx_snapshot_technical_time ON snapshot_technical(time);

CREATE INDEX idx_snapshot_fundamental_symbol ON snapshot_fundamental(symbol);
CREATE INDEX idx_snapshot_fundamental_time ON snapshot_fundamental(time);

CREATE INDEX idx_snapshot_setup_symbol ON snapshot_setup(symbol);
CREATE INDEX idx_snapshot_setup_time ON snapshot_setup(time);

CREATE INDEX idx_snapshot_bull_flag_symbol ON snapshot_bull_flag(symbol);
CREATE INDEX idx_snapshot_bull_flag_time ON snapshot_bull_flag(time);

CREATE INDEX idx_snapshot_earning_symbol ON snapshot_earning(symbol);
CREATE INDEX idx_snapshot_earning_time ON snapshot_earning(time);

-- Utility indexes
CREATE INDEX idx_wishlist_user_id ON wishlist(user_id);
CREATE INDEX idx_wishlist_symbol ON wishlist(symbol);
CREATE INDEX idx_wishlist_purpose ON wishlist(purpose);

-- ==============================================
-- COMPRESSION POLICIES
-- ==============================================

-- Add compression policies for historical data
SELECT add_compression_policy('market_stock_hist_bars_min_ts', INTERVAL '7 days');
SELECT add_compression_policy('market_stock_hist_bars_hour_ts', INTERVAL '30 days');
SELECT add_compression_policy('market_stock_hist_bars_day_ts', INTERVAL '90 days');

SELECT add_compression_policy('rating', INTERVAL '30 days');
SELECT add_compression_policy('rating_indicator_result', INTERVAL '7 days');

SELECT add_compression_policy('snapshot_screening', INTERVAL '30 days');
SELECT add_compression_policy('snapshot_overview', INTERVAL '30 days');
SELECT add_compression_policy('snapshot_technical', INTERVAL '30 days');
SELECT add_compression_policy('snapshot_fundamental', INTERVAL '30 days');
SELECT add_compression_policy('snapshot_setup', INTERVAL '30 days');
SELECT add_compression_policy('snapshot_bull_flag', INTERVAL '30 days');
SELECT add_compression_policy('snapshot_earning', INTERVAL '30 days');

-- ==============================================
-- CONTINUOUS AGGREGATES
-- ==============================================

-- Daily price aggregates
CREATE MATERIALIZED VIEW daily_price_aggregates
WITH (timescaledb.continuous) AS
SELECT 
    symbol,
    time_bucket('1 day', time) AS day,
    first(open, time) AS open_price,
    max(high) AS high_price,
    min(low) AS low_price,
    last(close, time) AS close_price,
    sum(volume) AS total_volume,
    avg(close) AS avg_price
FROM market_stock_hist_bars_min_ts
GROUP BY symbol, day;

-- Add refresh policy for daily aggregates
SELECT add_continuous_aggregate_policy('daily_price_aggregates',
    start_offset => INTERVAL '1 day',
    end_offset => INTERVAL '1 hour',
    schedule_interval => INTERVAL '1 hour');

-- Weekly price aggregates
CREATE MATERIALIZED VIEW weekly_price_aggregates
WITH (timescaledb.continuous) AS
SELECT 
    symbol,
    time_bucket('1 week', time) AS week,
    first(open, time) AS open_price,
    max(high) AS high_price,
    min(low) AS low_price,
    last(close, time) AS close_price,
    sum(volume) AS total_volume,
    avg(close) AS avg_price
FROM market_stock_hist_bars_day_ts
GROUP BY symbol, week;

-- Add refresh policy for weekly aggregates
SELECT add_continuous_aggregate_policy('weekly_price_aggregates',
    start_offset => INTERVAL '1 week',
    end_offset => INTERVAL '1 day',
    schedule_interval => INTERVAL '1 day');

-- ==============================================
-- FUNCTIONS AND TRIGGERS
-- ==============================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers for updated_at
CREATE TRIGGER update_market_symbol_updated_at BEFORE UPDATE ON market_symbol FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_market_stock_updated_at BEFORE UPDATE ON market_stock FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_user_static_setting_updated_at BEFORE UPDATE ON user_static_setting FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_portfolio_updated_at BEFORE UPDATE ON portfolio FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_holding_updated_at BEFORE UPDATE ON holding FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_order_updated_at BEFORE UPDATE ON "order" FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_trade_updated_at BEFORE UPDATE ON trade FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_cash_balance_updated_at BEFORE UPDATE ON cash_balance FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_strategy_updated_at BEFORE UPDATE ON strategy FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_screening_updated_at BEFORE UPDATE ON screening FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_wishlist_updated_at BEFORE UPDATE ON wishlist FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ==============================================
-- VIEWS
-- ==============================================

-- Portfolio summary view
CREATE VIEW portfolio_summary AS
SELECT 
    p.portfolio_id,
    p.user_id,
    p.name,
    p.initial_capital,
    p.current_value,
    p.cash_balance,
    COALESCE(SUM(h.market_value), 0) AS total_holdings_value,
    COALESCE(SUM(h.unrealized_pnl), 0) AS total_unrealized_pnl,
    COALESCE(SUM(h.unrealized_pnl_percent * h.market_value) / NULLIF(SUM(h.market_value), 0), 0) AS weighted_unrealized_pnl_percent,
    p.is_active,
    p.created_at,
    p.updated_at
FROM portfolio p
LEFT JOIN holding h ON p.portfolio_id = h.portfolio_id
GROUP BY p.portfolio_id, p.user_id, p.name, p.initial_capital, p.current_value, p.cash_balance, p.is_active, p.created_at, p.updated_at;

-- Market overview view
CREATE VIEW market_overview AS
SELECT 
    ms.symbol,
    ms.name,
    ms.market,
    ms.asset_type,
    ms.status,
    ms_stock.industry,
    ms_stock.sector,
    ms_stock.exchange,
    COALESCE(latest_price.close, 0) AS current_price,
    COALESCE(latest_price.volume, 0) AS current_volume,
    COALESCE(daily_change.change_percent, 0) AS daily_change_percent
FROM market_symbol ms
LEFT JOIN market_stock ms_stock ON ms.symbol = ms_stock.symbol
LEFT JOIN LATERAL (
    SELECT close, volume
    FROM market_stock_hist_bars_day_ts
    WHERE symbol = ms.symbol
    ORDER BY time DESC
    LIMIT 1
) latest_price ON true
LEFT JOIN LATERAL (
    SELECT 
        (last(close, time) - first(open, time)) / first(open, time) * 100 AS change_percent
    FROM market_stock_hist_bars_day_ts
    WHERE symbol = ms.symbol
    AND time >= CURRENT_DATE
    GROUP BY symbol
) daily_change ON true;

-- ==============================================
-- INITIAL DATA
-- ==============================================

-- Insert default strategy categories
INSERT INTO strategy_category (name, description) VALUES
('Momentum', 'Momentum-based trading strategies'),
('Mean Reversion', 'Mean reversion trading strategies'),
('Breakout', 'Breakout trading strategies'),
('Trend Following', 'Trend following strategies'),
('Scalping', 'High-frequency scalping strategies'),
('Swing Trading', 'Swing trading strategies'),
('Position Trading', 'Long-term position trading'),
('Arbitrage', 'Arbitrage opportunities'),
('Pairs Trading', 'Pairs trading strategies'),
('Bull Flag', 'Bull flag pattern strategies');

-- Insert default utilities lookup
INSERT INTO utilities_lookup (category, key, value, description) VALUES
('market', 'exchanges', 'NYSE,NASDAQ,AMEX,OTC', 'Available stock exchanges'),
('market', 'asset_types', 'Stock,ETF,Option,Future,Crypto', 'Available asset types'),
('trading', 'order_types', 'MARKET,LIMIT,STOP,STOP_LIMIT', 'Available order types'),
('trading', 'time_in_force', 'GTC,IOC,FOK,DAY', 'Available time in force options'),
('portfolio', 'funding_types', 'DEPOSIT,WITHDRAWAL,DIVIDEND,INTEREST', 'Available funding types'),
('strategy', 'signal_types', 'BUY,SELL,HOLD', 'Available signal types'),
('risk', 'risk_levels', 'LOW,MEDIUM,HIGH', 'Available risk levels');

-- ==============================================
-- GRANTS AND PERMISSIONS
-- ==============================================

-- Create service-specific users (for microservices)
-- Note: These would be created in production with proper passwords

-- Data Service User
-- CREATE USER bifrost_data_service WITH PASSWORD 'secure_password';
-- GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO bifrost_data_service;
-- GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO bifrost_data_service;

-- Portfolio Service User
-- CREATE USER bifrost_portfolio_service WITH PASSWORD 'secure_password';
-- GRANT SELECT, INSERT, UPDATE ON portfolio, holding, transaction, "order", trade, cash_balance, funding TO bifrost_portfolio_service;
-- GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO bifrost_portfolio_service;

-- Strategy Service User
-- CREATE USER bifrost_strategy_service WITH PASSWORD 'secure_password';
-- GRANT SELECT, INSERT, UPDATE ON strategy, screening, rating, snapshot_* TO bifrost_strategy_service;
-- GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO bifrost_strategy_service;

-- Trading Service User
-- CREATE USER bifrost_trading_service WITH PASSWORD 'secure_password';
-- GRANT SELECT, INSERT, UPDATE ON "order", trade, transaction TO bifrost_trading_service;
-- GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO bifrost_trading_service;

-- Web Portal User (read-only)
-- CREATE USER bifrost_web_portal WITH PASSWORD 'secure_password';
-- GRANT SELECT ON ALL TABLES IN SCHEMA public TO bifrost_web_portal;

COMMIT;
