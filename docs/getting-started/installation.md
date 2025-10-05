# 🚀 Installation Guide

This guide will help you install and configure Bifrost Trader for different environments.

## 📋 Prerequisites

### **System Requirements**
- **Python**: 3.9 or higher
- **Memory**: 8GB RAM minimum, 16GB recommended
- **Storage**: 50GB free space minimum
- **Network**: Internet connection for data feeds

### **Software Dependencies**
- **Docker**: For containerized deployment
- **PostgreSQL**: Database server
- **Redis**: Caching and message broker
- **Git**: Version control

## 🐳 Docker Installation (Recommended)

### **Quick Start**
```bash
# Clone the repository
git clone https://github.com/weitingzhao/bifrost-trader.git
cd bifrost-trader

# Start the database services
docker-compose -f docker-compose-db.yml up -d

# Start the application services
docker-compose up -d
```

### **Configuration**
1. Copy `env.example` to `.env`
2. Update database credentials
3. Configure API keys
4. Set environment variables

## 💻 Local Development Installation

### **Python Environment**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### **Database Setup**
```bash
# Start PostgreSQL and Redis
docker-compose -f docker-compose-db.yml up -d

# Run database migrations
python scripts/setup-database.py
```

### **Service Configuration**
```bash
# Start individual services
python services/api-gateway/main.py
python services/web-portal/main.py
python services/data-service/main.py
```

## 🔧 Configuration

### **Environment Variables**
- `DB_HOST`: Database host
- `DB_PORT`: Database port
- `DB_NAME`: Database name
- `DB_USERNAME`: Database username
- `DB_PASSWORD`: Database password
- `REDIS_URL`: Redis connection URL

### **API Keys**
- **Market Data**: Configure data provider API keys
- **Broker APIs**: Set up broker connection credentials
- **Monitoring**: Configure monitoring service keys

## ✅ Verification

### **Health Checks**
```bash
# Check API Gateway
curl http://localhost:8000/health

# Check Web Portal
curl http://localhost:8006/health

# Check Database
psql -h localhost -U postgres -d bifrost_trader -c "SELECT 1"
```

### **Service Status**
- **API Gateway**: http://localhost:8000
- **Web Portal**: http://localhost:8006
- **Data Service**: http://localhost:8001
- **Portfolio Service**: http://localhost:8002
- **Strategy Service**: http://localhost:8003

## 🆘 Troubleshooting

### **Common Issues**
- **Port Conflicts**: Check if ports are already in use
- **Database Connection**: Verify PostgreSQL is running
- **Permission Issues**: Check file permissions
- **Dependency Issues**: Ensure all dependencies are installed

### **Getting Help**
- Check the [Troubleshooting Guide](../guides/troubleshooting.md)
- Create a [GitHub Issue](https://github.com/weitingzhao/bifrost-trader/issues)
- Review the [Configuration Reference](../reference/configuration.md)

---

**🎯 Once installation is complete, proceed to the [Quick Start Tutorial](quick-start.md) to run your first backtest!**
