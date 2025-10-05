"""
Web Portal Service Documentation

This service provides the web interface for the Bifrost Trader platform.
"""

# Web Portal Service
# Port: 8006
# Purpose: Web interface and real-time updates

# API Endpoints:
# GET / - Dashboard page
# GET /trading - Live trading page
# GET /backtesting - Backtesting page
# GET /portfolio - Portfolio management page
# GET /analytics - Analytics page
# GET /research - Research page
# GET /settings - Settings page
# GET /health - Health check

# API Routes:
# /api/dashboard/* - Dashboard data endpoints
# /api/trading/* - Trading operations endpoints
# /api/portfolio/* - Portfolio management endpoints
# /ws/* - WebSocket endpoints for real-time updates

# Dependencies:
# - FastAPI for web framework
# - WebSockets for real-time communication
# - Jinja2 for templating
# - Chart.js for data visualization

# Integration:
# - Connects to all Bifrost microservices
# - Provides unified web interface
# - Real-time data streaming via WebSockets
# - Professional trading interface
