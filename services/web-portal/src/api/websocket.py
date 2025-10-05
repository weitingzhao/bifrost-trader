"""
WebSocket API endpoints
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from ..services.websocket_service import WebSocketService
import json

router = APIRouter()
websocket_service = WebSocketService()

@router.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    """Main WebSocket endpoint for real-time updates."""
    await websocket_service.handle_websocket(websocket)

@router.websocket("/market-data")
async def market_data_websocket(websocket: WebSocket):
    """WebSocket endpoint specifically for market data."""
    await websocket_service.connect(websocket)
    try:
        while True:
            # Send market data updates
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("type") == "ping":
                await websocket_service.send_personal_message(json.dumps({
                    "type": "pong",
                    "timestamp": "2024-01-01T00:00:00Z"
                }), websocket)
                
    except WebSocketDisconnect:
        websocket_service.disconnect(websocket)
    except Exception as e:
        print(f"Market data WebSocket error: {e}")
        websocket_service.disconnect(websocket)

@router.websocket("/trading")
async def trading_websocket(websocket: WebSocket):
    """WebSocket endpoint for trading updates."""
    await websocket_service.connect(websocket)
    try:
        while True:
            # Send trading updates
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("type") == "ping":
                await websocket_service.send_personal_message(json.dumps({
                    "type": "pong",
                    "timestamp": "2024-01-01T00:00:00Z"
                }), websocket)
                
    except WebSocketDisconnect:
        websocket_service.disconnect(websocket)
    except Exception as e:
        print(f"Trading WebSocket error: {e}")
        websocket_service.disconnect(websocket)
