# 🎛️ Service Control Center

**Service**: Control Center  
**Port**: 8007  
**URL**: http://localhost:8007  
**Status**: ✅ **OPERATIONAL**

## Overview

The Service Control Center is a centralized management interface for all Bifrost Trader microservices. It provides comprehensive service management, health monitoring, and unified API access through a modern web interface.

## Features

### 🎯 **Service Management**
- **Start/Stop/Restart Services**: Control service lifecycle with one click
- **Service Status Monitoring**: Real-time status updates for all services
- **Service Logs**: View and monitor service logs in real-time
- **Service Metrics**: CPU, memory, and performance metrics
- **Bulk Operations**: Manage multiple services simultaneously

### 📊 **Health Monitoring**
- **Real-time Health Checks**: Continuous monitoring of all services
- **WebSocket Updates**: Live status updates without page refresh
- **Health History**: Track service health over time
- **Alert System**: Automatic alerts for service failures
- **Performance Metrics**: Response time and availability tracking

### 🔗 **Unified API Access**
- **API Proxy**: Access any service through the control center
- **Service Discovery**: Automatic discovery of all services
- **API Documentation**: Direct links to service documentation
- **Health Endpoints**: Centralized health check access

### 🎨 **Modern UI Dashboard**
- **Service Grid**: Visual overview of all services by category
- **Real-time Updates**: Live status updates via WebSocket
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Dark/Light Theme**: User preference support
- **Interactive Charts**: Visual representation of metrics

## Service Categories

### 🏗️ **Core Services**
- **API Gateway** (Port 8000): Central API routing
- **Data Service** (Port 8001): Market data management
- **Portfolio Service** (Port 8002): Portfolio management
- **Strategy Service** (Port 8003): Trading strategies and backtesting

### 📈 **Trading Services**
- **Execution Service** (Port 8004): Trade execution
- **Risk Service** (Port 8005): Risk management and VaR

### 🖥️ **User Interface**
- **Web Portal** (Port 8006): Main trading dashboard
- **Control Center** (Port 8007): This service

### 🧠 **Analytics Services**
- **ML Service** (Port 8008): Machine learning models
- **Analytics Service** (Port 8009): Data analysis and reporting

### 🔧 **Supporting Services**
- **Compliance Service** (Port 8010): Regulatory compliance
- **News Service** (Port 8011): Market news and information
- **Microstructure Service** (Port 8012): Market microstructure analysis

## API Endpoints

### Service Management
```
GET    /api/services/                    # List all services
GET    /api/services/{name}              # Get service details
POST   /api/services/{name}/start        # Start service
POST   /api/services/{name}/stop         # Stop service
POST   /api/services/{name}/restart      # Restart service
GET    /api/services/{name}/logs         # Get service logs
GET    /api/services/{name}/metrics      # Get service metrics
```

### Health Monitoring
```
GET    /api/health/                      # System health overview
GET    /api/health/services              # All services health
GET    /api/health/services/{name}       # Service health
GET    /api/health/history               # Health history
GET    /api/health/alerts                # Health alerts
```

### API Proxy
```
ALL    /api/proxy/{service}/{path}       # Proxy to any service
GET    /api/proxy/{service}/health       # Service health check
GET    /api/proxy/{service}/docs         # Service documentation
GET    /api/proxy/services/list          # Available services
```

### WebSocket
```
WS     /ws                              # Real-time updates
```

## Usage

### Web Interface
1. **Access Dashboard**: Navigate to http://localhost:8007
2. **View Services**: Browse services by category
3. **Manage Services**: Use start/stop/restart buttons
4. **Monitor Health**: View real-time status updates
5. **Access Services**: Click to open services in new tabs

### API Access
```bash
# List all services
curl http://localhost:8007/api/services/

# Start a service
curl -X POST http://localhost:8007/api/services/web-portal/start

# Check service health
curl http://localhost:8007/api/health/services/web-portal

# Proxy to a service
curl http://localhost:8007/api/proxy/web-portal/health
```

### Service Management
```bash
# Start Control Center
cd services/control-center
python -m uvicorn main:app --host 0.0.0.0 --port 8007 --reload

# Access via browser
open http://localhost:8007
```

## Configuration

### Service Registry
Services are configured in `config/services.yaml`:
```yaml
services:
  - name: web-portal
    port: 8006
    category: ui
    description: Web Portal Dashboard
    has_ui: true
    management: uvicorn
    health_endpoint: /health
    docs_endpoint: /docs
    url: http://localhost:8006
```

### Environment Variables
```bash
PORT=8007                    # Control Center port
HOST=0.0.0.0               # Bind address
LOG_LEVEL=info              # Logging level
```

## Architecture

### Components
- **Service Registry**: Manages service configurations
- **Health Monitor**: Tracks service health and metrics
- **Service Manager**: Controls service lifecycle
- **API Proxy**: Routes requests to services
- **WebSocket Service**: Real-time updates

### Data Flow
1. **Service Discovery**: Registry loads service configurations
2. **Health Monitoring**: Continuous polling of service health
3. **WebSocket Updates**: Real-time status broadcast
4. **API Proxy**: Request routing to target services
5. **Service Management**: Process control and lifecycle management

## Security

### Authentication
- API key validation for management actions
- Rate limiting on management endpoints
- Audit logging for all management actions

### Access Control
- Read-only mode for monitoring
- Role-based access control (planned)
- Service isolation and sandboxing

## Monitoring

### Metrics
- Service uptime and availability
- Response time tracking
- Resource usage (CPU, memory)
- Error rates and failure tracking

### Alerts
- Service failure notifications
- Performance degradation alerts
- Resource usage warnings
- Health check failures

## Troubleshooting

### Common Issues
1. **Service Won't Start**: Check port availability and dependencies
2. **Health Check Fails**: Verify service endpoints and configuration
3. **WebSocket Disconnected**: Check network connectivity
4. **API Proxy Errors**: Verify target service availability

### Debug Mode
```bash
# Enable debug logging
LOG_LEVEL=debug python -m uvicorn main:app --reload
```

## Integration

### With Other Services
- **API Gateway**: Central routing through control center
- **Web Portal**: Direct access to trading interface
- **Data Service**: Market data health monitoring
- **All Services**: Unified management and monitoring

### External Tools
- **Prometheus**: Metrics collection (planned)
- **Grafana**: Dashboard visualization (planned)
- **Docker**: Container management (planned)
- **Kubernetes**: Orchestration (planned)

## Future Enhancements

### Planned Features
- **Service Templates**: Predefined service configurations
- **Auto-scaling**: Automatic service scaling based on load
- **Service Dependencies**: Dependency management and ordering
- **Backup/Restore**: Service state backup and recovery
- **Multi-environment**: Support for dev/staging/production

### Advanced Monitoring
- **Distributed Tracing**: Request tracing across services
- **Performance Profiling**: Detailed performance analysis
- **Capacity Planning**: Resource usage forecasting
- **Anomaly Detection**: Automatic issue detection

---

**Last Updated**: October 20, 2025  
**Version**: 1.0.0  
**Status**: Production Ready
