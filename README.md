# Bifrost Trader

A comprehensive microservices-based trading platform refactored from Smart Trader. Bifrost Trader represents the next generation of trading infrastructure, designed for scalability, maintainability, and high performance with advanced backtesting capabilities.

## 🎯 Project Overview

Bifrost Trader is a sophisticated microservices architecture that transforms the monolithic Smart Trader application into a distributed system optimized for modern trading operations. The platform combines real-time market data, technical analysis, portfolio management, automated trading capabilities, and advanced backtesting through independent, scalable services.

## ✨ Key Features

### 📊 Market Data & Analysis
- **Real-time Stock Data**: Integration with Yahoo Finance API for live market data
- **Historical Data Management**: TimescaleDB-powered time-series storage for OHLCV data
- **Technical Indicators**: Comprehensive technical analysis tools including:
  - Bollinger Bands with custom smoothing
  - MACD (Moving Average Convergence Divergence)
  - RSI (Relative Strength Index)
  - ADX (Average Directional Index)
  - Custom Nadaraya-Watson smoothing indicators
- **Fundamental Analysis**: Company financials, earnings data, and valuation metrics

### 🔍 Stock Screening & Research
- **Advanced Screeners**: Multi-criteria stock filtering based on technical and fundamental metrics
- **Snapshot System**: Time-series snapshots of market data for historical analysis
- **Research Tools**: Comprehensive research capabilities with customizable indicators
- **Market Comparison**: Side-by-side analysis of multiple securities

### 💼 Portfolio Management
- **Multi-Portfolio Support**: Manage multiple portfolios with different strategies
- **Position Tracking**: Real-time position monitoring and P&L tracking
- **Order Management**: Comprehensive order system with various order types (Market, Limit, Stop, Stop-Limit)
- **Transaction History**: Complete audit trail of all trading activities
- **Cash Flow Management**: Track deposits, withdrawals, and cash balances

### 🤖 Advanced Backtesting & Strategy Engine
- **Professional Backtesting**: Complete Backtrader framework integration for strategy development
- **Multi-timeframe Analysis**: Support for multiple timeframes (daily, hourly, minute-level)
- **Strategy Optimization**: Ray-powered distributed optimization for parameter tuning
- **Live Trading**: Real-time strategy execution with Interactive Brokers integration
- **Custom Indicators**: Support for custom technical indicators and overlays
- **Performance Analytics**: Detailed performance metrics and trade analysis

### 📈 Visualization & Reporting
- **Interactive Charts**: Bokeh-powered interactive charts and dashboards
- **Real-time Dashboards**: Live market data visualization
- **Performance Reports**: Comprehensive performance analytics and reporting
- **Strategy Visualization**: Advanced plotting and analysis tools

### 🛡️ Risk Management
- **Built-in Risk Controls**: Position sizing and risk management
- **Compliance Monitoring**: Regulatory compliance and reporting
- **Alert Systems**: Real-time risk alerts and notifications

## 🏗️ Technical Architecture

### **Backend Technologies**
- **FastAPI**: Modern async web framework with automatic API documentation
- **PostgreSQL + TimescaleDB**: Primary database with time-series optimization
- **Redis**: Caching and message broker for real-time features
- **Celery**: Asynchronous task processing for data fetching and analysis

### **Trading & Analysis**
- **Backtrader**: Professional backtesting and live trading framework
- **Interactive Brokers API**: Live trading integration
- **yfinance**: Market data provider
- **TA-Lib**: Technical analysis library
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing

### **Frontend & Visualization**
- **Bootstrap 5**: Responsive UI framework
- **Bokeh**: Interactive data visualization
- **Panel**: Dashboard and app framework
- **WebSockets**: Real-time data streaming

### **Data Processing & Optimization**
- **Ray**: Distributed computing for strategy optimization
- **Scikit-learn**: Machine learning capabilities
- **Matplotlib/Plotly**: Additional visualization options
- **TimescaleDB**: High-performance time-series database

## 🏗️ Architecture Overview

### **Service Distribution**
```
bifrost-trader/
├── services/
│   ├── data-service/           # Market data ingestion (10.0.0.75)
│   ├── portfolio-service/       # Portfolio management (10.0.0.80)
│   ├── strategy-service/        # Strategy development (10.0.0.60)
│   ├── execution-service/       # Order execution (10.0.0.80)
│   ├── risk-service/           # Risk management (10.0.0.80)
│   ├── ml-service/             # AI/ML trading (10.0.0.60)
│   ├── analytics-service/       # Advanced analytics (10.0.0.60)
│   ├── compliance-service/      # Regulatory compliance (10.0.0.80)
│   ├── news-service/           # News & sentiment (10.0.0.75)
│   ├── microstructure-service/ # Market microstructure (10.0.0.60)
│   ├── web-portal/             # User interface (10.0.0.75)
│   └── api-gateway/            # API gateway (10.0.0.75)
├── shared/
│   ├── models/                 # Shared data models
│   ├── utils/                 # Common utilities
│   ├── configs/               # Configuration files
│   └── schemas/               # API schemas
├── infrastructure/
│   ├── docker/                # Docker configurations
│   ├── kubernetes/            # K8s configurations
│   └── monitoring/            # Monitoring setup
└── docs/                      # Documentation
```

## 🔄 Migration from Smart Trader

This project is a refactored version of the Smart Trader application, located at:
- **Source**: `/Users/vision-mac-trader/Desktop/workspace/projects/smart-trader`
- **Target**: `/Users/vision-mac-trader/Desktop/workspace/projects/bifrost-trader`

### **Key Changes**
- **Monolithic → Microservices**: Breaking down Django monolith into independent services
- **Django → FastAPI**: Modern async API framework for better performance
- **Single Database → Service Databases**: Each service manages its own data
- **Synchronous → Asynchronous**: Event-driven architecture with message queues

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Docker & Docker Compose
- PostgreSQL with TimescaleDB
- Redis
- Node.js (for frontend services)

### Development Setup

1. **Clone and Setup**
   ```bash
   cd /Users/vision-mac-trader/Desktop/workspace/projects/bifrost-trader
   ```

2. **Environment Configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start Services**
   ```bash
   docker-compose up -d
   ```

4. **Access Services**
   - API Gateway: http://localhost:8000
   - Data Service: http://localhost:8001
   - Portfolio Service: http://localhost:8002
   - Strategy Service: http://localhost:8003

## 📋 Service Details

### **Data Service** (Port 8001)
- Market data ingestion and storage
- Real-time data streaming
- Historical data management
- Data validation and cleaning

### **Portfolio Service** (Port 8002)
- Portfolio management
- Position tracking
- Transaction history
- Performance analytics

### **Strategy Service** (Port 8003)
- Strategy development
- Backtesting engine
- Live strategy execution
- Performance optimization

### **Risk Service** (Port 8004)
- Risk calculations
- Position sizing
- Compliance monitoring
- Alert systems

### **ML Service** (Port 8005)
- Machine learning models
- Pattern recognition
- Sentiment analysis
- Predictive analytics

### **Web Portal** (Port 8006)
- User interface
- Dashboard
- Real-time charts
- Notifications

### **API Gateway** (Port 8000)
- Service routing
- Authentication
- Rate limiting
- Load balancing

## 🔧 Development

### **Service Development**
Each service follows a standard structure:
```
service-name/
├── src/
│   ├── models/         # Data models
│   ├── services/       # Business logic
│   ├── api/           # API endpoints
│   └── utils/         # Utilities
├── tests/             # Unit tests
├── requirements.txt   # Dependencies
├── Dockerfile        # Container config
└── main.py           # Service entry point
```

### **Adding New Services**
1. Create service directory in `services/`
2. Follow standard structure
3. Add to API gateway routing
4. Update docker-compose.yml
5. Add service documentation

## 📊 Monitoring & Observability

- **Health Checks**: Each service provides `/health` and `/ready` endpoints
- **Metrics**: Prometheus-compatible metrics
- **Logging**: Structured logging with correlation IDs
- **Tracing**: Distributed tracing for request flow

## 🤝 Contributing

1. Follow the microservices architecture patterns
2. Maintain service independence
3. Use shared models and utilities
4. Write comprehensive tests
5. Update documentation

## 📄 License

This project is licensed under the same terms as Smart Trader.

## 🆘 Support

For questions and support:
- Check service-specific documentation
- Review the migration guide
- Consult the API documentation
- Create issues for bugs or feature requests

---

**Note**: This platform is designed for educational and research purposes. Always ensure compliance with local financial regulations when using automated trading features.
