/**
 * LLM Hub Control Center JavaScript
 * One-click fixes and service management
 */

class ControlCenter {
    constructor() {
        this.gatewayUrl = 'http://localhost:8080';
        this.bridgeUrl = 'http://localhost:3000';
        this.lmStudioUrl = 'http://localhost:1234';
        this.controlApiUrl = 'http://localhost:9000';

        this.init();
    }

    init() {
        // Auto-refresh status every 30 seconds
        this.refreshStatus();
        setInterval(() => this.refreshStatus(), 30000);
    }

    async refreshStatus() {
        const refreshBtn = document.getElementById('refresh-text');
        refreshBtn.innerHTML = '<div class="loading"></div> Checking...';

        try {
            await Promise.all([
                this.checkGatewayStatus(),
                this.checkBridgeStatus(),
                this.checkLMStudioStatus(),
                this.checkDockerStatus()
            ]);

            this.updateSystemStatus();
        } catch (error) {
            console.error('Status check failed:', error);
        } finally {
            refreshBtn.textContent = 'Refresh Status';
        }
    }

    async checkGatewayStatus() {
        try {
            const response = await fetch(`${this.gatewayUrl}/health`, { timeout: 5000 });
            const data = await response.json();

            document.getElementById('gateway-status').textContent =
                response.ok ? '✅ Healthy' : '❌ Unhealthy';
            document.getElementById('gateway-status').className =
                response.ok ? 'metric-value' : 'metric-value error';
        } catch (error) {
            document.getElementById('gateway-status').textContent = '❌ Offline';
            document.getElementById('gateway-status').className = 'metric-value error';
        }
    }

    async checkBridgeStatus() {
        try {
            const response = await fetch(`${this.bridgeUrl}/health`, { timeout: 5000 });
            const data = await response.json();

            document.getElementById('bridge-status').textContent =
                response.ok ? '✅ Healthy' : '❌ Unhealthy';
            document.getElementById('bridge-status').className =
                response.ok ? 'metric-value' : 'metric-value error';
        } catch (error) {
            document.getElementById('bridge-status').textContent = '❌ Offline';
            document.getElementById('bridge-status').className = 'metric-value error';
        }
    }

    async checkLMStudioStatus() {
        try {
            const response = await fetch(`${this.lmStudioUrl}/v1/models`, { timeout: 5000 });

            document.getElementById('lmstudio-status').textContent =
                response.ok ? '✅ Running' : '❌ Error';
            document.getElementById('lmstudio-status').className =
                response.ok ? 'metric-value' : 'metric-value error';
        } catch (error) {
            document.getElementById('lmstudio-status').textContent = '❌ Not Running';
            document.getElementById('lmstudio-status').className = 'metric-value error';
        }
    }

    async checkDockerStatus() {
        // Check if Docker containers are running by checking if services respond
        const gatewayOk = document.getElementById('gateway-status').textContent.includes('✅');
        const bridgeOk = document.getElementById('bridge-status').textContent.includes('✅');

        if (gatewayOk && bridgeOk) {
            document.getElementById('docker-status').textContent = '✅ Running';
            document.getElementById('docker-status').className = 'metric-value';
        } else {
            document.getElementById('docker-status').textContent = '❌ Issues';
            document.getElementById('docker-status').className = 'metric-value error';
        }
    }

    updateSystemStatus() {
        const statuses = [
            document.getElementById('gateway-status').textContent,
            document.getElementById('bridge-status').textContent,
            document.getElementById('lmstudio-status').textContent,
            document.getElementById('docker-status').textContent
        ];

        const allHealthy = statuses.every(status => status.includes('✅'));
        const systemStatusDot = document.getElementById('system-status');

        if (allHealthy) {
            systemStatusDot.className = 'status-dot status-healthy';
        } else {
            systemStatusDot.className = 'status-dot status-unhealthy';
        }
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        document.body.appendChild(notification);

        setTimeout(() => notification.classList.add('show'), 100);
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => document.body.removeChild(notification), 300);
        }, 3000);
    }

    async executeCommand(command, successMessage, errorMessage) {
        try {
            this.showNotification('Executing command...', 'info');

            // Call the control API
            const response = await fetch(`${this.controlApiUrl}/api/commands/${command}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                const result = await response.json();
                this.showNotification(result.message || successMessage, 'success');
            } else {
                throw new Error(`API call failed: ${response.statusText}`);
            }

            setTimeout(() => this.refreshStatus(), 1000);
        } catch (error) {
            console.error('Command execution failed:', error);
            this.showNotification(errorMessage, 'error');
        }
    }
}

// Initialize Control Center
const controlCenter = new ControlCenter();

// Global functions for button clicks
async function refreshStatus() {
    await controlCenter.refreshStatus();
}

async function startAllServices() {
    await controlCenter.executeCommand(
        'start-services',
        '✅ All services started successfully!',
        '❌ Failed to start services'
    );
}

async function restartAllServices() {
    await controlCenter.executeCommand(
        'restart-services',
        '✅ All services restarted successfully!',
        '❌ Failed to restart services'
    );
}

async function stopAllServices() {
    if (confirm('Are you sure you want to stop all services?')) {
        await controlCenter.executeCommand(
            'stop-services',
            '✅ All services stopped successfully!',
            '❌ Failed to stop services'
        );
    }
}

async function viewLogs() {
    window.open('logs.html', '_blank');
}

async function fixDockerIssues() {
    await controlCenter.executeCommand(
        'fix-docker',
        '✅ Docker issues fixed!',
        '❌ Failed to fix Docker issues'
    );
}

async function fixLMStudioConnection() {
    await controlCenter.executeCommand(
        'fix-lmstudio',
        '✅ LM Studio connection fixed!',
        '❌ Failed to fix LM Studio connection'
    );
}

async function fixPortConflicts() {
    await controlCenter.executeCommand(
        'fix-ports',
        '✅ Port conflicts resolved!',
        '❌ Failed to resolve port conflicts'
    );
}

async function resetConfiguration() {
    if (confirm('This will reset all configuration to defaults. Continue?')) {
        await controlCenter.executeCommand(
            'reset-config',
            '✅ Configuration reset successfully!',
            '❌ Failed to reset configuration'
        );
    }
}

function openDashboard() {
    window.open('../dashboard/index.html', '_blank');
}

function openDocumentation() {
    window.open('../../docs/README.md', '_blank');
}

async function runDiagnostics() {
    await controlCenter.executeCommand(
        'run-diagnostics',
        '✅ Diagnostics completed! Check logs for details.',
        '❌ Diagnostics failed'
    );
}

async function setupAutostart() {
    await controlCenter.executeCommand(
        'setup-autostart',
        '✅ Autostart configured successfully!',
        '❌ Failed to setup autostart'
    );
}
