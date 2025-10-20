# Market Data Service Architecture

**Service Name:** market-data-service (formerly data-service)  
**Port:** 8001  
**Database Access:** 🔴 Direct (Tier 1)  
**Status:** 🚧 In Progress  
**Last Updated:** October 6, 2025

---

## 🎯 Overview

The Market Data Service is responsible for all market data operations including data ingestion, symbol management, historical data storage, and real-time data processing. This service has primary ownership of the market data domain in the database.

---

## 🏗️ Architecture

### Technology Stack

- **Framework:** FastAPI 0.104+
- **ORM:** SQLAlchemy 2.0+ with async support
- **Database Driver:** AsyncPG
- **Validation:** Pydantic v2
- **Database:** PostgreSQL 17 with TimescaleDB
- **Cache:** Redis (optional)
- **Task Queue:** Celery (for data ingestion)

### Directory Structure

```
data-service/
├── main.py                      # FastAPI application entry point
├── requirements.txt             # Python dependencies
├── ARCHITECTURE.md             # This file
├── src/
│   ├── api/                    # API endpoints
│   │   ├── __init__.py
│   │   └── endpoints/
│   │       ├── market_data.py  # Market data endpoints
│   │       └── symbols.py      # Symbol endpoints
│   ├── database/               # Database configuration
│   │   ├── __init__.py
│   │   ├── connection.py       # Async database connection
│   │   └── models.py           # Model registry
│   ├── models/                 # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── market_reference.py # Symbol and reference data
│   │   └── market_data.py      # Market data models
│   ├── repositories/           # Data access layer
│   │   ├── __init__.py
│   │   ├── base.py            # Base repository
│   │   ├── market_reference.py # Symbol repository
│   │   └── market_data.py      # Market data repository
│   ├── schemas/                # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── market_reference.py # Symbol schemas
│   │   └── market_data.py      # Market data schemas
│   ├── services/               # Business logic
│   │   ├── __init__.py
│   │   ├── yahoo_finance_service.py
│   │   ├── data_ingestion_service.py
│   │   └── timescaledb_service.py
│   └── tasks/                  # Celery tasks
│       └── data_ingestion.py
└── tests/                      # Unit and integration tests
    ├── test_models.py
    ├── test_repositories.py
    └── test_api.py
```

---

## 🗄️ Database Tables

### Primary Tables (Read/Write Access)

#### Market Reference Tables
- **market_symbol** - Symbol master data
  - Primary key: symbol (VARCHAR)
  - Indexes: symbol
  - Contains: Basic symbol information, IPO date, status

- **market_stock** - Detailed company information
  - Primary key: symbol (VARCHAR)
  - Foreign key: market_symbol.symbol
  - Contains: Company details, financials, sector/industry

- **market_stock_risk_metrics** - Risk calculations
  - Primary key: symbol (VARCHAR)
  - Foreign key: market_symbol.symbol
  - Contains: Beta, volatility, VaR, Sharpe ratio

#### Time-Series Tables (TimescaleDB Hypertables)
- **market_stock_hist_bars_min_ts** - Minute-level price data
  - Composite PK: (symbol, time)
  - Partitioned by: time (1 day chunks)
  - Compression: After 1 day
  - Retention: 6 months

- **market_stock_hist_bars_hour_ts** - Hourly price data
  - Composite PK: (symbol, time)
  - Partitioned by: time (7 day chunks)
  - Compression: After 7 days
  - Retention: 2 years

- **market_stock_hist_bars_day_ts** - Daily price data
  - Composite PK: (symbol, time)
  - Partitioned by: time (30 day chunks)
  - Compression: After 30 days
  - Retention: 10 years

#### Snapshot Tables
- **snapshot_screening** - Screening snapshot data
- **snapshot_overview** - Market overview snapshots
- **snapshot_technical** - Technical analysis snapshots
- **snapshot_fundamental** - Fundamental analysis snapshots
- **snapshot_setup** - Trading setup snapshots
- **snapshot_bull_flag** - Bull flag pattern snapshots
- **snapshot_earning** - Earnings snapshot data

### Read-Only Tables
- All other tables for cross-domain queries

---

## 🔐 Database Access

### Database User
```sql
CREATE USER market_data_service_user WITH PASSWORD 'secure_password';

-- Grant full access to primary tables
GRANT SELECT, INSERT, UPDATE, DELETE ON 
    market_symbol, 
    market_stock, 
    market_stock_risk_metrics,
    market_stock_hist_bars_min_ts,
    market_stock_hist_bars_hour_ts,
    market_stock_hist_bars_day_ts,
    snapshot_*
TO market_data_service_user;

-- Grant read access to all tables
GRANT SELECT ON ALL TABLES TO market_data_service_user;
```

### Connection Configuration
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=bifrost_trader
DB_USERNAME=market_data_service_user
DB_PASSWORD=secure_password
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20
DB_POOL_TIMEOUT=30
DB_POOL_RECYCLE=3600
```

---

## 🚀 Key Features

### 1. Market Data Ingestion
- **Data Sources:**
  - Yahoo Finance API
  - Alpha Vantage
  - IEX Cloud
  - Real-time WebSocket feeds

- **Ingestion Modes:**
  - Real-time: WebSocket streaming
  - Batch: Scheduled data pulls
  - Backfill: Historical data retrieval

### 2. Symbol Management
- Symbol lookup and search
- Symbol validation
- Company information retrieval
- Symbol status tracking (active, delisted)

### 3. Historical Data
- Multiple timeframes (1min, 5min, 15min, 1hour, 1day)
- OHLCV data
- Dividend and split adjustments
- Data quality validation

### 4. Snapshot Generation
- Technical analysis snapshots
- Fundamental analysis snapshots
- Market overview snapshots
- Trading setup detection

### 5. TimescaleDB Optimization
- Automatic hypertable creation
- Compression policies
- Continuous aggregates
- Retention policies
- Query optimization

---

## 📡 API Endpoints

### Symbol Endpoints

```http
GET    /api/symbols                 # List all symbols
GET    /api/symbols/{symbol}        # Get symbol details
POST   /api/symbols                 # Create symbol
PUT    /api/symbols/{symbol}        # Update symbol
DELETE /api/symbols/{symbol}        # Delete symbol
GET    /api/symbols/search?q={query} # Search symbols
```

### Market Data Endpoints

```http
GET    /api/market-data/{symbol}           # Get latest price
GET    /api/market-data/{symbol}/history   # Get historical data
POST   /api/market-data                    # Create market data
POST   /api/market-data/bulk               # Bulk create
GET    /api/market-data/{symbol}/range     # Get data range
GET    /api/market-data/statistics         # Get statistics
```

### Historical Data Endpoints

```http
GET    /api/historical/{symbol}/minute     # Minute data
GET    /api/historical/{symbol}/hour       # Hourly data
GET    /api/historical/{symbol}/day        # Daily data
GET    /api/historical/{symbol}/latest     # Latest bar
POST   /api/historical/ingest              # Ingest historical data
```

### Snapshot Endpoints

```http
GET    /api/snapshots/{symbol}/technical   # Technical snapshot
GET    /api/snapshots/{symbol}/fundamental # Fundamental snapshot
POST   /api/snapshots/generate             # Generate snapshots
```

---

## 🔄 Data Flow

### 1. Real-Time Data Ingestion
```
WebSocket Feed → Data Validation → Database Write → Cache Update → Event Publish
```

### 2. Batch Data Ingestion
```
External API → Celery Task → Data Transformation → Bulk Insert → Compression
```

### 3. Historical Data Query
```
API Request → Cache Check → Database Query → Response Transform → Cache Store
```

---

## 🧪 Testing

### Unit Tests
```bash
pytest tests/test_models.py
pytest tests/test_repositories.py
pytest tests/test_schemas.py
```

### Integration Tests
```bash
pytest tests/test_api.py
pytest tests/test_database.py
```

### Performance Tests
```bash
pytest tests/test_performance.py
```

---

## 📊 Performance Considerations

### Database Optimization
- **Connection Pooling:** 10 base + 20 overflow connections
- **Prepared Statements:** All queries use parameterized statements
- **Batch Operations:** Bulk inserts for historical data
- **Indexes:** Optimized for symbol + time queries

### Caching Strategy
- **Redis Cache:** Latest prices (TTL: 5 minutes)
- **Application Cache:** Symbol metadata (TTL: 1 hour)
- **Query Cache:** Common historical queries (TTL: 15 minutes)

### TimescaleDB Features
- **Compression:** 90%+ storage reduction
- **Continuous Aggregates:** Pre-computed hourly/daily aggregates
- **Partition Pruning:** Automatic partition elimination
- **Parallel Query:** Leverage PostgreSQL parallel workers

---

## 🔍 Monitoring

### Key Metrics
- **Ingestion Rate:** Records per second
- **Query Performance:** P50, P95, P99 latency
- **Database Connections:** Active/idle connections
- **Cache Hit Rate:** Redis cache effectiveness
- **Error Rate:** Failed requests percentage

### Health Checks
```http
GET /health         # Service health
GET /health/db      # Database health
GET /health/cache   # Cache health
```

---

## 🚧 TODO

### Phase 1: Foundation (✅ Complete)
- [x] SQLAlchemy models
- [x] Pydantic schemas
- [x] Repository pattern
- [x] Async database connection
- [x] TimescaleDB integration

### Phase 2: API Implementation (⏳ In Progress)
- [ ] Symbol API endpoints
- [ ] Market data API endpoints
- [ ] Historical data API endpoints
- [ ] Snapshot API endpoints

### Phase 3: Testing (⏳ Pending)
- [ ] Unit tests (>90% coverage)
- [ ] Integration tests
- [ ] Performance tests
- [ ] Load tests

### Phase 4: Production Ready (⏳ Pending)
- [ ] Monitoring and alerting
- [ ] Documentation
- [ ] Deployment configuration
- [ ] CI/CD pipeline

---

## 📚 References

- [Data Access Architecture](../../docs/architecture/data-access-architecture.md)
- [Database Schema](../../database/schema/bifrost_trader_schema.sql)
- [Services Dependency Map](../../docs/architecture/services-dependency-map.md)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [TimescaleDB Documentation](https://docs.timescale.com/)

---

**Maintained by:** Bifrost Trader Development Team  
**Contact:** development@bifrost-trader.com  
**Last Updated:** October 6, 2025




