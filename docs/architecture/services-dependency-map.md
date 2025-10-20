# 🗺️ Bifrost Trader Services Dependency Map

This document provides a comprehensive overview of the microservices architecture, their dependencies, and communication patterns in Bifrost Trader.

## 🎯 **Services Overview**

### **Core Services (Direct Database Access)**
1. **API Gateway** (Port 8000) - ✅ **COMPLETE** - 🟢 No DB Access
2. **Market Data Service** (Port 8001) - 🚧 **IN PROGRESS** - 🔴 Direct DB Access
3. **Portfolio Service** (Port 8002) - 🚧 **IN PROGRESS** - 🔴 Direct DB Access
4. **Strategy Service** (Port 8003) - 🚧 **IN PROGRESS** - 🔴 Direct DB Access
5. **Execution Service** (Port 8004) - ❌ **PLANNED** - 🔴 Direct DB Access
6. **Risk Service** (Port 8005) - ❌ **PLANNED** - 🔴 Direct DB Access
7. **Web Portal** (Port 8006) - ✅ **COMPLETE** - 🟡 Limited DB Access
8. **Control Center** (Port 8007) - ✅ **COMPLETE** - 🟢 No DB Access

### **Supporting Services (API-Only or Limited DB Access)**
9. **Analytics Service** (Port 8008) - ❌ **PLANNED** - 🟡 Limited DB Access
9. **ML Service** (Port 8008) - ❌ **PLANNED** - 🟢 No DB Access (API Only)
10. **News Service** (Port 8009) - ❌ **PLANNED** - 🟢 No DB Access (API Only)
11. **Compliance Service** (Port 8010) - ❌ **PLANNED** - 🟢 No DB Access (API Only)
12. **Microstructure Service** (Port 8011) - ❌ **PLANNED** - 🟢 No DB Access (API Only)

## 🗄️ **Database Access Patterns**

### **Service Tier Classification**

**🔴 Tier 1: Direct Database Access**
- Market Data Service (Port 8001)
- Portfolio Service (Port 8002)
- Strategy Service (Port 8003)
- Execution Service (Port 8004)
- Risk Service (Port 8005)

These services have primary ownership of specific database tables and can perform read/write operations.

**🟡 Tier 2: Limited Database Access**
- Web Portal (Port 8006)
- Analytics Service (Port 8007)

These services primarily read data with minimal writes (user preferences, cache, etc.).

**🟢 Tier 3: No Direct Database Access**
- API Gateway (Port 8000)
- Control Center (Port 8007)
- ML Service (Port 8008)
- News Service (Port 8009)
- Compliance Service (Port 8010)
- Microstructure Service (Port 8011)

These services communicate only through APIs and have no direct database connections.

### **Database Table Ownership**

| Service | Primary Tables | Read-Only Tables |
|---------|---------------|------------------|
| Market Data | market_symbol, market_stock, hist_bars_*, snapshot_* | All (for queries) |
| Portfolio | portfolio, holding, transaction, cash_balance | market_symbol, hist_bars_* |
| Strategy | strategy, screening, rating | market_*, portfolio, holding, snapshot_* |
| Execution | order, trade | market_symbol, portfolio, strategy |
| Risk | risk_metrics | All (for risk analysis) |
| Web Portal | user_settings, wishlist | All (for display) |
| Analytics | analytics_* | All (for reporting) |

**See:** [Data Access Architecture Documentation](./data-access-architecture.md) for complete details.

---

## 🏗️ **Dependency Architecture**

```mermaid
graph TB
    subgraph "Client Layer"
        WEB[Web Portal<br/>Port 8006]
        API[External APIs]
    end
    
    subgraph "Gateway Layer"
        GATEWAY[API Gateway<br/>Port 8000]
    end
    
    subgraph "Core Services"
        DATA[Data Service<br/>Port 8001]
        PORTFOLIO[Portfolio Service<br/>Port 8002]
        STRATEGY[Strategy Service<br/>Port 8003]
        EXECUTION[Execution Service<br/>Port 8004]
        RISK[Risk Service<br/>Port 8005]
    end
    
    subgraph "Supporting Services"
        ANALYTICS[Analytics Service<br/>Port 8007]
        ML[ML Service<br/>Port 8008]
        NEWS[News Service<br/>Port 8009]
        COMPLIANCE[Compliance Service<br/>Port 8010]
        MICRO[Microstructure Service<br/>Port 8011]
    end
    
    subgraph "Infrastructure"
        DB[(PostgreSQL<br/>+ TimescaleDB)]
        REDIS[(Redis<br/>Cache & Queue)]
        RABBITMQ[(RabbitMQ<br/>Message Queue)]
    end
    
    subgraph "External Services"
        YAHOO[Yahoo Finance API]
        IB[Interactive Brokers]
        ALPACA[Alpaca API]
    end
    
    %% Client to Gateway
    WEB --> GATEWAY
    API --> GATEWAY
    
    %% Gateway to Services
    GATEWAY --> DATA
    GATEWAY --> PORTFOLIO
    GATEWAY --> STRATEGY
    GATEWAY --> EXECUTION
    GATEWAY --> RISK
    GATEWAY --> ANALYTICS
    GATEWAY --> ML
    GATEWAY --> NEWS
    GATEWAY --> COMPLIANCE
    GATEWAY --> MICRO
    
    %% Core Service Dependencies
    PORTFOLIO --> DATA
    STRATEGY --> DATA
    STRATEGY --> PORTFOLIO
    EXECUTION --> DATA
    EXECUTION --> PORTFOLIO
    EXECUTION --> STRATEGY
    RISK --> DATA
    RISK --> PORTFOLIO
    RISK --> STRATEGY
    
    %% Supporting Service Dependencies
    ANALYTICS --> DATA
    ANALYTICS --> PORTFOLIO
    ANALYTICS --> STRATEGY
    ML --> DATA
    ML --> PORTFOLIO
    ML --> STRATEGY
    NEWS --> DATA
    COMPLIANCE --> PORTFOLIO
    COMPLIANCE --> RISK
    MICRO --> DATA
    
    %% Infrastructure Dependencies
    DATA --> DB
    DATA --> REDIS
    PORTFOLIO --> DB
    PORTFOLIO --> REDIS
    STRATEGY --> DB
    STRATEGY --> REDIS
    EXECUTION --> DB
    EXECUTION --> REDIS
    EXECUTION --> RABBITMQ
    RISK --> DB
    RISK --> REDIS
    
    %% External Service Dependencies
    DATA --> YAHOO
    EXECUTION --> IB
    EXECUTION --> ALPACA
```

## 📊 **Detailed Service Dependencies**

### **1. API Gateway (Port 8000) - ✅ COMPLETE**
**Purpose**: Central routing, service discovery, authentication
**Dependencies**: None (entry point)
**Provides**: 
- Service routing
- Load balancing
- Authentication/authorization
- Rate limiting
- Health monitoring

### **2. Data Service (Port 8001) - 🚧 IN PROGRESS**
**Purpose**: Market data ingestion, storage, and retrieval
**Dependencies**: 
- **Database**: PostgreSQL + TimescaleDB
- **Cache**: Redis
- **External**: Yahoo Finance API
**Provides**:
- Market symbol management
- Historical data storage
- Real-time data streaming
- Data validation and cleaning

**Current Status**:
- ✅ Basic FastAPI structure
- ✅ MarketSymbol and MarketData models
- ✅ Yahoo Finance service (partial)
- 🚧 Data ingestion pipeline
- ❌ Real-time data streaming
- ❌ Data validation

### **3. Portfolio Service (Port 8002) - 🚧 IN PROGRESS**
**Purpose**: Portfolio management, position tracking, P&L calculation
**Dependencies**:
- **Data Service**: For real-time pricing
- **Database**: PostgreSQL
- **Cache**: Redis
**Provides**:
- Portfolio CRUD operations
- Position tracking
- P&L calculations
- Cash balance management
- Transaction history

**Current Status**:
- ✅ Basic models (portfolio_reference.py)
- 🚧 FastAPI structure
- ❌ Business logic implementation
- ❌ Data Service integration

### **4. Strategy Service (Port 8003) - 🚧 IN PROGRESS**
**Purpose**: Strategy development, backtesting, optimization
**Dependencies**:
- **Data Service**: For historical data
- **Portfolio Service**: For position data
- **Database**: PostgreSQL
- **Cache**: Redis
**Provides**:
- Strategy development framework
- Backtesting engine
- Performance analytics
- Strategy optimization

**Current Status**:
- ✅ Backtrader framework migrated
- ✅ Cerebro integration
- ✅ Strategy templates
- 🚧 FastAPI integration
- ❌ Data Service integration
- ❌ Portfolio Service integration

### **5. Execution Service (Port 8004) - ❌ PLANNED**
**Purpose**: Order execution, trade management, broker integration
**Dependencies**:
- **Data Service**: For real-time pricing
- **Portfolio Service**: For position updates
- **Strategy Service**: For strategy signals
- **Risk Service**: For risk checks
- **Database**: PostgreSQL
- **Message Queue**: RabbitMQ
**Provides**:
- Order placement and management
- Trade execution
- Broker integration (IB, Alpaca)
- Execution reporting

### **6. Risk Service (Port 8005) - ❌ PLANNED**
**Purpose**: Risk management, compliance, position limits
**Dependencies**:
- **Data Service**: For market data
- **Portfolio Service**: For position data
- **Strategy Service**: For strategy risk
- **Database**: PostgreSQL
- **Cache**: Redis
**Provides**:
- VaR calculations
- Drawdown monitoring
- Position limits
- Compliance checking
- Risk reporting

### **7. Web Portal (Port 8006) - ✅ COMPLETE**
**Purpose**: User interface, dashboard, real-time monitoring
**Dependencies**:
- **API Gateway**: For service communication
- **Database**: PostgreSQL (direct access)
- **Cache**: Redis
**Provides**:
- User dashboard
- Portfolio visualization
- Real-time data display
- Strategy monitoring
- Trading interface

## 🔄 **Communication Patterns**

### **Synchronous Communication (REST APIs)**
- **Request-Response**: Direct API calls between services
- **Used for**: Real-time data requests, immediate operations
- **Examples**: 
  - Portfolio Service → Data Service (get current price)
  - Web Portal → Portfolio Service (get portfolio data)

### **Asynchronous Communication (Message Queue)**
- **Event-Driven**: Services publish/subscribe to events
- **Used for**: Non-critical operations, batch processing
- **Examples**:
  - Data Service → Portfolio Service (price updates)
  - Strategy Service → Execution Service (trade signals)

### **Database Sharing**
- **Shared Database**: Some services share database access
- **Used for**: Complex queries, data consistency
- **Examples**:
  - All services → Market data tables
  - Portfolio/Strategy services → Transaction tables

## 🚀 **Implementation Priority**

### **Phase 1: Foundation (Current)**
1. **Data Service** - Complete market data infrastructure
2. **Portfolio Service** - Basic portfolio management
3. **Strategy Service** - Backtesting integration

### **Phase 2: Core Trading (Next)**
4. **Execution Service** - Order execution
5. **Risk Service** - Risk management
6. **Enhanced Integration** - Service communication

### **Phase 3: Advanced Features (Future)**
7. **Analytics Service** - Advanced analytics
8. **ML Service** - Machine learning
9. **News Service** - News integration
10. **Compliance Service** - Regulatory compliance
11. **Microstructure Service** - Market microstructure

## 📋 **Service Health & Status**

### **✅ Production Ready**
- **API Gateway**: Complete and functional
- **Web Portal**: Complete with database integration

### **🚧 In Development**
- **Data Service**: Basic structure, needs enhancement
- **Portfolio Service**: Models exist, needs implementation
- **Strategy Service**: Backtrader migrated, needs API integration

### **❌ Planned**
- **Execution Service**: Not started
- **Risk Service**: Not started
- **Analytics Service**: Not started
- **ML Service**: Not started
- **News Service**: Not started
- **Compliance Service**: Not started
- **Microstructure Service**: Not started

## 🔧 **Development Guidelines**

### **Service Independence**
- Each service should be independently deployable
- Services should have their own database schemas
- Minimal direct dependencies between services

### **Communication Standards**
- Use REST APIs for synchronous communication
- Use message queues for asynchronous communication
- Implement circuit breakers for fault tolerance

### **Data Consistency**
- Use eventual consistency for non-critical data
- Implement saga pattern for distributed transactions
- Use event sourcing for audit trails

---

**🎯 This dependency map serves as the blueprint for building and integrating all Bifrost Trader services. It ensures proper service boundaries, clear dependencies, and scalable architecture.**
