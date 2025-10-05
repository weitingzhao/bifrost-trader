# Bifrost Trader Portal Design Plan

## 🎯 **Portal Overview**

Based on the analysis of Smart Trader's existing portal and the Django Soft UI Dashboard template, Bifrost Trader will feature a modern, professional trading platform interface that combines the best of both designs with enhanced microservices architecture.

## 🎨 **Design Foundation**

### **Base Template: Django Soft UI Dashboard**
- **Modern UI Framework**: Bootstrap 5 with Soft UI design system
- **Professional Look**: Clean, minimalist interface with subtle shadows and gradients
- **Responsive Design**: Mobile-first approach with adaptive layouts
- **Dark/Light Theme**: Toggle between themes for user preference
- **Component Library**: Rich set of pre-built components (cards, charts, tables, forms)

### **Smart Trader Features Integration**
- **Trading-Specific Components**: Portfolio management, position tracking, strategy execution
- **Real-time Data Visualization**: Live charts, market data, performance metrics
- **Advanced Analytics**: Backtesting results, optimization charts, risk analysis
- **Professional Trading Tools**: Order management, screening, research capabilities

## 🏗️ **Portal Architecture**

### **Service Structure**
```
bifrost-trader/services/web-portal/
├── src/
│   ├── __init__.py
│   ├── main.py                  # FastAPI application
│   ├── models/                  # Data models
│   │   ├── __init__.py
│   │   ├── user.py              # User models
│   │   ├── dashboard.py         # Dashboard data models
│   │   └── trading.py           # Trading-specific models
│   ├── services/                # Business logic
│   │   ├── __init__.py
│   │   ├── dashboard_service.py # Dashboard data aggregation
│   │   ├── trading_service.py   # Trading operations
│   │   ├── notification_service.py # Real-time notifications
│   │   └── websocket_service.py # WebSocket connections
│   ├── api/                     # API endpoints
│   │   ├── __init__.py
│   │   ├── dashboard.py         # Dashboard APIs
│   │   ├── trading.py           # Trading APIs
│   │   ├── portfolio.py         # Portfolio APIs
│   │   └── websocket.py         # WebSocket endpoints
│   ├── templates/               # HTML templates
│   │   ├── layouts/
│   │   │   ├── base.html        # Base template
│   │   │   ├── base-trading.html # Trading-specific base
│   │   │   └── base-fullscreen.html # Fullscreen charts
│   │   ├── includes/
│   │   │   ├── sidebar.html     # Navigation sidebar
│   │   │   ├── navigation.html  # Top navigation
│   │   │   ├── trading-sidebar.html # Trading-specific sidebar
│   │   │   └── scripts.html     # JavaScript includes
│   │   ├── pages/
│   │   │   ├── dashboard/       # Dashboard pages
│   │   │   ├── trading/         # Trading pages
│   │   │   ├── portfolio/       # Portfolio pages
│   │   │   ├── analytics/       # Analytics pages
│   │   │   └── settings/        # Settings pages
│   │   └── components/          # Reusable components
│   │       ├── charts/          # Chart components
│   │       ├── tables/          # Data tables
│   │       └── forms/           # Form components
│   ├── static/                  # Static assets
│   │   ├── css/
│   │   │   ├── soft-ui-dashboard.css # Base Soft UI styles
│   │   │   ├── trading.css      # Trading-specific styles
│   │   │   └── custom.css       # Custom styles
│   │   ├── js/
│   │   │   ├── trading.js       # Trading functionality
│   │   │   ├── charts.js        # Chart interactions
│   │   │   ├── websocket.js     # WebSocket handling
│   │   │   └── dashboard.js     # Dashboard interactions
│   │   ├── img/
│   │   │   ├── logos/           # Bifrost Trader logos
│   │   │   ├── icons/           # Custom icons
│   │   │   └── charts/          # Chart backgrounds
│   │   └── fonts/               # Custom fonts
│   └── utils/                   # Utilities
│       ├── __init__.py
│       ├── decorators.py        # Custom decorators
│       ├── helpers.py           # Template helpers
│       └── validators.py        # Form validators
├── tests/                       # Test suite
├── docs/                        # Documentation
├── requirements.txt             # Dependencies
├── Dockerfile                   # Container config
└── README.md                    # Service documentation
```

## 📱 **Page Structure & Navigation**

### **Main Navigation Sidebar**
```html
<!-- Trading-Focused Sidebar -->
<aside class="sidenav navbar navbar-vertical navbar-expand-xs border-0 border-radius-xl my-3 fixed-start ms-3" id="sidenav-main">
  <div class="sidenav-header">
    <a class="navbar-brand m-0" href="/">
      <img src="{% static 'assets/img/logo-bifrost-trader.png' %}" class="navbar-brand-img h-100" alt="Bifrost Trader">
      <span class="ms-1 font-weight-bold">Bifrost Trader</span>
    </a>
  </div>
  
  <div class="collapse navbar-collapse w-auto h-auto" id="sidenav-collapse-main">
    <ul class="navbar-nav">
      
      <!-- Dashboard Section -->
      <li class="nav-item">
        <a class="nav-link" href="{% url 'dashboard' %}">
          <div class="icon icon-shape icon-sm shadow border-radius-md bg-white text-center me-2">
            <i class="ni ni-chart-pie-35 text-dark text-sm opacity-10"></i>
          </div>
          <span class="nav-link-text ms-1">Dashboard</span>
        </a>
      </li>
      
      <!-- Trading Section -->
      <li class="nav-item">
        <a data-bs-toggle="collapse" href="#tradingExamples" class="nav-link" aria-controls="tradingExamples" role="button" aria-expanded="false">
          <div class="icon icon-shape icon-sm shadow border-radius-md bg-white text-center me-2">
            <i class="ni ni-chart-bar-32 text-dark text-sm opacity-10"></i>
          </div>
          <span class="nav-link-text ms-1">Trading</span>
        </a>
        <div class="collapse" id="tradingExamples">
          <ul class="nav ms-4 ps-3">
            <li class="nav-item">
              <a class="nav-link" href="{% url 'live_trading' %}">
                <span class="sidenav-mini-icon">L</span>
                <span class="sidenav-normal">Live Trading</span>
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="{% url 'backtesting' %}">
                <span class="sidenav-mini-icon">B</span>
                <span class="sidenav-normal">Backtesting</span>
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="{% url 'strategy_optimization' %}">
                <span class="sidenav-mini-icon">O</span>
                <span class="sidenav-normal">Strategy Optimization</span>
              </a>
            </li>
          </ul>
        </div>
      </li>
      
      <!-- Portfolio Section -->
      <li class="nav-item">
        <a data-bs-toggle="collapse" href="#portfolioExamples" class="nav-link" aria-controls="portfolioExamples" role="button" aria-expanded="false">
          <div class="icon icon-shape icon-sm shadow border-radius-md bg-white text-center me-2">
            <i class="ni ni-briefcase-24 text-dark text-sm opacity-10"></i>
          </div>
          <span class="nav-link-text ms-1">Portfolio</span>
        </a>
        <div class="collapse" id="portfolioExamples">
          <ul class="nav ms-4 ps-3">
            <li class="nav-item">
              <a class="nav-link" href="{% url 'portfolio_overview' %}">
                <span class="sidenav-mini-icon">O</span>
                <span class="sidenav-normal">Overview</span>
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="{% url 'positions' %}">
                <span class="sidenav-mini-icon">P</span>
                <span class="sidenav-normal">Positions</span>
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="{% url 'orders' %}">
                <span class="sidenav-mini-icon">O</span>
                <span class="sidenav-normal">Orders</span>
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="{% url 'performance' %}">
                <span class="sidenav-mini-icon">P</span>
                <span class="sidenav-normal">Performance</span>
              </a>
            </li>
          </ul>
        </div>
      </li>
      
      <!-- Analytics Section -->
      <li class="nav-item">
        <a data-bs-toggle="collapse" href="#analyticsExamples" class="nav-link" aria-controls="analyticsExamples" role="button" aria-expanded="false">
          <div class="icon icon-shape icon-sm shadow border-radius-md bg-white text-center me-2">
            <i class="ni ni-chart-line text-dark text-sm opacity-10"></i>
          </div>
          <span class="nav-link-text ms-1">Analytics</span>
        </a>
        <div class="collapse" id="analyticsExamples">
          <ul class="nav ms-4 ps-3">
            <li class="nav-item">
              <a class="nav-link" href="{% url 'market_analysis' %}">
                <span class="sidenav-mini-icon">M</span>
                <span class="sidenav-normal">Market Analysis</span>
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="{% url 'risk_analysis' %}">
                <span class="sidenav-mini-icon">R</span>
                <span class="sidenav-normal">Risk Analysis</span>
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="{% url 'ml_insights' %}">
                <span class="sidenav-mini-icon">M</span>
                <span class="sidenav-normal">ML Insights</span>
              </a>
            </li>
          </ul>
        </div>
      </li>
      
      <!-- Research Section -->
      <li class="nav-item">
        <a data-bs-toggle="collapse" href="#researchExamples" class="nav-link" aria-controls="researchExamples" role="button" aria-expanded="false">
          <div class="icon icon-shape icon-sm shadow border-radius-md bg-white text-center me-2">
            <i class="ni ni-bullet-list-67 text-dark text-sm opacity-10"></i>
          </div>
          <span class="nav-link-text ms-1">Research</span>
        </a>
        <div class="collapse" id="researchExamples">
          <ul class="nav ms-4 ps-3">
            <li class="nav-item">
              <a class="nav-link" href="{% url 'screening' %}">
                <span class="sidenav-mini-icon">S</span>
                <span class="sidenav-normal">Stock Screening</span>
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="{% url 'news_sentiment' %}">
                <span class="sidenav-mini-icon">N</span>
                <span class="sidenav-normal">News & Sentiment</span>
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="{% url 'market_microstructure' %}">
                <span class="sidenav-mini-icon">M</span>
                <span class="sidenav-normal">Market Microstructure</span>
              </a>
            </li>
          </ul>
        </div>
      </li>
      
      <!-- Settings Section -->
      <li class="nav-item">
        <a class="nav-link" href="{% url 'settings' %}">
          <div class="icon icon-shape icon-sm shadow border-radius-md bg-white text-center me-2">
            <i class="ni ni-settings-gear-65 text-dark text-sm opacity-10"></i>
          </div>
          <span class="nav-link-text ms-1">Settings</span>
        </a>
      </li>
      
    </ul>
  </div>
</aside>
```

## 🎯 **Key Pages & Features**

### **1. Dashboard Page**
```html
<!-- Main Dashboard -->
<div class="container-fluid py-4">
  <div class="row">
    <!-- Portfolio Summary Cards -->
    <div class="col-lg-3 col-sm-6 mb-4">
      <div class="card">
        <div class="card-body p-3">
          <div class="row">
            <div class="col-8">
              <div class="numbers">
                <p class="text-sm mb-0 text-capitalize font-weight-bold">Total Portfolio Value</p>
                <h5 class="font-weight-bolder mb-0">
                  ${{ portfolio_value|floatformat:2 }}
                  <span class="text-success text-sm font-weight-bolder">+{{ daily_return|floatformat:1 }}%</span>
                </h5>
              </div>
            </div>
            <div class="col-4 text-end">
              <div class="icon icon-shape bg-gradient-success shadow text-center border-radius-md">
                <i class="ni ni-money-coins text-lg opacity-10"></i>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Active Positions -->
    <div class="col-lg-3 col-sm-6 mb-4">
      <div class="card">
        <div class="card-body p-3">
          <div class="row">
            <div class="col-8">
              <div class="numbers">
                <p class="text-sm mb-0 text-capitalize font-weight-bold">Active Positions</p>
                <h5 class="font-weight-bolder mb-0">{{ active_positions }}</h5>
              </div>
            </div>
            <div class="col-4 text-end">
              <div class="icon icon-shape bg-gradient-info shadow text-center border-radius-md">
                <i class="ni ni-chart-bar-32 text-lg opacity-10"></i>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Today's P&L -->
    <div class="col-lg-3 col-sm-6 mb-4">
      <div class="card">
        <div class="card-body p-3">
          <div class="row">
            <div class="col-8">
              <div class="numbers">
                <p class="text-sm mb-0 text-capitalize font-weight-bold">Today's P&L</p>
                <h5 class="font-weight-bolder mb-0">
                  ${{ today_pnl|floatformat:2 }}
                  <span class="{% if today_pnl >= 0 %}text-success{% else %}text-danger{% endif %} text-sm font-weight-bolder">
                    {% if today_pnl >= 0 %}+{% endif %}{{ today_pnl_percent|floatformat:1 }}%
                  </span>
                </h5>
              </div>
            </div>
            <div class="col-4 text-end">
              <div class="icon icon-shape bg-gradient-{% if today_pnl >= 0 %}success{% else %}danger{% endif %} shadow text-center border-radius-md">
                <i class="ni ni-chart-line text-lg opacity-10"></i>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Risk Metrics -->
    <div class="col-lg-3 col-sm-6 mb-4">
      <div class="card">
        <div class="card-body p-3">
          <div class="row">
            <div class="col-8">
              <div class="numbers">
                <p class="text-sm mb-0 text-capitalize font-weight-bold">Portfolio VaR</p>
                <h5 class="font-weight-bolder mb-0">
                  ${{ portfolio_var|floatformat:2 }}
                  <span class="text-warning text-sm font-weight-bolder">{{ var_percentile }}%</span>
                </h5>
              </div>
            </div>
            <div class="col-4 text-end">
              <div class="icon icon-shape bg-gradient-warning shadow text-center border-radius-md">
                <i class="ni ni-shield text-lg opacity-10"></i>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  
  <!-- Real-time Charts -->
  <div class="row mt-4">
    <div class="col-lg-8">
      <div class="card z-index-2">
        <div class="card-header pb-0">
          <h6>Portfolio Performance</h6>
          <p class="text-sm">
            <i class="fa fa-circle text-success"></i>
            <span class="font-weight-bold">Live</span> Real-time updates
          </p>
        </div>
        <div class="card-body p-3">
          <div class="chart">
            <canvas id="portfolio-chart" class="chart-canvas" height="300"></canvas>
          </div>
        </div>
      </div>
    </div>
    
    <div class="col-lg-4">
      <div class="card">
        <div class="card-header pb-0">
          <h6>Top Positions</h6>
        </div>
        <div class="card-body p-3">
          <div class="table-responsive">
            <table class="table align-items-center">
              <tbody>
                {% for position in top_positions %}
                <tr>
                  <td class="w-30">
                    <div class="d-flex px-2 py-1 align-items-center">
                      <div class="ms-4">
                        <h6 class="text-sm mb-0">{{ position.symbol }}</h6>
                        <p class="text-xs text-secondary mb-0">{{ position.quantity }} shares</p>
                      </div>
                    </div>
                  </td>
                  <td>
                    <div class="text-center">
                      <h6 class="text-sm mb-0">${{ position.current_value|floatformat:2 }}</h6>
                      <p class="text-xs text-secondary mb-0">{{ position.weight|floatformat:1 }}%</p>
                    </div>
                  </td>
                  <td class="align-middle text-sm">
                    <div class="col text-center">
                      <span class="text-xs font-weight-bold {% if position.pnl >= 0 %}text-success{% else %}text-danger{% endif %}">
                        {% if position.pnl >= 0 %}+{% endif %}${{ position.pnl|floatformat:2 }}
                      </span>
                    </div>
                  </td>
                </tr>
                {% endfor %}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
```

### **2. Live Trading Page**
```html
<!-- Live Trading Interface -->
<div class="container-fluid py-4">
  <div class="row">
    <!-- Trading Panel -->
    <div class="col-lg-4">
      <div class="card">
        <div class="card-header pb-0">
          <h6>Quick Trade</h6>
        </div>
        <div class="card-body p-3">
          <form id="quick-trade-form">
            <div class="mb-3">
              <label class="form-label">Symbol</label>
              <input type="text" class="form-control" id="trade-symbol" placeholder="AAPL">
            </div>
            <div class="mb-3">
              <label class="form-label">Action</label>
              <select class="form-select" id="trade-action">
                <option value="buy">Buy</option>
                <option value="sell">Sell</option>
              </select>
            </div>
            <div class="mb-3">
              <label class="form-label">Quantity</label>
              <input type="number" class="form-control" id="trade-quantity" placeholder="100">
            </div>
            <div class="mb-3">
              <label class="form-label">Order Type</label>
              <select class="form-select" id="order-type">
                <option value="market">Market</option>
                <option value="limit">Limit</option>
                <option value="stop">Stop</option>
              </select>
            </div>
            <button type="submit" class="btn btn-primary w-100">Place Order</button>
          </form>
        </div>
      </div>
      
      <!-- Account Summary -->
      <div class="card mt-4">
        <div class="card-header pb-0">
          <h6>Account Summary</h6>
        </div>
        <div class="card-body p-3">
          <div class="row">
            <div class="col-6">
              <p class="text-sm mb-0">Buying Power</p>
              <h6 class="font-weight-bolder mb-0">${{ buying_power|floatformat:2 }}</h6>
            </div>
            <div class="col-6">
              <p class="text-sm mb-0">Cash</p>
              <h6 class="font-weight-bolder mb-0">${{ cash_balance|floatformat:2 }}</h6>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Live Chart -->
    <div class="col-lg-8">
      <div class="card z-index-2">
        <div class="card-header pb-0">
          <div class="d-flex justify-content-between">
            <h6 id="chart-symbol">AAPL</h6>
            <div class="btn-group" role="group">
              <button type="button" class="btn btn-sm btn-outline-primary" data-timeframe="1m">1m</button>
              <button type="button" class="btn btn-sm btn-outline-primary" data-timeframe="5m">5m</button>
              <button type="button" class="btn btn-sm btn-outline-primary active" data-timeframe="1h">1h</button>
              <button type="button" class="btn btn-sm btn-outline-primary" data-timeframe="1d">1d</button>
            </div>
          </div>
        </div>
        <div class="card-body p-3">
          <div class="chart">
            <canvas id="live-chart" class="chart-canvas" height="400"></canvas>
          </div>
        </div>
      </div>
    </div>
  </div>
  
  <!-- Active Orders -->
  <div class="row mt-4">
    <div class="col-12">
      <div class="card">
        <div class="card-header pb-0">
          <h6>Active Orders</h6>
        </div>
        <div class="card-body p-3">
          <div class="table-responsive">
            <table class="table align-items-center" id="orders-table">
              <thead>
                <tr>
                  <th>Symbol</th>
                  <th>Side</th>
                  <th>Quantity</th>
                  <th>Price</th>
                  <th>Status</th>
                  <th>Time</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <!-- Orders populated via WebSocket -->
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
```

### **3. Backtesting Page**
```html
<!-- Backtesting Interface -->
<div class="container-fluid py-4">
  <div class="row">
    <!-- Backtest Configuration -->
    <div class="col-lg-4">
      <div class="card">
        <div class="card-header pb-0">
          <h6>Backtest Configuration</h6>
        </div>
        <div class="card-body p-3">
          <form id="backtest-form">
            <div class="mb-3">
              <label class="form-label">Strategy</label>
              <select class="form-select" id="strategy-select">
                <option value="three_step">Three Step Strategy</option>
                <option value="momentum">Momentum Strategy</option>
                <option value="mean_reversion">Mean Reversion</option>
              </select>
            </div>
            <div class="mb-3">
              <label class="form-label">Symbols</label>
              <input type="text" class="form-control" id="backtest-symbols" placeholder="AAPL,MSFT,GOOGL">
            </div>
            <div class="mb-3">
              <label class="form-label">Start Date</label>
              <input type="date" class="form-control" id="start-date">
            </div>
            <div class="mb-3">
              <label class="form-label">End Date</label>
              <input type="date" class="form-control" id="end-date">
            </div>
            <div class="mb-3">
              <label class="form-label">Initial Capital</label>
              <input type="number" class="form-control" id="initial-capital" value="100000">
            </div>
            <button type="submit" class="btn btn-primary w-100">Run Backtest</button>
          </form>
        </div>
      </div>
      
      <!-- Strategy Parameters -->
      <div class="card mt-4">
        <div class="card-header pb-0">
          <h6>Strategy Parameters</h6>
        </div>
        <div class="card-body p-3" id="strategy-params">
          <!-- Dynamic parameters based on selected strategy -->
        </div>
      </div>
    </div>
    
    <!-- Backtest Results -->
    <div class="col-lg-8">
      <div class="card z-index-2">
        <div class="card-header pb-0">
          <h6>Backtest Results</h6>
        </div>
        <div class="card-body p-3">
          <div class="chart">
            <canvas id="backtest-chart" class="chart-canvas" height="300"></canvas>
          </div>
        </div>
      </div>
      
      <!-- Performance Metrics -->
      <div class="row mt-4">
        <div class="col-lg-3 col-sm-6 mb-4">
          <div class="card">
            <div class="card-body p-3">
              <div class="numbers">
                <p class="text-sm mb-0 text-capitalize font-weight-bold">Total Return</p>
                <h5 class="font-weight-bolder mb-0" id="total-return">--</h5>
              </div>
            </div>
          </div>
        </div>
        <div class="col-lg-3 col-sm-6 mb-4">
          <div class="card">
            <div class="card-body p-3">
              <div class="numbers">
                <p class="text-sm mb-0 text-capitalize font-weight-bold">Sharpe Ratio</p>
                <h5 class="font-weight-bolder mb-0" id="sharpe-ratio">--</h5>
              </div>
            </div>
          </div>
        </div>
        <div class="col-lg-3 col-sm-6 mb-4">
          <div class="card">
            <div class="card-body p-3">
              <div class="numbers">
                <p class="text-sm mb-0 text-capitalize font-weight-bold">Max Drawdown</p>
                <h5 class="font-weight-bolder mb-0" id="max-drawdown">--</h5>
              </div>
            </div>
          </div>
        </div>
        <div class="col-lg-3 col-sm-6 mb-4">
          <div class="card">
            <div class="card-body p-3">
              <div class="numbers">
                <p class="text-sm mb-0 text-capitalize font-weight-bold">Win Rate</p>
                <h5 class="font-weight-bolder mb-0" id="win-rate">--</h5>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
```

## 🔧 **Technical Implementation**

### **FastAPI Application Structure**
```python
# src/main.py
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from contextlib import asynccontextmanager

from .services.dashboard_service import DashboardService
from .services.trading_service import TradingService
from .services.websocket_service import WebSocketService
from .api import dashboard, trading, portfolio, websocket

# Services
dashboard_service = DashboardService()
trading_service = TradingService()
websocket_service = WebSocketService()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Start WebSocket service
    asyncio.create_task(websocket_service.start())
    yield
    # Cleanup
    await websocket_service.stop()

# Create FastAPI app
app = FastAPI(
    title="Bifrost Trader Web Portal",
    version="1.0.0",
    description="Trading platform web interface",
    lifespan=lifespan
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(dashboard.router)
app.include_router(trading.router)
app.include_router(portfolio.router)
app.include_router(websocket.router)

# Template routes
@app.get("/")
async def dashboard_page(request: Request):
    """Main dashboard page."""
    dashboard_data = await dashboard_service.get_dashboard_data()
    return templates.TemplateResponse("pages/dashboard/overview.html", {
        "request": request,
        "dashboard_data": dashboard_data
    })

@app.get("/trading")
async def trading_page(request: Request):
    """Live trading page."""
    trading_data = await trading_service.get_trading_data()
    return templates.TemplateResponse("pages/trading/live.html", {
        "request": request,
        "trading_data": trading_data
    })

@app.get("/backtesting")
async def backtesting_page(request: Request):
    """Backtesting page."""
    return templates.TemplateResponse("pages/trading/backtesting.html", {
        "request": request
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8006, reload=True)
```

### **WebSocket Integration**
```python
# src/services/websocket_service.py
import asyncio
import json
from typing import Dict, List
from fastapi import WebSocket

class WebSocketService:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.data_service_url = "http://data-service:8001"
        self.trading_service_url = "http://execution-service:8004"
    
    async def connect(self, websocket: WebSocket):
        """Accept WebSocket connection."""
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        """Remove WebSocket connection."""
        self.active_connections.remove(websocket)
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Send message to specific WebSocket."""
        await websocket.send_text(message)
    
    async def broadcast(self, message: str):
        """Broadcast message to all connected clients."""
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                # Remove broken connections
                self.active_connections.remove(connection)
    
    async def start(self):
        """Start WebSocket service."""
        asyncio.create_task(self.market_data_broadcast())
        asyncio.create_task(self.order_updates_broadcast())
    
    async def market_data_broadcast(self):
        """Broadcast real-time market data."""
        while True:
            try:
                # Get market data from data service
                market_data = await self.get_market_data()
                await self.broadcast(json.dumps({
                    "type": "market_data",
                    "data": market_data
                }))
                await asyncio.sleep(1)  # Update every second
            except Exception as e:
                print(f"Market data broadcast error: {e}")
                await asyncio.sleep(5)
    
    async def order_updates_broadcast(self):
        """Broadcast order updates."""
        while True:
            try:
                # Get order updates from execution service
                order_updates = await self.get_order_updates()
                if order_updates:
                    await self.broadcast(json.dumps({
                        "type": "order_update",
                        "data": order_updates
                    }))
                await asyncio.sleep(0.5)  # Update every 500ms
            except Exception as e:
                print(f"Order updates broadcast error: {e}")
                await asyncio.sleep(5)
```

## 🎨 **UI/UX Features**

### **Real-time Updates**
- **Live Charts**: Real-time price charts with WebSocket updates
- **Portfolio Tracking**: Live P&L and position updates
- **Order Status**: Real-time order execution updates
- **Market Data**: Live market data streaming

### **Interactive Components**
- **Drag & Drop**: Portfolio rebalancing interface
- **Chart Interactions**: Zoom, pan, technical indicators
- **Quick Actions**: One-click trading buttons
- **Responsive Design**: Mobile-optimized trading interface

### **Professional Features**
- **Dark/Light Theme**: User preference toggle
- **Customizable Dashboard**: Drag-and-drop widgets
- **Advanced Charts**: Multiple chart types and overlays
- **Risk Management**: Real-time risk monitoring

## 🚀 **Deployment Strategy**

### **Docker Configuration**
```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8006

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8006"]
```

### **Service Integration**
- **API Gateway**: Routes requests to web portal
- **Microservices**: Integrates with all Bifrost services
- **WebSocket**: Real-time communication
- **Static Assets**: CDN integration for performance

---

**Last Updated**: December 2024  
**Status**: Ready for Implementation  
**Priority**: HIGH - Critical for User Experience
