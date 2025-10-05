# 🤖 AI Reference

This document provides essential reference information for AI assistants working on the Bifrost Trader project.

## 🏗️ **Architecture & Implementation Status**

**IMPORTANT:** Before suggesting any new features or answering questions about project structure, 
ALWAYS reference the [Architecture Overview](../architecture/overview.md) first.

This document contains:
- Current implementation status (what exists vs. what's missing)
- Target microservices architecture
- Migration plan and priorities
- Critical safety requirements
- Hardware allocation strategy

## ⚠️ **Critical Missing Components (DO NOT ASSUME THEY EXIST)**

- **Advanced Risk Management System**: VaR, drawdown monitoring, correlation analysis
- **Compliance & Regulatory Framework**: PDT rules, wash sales, audit trails
- **Advanced Analytics**: TCA, performance attribution
- **Comprehensive Testing Infrastructure**: Full test coverage and automation
- **Production Monitoring Stack**: Complete observability and alerting

**Always verify component existence before suggesting usage.**

## 🎯 **AI Assistant Guidelines**

### **Before Implementation**
1. **Check Architecture**: Review [Architecture Overview](../architecture/overview.md)
2. **Verify Components**: Ensure required components exist
3. **Follow Patterns**: Use established patterns from [Development Guide](../development/index.md)
4. **Reference Database**: Check [Database Design](../architecture/database.md) for data access

### **During Development**
1. **Use Type Hints**: All functions must have type hints
2. **Follow Async Patterns**: Use async for I/O operations
3. **Implement Error Handling**: Comprehensive error handling required
4. **Add Tests**: Include unit and integration tests
5. **Document Code**: Add docstrings and comments

### **After Implementation**
1. **Update Documentation**: Keep knowledge base current
2. **Test Integration**: Verify service integration
3. **Review Code Quality**: Ensure standards compliance
4. **Document Decisions**: Record architectural choices

## 🔍 **Project Context**

### **Current Implementation Status**
- **✅ Web Portal**: Complete with database integration
- **✅ API Gateway**: Complete with service routing
- **✅ Database Infrastructure**: Complete with TimescaleDB
- **🔄 Data Service**: In progress
- **🔄 Portfolio Service**: In progress
- **🔄 Strategy Service**: In progress
- **📋 Execution Service**: Planned
- **📋 Risk Service**: Planned

### **Technology Stack**
- **Backend**: Python with FastAPI
- **Database**: PostgreSQL with TimescaleDB
- **Caching**: Redis
- **Message Queue**: RabbitMQ
- **Monitoring**: Prometheus and Grafana
- **Containerization**: Docker and Kubernetes

### **Service Architecture**
- **API Gateway**: Port 8000 (Central routing)
- **Data Service**: Port 8001 (Market data)
- **Portfolio Service**: Port 8002 (Portfolio management)
- **Strategy Service**: Port 8003 (Backtesting and execution)
- **Execution Service**: Port 8004 (Order execution)
- **Risk Service**: Port 8005 (Risk management)
- **Web Portal**: Port 8006 (User interface)

## 🚨 **Critical Safety Requirements**

### **Trading Safety**
- **Position Limits**: Never exceed defined position limits
- **Risk Controls**: Implement proper risk management
- **Order Validation**: Validate all orders before execution
- **Audit Trails**: Maintain complete audit trails

### **Data Safety**
- **Backup Strategy**: Regular database backups
- **Data Validation**: Validate all incoming data
- **Error Handling**: Graceful error handling
- **Monitoring**: Continuous system monitoring

### **Security Requirements**
- **Authentication**: Proper user authentication
- **Authorization**: Role-based access control
- **Data Encryption**: Encrypt sensitive data
- **Network Security**: Secure network communications

## 📊 **Hardware Allocation Strategy**

### **Development Environment**
- **CPU**: 4+ cores recommended
- **Memory**: 8GB minimum, 16GB recommended
- **Storage**: 50GB free space minimum
- **Network**: Stable internet connection

### **Production Environment**
- **CPU**: 8+ cores per service
- **Memory**: 16GB+ per service
- **Storage**: SSD with 100GB+ per service
- **Network**: High-speed, low-latency connection

## 🎯 **AI Collaboration Best Practices**

### **Context-Aware Prompts**
Always include project context in prompts:
```
"Based on the Architecture Overview, create a Portfolio Service API endpoint 
that follows the microservices patterns defined in the Development Guide. 
Use the database models from Database Design and ensure compatibility 
with the existing web-portal service."
```

### **Knowledge References**
- **Architecture**: [Architecture Overview](../architecture/overview.md)
- **Database**: [Database Design](../architecture/database.md)
- **Development**: [Development Guide](../development/index.md)
- **Migration**: [Migration Guide](../development/migration-guide.md)
- **AI Collaboration**: [AI Collaboration Guide](../guides/ai-collaboration.md)

### **Quality Standards**
- **Code Quality**: Follow established patterns
- **Test Coverage**: >90% for all code
- **Documentation**: Comprehensive docstrings
- **Error Handling**: Graceful error handling
- **Type Safety**: Use type hints throughout

---

**🎯 This reference provides essential context for AI assistants working on Bifrost Trader. Always verify component existence and follow established patterns when making suggestions or implementing features.**
