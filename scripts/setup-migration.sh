#!/bin/bash

# Bifrost Trader Migration Script
# This script helps migrate components from smart-trader to bifrost-trader

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Project paths
SMART_TRADER_PATH="/Users/vision-mac-trader/Desktop/workspace/projects/smart-trader"
BIFROST_TRADER_PATH="/Users/vision-mac-trader/Desktop/workspace/projects/bifrost-trader"

echo -e "${BLUE}🚀 Bifrost Trader Migration Script${NC}"
echo "=================================="

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if paths exist
check_paths() {
    print_info "Checking project paths..."
    
    if [ ! -d "$SMART_TRADER_PATH" ]; then
        print_error "Smart Trader path not found: $SMART_TRADER_PATH"
        exit 1
    fi
    
    if [ ! -d "$BIFROST_TRADER_PATH" ]; then
        print_error "Bifrost Trader path not found: $BIFROST_TRADER_PATH"
        exit 1
    fi
    
    print_status "Project paths verified"
}

# Create service structure
create_service_structure() {
    print_info "Creating service structure..."
    
    cd "$BIFROST_TRADER_PATH"
    
    # Create service directories
    services=("data-service" "portfolio-service" "strategy-service" "execution-service" "risk-service" "ml-service" "analytics-service" "compliance-service" "news-service" "microstructure-service" "web-portal")
    
    for service in "${services[@]}"; do
        if [ ! -d "services/$service" ]; then
            mkdir -p "services/$service/src/{models,services,api,tasks}"
            mkdir -p "services/$service/tests"
            mkdir -p "services/$service/docs"
            print_status "Created structure for $service"
        else
            print_warning "$service structure already exists"
        fi
    done
}

# Copy essential files
copy_essential_files() {
    print_info "Copying essential files..."
    
    # Copy requirements.txt as reference
    if [ -f "$SMART_TRADER_PATH/requirements.txt" ]; then
        cp "$SMART_TRADER_PATH/requirements.txt" "$BIFROST_TRADER_PATH/requirements-smart-trader.txt"
        print_status "Copied requirements.txt as reference"
    fi
    
    # Copy environment example
    if [ -f "$SMART_TRADER_PATH/.env.example" ]; then
        cp "$SMART_TRADER_PATH/.env.example" "$BIFROST_TRADER_PATH/.env-smart-trader.example"
        print_status "Copied .env.example as reference"
    fi
    
    # Copy documentation
    if [ -d "$SMART_TRADER_PATH/docs" ]; then
        cp -r "$SMART_TRADER_PATH/docs" "$BIFROST_TRADER_PATH/docs-smart-trader"
        print_status "Copied documentation as reference"
    fi
}

# Create migration reference
create_migration_reference() {
    print_info "Creating migration reference..."
    
    cd "$BIFROST_TRADER_PATH"
    
    # Create reference file
    cat > "MIGRATION_REFERENCE.md" << EOF
# Migration Reference - Smart Trader to Bifrost Trader

## Source Project
- **Path**: $SMART_TRADER_PATH
- **Type**: Django Monolithic Application
- **Database**: PostgreSQL with TimescaleDB
- **Framework**: Django 5.1.6

## Target Project
- **Path**: $BIFROST_TRADER_PATH
- **Type**: Microservices Architecture
- **Database**: Service-specific PostgreSQL
- **Framework**: FastAPI

## Migration Mapping

### Models Migration
| Smart Trader | Bifrost Trader | Status |
|--------------|----------------|--------|
| apps/common/models/market.py | services/data-service/src/models/ | 🚧 In Progress |
| apps/common/models/portfolio.py | services/portfolio-service/src/models/ | 📋 Planned |
| apps/common/models/strategy.py | services/strategy-service/src/models/ | 📋 Planned |
| apps/common/models/main.py | services/risk-service/src/models/ | 📋 Planned |

### Services Migration
| Smart Trader | Bifrost Trader | Status |
|--------------|----------------|--------|
| business/services/fetching/ | services/data-service/src/services/ | 🚧 In Progress |
| business/researchs/position/ | services/portfolio-service/src/services/ | 📋 Planned |
| cerebro/ | services/strategy-service/src/strategies/ | 📋 Planned |
| business/researchs/ | services/strategy-service/src/services/ | 📋 Planned |

### API Migration
| Smart Trader | Bifrost Trader | Status |
|--------------|----------------|--------|
| apps/api/ | services/*/src/api/ | 🚧 In Progress |
| home/views/ | services/*/src/api/ | 📋 Planned |

### Tasks Migration
| Smart Trader | Bifrost Trader | Status |
|--------------|----------------|--------|
| apps/tasks/controller/ | services/*/src/tasks/ | 🚧 In Progress |

## Migration Commands

### Data Service
\`\`\`bash
# Copy market models
cp $SMART_TRADER_PATH/apps/common/models/market.py $BIFROST_TRADER_PATH/services/data-service/src/models/market_reference.py

# Copy data services
cp -r $SMART_TRADER_PATH/business/services/fetching/ $BIFROST_TRADER_PATH/services/data-service/src/services/fetching_reference/

# Copy data tasks
cp -r $SMART_TRADER_PATH/apps/tasks/controller/ $BIFROST_TRADER_PATH/services/data-service/src/tasks/tasks_reference/
\`\`\`

### Portfolio Service
\`\`\`bash
# Copy portfolio models
cp $SMART_TRADER_PATH/apps/common/models/portfolio.py $BIFROST_TRADER_PATH/services/portfolio-service/src/models/portfolio_reference.py

# Copy portfolio views
cp -r $SMART_TRADER_PATH/home/views/position/ $BIFROST_TRADER_PATH/services/portfolio-service/src/api/position_reference/
cp -r $SMART_TRADER_PATH/home/views/cash_flow/ $BIFROST_TRADER_PATH/services/portfolio-service/src/api/cash_flow_reference/
\`\`\`

### Strategy Service
\`\`\`bash
# Copy strategy models
cp $SMART_TRADER_PATH/apps/common/models/strategy.py $BIFROST_TRADER_PATH/services/strategy-service/src/models/strategy_reference.py

# Copy cerebro directory
cp -r $SMART_TRADER_PATH/cerebro/ $BIFROST_TRADER_PATH/services/strategy-service/src/cerebro_reference/

# Copy backtrader directory
cp -r $SMART_TRADER_PATH/backtrader/ $BIFROST_TRADER_PATH/services/strategy-service/src/backtrader_reference/
\`\`\`

## Next Steps
1. Complete data service migration
2. Start portfolio service migration
3. Migrate strategy service
4. Set up service communication
5. Implement monitoring and logging

EOF

    print_status "Created migration reference file"
}

# Create Docker Compose file
create_docker_compose() {
    print_info "Creating Docker Compose configuration..."
    
    cd "$BIFROST_TRADER_PATH"
    
    cat > "docker-compose.yml" << EOF
version: '3.8'

services:
  # Database
  postgres:
    image: timescale/timescaledb:latest-pg15
    environment:
      POSTGRES_DB: bifrost_trader
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # API Gateway
  api-gateway:
    build:
      context: ./services/api-gateway
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATA_SERVICE_URL=http://data-service:8001
      - PORTFOLIO_SERVICE_URL=http://portfolio-service:8002
      - STRATEGY_SERVICE_URL=http://strategy-service:8003
      - RISK_SERVICE_URL=http://risk-service:8004
      - ML_SERVICE_URL=http://ml-service:8005
    depends_on:
      - postgres
      - redis
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Data Service
  data-service:
    build:
      context: ./services/data-service
      dockerfile: Dockerfile
    ports:
      - "8001:8001"
    environment:
      - DATABASE_URL=postgresql://postgres:password@postgres:5432/bifrost_trader
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8001/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Portfolio Service
  portfolio-service:
    build:
      context: ./services/portfolio-service
      dockerfile: Dockerfile
    ports:
      - "8002:8002"
    environment:
      - DATABASE_URL=postgresql://postgres:password@postgres:5432/bifrost_trader
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8002/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Strategy Service
  strategy-service:
    build:
      context: ./services/strategy-service
      dockerfile: Dockerfile
    ports:
      - "8003:8003"
    environment:
      - DATABASE_URL=postgresql://postgres:password@postgres:5432/bifrost_trader
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8003/health"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  postgres_data:
  redis_data:

networks:
  default:
    name: bifrost-trader-network
EOF

    print_status "Created Docker Compose configuration"
}

# Create service requirements
create_service_requirements() {
    print_info "Creating service requirements..."
    
    cd "$BIFROST_TRADER_PATH"
    
    # Data Service requirements
    cat > "services/data-service/requirements.txt" << EOF
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
redis==5.0.1
pandas==2.1.4
numpy==1.24.3
yfinance==0.2.54
python-dotenv==1.0.0
celery==5.3.4
httpx==0.25.2
python-dateutil==2.8.2
pytz==2023.3
EOF

    # Portfolio Service requirements
    cat > "services/portfolio-service/requirements.txt" << EOF
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
redis==5.0.1
pandas==2.1.4
numpy==1.24.3
python-dotenv==1.0.0
celery==5.3.4
httpx==0.25.2
python-dateutil==2.8.2
pytz==2023.3
EOF

    # Strategy Service requirements
    cat > "services/strategy-service/requirements.txt" << EOF
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
redis==5.0.1
pandas==2.1.4
numpy==1.24.3
python-dotenv==1.0.0
celery==5.3.4
httpx==0.25.2
python-dateutil==2.8.2
pytz==2023.3
backtrader==1.9.78.123
matplotlib==3.7.2
plotly==5.17.0
scikit-learn==1.3.2
ray==2.8.0
EOF

    print_status "Created service requirements files"
}

# Main execution
main() {
    echo "Starting migration setup..."
    
    check_paths
    create_service_structure
    copy_essential_files
    create_migration_reference
    create_docker_compose
    create_service_requirements
    
    print_status "Migration setup completed!"
    print_info "Next steps:"
    echo "1. Review the MIGRATION_REFERENCE.md file"
    echo "2. Start migrating data service components"
    echo "3. Use 'docker-compose up -d' to start services"
    echo "4. Test individual services and API Gateway"
}

# Run main function
main "$@"
