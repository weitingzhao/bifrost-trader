# PostgreSQL Configuration for Bifrost Trader

## Database Setup

Bifrost Trader uses **PostgreSQL with TimescaleDB** extension for optimal time-series data handling, following the same architecture as Smart Trader.

### Environment Configuration

Create `.env` file with the following database settings:

```bash
# Database Configuration
DB_ENGINE=timescale.db.backends.postgresql
DB_NAME=bifrost_trader
DB_USERNAME=postgres
DB_PASS=Spm123!@#
DB_HOST=localhost
DB_PORT=5432

# TimescaleDB Configuration
TIMESCALEDB_TELEMETRY=off
PGDATA=/var/lib/postgresql/data/pgdata

# Redis Configuration (for caching and message broker)
REDIS_HOST=localhost
REDIS_PORT=6379

# API Configuration
API_BASE_URL=http://localhost:8000
```

### Production Configuration

For production deployment:

```bash
# Production Database
DB_ENGINE=timescale.db.backends.postgresql
DB_NAME=bifrost_trader_prod
DB_USERNAME=bifrost_db_user
DB_PASS=your_secure_password
DB_HOST=your_postgres_host
DB_PORT=5432
```

## Docker Setup

### docker-compose.yml for Database

```yaml
version: '3.8'

services:
  postgres:
    image: timescale/timescaledb:latest-pg17
    container_name: bifrost-trader.postgres
    restart: always
    environment:
      - POSTGRES_USER=${DB_USERNAME}
      - POSTGRES_PASSWORD=${DB_PASS}
      - POSTGRES_DB=${DB_NAME}
      - TIMESCALEDB_TELEMETRY=off
      - PGDATA=/var/lib/postgresql/data/pgdata
    ports:
      - "5432:5432"
    env_file:
      - .env
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./database/init:/docker-entrypoint-initdb.d
    command: [
      "postgres",
      "-c", "max_connections=200",
      "-c", "shared_buffers=4GB",
      "-c", "effective_cache_size=8GB",
      "-c", "maintenance_work_mem=1GB",
      "-c", "random_page_cost=1.1",
      "-c", "work_mem=100MB",
      "-c", "min_wal_size=2GB",
      "-c", "max_wal_size=8GB",
      "-c", "checkpoint_completion_target=0.9",
      "-c", "wal_buffers=16MB",
      "-c", "default_statistics_target=100"
    ]
    networks:
      - bifrost_network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USERNAME} -d ${DB_NAME}"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: bifrost-trader.redis
    restart: always
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - bifrost_network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
  redis_data:

networks:
  bifrost_network:
    driver: bridge
```

## Database Schema Overview

### Core Tables (Migrated from Smart Trader)

#### Market Data Tables
- **`market_symbol`**: Master table for all market symbols
- **`market_stock`**: Detailed company information
- **`market_stock_hist_bars_min_ts`**: Minute-level price data (TimescaleDB)
- **`market_stock_hist_bars_day_ts`**: Daily price data (TimescaleDB)
- **`market_stock_hist_bars_hour_ts`**: Hourly price data (TimescaleDB)

#### Portfolio Management
- **`portfolio`**: User portfolios
- **`holding`**: Stock holdings in portfolios
- **`transaction`**: Buy/sell transactions
- **`order`**: Trading orders
- **`trade`**: Trade records
- **`funding`**: Portfolio funding records
- **`cash_balance`**: Cash balance tracking

#### Strategy & Analysis
- **`strategy`**: Trading strategies
- **`screening`**: Stock screening configurations
- **`rating`**: Strategy ratings for symbols
- **`snapshot_*`**: Various snapshot tables for analysis

#### User Management
- **`user_static_setting`**: User trading preferences
- **`utilities_lookup`**: System lookup tables
- **`wishlist`**: User watchlists

## Microservices Database Access

Each microservice will have its own database connection:

### Data Service
- **Primary**: Market data tables
- **Read/Write**: Historical price data, company information

### Portfolio Service
- **Primary**: Portfolio, holdings, transactions
- **Read/Write**: User portfolios, trade records

### Strategy Service
- **Primary**: Strategies, ratings, snapshots
- **Read/Write**: Strategy configurations, analysis results

### Trading Service
- **Primary**: Orders, trades, executions
- **Read/Write**: Order management, trade execution

## Connection Utilities

### Python Database Connection

```python
import psycopg2
import os
from sqlalchemy import create_engine
from typing import Dict, Any

class DatabaseConfig:
    def __init__(self):
        self.host = os.getenv('DB_HOST', 'localhost')
        self.port = os.getenv('DB_PORT', '5432')
        self.dbname = os.getenv('DB_NAME', 'bifrost_trader')
        self.user = os.getenv('DB_USERNAME', 'postgres')
        self.password = os.getenv('DB_PASS', '')
        
    def get_connection_string(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}"
    
    def get_psycopg2_connection(self):
        return psycopg2.connect(
            host=self.host,
            port=self.port,
            dbname=self.dbname,
            user=self.user,
            password=self.password
        )
    
    def get_sqlalchemy_engine(self):
        return create_engine(self.get_connection_string())
```

## Performance Optimization

### TimescaleDB Hypertables
- All time-series tables use TimescaleDB hypertables
- Automatic partitioning by time
- Compression for historical data
- Continuous aggregates for performance

### Indexing Strategy
- Primary keys on all tables
- Composite indexes on frequently queried columns
- Time-based indexes for time-series data
- Symbol-based indexes for market data

### Connection Pooling
- PgBouncer for connection pooling
- Separate pools for read/write operations
- Connection limits per service

## Migration from Smart Trader

### Data Migration Steps
1. **Schema Export**: Export Smart Trader schema
2. **Data Export**: Export existing data
3. **Schema Import**: Import to Bifrost Trader
4. **Data Import**: Import historical data
5. **Validation**: Verify data integrity

### Schema Updates
- Add microservice-specific fields
- Update foreign key relationships
- Add new indexes for microservices
- Implement proper partitioning

## Monitoring & Maintenance

### Database Monitoring
- Connection monitoring
- Query performance tracking
- Disk usage monitoring
- Backup verification

### Maintenance Tasks
- Regular VACUUM and ANALYZE
- Index maintenance
- Partition management
- Backup scheduling

## Security

### Access Control
- Service-specific database users
- Role-based permissions
- Network access restrictions
- SSL/TLS encryption

### Data Protection
- Regular backups
- Point-in-time recovery
- Data encryption at rest
- Audit logging
