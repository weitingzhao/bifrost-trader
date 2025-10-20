# 🎛️ Service Control Center - Individual Service Endpoints

**Control Center URL**: http://localhost:8007

## 📋 **Available Service Endpoints**

Each Bifrost Trader service now has its own dedicated endpoint under the Control Center:

### 🏗️ **Core Services**
- **API Gateway**: http://localhost:8007/api-gateway
- **Data Service**: http://localhost:8007/data  
- **Portfolio Service**: http://localhost:8007/portfolio
- **Strategy Service**: http://localhost:8007/strategy

### 📈 **Trading Services**
- **Execution Service**: http://localhost:8007/execution
- **Risk Service**: http://localhost:8007/risk

### 🖥️ **User Interface**
- **Web Portal**: http://localhost:8007/web-portal
- **Control Center**: http://localhost:8007/ (main dashboard)

### 🧠 **Analytics Services**
- **ML Service**: http://localhost:8007/ml
- **Analytics Service**: http://localhost:8007/analytics

### 🔧 **Supporting Services**
- **Compliance Service**: http://localhost:8007/compliance
- **News Service**: http://localhost:8007/news
- **Microstructure Service**: http://localhost:8007/microstructure

### 📋 **Service Management**
- **All Services List**: http://localhost:8007/services
- **Service Details**: http://localhost:8007/service/{service-name}

## 🎯 **Service Page Features**

Each service endpoint provides:

### 📊 **Service Information**
- Service name, port, and description
- Category and management type
- URL and documentation links
- Health endpoint access

### ⚡ **Quick Actions**
- **Open Service**: Direct link to service URL
- **View API Docs**: Access to service documentation
- **Check Health**: Health status endpoint
- **Manage Service**: Full service management interface

### 🔧 **Service Management**
- Start/Stop/Restart service
- View service logs
- Monitor service metrics
- Health status monitoring

### 📈 **Real-time Status**
- Health status indicators
- Response time monitoring
- Memory and CPU usage
- Service uptime tracking

## 🌐 **Access Methods**

### 1. **Direct Service URLs**
```
http://localhost:8007/data          # Data Service
http://localhost:8007/portfolio    # Portfolio Service
http://localhost:8007/strategy     # Strategy Service
http://localhost:8007/web-portal   # Web Portal
```

### 2. **Service Management**
```
http://localhost:8007/service/data-service     # Full management
http://localhost:8007/service/portfolio-service # Full management
http://localhost:8007/service/strategy-service  # Full management
```

### 3. **API Access**
```
GET /api/services/                    # List all services
GET /api/services/{name}              # Service details
POST /api/services/{name}/start       # Start service
POST /api/services/{name}/stop        # Stop service
POST /api/services/{name}/restart     # Restart service
```

### 4. **Health Monitoring**
```
GET /api/health/                      # System health
GET /api/health/services/{name}       # Service health
GET /api/proxy/{name}/health          # Proxy health check
```

## 🎨 **User Interface**

### **Service Page Layout**
- **Header**: Service name, port, and quick actions
- **Information**: Detailed service information
- **Quick Actions**: Direct access buttons
- **Features**: Service capabilities list
- **API Endpoints**: Available API documentation
- **Status**: Real-time health and metrics

### **Navigation**
- **Back to Control Center**: Return to main dashboard
- **Open Service**: Direct access to service
- **API Docs**: Service documentation
- **Health Check**: Service health status
- **Manage Service**: Full management interface

## 🔗 **Integration Points**

### **Service Discovery**
- Automatic service detection
- Category-based organization
- Status monitoring
- Health checking

### **API Proxy**
- Unified access to all services
- Request routing and forwarding
- Health check aggregation
- Service documentation access

### **Management Interface**
- Service lifecycle control
- Log viewing and monitoring
- Metrics collection
- Health status tracking

## 📱 **Responsive Design**

- **Desktop**: Full-featured interface
- **Tablet**: Optimized layout
- **Mobile**: Touch-friendly design
- **Cross-browser**: Modern browser support

## 🚀 **Usage Examples**

### **Access Data Service**
```bash
# Open in browser
open http://localhost:8007/data

# Or via curl
curl http://localhost:8007/data
```

### **Manage Portfolio Service**
```bash
# Full management interface
open http://localhost:8007/service/portfolio-service

# Start service via API
curl -X POST http://localhost:8007/api/services/portfolio-service/start
```

### **Check Service Health**
```bash
# Health status
curl http://localhost:8007/api/health/services/data-service

# Proxy health check
curl http://localhost:8007/api/proxy/data-service/health
```

## 🎯 **Benefits**

### **Centralized Access**
- Single point of access for all services
- Consistent interface across services
- Unified management capabilities

### **Service Discovery**
- Easy service identification
- Category-based organization
- Status at a glance

### **Management Efficiency**
- Quick service actions
- Real-time monitoring
- Health status tracking

### **Developer Experience**
- Direct API access
- Service documentation
- Health monitoring
- Development tools

---

**Last Updated**: October 20, 2025  
**Control Center**: http://localhost:8007  
**Status**: ✅ **OPERATIONAL**
