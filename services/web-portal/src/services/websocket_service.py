"""
WebSocket Service

Handles real-time WebSocket connections and data broadcasting.
"""

import asyncio
import json
from datetime import datetime
from typing import Any, Dict, List, Set

import httpx
from fastapi import WebSocket, WebSocketDisconnect


class WebSocketService:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.data_service_url = "http://data-service:8001"
        self.execution_service_url = "http://execution-service:8004"
        self.portfolio_service_url = "http://portfolio-service:8002"
        self.running = False

    async def connect(self, websocket: WebSocket):
        """Accept WebSocket connection."""
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"WebSocket connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        """Remove WebSocket connection."""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        print(
            f"WebSocket disconnected. Total connections: {len(self.active_connections)}"
        )

    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Send message to specific WebSocket."""
        try:
            await websocket.send_text(message)
        except Exception as e:
            print(f"Error sending personal message: {e}")
            self.disconnect(websocket)

    async def broadcast(self, message: str):
        """Broadcast message to all connected clients."""
        if not self.active_connections:
            return

        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                print(f"Error broadcasting to connection: {e}")
                disconnected.append(connection)

        # Remove broken connections
        for connection in disconnected:
            self.disconnect(connection)

    async def start(self):
        """Start WebSocket service."""
        if self.running:
            return

        self.running = True
        print("Starting WebSocket service...")

        # Start background tasks
        asyncio.create_task(self.market_data_broadcast())
        asyncio.create_task(self.order_updates_broadcast())
        asyncio.create_task(self.portfolio_updates_broadcast())

    async def stop(self):
        """Stop WebSocket service."""
        self.running = False
        print("Stopping WebSocket service...")

    async def market_data_broadcast(self):
        """Broadcast real-time market data."""
        while self.running:
            try:
                if self.active_connections:
                    market_data = await self._get_market_data()
                    if market_data:
                        await self.broadcast(
                            json.dumps(
                                {
                                    "type": "market_data",
                                    "data": market_data,
                                    "timestamp": datetime.now().isoformat(),
                                }
                            )
                        )
                await asyncio.sleep(1)  # Update every second
            except Exception as e:
                print(f"Market data broadcast error: {e}")
                await asyncio.sleep(5)

    async def order_updates_broadcast(self):
        """Broadcast order updates."""
        while self.running:
            try:
                if self.active_connections:
                    order_updates = await self._get_order_updates()
                    if order_updates:
                        await self.broadcast(
                            json.dumps(
                                {
                                    "type": "order_update",
                                    "data": order_updates,
                                    "timestamp": datetime.now().isoformat(),
                                }
                            )
                        )
                await asyncio.sleep(0.5)  # Update every 500ms
            except Exception as e:
                print(f"Order updates broadcast error: {e}")
                await asyncio.sleep(5)

    async def portfolio_updates_broadcast(self):
        """Broadcast portfolio updates."""
        while self.running:
            try:
                if self.active_connections:
                    portfolio_updates = await self._get_portfolio_updates()
                    if portfolio_updates:
                        await self.broadcast(
                            json.dumps(
                                {
                                    "type": "portfolio_update",
                                    "data": portfolio_updates,
                                    "timestamp": datetime.now().isoformat(),
                                }
                            )
                        )
                await asyncio.sleep(2)  # Update every 2 seconds
            except Exception as e:
                print(f"Portfolio updates broadcast error: {e}")
                await asyncio.sleep(5)

    async def _get_market_data(self) -> Dict[str, Any]:
        """Get market data from data service."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.data_service_url}/api/market/quotes"
                )
                if response.status_code == 200:
                    return response.json()
        except Exception as e:
            print(f"Market data fetch error: {e}")

        # Return default data
        return {
            "AAPL": {
                "price": 175.50 + (asyncio.get_event_loop().time() % 10 - 5) * 0.1,
                "change": 2.25,
                "change_percent": 1.30,
                "volume": 45000000,
                "bid": 175.45,
                "ask": 175.55,
            }
        }

    async def _get_order_updates(self) -> List[Dict[str, Any]]:
        """Get order updates from execution service."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.execution_service_url}/api/execution/orders/recent"
                )
                if response.status_code == 200:
                    return response.json()
        except Exception as e:
            print(f"Order updates fetch error: {e}")

        return []

    async def _get_portfolio_updates(self) -> Dict[str, Any]:
        """Get portfolio updates from portfolio service."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.portfolio_service_url}/api/portfolio/summary"
                )
                if response.status_code == 200:
                    return response.json()
        except Exception as e:
            print(f"Portfolio updates fetch error: {e}")

        return {}

    async def handle_websocket(self, websocket: WebSocket):
        """Handle WebSocket connection."""
        await self.connect(websocket)
        try:
            while True:
                # Wait for messages from client
                data = await websocket.receive_text()
                message = json.loads(data)

                # Handle different message types
                if message.get("type") == "ping":
                    await self.send_personal_message(
                        json.dumps(
                            {"type": "pong", "timestamp": datetime.now().isoformat()}
                        ),
                        websocket,
                    )
                elif message.get("type") == "subscribe":
                    # Handle subscription requests
                    await self._handle_subscription(message, websocket)
                elif message.get("type") == "unsubscribe":
                    # Handle unsubscription requests
                    await self._handle_unsubscription(message, websocket)

        except WebSocketDisconnect:
            self.disconnect(websocket)
        except Exception as e:
            print(f"WebSocket error: {e}")
            self.disconnect(websocket)

    async def _handle_subscription(self, message: Dict[str, Any], websocket: WebSocket):
        """Handle subscription requests."""
        subscription_type = message.get("data", {}).get("type")
        if subscription_type == "market_data":
            # Send current market data
            market_data = await self._get_market_data()
            await self.send_personal_message(
                json.dumps(
                    {
                        "type": "market_data",
                        "data": market_data,
                        "timestamp": datetime.now().isoformat(),
                    }
                ),
                websocket,
            )
        elif subscription_type == "portfolio":
            # Send current portfolio data
            portfolio_data = await self._get_portfolio_updates()
            await self.send_personal_message(
                json.dumps(
                    {
                        "type": "portfolio_update",
                        "data": portfolio_data,
                        "timestamp": datetime.now().isoformat(),
                    }
                ),
                websocket,
            )

    async def _handle_unsubscription(
        self, message: Dict[str, Any], websocket: WebSocket
    ):
        """Handle unsubscription requests."""
        # For now, just acknowledge the unsubscription
        await self.send_personal_message(
            json.dumps(
                {
                    "type": "unsubscribed",
                    "data": message.get("data"),
                    "timestamp": datetime.now().isoformat(),
                }
            ),
            websocket,
        )
