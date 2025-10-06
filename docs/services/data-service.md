# 📊 Data Service Documentation

The Data Service is the foundation of Bifrost Trader, responsible for market data ingestion, storage, and retrieval. It provides real-time and historical market data to all other services in the platform.

## 🎯 **Service Overview**

### **Purpose**
- **Market Data Ingestion**: Fetch data from external sources (Yahoo Finance)
- **Data Storage**: Store data in TimescaleDB for time-series optimization
- **Data Retrieval**: Provide APIs for accessing market data
- **Data Validation**: Ensure data quality and consistency

### **Port**: 8001
### **Status**: 🚧 **IN PROGRESS** - Enhanced with complete Yahoo Finance integration

## 🏗️ **Architecture**

### **Core Components**
1. **Yahoo Finance Service** - External data fetching
2. **Data Ingestion Service** - Data pipeline management
3. **Market Symbol Model** - Symbol metadata storage
4. **Market Data Model** - Time-series data storage
5. **FastAPI Application** - REST API endpoints

### **Database Integration**
- **PostgreSQL + TimescaleDB** - Time-series optimized storage
- **Redis** - Caching layer for frequently accessed data
- **Connection Pooling** - Efficient database connections

## 📊 **Data Models**

### **Market Symbol Model**
```python
class MarketSymbolModel(Base):
    __tablename__ = 'market_symbol'
    
    symbol = Column(String(20), primary_key=True)
    name = Column(String(200), nullable=False)
    market = Column(String(50), nullable=False)
    asset_type = Column(String(50), nullable=False)
    sector = Column(String(100), nullable=True)
    industry = Column(String(100), nullable=True)
    country = Column(String(50), nullable=True)
    currency = Column(String(10), nullable=True)
    # ... additional fields
```

### **Market Data Model**
```python
class MarketDataModel(Base):
    __tablename__ = 'market_data'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(20), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    open_price = Column(Float, nullable=False)
    high_price = Column(Float, nullable=False)
    low_price = Column(Float, nullable=False)
    close_price = Column(Float, nullable=False)
    volume = Column(Integer, nullable=False)
    adjusted_close = Column(Float, nullable=True)
    # ... additional fields
```

## 🚀 **API Endpoints**

### **Health & Status**
- `GET /health` - Service health check
- `GET /stats/data` - Data ingestion statistics

### **Symbol Management**
- `GET /symbols/{symbol}/info` - Get comprehensive symbol information
- `GET /symbols/{symbol}/latest-price` - Get latest price data
- `GET /symbols/search?query={query}` - Search for symbols
- `POST /symbols/{symbol}/validate` - Validate symbol existence

### **Data Ingestion**
- `POST /symbols/{symbol}/ingest` - Ingest all data for a symbol
- `POST /symbols/batch-ingest` - Batch ingest multiple symbols

### **Historical Data**
- `GET /symbols/{symbol}/historical` - Get historical data
- `GET /symbols/{symbol}/data` - Get market data with filters

## 🔧 **Services**

### **Yahoo Finance Service**
**Purpose**: Fetch data from Yahoo Finance API
**Features**:
- Historical data fetching
- Real-time price data
- Company information retrieval
- Symbol validation
- Batch data processing

**Key Methods**:
```python
async def get_historical_data(symbol: str, period: str) -> Dict[str, Any]
async def get_company_info(symbol: str) -> Dict[str, Any]
async def get_latest_price(symbol: str) -> Dict[str, Any]
async def batch_get_data(symbols: List[str]) -> Dict[str, Any]
def validate_symbol(symbol: str) -> bool
async def search_symbols(query: str) -> List[Dict[str, Any]]
```

### **Data Ingestion Service**
**Purpose**: Manage the complete data ingestion pipeline
**Features**:
- Symbol information ingestion
- Historical data ingestion
- Real-time price updates
- Batch processing
- Data validation and cleaning

**Key Methods**:
```python
async def ingest_symbol_info(symbol: str) -> Dict[str, Any]
async def ingest_historical_data(symbol: str, period: str) -> Dict[str, Any]
async def ingest_latest_price(symbol: str) -> Dict[str, Any]
async def batch_ingest_symbols(symbols: List[str]) -> Dict[str, Any]
async def update_symbol_data(symbol: str) -> Dict[str, Any]
def get_ingestion_stats() -> Dict[str, Any]
```

## 📈 **Data Flow**

### **Ingestion Pipeline**
1. **Symbol Validation** - Verify symbol exists
2. **Company Info** - Fetch and store company metadata
3. **Historical Data** - Fetch and store historical OHLCV data
4. **Real-time Updates** - Fetch and store latest price data
5. **Data Validation** - Ensure data quality and consistency

### **Retrieval Pipeline**
1. **API Request** - Receive request from client
2. **Cache Check** - Check Redis for cached data
3. **Database Query** - Query TimescaleDB if not cached
4. **Data Processing** - Format and validate response
5. **Response** - Return data to client

## 🎯 **Usage Examples**

### **Ingest Symbol Data**
```bash
# Ingest all data for Apple stock
curl -X POST "http://localhost:8001/symbols/AAPL/ingest"
```

### **Get Symbol Information**
```bash
# Get comprehensive info for Apple
curl "http://localhost:8001/symbols/AAPL/info"
```

### **Get Latest Price**
```bash
# Get latest price for Apple
curl "http://localhost:8001/symbols/AAPL/latest-price"
```

### **Search Symbols**
```bash
# Search for Apple-related symbols
curl "http://localhost:8001/symbols/search?query=AAPL"
```

### **Batch Ingest**
```bash
# Ingest multiple symbols
curl -X POST "http://localhost:8001/symbols/batch-ingest" \
  -H "Content-Type: application/json" \
  -d '["AAPL", "MSFT", "GOOGL"]'
```

## 🔧 **Configuration**

### **Environment Variables**
```bash
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=bifrost_trader
DB_USERNAME=postgres
DB_PASS=your_password

# Service Configuration
PORT=8001
HOST=0.0.0.0
LOG_LEVEL=INFO

# Redis Configuration
REDIS_URL=redis://localhost:6379
```

### **Dependencies**
```python
# Core dependencies
fastapi>=0.104.0
uvicorn>=0.24.0
sqlalchemy>=2.0.0
psycopg2-binary>=2.9.0
pandas>=2.0.0
yfinance>=0.2.0

# Development dependencies
pytest>=7.0.0
pytest-asyncio>=0.21.0
```

## 🚀 **Development**

### **Running the Service**
```bash
# Start the service
cd services/data-service
python main.py

# Or with uvicorn
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

### **Testing**
```bash
# Run tests
cd services/data-service
pytest tests/

# Run with coverage
pytest --cov=src tests/
```

## 📊 **Performance**

### **Optimizations**
- **Connection Pooling** - Efficient database connections
- **Batch Processing** - Bulk data operations
- **Caching** - Redis for frequently accessed data
- **Async Operations** - Non-blocking I/O
- **Indexing** - Optimized database queries

### **Monitoring**
- **Health Checks** - Service status monitoring
- **Data Statistics** - Ingestion metrics
- **Performance Metrics** - Response times and throughput
- **Error Tracking** - Comprehensive error logging

## 🔗 **Integration**

### **Dependencies**
- **Database**: PostgreSQL + TimescaleDB
- **Cache**: Redis
- **External**: Yahoo Finance API

### **Used By**
- **Portfolio Service** - For real-time pricing
- **Strategy Service** - For historical data
- **Risk Service** - For market data
- **Analytics Service** - For data analysis
- **Web Portal** - For data display

## 🎯 **Future Enhancements**

### **Planned Features**
- **Real-time Streaming** - WebSocket data streaming
- **Multiple Data Sources** - Alpha Vantage, IEX Cloud
- **Data Quality Metrics** - Advanced data validation
- **Automated Scheduling** - Scheduled data updates
- **Data Compression** - Efficient storage optimization

### **Performance Improvements**
- **Parallel Processing** - Multi-threaded data ingestion
- **Smart Caching** - Intelligent cache management
- **Data Partitioning** - Optimized data storage
- **Query Optimization** - Enhanced database performance

---

**🎯 The Data Service provides the foundation for all market data operations in Bifrost Trader, ensuring reliable, fast, and comprehensive access to financial market data.**
