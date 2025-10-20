/**
 * Control Center JavaScript
 * Handles real-time updates, service management, and UI interactions
 */

class ControlCenter {
    constructor() {
        this.ws = null;
        this.reconnectInterval = null;
        this.updateInterval = null;
        this.isConnected = false;
        
        this.init();
    }
    
    init() {
        this.connectWebSocket();
        this.startPeriodicUpdates();
        this.setupEventListeners();
        this.updateCurrentTime();
    }
    
    connectWebSocket() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws`;
        
        try {
            this.ws = new WebSocket(wsUrl);
            
            this.ws.onopen = () => {
                console.log('WebSocket connected');
                this.updateConnectionStatus(true);
                this.clearReconnectInterval();
            };
            
            this.ws.onmessage = (event) => {
                const data = JSON.parse(event.data);
                this.handleWebSocketMessage(data);
            };
            
            this.ws.onclose = () => {
                console.log('WebSocket disconnected');
                this.updateConnectionStatus(false);
                this.scheduleReconnect();
            };
            
            this.ws.onerror = (error) => {
                console.error('WebSocket error:', error);
                this.updateConnectionStatus(false);
            };
            
        } catch (error) {
            console.error('Failed to connect WebSocket:', error);
            this.scheduleReconnect();
        }
    }
    
    handleWebSocketMessage(data) {
        switch (data.type) {
            case 'health_update':
                this.updateServiceStatuses(data.services);
                break;
            case 'service_action':
                this.handleServiceAction(data);
                break;
            default:
                console.log('Unknown message type:', data.type);
        }
    }
    
    updateServiceStatuses(services) {
        for (const [serviceName, health] of Object.entries(services)) {
            this.updateServiceStatus(serviceName, health);
        }
    }
    
    updateServiceStatus(serviceName, health) {
        // Update status badge
        const statusElement = document.getElementById(`status-${serviceName}`);
        if (statusElement) {
            const badgeClass = this.getStatusBadgeClass(health.status);
            statusElement.className = `badge ${badgeClass}`;
            statusElement.textContent = health.status;
        }
        
        // Update health indicators if present
        const responseTimeElement = document.getElementById('response-time');
        if (responseTimeElement && serviceName === this.getCurrentServiceName()) {
            responseTimeElement.textContent = health.response_time ? 
                `${health.response_time.toFixed(2)}s` : 'N/A';
        }
        
        const lastCheckElement = document.getElementById('last-check');
        if (lastCheckElement && serviceName === this.getCurrentServiceName()) {
            lastCheckElement.textContent = health.last_check ? 
                new Date(health.last_check).toLocaleString() : 'Never';
        }
        
        const uptimeElement = document.getElementById('uptime');
        if (uptimeElement && serviceName === this.getCurrentServiceName()) {
            uptimeElement.textContent = health.uptime ? 
                `${health.uptime.toFixed(1)}s` : 'N/A';
        }
        
        const cpuElement = document.getElementById('cpu-usage');
        if (cpuElement && serviceName === this.getCurrentServiceName()) {
            cpuElement.textContent = health.cpu_usage ? 
                `${health.cpu_usage.toFixed(1)}%` : 'N/A';
        }
        
        const memoryElement = document.getElementById('memory-usage');
        if (memoryElement && serviceName === this.getCurrentServiceName()) {
            memoryElement.textContent = health.memory_usage ? 
                `${health.memory_usage.toFixed(1)} MB` : 'N/A';
        }
    }
    
    getStatusBadgeClass(status) {
        switch (status) {
            case 'running':
                return 'bg-success';
            case 'error':
                return 'bg-danger';
            case 'stopped':
                return 'bg-warning';
            default:
                return 'bg-secondary';
        }
    }
    
    getCurrentServiceName() {
        const path = window.location.pathname;
        const match = path.match(/\/service\/([^\/]+)/);
        return match ? match[1] : null;
    }
    
    updateConnectionStatus(connected) {
        const statusElement = document.getElementById('connection-status');
        const textElement = document.getElementById('connection-text');
        
        if (statusElement && textElement) {
            if (connected) {
                statusElement.className = 'fas fa-circle text-success me-1';
                textElement.textContent = 'Connected';
                this.isConnected = true;
            } else {
                statusElement.className = 'fas fa-circle text-danger me-1';
                textElement.textContent = 'Disconnected';
                this.isConnected = false;
            }
        }
    }
    
    scheduleReconnect() {
        if (!this.reconnectInterval) {
            this.reconnectInterval = setInterval(() => {
                this.connectWebSocket();
            }, 5000);
        }
    }
    
    clearReconnectInterval() {
        if (this.reconnectInterval) {
            clearInterval(this.reconnectInterval);
            this.reconnectInterval = null;
        }
    }
    
    startPeriodicUpdates() {
        this.updateInterval = setInterval(() => {
            if (!this.isConnected) {
                this.fetchSystemStatus();
            }
        }, 30000); // Fallback every 30 seconds if WebSocket is not connected
    }
    
    async fetchSystemStatus() {
        try {
            const response = await fetch('/api/health/');
            const data = await response.json();
            
            // Update overview if on dashboard
            if (window.location.pathname === '/') {
                this.updateSystemOverview(data);
            }
        } catch (error) {
            console.error('Failed to fetch system status:', error);
        }
    }
    
    updateSystemOverview(overview) {
        // Update overview cards if present
        const totalElement = document.querySelector('.text-primary');
        const runningElement = document.querySelector('.text-success');
        const stoppedElement = document.querySelector('.text-warning');
        const errorElement = document.querySelector('.text-danger');
        
        if (totalElement) totalElement.textContent = overview.total_services;
        if (runningElement) runningElement.textContent = overview.running_services;
        if (stoppedElement) stoppedElement.textContent = overview.stopped_services;
        if (errorElement) errorElement.textContent = overview.error_services;
    }
    
    setupEventListeners() {
        // Service management buttons
        document.addEventListener('click', (event) => {
            if (event.target.closest('[onclick*="startService"]')) {
                const serviceName = this.extractServiceName(event.target);
                this.startService(serviceName);
            } else if (event.target.closest('[onclick*="stopService"]')) {
                const serviceName = this.extractServiceName(event.target);
                this.stopService(serviceName);
            } else if (event.target.closest('[onclick*="restartService"]')) {
                const serviceName = this.extractServiceName(event.target);
                this.restartService(serviceName);
            }
        });
    }
    
    extractServiceName(element) {
        const onclick = element.getAttribute('onclick') || 
                       element.closest('[onclick]')?.getAttribute('onclick');
        if (onclick) {
            const match = onclick.match(/['"]([^'"]+)['"]/);
            return match ? match[1] : null;
        }
        return null;
    }
    
    async startService(serviceName) {
        await this.performServiceAction(serviceName, 'start');
    }
    
    async stopService(serviceName) {
        await this.performServiceAction(serviceName, 'stop');
    }
    
    async restartService(serviceName) {
        await this.performServiceAction(serviceName, 'restart');
    }
    
    async performServiceAction(serviceName, action) {
        try {
            this.showLoadingState(serviceName, action);
            
            const response = await fetch(`/api/services/${serviceName}/${action}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.showToast('success', result.message);
                // Refresh page after a short delay to show updated status
                setTimeout(() => {
                    if (window.location.pathname.includes('/service/')) {
                        window.location.reload();
                    }
                }, 2000);
            } else {
                this.showToast('error', result.message);
            }
            
        } catch (error) {
            this.showToast('error', `Failed to ${action} service: ${error.message}`);
        } finally {
            this.hideLoadingState(serviceName, action);
        }
    }
    
    showLoadingState(serviceName, action) {
        const button = document.getElementById(`${action}-${serviceName}`) || 
                     document.getElementById(`${action}-btn`);
        if (button) {
            button.disabled = true;
            button.innerHTML = `<i class="fas fa-spinner fa-spin me-1"></i>${action.charAt(0).toUpperCase() + action.slice(1)}ing...`;
        }
    }
    
    hideLoadingState(serviceName, action) {
        const button = document.getElementById(`${action}-${serviceName}`) || 
                     document.getElementById(`${action}-btn`);
        if (button) {
            button.disabled = false;
            const icon = action === 'start' ? 'play' : action === 'stop' ? 'stop' : 'redo';
            button.innerHTML = `<i class="fas fa-${icon} me-1"></i>${action.charAt(0).toUpperCase() + action.slice(1)}`;
        }
    }
    
    showToast(type, message) {
        const toast = document.getElementById('toast');
        const toastMessage = document.getElementById('toast-message');
        
        if (toast && toastMessage) {
            toastMessage.textContent = message;
            
            // Update toast header based on type
            const toastHeader = toast.querySelector('.toast-header');
            if (toastHeader) {
                const icon = toastHeader.querySelector('i');
                if (icon) {
                    icon.className = type === 'success' ? 'fas fa-check-circle me-2' : 
                                   type === 'error' ? 'fas fa-exclamation-circle me-2' : 
                                   'fas fa-info-circle me-2';
                }
            }
            
            const toastInstance = new bootstrap.Toast(toast);
            toastInstance.show();
        }
    }
    
    updateCurrentTime() {
        const timeElement = document.getElementById('current-time');
        if (timeElement) {
            const now = new Date();
            timeElement.textContent = now.toLocaleString();
        }
    }
    
    // Utility functions for global access
    openService(url) {
        window.open(url, '_blank');
    }
    
    openDocs(url) {
        window.open(url, '_blank');
    }
    
    viewServiceDetails(serviceName) {
        window.location.href = `/service/${serviceName}`;
    }
    
    refreshLogs() {
        window.location.reload();
    }
}

// Initialize Control Center when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.controlCenter = new ControlCenter();
    
    // Update time every second
    setInterval(() => {
        window.controlCenter.updateCurrentTime();
    }, 1000);
});

// Global functions for backward compatibility
function openService(url) {
    window.controlCenter.openService(url);
}

function openDocs(url) {
    window.controlCenter.openDocs(url);
}

function viewServiceDetails(serviceName) {
    window.controlCenter.viewServiceDetails(serviceName);
}

function startService(serviceName) {
    window.controlCenter.startService(serviceName);
}

function stopService(serviceName) {
    window.controlCenter.stopService(serviceName);
}

function restartService(serviceName) {
    window.controlCenter.restartService(serviceName);
}

function refreshLogs() {
    window.controlCenter.refreshLogs();
}
