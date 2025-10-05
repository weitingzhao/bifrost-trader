# 📋 Reference

This section provides reference documentation for Bifrost Trader components and tools.

## 🎯 **Reference Documentation**

### **🤖 [AI Reference](ai-reference.md)**
Essential reference information for AI assistants working on the Bifrost Trader project:
- Architecture and implementation status
- Critical missing components
- AI assistant guidelines
- Project context and safety requirements

## 🔍 **Quick Reference**

### **Architecture Status**
- **Web Portal Service**: ✅ Complete (Port 8006)
- **API Gateway Service**: ✅ Complete (Port 8000)
- **Database Infrastructure**: ✅ Complete
- **Data Service**: 🔄 Partially implemented (Port 8001)
- **Portfolio Service**: 🔄 Partially implemented (Port 8002)
- **Strategy Service**: 🔄 Partially implemented (Port 8003)
- **Execution Service**: ❌ Not implemented (Port 8004)
- **Risk Service**: ❌ Not implemented (Port 8005)

### **Critical Missing Components**
- **Advanced Risk Management System**: VaR, drawdown monitoring, correlation analysis
- **Compliance & Regulatory Framework**: PDT rules, wash sales, audit trails
- **Advanced Analytics**: TCA, performance attribution
- **Comprehensive Testing Infrastructure**: Full test coverage and automation
- **Production Monitoring Stack**: Complete observability and alerting

### **AI Assistant Guidelines**
- **Before Implementation**: Check architecture, verify components, follow patterns
- **During Development**: Use type hints, async patterns, error handling, tests
- **After Implementation**: Update documentation, test integration, review quality

## 🎯 **Key Information**

### **Project Context**
- **Source Project**: Smart Trader (monolithic Django)
- **Target Project**: Bifrost Trader (microservices FastAPI)
- **Migration Status**: In progress
- **Current Focus**: Web portal and database integration

### **Technology Stack**
- **Backend**: Python with FastAPI
- **Database**: PostgreSQL with TimescaleDB
- **Caching**: Redis
- **Message Queue**: RabbitMQ
- **Monitoring**: Prometheus and Grafana
- **Containerization**: Docker and Kubernetes

### **Development Standards**
- **Type Hints**: Required for all functions
- **Pydantic Models**: Input validation and serialization
- **Async Operations**: Use async for I/O operations
- **Error Handling**: Comprehensive error handling required
- **Test Coverage**: >90% for all code

---

**🎯 This reference section provides essential information for AI assistants and developers working on the Bifrost Trader project. Always check the [AI Reference](ai-reference.md) before suggesting new features or answering questions about project structure.**
