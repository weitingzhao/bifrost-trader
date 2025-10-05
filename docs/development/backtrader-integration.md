# Standalone Backtrader Service Migration Plan

## 🎯 **Objective**

Create a standalone, production-ready backtesting service that can operate independently from the main Bifrost Trader platform. This service will provide comprehensive stock backtesting capabilities using the complete Backtrader framework migrated from Smart Trader.

## 📊 **Current State Analysis**

### **Smart Trader Backtrader Components**
```
smart-trader/
├── backtrader/                    # Complete Backtrader framework
│   ├── __init__.py              # Main framework imports
│   ├── cerebro.py               # Core cerebro engine
│   ├── strategy.py              # Strategy base classes
│   ├── broker.py                # Broker implementations
│   ├── feeds/                   # Data feed implementations
│   ├── indicators/              # Technical indicators
│   ├── analyzers/               # Performance analyzers
│   ├── observers/               # Market observers
│   ├── sizers/                  # Position sizing
│   └── utils/                   # Utility functions
├── cerebro/                      # Custom cerebro implementation
│   ├── cerebro_base.py          # Base cerebro class
│   ├── ray_strategy.py          # Ray optimization
│   ├── ray_optimize.py          # Distributed optimization
│   ├── strategy/                # Custom strategies
│   │   ├── three_step_strategy.py
│   │   ├── live_strategy.py
│   │   └── indicator/           # Custom indicators
│   └── datafeed_tradingview/    # TradingView integration
└── backtrader_plotting/         # Visualization components
    ├── bokeh/                   # Bokeh plotting
    └── schemes/                 # Plot schemes
```

### **Bifrost Trader Current State**
```
bifrost-trader/services/strategy-service/
├── src/
│   ├── backtrader/              # ✅ Complete framework migrated
│   ├── cerebro/                 # ✅ Custom implementation migrated
│   ├── models/                  # ✅ Strategy models copied
│   └── api/                     # ❌ FastAPI implementation needed
```

## 🚀 **Migration Strategy**

### **Phase 1: Standalone Service Creation** (Priority: HIGH)
**Timeline: 1-2 weeks**

#### **1.1 Create Standalone Backtrader Service**
```bash
# Create new standalone service
mkdir -p services/backtrader-service
cd services/backtrader-service
```

#### **1.2 Service Structure**
```
backtrader-service/
├── src/
│   ├── __init__.py
│   ├── main.py                  # FastAPI application
│   ├── models/                  # Data models
│   │   ├── __init__.py
│   │   ├── strategy.py          # Strategy models
│   │   ├── backtest.py          # Backtest request/response
│   │   └── optimization.py      # Optimization models
│   ├── services/                # Business logic
│   │   ├── __init__.py
│   │   ├── backtest_service.py  # Core backtesting logic
│   │   ├── optimization_service.py # Ray optimization
│   │   ├── data_service.py      # Data preparation
│   │   └── visualization_service.py # Plotting service
│   ├── api/                     # API endpoints
│   │   ├── __init__.py
│   │   ├── backtest.py          # Backtest endpoints
│   │   ├── optimization.py      # Optimization endpoints
│   │   ├── strategies.py        # Strategy management
│   │   └── visualization.py     # Plot endpoints
│   ├── backtrader/              # Complete framework
│   │   └── [entire backtrader framework]
│   ├── cerebro/                 # Custom implementation
│   │   └── [custom cerebro components]
│   ├── strategies/              # Strategy implementations
│   │   ├── __init__.py
│   │   ├── base_strategy.py     # Base strategy class
│   │   ├── three_step_strategy.py
│   │   ├── live_strategy.py
│   │   └── custom/              # Custom strategies
│   ├── indicators/              # Custom indicators
│   │   ├── __init__.py
│   │   ├── bollinger_smoother.py
│   │   ├── adaptive_super_trend.py
│   │   └── gaussian_filter.py
│   └── utils/                   # Utilities
│       ├── __init__.py
│       ├── data_loader.py       # Data loading utilities
│       ├── config.py            # Configuration
│       └── validators.py         # Input validation
├── tests/                       # Test suite
│   ├── __init__.py
│   ├── test_backtest.py
│   ├── test_optimization.py
│   ├── test_strategies.py
│   └── fixtures/                # Test data
├── docs/                        # Documentation
│   ├── README.md
│   ├── API.md
│   └── examples/                # Usage examples
├── requirements.txt              # Dependencies
├── Dockerfile                   # Container config
├── docker-compose.yml           # Local development
└── README.md                    # Service documentation
```

### **Phase 2: Core API Implementation** (Priority: HIGH)
**Timeline: 2-3 weeks**

#### **2.1 FastAPI Application Structure**
```python
# src/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from .api import backtest, optimization, strategies, visualization
from .services.backtest_service import BacktestService
from .services.optimization_service import OptimizationService
from .utils.config import load_environment

# Load environment
load_environment()

# Setup logging
logger = logging.getLogger("backtrader-service")

# Services
backtest_service = BacktestService()
optimization_service = OptimizationService()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    logger.info("Starting Backtrader Service...")
    yield
    logger.info("Shutting down Backtrader Service...")

# Create FastAPI app
app = FastAPI(
    title="Bifrost Trader Backtrader Service",
    version="1.0.0",
    description="Standalone backtesting service with Backtrader framework",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(backtest.router, prefix="/api/backtest", tags=["backtest"])
app.include_router(optimization.router, prefix="/api/optimization", tags=["optimization"])
app.include_router(strategies.router, prefix="/api/strategies", tags=["strategies"])
app.include_router(visualization.router, prefix="/api/visualization", tags=["visualization"])

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "backtrader-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8004, reload=True)
```

#### **2.2 Core API Endpoints**

**Backtest Endpoints:**
```python
# src/api/backtest.py
from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Dict, Any, Optional
from ..models.backtest import BacktestRequest, BacktestResponse
from ..services.backtest_service import BacktestService

router = APIRouter()
backtest_service = BacktestService()

@router.post("/run", response_model=BacktestResponse)
async def run_backtest(request: BacktestRequest):
    """Run a backtest with specified parameters."""
    try:
        result = await backtest_service.run_backtest(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/run-async")
async def run_backtest_async(request: BacktestRequest, background_tasks: BackgroundTasks):
    """Run backtest asynchronously."""
    task_id = await backtest_service.run_backtest_async(request)
    return {"task_id": task_id, "status": "started"}

@router.get("/status/{task_id}")
async def get_backtest_status(task_id: str):
    """Get backtest status."""
    status = await backtest_service.get_task_status(task_id)
    return status

@router.get("/result/{task_id}")
async def get_backtest_result(task_id: str):
    """Get backtest result."""
    result = await backtest_service.get_task_result(task_id)
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    return result
```

**Optimization Endpoints:**
```python
# src/api/optimization.py
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from ..models.optimization import OptimizationRequest, OptimizationResponse
from ..services.optimization_service import OptimizationService

router = APIRouter()
optimization_service = OptimizationService()

@router.post("/run", response_model=OptimizationResponse)
async def run_optimization(request: OptimizationRequest):
    """Run strategy optimization with Ray."""
    try:
        result = await optimization_service.run_optimization(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/strategies")
async def get_available_strategies():
    """Get list of available strategies."""
    strategies = await optimization_service.get_available_strategies()
    return {"strategies": strategies}
```

### **Phase 3: Core Service Implementation** (Priority: HIGH)
**Timeline: 2-3 weeks**

#### **3.1 Backtest Service Implementation**
```python
# src/services/backtest_service.py
import asyncio
import uuid
from typing import Dict, Any, Optional
from datetime import datetime
import pandas as pd
import backtrader as bt
from cerebro.cerebro_base import cerebroBase
from ..models.backtest import BacktestRequest, BacktestResponse
from ..utils.data_loader import DataLoader

class BacktestService:
    def __init__(self):
        self.tasks = {}  # Store running tasks
        self.data_loader = DataLoader()
    
    async def run_backtest(self, request: BacktestRequest) -> BacktestResponse:
        """Run a backtest synchronously."""
        try:
            # Prepare data
            data = await self.data_loader.load_data(
                symbols=request.symbols,
                start_date=request.start_date,
                end_date=request.end_date,
                interval=request.interval
            )
            
            # Create cerebro instance
            cerebro_instance = cerebroBase(stdstats=True)
            cerebro_instance.set_data({
                'symbols': '|'.join(request.symbols),
                'period': request.period,
                'interval': request.interval,
                'since': request.start_date.isoformat()
            })
            
            # Add strategy
            strategy_class = self._get_strategy_class(request.strategy_name)
            cerebro_instance.cerebro.addstrategy(
                strategy_class, 
                **request.strategy_params
            )
            
            # Run backtest
            result = cerebro_instance.run()
            
            # Process results
            return self._process_backtest_result(result, request)
            
        except Exception as e:
            raise Exception(f"Backtest failed: {str(e)}")
    
    async def run_backtest_async(self, request: BacktestRequest) -> str:
        """Run backtest asynchronously."""
        task_id = str(uuid.uuid4())
        
        # Store task info
        self.tasks[task_id] = {
            'status': 'running',
            'start_time': datetime.now(),
            'request': request,
            'result': None,
            'error': None
        }
        
        # Run in background
        asyncio.create_task(self._run_backtest_task(task_id, request))
        
        return task_id
    
    async def _run_backtest_task(self, task_id: str, request: BacktestRequest):
        """Background task for running backtest."""
        try:
            result = await self.run_backtest(request)
            self.tasks[task_id]['result'] = result
            self.tasks[task_id]['status'] = 'completed'
        except Exception as e:
            self.tasks[task_id]['error'] = str(e)
            self.tasks[task_id]['status'] = 'failed'
    
    def _get_strategy_class(self, strategy_name: str):
        """Get strategy class by name."""
        strategy_map = {
            'three_step': ThreeStepStrategy,
            'live': LiveStrategy,
            # Add more strategies
        }
        return strategy_map.get(strategy_name, ThreeStepStrategy)
    
    def _process_backtest_result(self, result, request: BacktestRequest) -> BacktestResponse:
        """Process backtest result into response format."""
        # Extract performance metrics
        strategy_result = result[0]
        
        # Get analyzer results
        analyzers = {}
        for analyzer in strategy_result.analyzers:
            analyzers[analyzer.__class__.__name__] = analyzer.get_analysis()
        
        return BacktestResponse(
            success=True,
            strategy_name=request.strategy_name,
            symbols=request.symbols,
            start_date=request.start_date,
            end_date=request.end_date,
            initial_capital=request.initial_capital,
            final_capital=strategy_result.broker.getvalue(),
            total_return=(strategy_result.broker.getvalue() - request.initial_capital) / request.initial_capital,
            analyzers=analyzers,
            trades_count=len(strategy_result.broker.get_trades()),
            execution_time=datetime.now().isoformat()
        )
```

#### **3.2 Optimization Service Implementation**
```python
# src/services/optimization_service.py
import ray
from typing import Dict, Any, List
from ..models.optimization import OptimizationRequest, OptimizationResponse
from cerebro.ray_optimize import RayStrategyOptimize

class OptimizationService:
    def __init__(self):
        # Initialize Ray
        if not ray.is_initialized():
            ray.init()
    
    async def run_optimization(self, request: OptimizationRequest) -> OptimizationResponse:
        """Run strategy optimization with Ray."""
        try:
            # Create optimization instance
            optimizer = RayStrategyOptimize.remote(stdstats=True)
            
            # Set optimization parameters
            optimizer.set_data.remote({
                'symbols': '|'.join(request.symbols),
                'period': request.period,
                'interval': request.interval,
                'since': request.start_date.isoformat()
            })
            
            # Set parameter ranges
            optimizer.set_parameter_ranges.remote(request.parameter_ranges)
            
            # Run optimization
            results = await optimizer.run.remote()
            
            # Process results
            return self._process_optimization_results(results, request)
            
        except Exception as e:
            raise Exception(f"Optimization failed: {str(e)}")
    
    def _process_optimization_results(self, results, request: OptimizationRequest) -> OptimizationResponse:
        """Process optimization results."""
        # Find best parameters
        best_result = max(results, key=lambda x: x.analyzers.sharpe.get_analysis()['sharperatio'])
        
        return OptimizationResponse(
            success=True,
            best_parameters=best_result.params,
            best_performance=best_result.analyzers.sharpe.get_analysis(),
            all_results=results,
            optimization_time=datetime.now().isoformat()
        )
```

### **Phase 4: Data Integration** (Priority: MEDIUM)
**Timeline: 1-2 weeks**

#### **4.1 Data Service Integration**
```python
# src/services/data_service.py
import httpx
from typing import List, Dict, Any
from datetime import datetime, timedelta

class DataService:
    def __init__(self, data_service_url: str = "http://localhost:8001"):
        self.data_service_url = data_service_url
    
    async def get_historical_data(self, symbols: List[str], start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Get historical data from data service."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.data_service_url}/data/{symbols[0]}/historical",
                params={
                    "start_date": start_date.isoformat(),
                    "end_date": end_date.isoformat(),
                    "period": "max"
                }
            )
            return response.json()
    
    async def get_latest_data(self, symbol: str) -> Dict[str, Any]:
        """Get latest data for symbol."""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.data_service_url}/data/{symbol}/latest")
            return response.json()
```

### **Phase 5: Visualization Service** (Priority: MEDIUM)
**Timeline: 1-2 weeks**

#### **5.1 Visualization Service Implementation**
```python
# src/services/visualization_service.py
from backtrader_plotting import Bokeh
from backtrader_plotting.schemes import Tradimo
from typing import Dict, Any
import io
import base64

class VisualizationService:
    def __init__(self):
        self.bokeh_config = {
            'style': 'bar',
            'plot_mode': 'single',
            'scheme': Tradimo(),
            'output_mode': 'memory'
        }
    
    async def generate_plot(self, cerebro_instance, strategy_result) -> Dict[str, Any]:
        """Generate Bokeh plot for backtest results."""
        try:
            # Create Bokeh instance
            bokeh = Bokeh(**self.bokeh_config)
            
            # Generate plot
            cerebro_instance.plot(bokeh, iplot=False)
            
            # Get plot data
            plot_data = bokeh.figurepages[0].model
            
            # Convert to JSON-serializable format
            return {
                'success': True,
                'plot_data': plot_data,
                'plot_type': 'bokeh'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    async def generate_performance_chart(self, backtest_result) -> Dict[str, Any]:
        """Generate performance chart."""
        # Implementation for performance visualization
        pass
```

## 📋 **Implementation Checklist**

### **Phase 1: Service Setup**
- [ ] Create backtrader-service directory structure
- [ ] Copy complete backtrader framework
- [ ] Copy cerebro implementation
- [ ] Copy custom strategies and indicators
- [ ] Set up FastAPI application structure
- [ ] Configure logging and error handling

### **Phase 2: API Implementation**
- [ ] Implement backtest endpoints
- [ ] Implement optimization endpoints
- [ ] Implement strategy management endpoints
- [ ] Implement visualization endpoints
- [ ] Add input validation
- [ ] Add error handling
- [ ] Add API documentation

### **Phase 3: Core Services**
- [ ] Implement BacktestService
- [ ] Implement OptimizationService
- [ ] Implement DataService integration
- [ ] Implement VisualizationService
- [ ] Add async task management
- [ ] Add result caching
- [ ] Add performance monitoring

### **Phase 4: Data Integration**
- [ ] Integrate with data-service
- [ ] Implement data loading utilities
- [ ] Add data validation
- [ ] Add data caching
- [ ] Support multiple data sources

### **Phase 5: Visualization**
- [ ] Implement Bokeh plotting
- [ ] Add performance charts
- [ ] Add trade visualization
- [ ] Add strategy comparison charts
- [ ] Export plot functionality

### **Phase 6: Testing & Documentation**
- [ ] Write unit tests
- [ ] Write integration tests
- [ ] Add API documentation
- [ ] Add usage examples
- [ ] Performance testing
- [ ] Load testing

## 🚀 **Deployment Strategy**

### **Standalone Deployment**
```yaml
# docker-compose.yml
version: '3.8'
services:
  backtrader-service:
    build: .
    ports:
      - "8004:8004"
    environment:
      - REDIS_URL=redis://redis:6379
      - DATA_SERVICE_URL=http://data-service:8001
    depends_on:
      - redis
      - data-service
    volumes:
      - ./data:/app/data
      - ./results:/app/results
```

### **Production Deployment**
```yaml
# kubernetes deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backtrader-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: backtrader-service
  template:
    metadata:
      labels:
        app: backtrader-service
    spec:
      containers:
      - name: backtrader-service
        image: bifrost-trader/backtrader-service:latest
        ports:
        - containerPort: 8004
        env:
        - name: REDIS_URL
          value: "redis://redis-service:6379"
        - name: DATA_SERVICE_URL
          value: "http://data-service:8001"
```

## 📊 **Success Metrics**

### **Performance Targets**
- **Backtest Speed**: < 30 seconds for 1-year daily data
- **Optimization Speed**: < 5 minutes for 100 parameter combinations
- **API Response Time**: < 200ms for simple requests
- **Concurrent Users**: Support 50+ simultaneous backtests
- **Memory Usage**: < 2GB per backtest instance

### **Reliability Targets**
- **Uptime**: 99.9% availability
- **Error Rate**: < 0.1% API errors
- **Data Accuracy**: 100% accurate backtest results
- **Recovery Time**: < 30 seconds for service restart

## 🎯 **Next Steps**

### **Immediate Actions** (This Week)
1. Create backtrader-service directory structure
2. Copy backtrader framework and cerebro implementation
3. Set up basic FastAPI application
4. Implement core backtest endpoint

### **Short-term Goals** (Next 2 Weeks)
1. Complete API implementation
2. Implement core services
3. Add data service integration
4. Basic testing and validation

### **Medium-term Goals** (Next Month)
1. Complete visualization service
2. Add optimization capabilities
3. Performance optimization
4. Production deployment preparation

---

**Last Updated**: December 2024  
**Status**: Ready for Implementation  
**Priority**: HIGH
