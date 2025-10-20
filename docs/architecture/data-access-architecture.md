# 🗄️ Data Access Architecture for Bifrost Trader

**Last Updated:** October 6, 2025  
**Version:** 1.0  
**Status:** ✅ PRODUCTION READY

---

## 🎯 **Overview**

This document defines the comprehensive data access architecture for Bifrost Trader's microservices platform, including database access patterns, service responsibilities, and implementation guidelines.

---

## 🏗️ **Architecture Philosophy**

### **Hybrid Microservices Data Access Pattern**

Bifrost Trader implements a **hybrid approach** that balances:
- **Service Autonomy** - Each service owns its domain data
- **Code Reusability** - Shared utilities and patterns
- **Data Consistency** - Single source of truth (PostgreSQL)
- **Performance** - Optimized access patterns per service

---

## 📊 **Service Classification**

### **🔴 Tier 1: Direct Database Access Services**
Services with **primary ownership** of specific data domains and **direct database write access**.

#### **Market Data Service** (Port 8001)
```yaml
Service Name: market-data-service (renamed from data-service)
Primary Domain: Market data and reference information
Database User: market_data_service_user

Primary Tables (Read/Write):
  - market_symbol              # Symbol master data
  - market_stock               # Company information
  - market_stock_risk_metrics  # Risk calculations
  - market_stock_hist_bars_*   # Historical price data (TimescaleDB)
  - snapshot_*                 # Market analysis snapshots

Read-Only Tables:
  - All tables (for cross-domain queries)

Responsibilities:
  - Market data ingestion
  - Symbol management
  - Historical data storage
  - Real-time data processing
  - Market snapshots generation
```

#### **Portfolio Service** (Port 8002)
```yaml
Service Name: portfolio-service
Primary Domain: Portfolio management and holdings
Database User: portfolio_service_user

Primary Tables (Read/Write):
  - portfolio        # User portfolios
  - holding          # Stock positions
  - transaction      # Buy/sell transactions
  - cash_balance     # Cash management
  - funding          # Deposits/withdrawals
  - wishlist         # User watchlists

Read-Only Tables:
  - market_symbol
  - market_stock
  - market_stock_hist_bars_*

Responsibilities:
  - Portfolio creation and management
  - Position tracking
  - P&L calculations
  - Transaction recording
  - Cash flow management
```

#### **Strategy Service** (Port 8003)
```yaml
Service Name: strategy-service
Primary Domain: Trading strategies and analysis
Database User: strategy_service_user

Primary Tables (Read/Write):
  - strategy                # Trading strategies
  - strategy_category       # Strategy classifications
  - screening               # Stock screening
  - rating                  # Strategy ratings
  - rating_indicator_result # Indicator results

Read-Only Tables:
  - market_symbol
  - market_stock_hist_bars_*
  - portfolio
  - holding
  - snapshot_*

Responsibilities:
  - Strategy development
  - Backtesting
  - Stock screening
  - Rating calculations
  - Strategy optimization
```

#### **Execution Service** (Port 8004)
```yaml
Service Name: execution-service
Primary Domain: Order execution and trade management
Database User: execution_service_user

Primary Tables (Read/Write):
  - order            # Trading orders
  - trade            # Trade executions

Read-Only Tables:
  - market_symbol
  - market_stock
  - portfolio
  - holding
  - cash_balance
  - strategy

Responsibilities:
  - Order management
  - Trade execution
  - Broker integration
  - Order routing
  - Execution analytics
```

#### **Risk Service** (Port 8005)
```yaml
Service Name: risk-service
Primary Domain: Risk management and compliance
Database User: risk_service_user

Primary Tables (Read/Write):
  - market_stock_risk_metrics  # Risk calculations
  - risk_alerts                # Risk alerts
  - compliance_logs            # Compliance tracking

Read-Only Tables:
  - All tables (for comprehensive risk analysis)

Responsibilities:
  - Risk calculations (VaR, CVaR, etc.)
  - Position monitoring
  - Compliance checking
  - Risk alerts
  - Drawdown monitoring
```

---

### **🟡 Tier 2: Limited Database Access Services**
Services with **read-heavy** access patterns and minimal writes, primarily for UI and reporting.

#### **Web Portal** (Port 8006)
```yaml
Service Name: web-portal
Primary Domain: User interface and dashboard
Database User: web_portal_user

Read-Only Tables:
  - All tables (for dashboard display)

Read/Write Tables:
  - user_static_setting  # User preferences
  - wishlist            # User watchlists

Responsibilities:
  - Dashboard display
  - User interface
  - Data visualization
  - User preferences
  - Real-time updates
```

#### **Analytics Service** (Port 8007)
```yaml
Service Name: analytics-service
Primary Domain: Analytics and reporting
Database User: analytics_service_user

Read-Only Tables:
  - All tables (for comprehensive analytics)

Read/Write Tables:
  - analytics_reports    # Generated reports
  - analytics_cache      # Analytics cache

Responsibilities:
  - Performance analytics
  - Custom reporting
  - Data aggregation
  - Trend analysis
  - Export functionality
```

---

### **🟢 Tier 3: No Direct Database Access Services**
Services that communicate **only through APIs** and have no direct database access.

#### **API Gateway** (Port 8000)
```yaml
Service Name: api-gateway
Primary Domain: API routing and load balancing
Database Access: None

Responsibilities:
  - Request routing
  - Load balancing
  - Authentication/Authorization
  - Rate limiting
  - Service discovery
  - Circuit breaking
```

#### **ML Service** (Port 8008)
```yaml
Service Name: ml-service
Primary Domain: Machine learning and predictions
Database Access: None (API calls only)

Data Sources:
  - Market Data Service API
  - Portfolio Service API
  - Strategy Service API

Responsibilities:
  - Model training
  - Price predictions
  - Pattern recognition
  - Anomaly detection
  - Model serving
```

#### **News Service** (Port 8009)
```yaml
Service Name: news-service
Primary Domain: News and sentiment analysis
Database Access: None (External APIs + Cache)

Data Sources:
  - External news APIs
  - Social media APIs
  - Redis cache

Responsibilities:
  - News aggregation
  - Sentiment analysis
  - Real-time news feeds
  - News filtering
  - Event detection
```

#### **Compliance Service** (Port 8010)
```yaml
Service Name: compliance-service
Primary Domain: Regulatory compliance
Database Access: None (API calls only)

Data Sources:
  - Risk Service API
  - Execution Service API
  - Portfolio Service API

Responsibilities:
  - Regulatory reporting
  - Audit trail generation
  - Compliance checks
  - Documentation
  - Report generation
```

#### **Microstructure Service** (Port 8011)
```yaml
Service Name: microstructure-service
Primary Domain: Market microstructure analysis
Database Access: None (Real-time data only)

Data Sources:
  - Real-time market data feeds
  - WebSocket streams
  - Redis cache

Responsibilities:
  - Order book analysis
  - Market depth analysis
  - Liquidity analysis
  - Spread analysis
  - Market impact estimation
```

---

## 🔐 **Database Access Control**

### **Service-Specific Database Users**

Each service uses a dedicated PostgreSQL user with granular permissions:

```sql
-- Market Data Service User
CREATE USER market_data_service_user WITH PASSWORD 'secure_password';
GRANT SELECT, INSERT, UPDATE, DELETE ON 
    market_symbol, 
    market_stock, 
    market_stock_risk_metrics,
    market_stock_hist_bars_min_ts,
    market_stock_hist_bars_hour_ts,
    market_stock_hist_bars_day_ts,
    snapshot_screening,
    snapshot_overview,
    snapshot_technical,
    snapshot_fundamental,
    snapshot_setup,
    snapshot_bull_flag,
    snapshot_earning
TO market_data_service_user;
GRANT SELECT ON ALL TABLES TO market_data_service_user;

-- Portfolio Service User
CREATE USER portfolio_service_user WITH PASSWORD 'secure_password';
GRANT SELECT, INSERT, UPDATE, DELETE ON 
    portfolio,
    holding,
    transaction,
    cash_balance,
    funding,
    wishlist
TO portfolio_service_user;
GRANT SELECT ON market_symbol, market_stock, market_stock_hist_bars_* TO portfolio_service_user;

-- Strategy Service User
CREATE USER strategy_service_user WITH PASSWORD 'secure_password';
GRANT SELECT, INSERT, UPDATE, DELETE ON 
    strategy,
    strategy_category,
    strategy_strategy_category,
    screening,
    rating,
    rating_indicator_result
TO strategy_service_user;
GRANT SELECT ON market_symbol, market_stock_hist_bars_*, portfolio, holding, snapshot_* TO strategy_service_user;

-- Execution Service User
CREATE USER execution_service_user WITH PASSWORD 'secure_password';
GRANT SELECT, INSERT, UPDATE, DELETE ON 
    "order",
    trade
TO execution_service_user;
GRANT SELECT ON market_symbol, portfolio, holding, cash_balance, strategy TO execution_service_user;

-- Risk Service User
CREATE USER risk_service_user WITH PASSWORD 'secure_password';
GRANT SELECT, INSERT, UPDATE, DELETE ON market_stock_risk_metrics TO risk_service_user;
GRANT SELECT ON ALL TABLES TO risk_service_user;

-- Web Portal User (Read-only + user settings)
CREATE USER web_portal_user WITH PASSWORD 'secure_password';
GRANT SELECT ON ALL TABLES TO web_portal_user;
GRANT INSERT, UPDATE, DELETE ON user_static_setting, wishlist TO web_portal_user;

-- Analytics Service User (Read-only)
CREATE USER analytics_service_user WITH PASSWORD 'secure_password';
GRANT SELECT ON ALL TABLES TO analytics_service_user;
```

### **Connection Configuration**

Each service configures its database connection with service-specific credentials:

```python
# services/market-data-service/.env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=bifrost_trader
DB_USERNAME=market_data_service_user
DB_PASSWORD=secure_password
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20

# services/portfolio-service/.env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=bifrost_trader
DB_USERNAME=portfolio_service_user
DB_PASSWORD=secure_password
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20
```

---

## 🏛️ **Shared Data Access Layer**

### **Architecture**

```
shared/
├── database/
│   ├── __init__.py
│   ├── connection.py          # Async database connection management
│   ├── base_repository.py     # Base repository pattern
│   └── permissions.py         # Service-specific permissions
├── models/
│   ├── __init__.py
│   ├── base.py                # Base model class
│   ├── market_data.py         # Market data models
│   ├── portfolio.py           # Portfolio models
│   ├── strategy.py            # Strategy models
│   └── execution.py           # Execution models
├── repositories/
│   ├── __init__.py
│   ├── base.py                # Base repository
│   ├── market_data_repo.py    # Market data repository
│   ├── portfolio_repo.py      # Portfolio repository
│   └── strategy_repo.py       # Strategy repository
└── schemas/
    ├── __init__.py
    ├── common.py              # Common Pydantic schemas
    ├── market_data.py         # Market data schemas
    ├── portfolio.py           # Portfolio schemas
    └── strategy.py            # Strategy schemas
```

### **Base Repository Pattern**

All repositories inherit from a base class with common CRUD operations:

```python
from shared.repositories.base import BaseRepository

class MarketDataRepository(BaseRepository[MarketData, MarketDataCreate, MarketDataUpdate]):
    async def get_latest_price(self, symbol: str) -> Optional[MarketData]:
        # Service-specific implementation
        pass
```

### **Usage in Services**

```python
# services/market-data-service/src/api/endpoints/market_data.py
from shared.repositories import MarketDataRepository
from shared.schemas import MarketDataResponse

@router.get("/market-data/{symbol}", response_model=MarketDataResponse)
async def get_market_data(
    symbol: str,
    db: AsyncSession = Depends(get_db_session)
):
    repo = MarketDataRepository(db)
    data = await repo.get_latest_price(symbol)
    return data
```

---

## 🔄 **Cross-Service Data Access**

### **Pattern 1: Direct Database Read (Same Database)**

Services can read from other service tables with read-only permissions:

```python
# portfolio-service reading market data
from shared.repositories import MarketDataRepository

class PortfolioService:
    async def calculate_portfolio_value(self, portfolio_id: int):
        # Read market data directly
        market_repo = MarketDataRepository(self.db)
        holdings = await self.portfolio_repo.get_holdings(portfolio_id)
        
        total_value = 0
        for holding in holdings:
            latest_price = await market_repo.get_latest_price(holding.symbol)
            total_value += holding.quantity * latest_price.close_price
        
        return total_value
```

### **Pattern 2: Service-to-Service API Call (Recommended)**

For complex operations or when database access is restricted:

```python
# ml-service calling market-data-service API
import httpx

class MLService:
    async def get_training_data(self, symbol: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"http://market-data-service:8001/api/historical/{symbol}",
                params={"days": 365}
            )
            return response.json()
```

### **Pattern 3: Event-Driven (For Real-time Updates)**

Use message queue for asynchronous communication:

```python
# market-data-service publishes price updates
from shared.events import EventBus

class MarketDataService:
    async def update_price(self, symbol: str, price: float):
        # Update database
        await self.repo.update_price(symbol, price)
        
        # Publish event
        await EventBus.publish("price.updated", {
            "symbol": symbol,
            "price": price,
            "timestamp": datetime.now()
        })

# portfolio-service subscribes to price updates
class PortfolioService:
    async def on_price_updated(self, event):
        # Update portfolio values
        await self.update_portfolio_values(event["symbol"])
```

---

## 📋 **Implementation Guidelines**

### **1. Service Development Checklist**

For each new service:

- [ ] Determine service tier (Direct DB / Limited DB / No DB)
- [ ] Create service-specific database user with appropriate permissions
- [ ] Implement SQLAlchemy models for primary tables
- [ ] Create Pydantic schemas for API validation
- [ ] Implement repository pattern for data access
- [ ] Add async database connection management
- [ ] Implement proper error handling
- [ ] Add comprehensive logging
- [ ] Create unit tests for repositories
- [ ] Create integration tests for database operations
- [ ] Document API endpoints
- [ ] Set up monitoring and metrics

### **2. Database Model Standards**

All SQLAlchemy models must follow these standards:

```python
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class ModelTemplate(Base):
    """Standard model template."""
    
    __tablename__ = "table_name"
    
    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Business fields
    name = Column(String(255), nullable=False)
    
    # Metadata (required on all models)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    # Indexes
    __table_args__ = (
        Index("idx_name", "name"),
    )
    
    def __repr__(self):
        return f"<ModelTemplate(id={self.id}, name='{self.name}')>"
```

### **3. Repository Pattern Standards**

```python
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from shared.repositories.base import BaseRepository

class ServiceRepository(BaseRepository[Model, CreateSchema, UpdateSchema]):
    """Service-specific repository."""
    
    def __init__(self, db_session: AsyncSession):
        super().__init__(Model, db_session)
    
    async def get_by_custom_field(self, field_value: str) -> Optional[Model]:
        """Service-specific query method."""
        return await self.get_by_field("custom_field", field_value)
    
    async def bulk_operation(self, items: List[CreateSchema]) -> List[Model]:
        """Service-specific bulk operation."""
        return await self.create_many(items)
```

### **4. Pydantic Schema Standards**

```python
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator

class EntityBase(BaseModel):
    """Base schema for entity."""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    
    @validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()

class EntityCreate(EntityBase):
    """Schema for creating entity."""
    pass

class EntityUpdate(BaseModel):
    """Schema for updating entity."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)

class EntityResponse(EntityBase):
    """Schema for entity API response."""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
```

---

## 🚀 **Performance Optimization**

### **Connection Pooling**

```python
# Optimized connection pool configuration
engine = create_async_engine(
    connection_string,
    pool_size=10,           # Base pool size
    max_overflow=20,        # Additional connections
    pool_timeout=30,        # Connection timeout
    pool_recycle=3600,      # Recycle connections after 1 hour
    pool_pre_ping=True,     # Test connections before use
    echo=False              # Disable SQL logging in production
)
```

### **Query Optimization**

```python
# Use selective loading
query = select(Model).options(
    selectinload(Model.relationship_1),
    joinedload(Model.relationship_2)
)

# Use pagination
query = query.offset(skip).limit(limit)

# Use indexes effectively
query = query.where(Model.indexed_field == value)
```

### **Caching Strategy**

```python
from redis import asyncio as aioredis

class CachedRepository:
    def __init__(self, db: AsyncSession, redis: aioredis.Redis):
        self.db = db
        self.redis = redis
    
    async def get_with_cache(self, key: str):
        # Try cache first
        cached = await self.redis.get(f"data:{key}")
        if cached:
            return json.loads(cached)
        
        # Query database
        data = await self.repo.get_by_field("key", key)
        
        # Cache result
        await self.redis.setex(
            f"data:{key}",
            3600,  # 1 hour TTL
            json.dumps(data.to_dict())
        )
        
        return data
```

---

## 📊 **Monitoring & Observability**

### **Database Metrics**

Track these metrics for each service:

- **Connection Pool Usage**: Active/idle connections
- **Query Performance**: Query duration, slow queries
- **Transaction Success Rate**: Commits vs rollbacks
- **Lock Contention**: Lock wait times
- **Cache Hit Rate**: Redis cache effectiveness

### **Service Health Checks**

```python
@router.get("/health")
async def health_check(db: AsyncSession = Depends(get_db_session)):
    try:
        # Test database connection
        await db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}
```

---

## 🎯 **Migration Path**

### **Phase 1: Foundation (Completed)**
- ✅ Refactor data-service models to SQLAlchemy
- ✅ Implement repository pattern
- ✅ Create async database connection
- ✅ Add TimescaleDB integration

### **Phase 2: Service Implementation (In Progress)**
- 🔄 Implement portfolio-service models
- 🔄 Implement strategy-service models
- 🔄 Implement execution-service models
- 🔄 Create service-specific repositories

### **Phase 3: Integration**
- ⏳ Set up service-specific database users
- ⏳ Implement cross-service data access patterns
- ⏳ Add caching layers
- ⏳ Implement event-driven communication

### **Phase 4: Optimization**
- ⏳ Add comprehensive monitoring
- ⏳ Optimize query performance
- ⏳ Implement advanced caching strategies
- ⏳ Add database scaling strategies

---

## 📚 **References**

- **SQLAlchemy Documentation**: https://docs.sqlalchemy.org/
- **FastAPI Database Integration**: https://fastapi.tiangolo.com/tutorial/sql-databases/
- **TimescaleDB Best Practices**: https://docs.timescale.com/
- **Microservices Data Patterns**: https://microservices.io/patterns/data/

---

**Last Updated**: October 6, 2025  
**Next Review**: After Phase 2 completion




