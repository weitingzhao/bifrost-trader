# Bifrost Trader

A microservices-based trading platform refactored from Smart Trader. Bifrost Trader represents the next generation of trading infrastructure, designed for scalability, maintainability, and high performance.

## 🎯 Project Overview

Bifrost Trader is a comprehensive microservices architecture that transforms the monolithic Smart Trader application into a distributed system optimized for modern trading operations. The platform provides real-time market data, portfolio management, strategy development, risk management, and execution capabilities through independent, scalable services.

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
