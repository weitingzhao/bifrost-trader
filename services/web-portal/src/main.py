"""
Bifrost Trader Web Portal Service

A modern FastAPI-based web portal for the Bifrost Trader microservices platform.
Provides real-time trading interface, portfolio management, and analytics.
"""

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import asyncio
import os
from contextlib import asynccontextmanager
from typing import Dict, List

from .services.dashboard_service import DashboardService
from .services.trading_service import TradingService
from .services.websocket_service import WebSocketService
from .api import dashboard, trading, portfolio, websocket
from .models.dashboard import DashboardData
from .models.trading import TradingData

# Service instances
dashboard_service = DashboardService()
trading_service = TradingService()
websocket_service = WebSocketService()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Start WebSocket service
    asyncio.create_task(websocket_service.start())
    print("🚀 Web Portal Service Started")
    yield
    # Cleanup
    await websocket_service.stop()
    print("🛑 Web Portal Service Stopped")

# Create FastAPI app
app = FastAPI(
    title="Bifrost Trader Web Portal",
    version="1.0.0",
    description="Modern trading platform web interface",
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

# Include API routers
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])
app.include_router(trading.router, prefix="/api/trading", tags=["trading"])
app.include_router(portfolio.router, prefix="/api/portfolio", tags=["portfolio"])
app.include_router(websocket.router, prefix="/ws", tags=["websocket"])

# Template routes
@app.get("/", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    """Main dashboard page."""
    try:
        return templates.TemplateResponse("simple_dashboard.html", {
            "request": request
        })
    except Exception as e:
        print(f"Dashboard error: {e}")
        return HTMLResponse(content="<h1>Bifrost Trader Dashboard</h1><p>Service is running on port 8006</p>")

@app.get("/trading", response_class=HTMLResponse)
async def trading_page(request: Request):
    """Live trading page."""
    try:
        trading_data = await trading_service.get_trading_data()
        return templates.TemplateResponse("pages/trading/live.html", {
            "request": request,
            "trading_data": trading_data
        })
    except Exception as e:
        print(f"Trading page error: {e}")
        return templates.TemplateResponse("pages/trading/live.html", {
            "request": request,
            "trading_data": None
        })

@app.get("/backtesting", response_class=HTMLResponse)
async def backtesting_page(request: Request):
    """Backtesting page."""
    return templates.TemplateResponse("pages/trading/backtesting.html", {
        "request": request
    })

@app.get("/portfolio", response_class=HTMLResponse)
async def portfolio_page(request: Request):
    """Portfolio management page."""
    return templates.TemplateResponse("pages/portfolio/overview.html", {
        "request": request
    })

@app.get("/analytics", response_class=HTMLResponse)
async def analytics_page(request: Request):
    """Analytics page."""
    return templates.TemplateResponse("pages/analytics/market.html", {
        "request": request
    })

@app.get("/research", response_class=HTMLResponse)
async def research_page(request: Request):
    """Research page."""
    return templates.TemplateResponse("pages/research/screening.html", {
        "request": request
    })

@app.get("/settings", response_class=HTMLResponse)
async def settings_page(request: Request):
    """Settings page."""
    return templates.TemplateResponse("pages/settings/account.html", {
        "request": request
    })

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "web-portal",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8006, reload=True)
