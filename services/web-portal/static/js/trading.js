// Trading functionality for Bifrost Trader Web Portal

class TradingInterface {
    constructor() {
        this.websocket = null;
        this.isConnected = false;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.connectWebSocket();
        this.loadInitialData();
    }

    setupEventListeners() {
        // Quick trade form
        const quickTradeForm = document.getElementById('quick-trade-form');
        if (quickTradeForm) {
            quickTradeForm.addEventListener('submit', this.handleQuickTrade.bind(this));
        }

        // Order cancellation
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('cancel-order')) {
                this.cancelOrder(e.target.dataset.orderId);
            }
        });

        // Chart timeframe buttons
        document.addEventListener('click', (e) => {
            if (e.target.dataset.timeframe) {
                this.changeTimeframe(e.target.dataset.timeframe);
            }
        });
    }

    async connectWebSocket() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws/trading`;
        
        try {
            this.websocket = new WebSocket(wsUrl);
            
            this.websocket.onopen = () => {
                console.log('Trading WebSocket connected');
                this.isConnected = true;
                this.updateConnectionStatus(true);
            };
            
            this.websocket.onmessage = (event) => {
                const message = JSON.parse(event.data);
                this.handleWebSocketMessage(message);
            };
            
            this.websocket.onclose = () => {
                console.log('Trading WebSocket disconnected');
                this.isConnected = false;
                this.updateConnectionStatus(false);
                // Reconnect after 5 seconds
                setTimeout(() => this.connectWebSocket(), 5000);
            };
            
            this.websocket.onerror = (error) => {
                console.error('Trading WebSocket error:', error);
                this.isConnected = false;
                this.updateConnectionStatus(false);
            };
        } catch (error) {
            console.error('Failed to connect WebSocket:', error);
        }
    }

    handleWebSocketMessage(message) {
        switch (message.type) {
            case 'market_data':
                this.updateMarketData(message.data);
                break;
            case 'order_update':
                this.updateOrderStatus(message.data);
                break;
            case 'portfolio_update':
                this.updatePortfolioData(message.data);
                break;
            case 'pong':
                // Handle ping response
                break;
        }
    }

    async handleQuickTrade(event) {
        event.preventDefault();
        
        const formData = new FormData(event.target);
        const orderData = {
            symbol: formData.get('symbol'),
            side: formData.get('side'),
            quantity: parseInt(formData.get('quantity')),
            order_type: formData.get('order_type'),
            price: formData.get('price') ? parseFloat(formData.get('price')) : null
        };

        try {
            const response = await fetch('/api/trading/orders', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(orderData)
            });

            const result = await response.json();
            
            if (response.ok) {
                this.showNotification('Order placed successfully', 'success');
                this.loadActiveOrders();
            } else {
                this.showNotification(result.error || 'Failed to place order', 'error');
            }
        } catch (error) {
            console.error('Error placing order:', error);
            this.showNotification('Failed to place order', 'error');
        }
    }

    async cancelOrder(orderId) {
        try {
            const response = await fetch(`/api/trading/orders/${orderId}`, {
                method: 'DELETE'
            });

            const result = await response.json();
            
            if (response.ok) {
                this.showNotification('Order cancelled successfully', 'success');
                this.loadActiveOrders();
            } else {
                this.showNotification(result.error || 'Failed to cancel order', 'error');
            }
        } catch (error) {
            console.error('Error cancelling order:', error);
            this.showNotification('Failed to cancel order', 'error');
        }
    }

    async loadInitialData() {
        await Promise.all([
            this.loadAccountSummary(),
            this.loadActiveOrders(),
            this.loadMarketData()
        ]);
    }

    async loadAccountSummary() {
        try {
            const response = await fetch('/api/trading/account-summary');
            const data = await response.json();
            
            if (response.ok) {
                this.updateAccountSummary(data);
            }
        } catch (error) {
            console.error('Error loading account summary:', error);
        }
    }

    async loadActiveOrders() {
        try {
            const response = await fetch('/api/trading/active-orders');
            const data = await response.json();
            
            if (response.ok) {
                this.updateActiveOrders(data.orders);
            }
        } catch (error) {
            console.error('Error loading active orders:', error);
        }
    }

    async loadMarketData() {
        try {
            const response = await fetch('/api/trading/market-data');
            const data = await response.json();
            
            if (response.ok) {
                this.updateMarketData(data);
            }
        } catch (error) {
            console.error('Error loading market data:', error);
        }
    }

    updateAccountSummary(data) {
        const elements = {
            'buying-power': data.buying_power,
            'cash-balance': data.cash_balance,
            'equity': data.equity
        };

        Object.entries(elements).forEach(([id, value]) => {
            const element = document.getElementById(id);
            if (element) {
                element.textContent = `$${value.toLocaleString('en-US', { minimumFractionDigits: 2 })}`;
            }
        });
    }

    updateActiveOrders(orders) {
        const tbody = document.querySelector('#orders-table tbody');
        if (!tbody) return;

        tbody.innerHTML = '';

        if (orders.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7" class="text-center text-muted">No active orders</td></tr>';
            return;
        }

        orders.forEach(order => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${order.symbol}</td>
                <td><span class="badge badge-sm bg-gradient-${order.side === 'BUY' ? 'success' : 'danger'}">${order.side}</span></td>
                <td>${order.quantity}</td>
                <td>${order.price ? `$${order.price.toFixed(2)}` : 'Market'}</td>
                <td><span class="badge badge-sm bg-gradient-${this.getStatusColor(order.status)}">${order.status}</span></td>
                <td>${new Date(order.timestamp).toLocaleTimeString()}</td>
                <td>
                    ${order.status === 'PENDING' ? `<button class="btn btn-sm btn-outline-danger cancel-order" data-order-id="${order.order_id}">Cancel</button>` : ''}
                </td>
            `;
            tbody.appendChild(row);
        });
    }

    updateMarketData(data) {
        Object.entries(data).forEach(([symbol, quote]) => {
            const priceElement = document.getElementById(`price-${symbol}`);
            if (priceElement) {
                priceElement.textContent = `$${quote.price.toFixed(2)}`;
                priceElement.className = `price-${quote.change >= 0 ? 'positive' : 'negative'}`;
            }
        });
    }

    updateOrderStatus(data) {
        // Update order status in real-time
        console.log('Order update:', data);
        this.loadActiveOrders(); // Refresh orders table
    }

    updatePortfolioData(data) {
        // Update portfolio data in real-time
        console.log('Portfolio update:', data);
        this.loadAccountSummary(); // Refresh account summary
    }

    updateConnectionStatus(connected) {
        const indicator = document.getElementById('connection-status');
        if (indicator) {
            indicator.className = `badge badge-sm bg-gradient-${connected ? 'success' : 'danger'}`;
            indicator.textContent = connected ? 'Connected' : 'Disconnected';
        }
    }

    getStatusColor(status) {
        const colors = {
            'FILLED': 'success',
            'PENDING': 'warning',
            'CANCELLED': 'secondary',
            'REJECTED': 'danger'
        };
        return colors[status] || 'secondary';
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        document.body.appendChild(notification);

        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 5000);
    }

    changeTimeframe(timeframe) {
        // Update active button
        document.querySelectorAll('[data-timeframe]').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-timeframe="${timeframe}"]`).classList.add('active');

        // Update chart
        this.updateChart(timeframe);
    }

    updateChart(timeframe) {
        // Update chart based on timeframe
        console.log(`Updating chart for timeframe: ${timeframe}`);
        // Implementation would depend on chart library being used
    }
}

// Initialize trading interface when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    if (document.querySelector('.trading-interface')) {
        window.tradingInterface = new TradingInterface();
    }
});
