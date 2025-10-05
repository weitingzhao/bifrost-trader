#!/usr/bin/env python3
"""
Test script for Bifrost Trader Web Portal Service
"""

import asyncio
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

async def test_services():
    """Test the web portal services."""
    print("🧪 Testing Bifrost Trader Web Portal Services...")
    
    try:
        # Test dashboard service
        from services.dashboard_service import DashboardService
        dashboard_service = DashboardService()
        print("✅ Dashboard Service imported successfully")
        
        # Test trading service
        from services.trading_service import TradingService
        trading_service = TradingService()
        print("✅ Trading Service imported successfully")
        
        # Test WebSocket service
        from services.websocket_service import WebSocketService
        websocket_service = WebSocketService()
        print("✅ WebSocket Service imported successfully")
        
        # Test main app
        from main import app
        print("✅ FastAPI App imported successfully")
        
        print("\n🎉 All services imported successfully!")
        print("📊 Web Portal Service is ready to run on port 8006")
        
    except Exception as e:
        print(f"❌ Error testing services: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = asyncio.run(test_services())
    sys.exit(0 if success else 1)
