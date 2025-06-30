"""
Health Endpoint
Aggregates service status and reports overall health
"""

import logging
from datetime import datetime
from typing import Dict, Any
from fastapi import APIRouter

logger = logging.getLogger(__name__)

class HealthManager:
    """Manages health status aggregation"""

    def __init__(self, discovery_client=None):
        self.discovery_client = discovery_client
        self.start_time = datetime.now()

    def get_health_status(self) -> Dict[str, Any]:
        """Get comprehensive health status for orchestration"""
        try:
            uptime = (datetime.now() - self.start_time).total_seconds()

            # Initialize health status
            health_status = {
                "status": "healthy",
                "service": "unified-gateway",
                "version": "1.0.0",
                "uptime_seconds": round(uptime, 2),
                "timestamp": datetime.now().isoformat(),
                "orchestration": {
                    "startup_complete": True,
                    "ready_for_traffic": True,
                    "dependencies_healthy": True
                },
                "components": {
                    "http_server": "healthy",
                    "auth_system": "healthy",
                    "rate_limiter": "healthy"
                },
                "dependencies": {},
                "metrics": {
                    "memory_usage_mb": 0,
                    "cpu_usage_percent": 0,
                    "active_connections": 0,
                    "requests_per_minute": 0
                }
            }

            # Check bridge dependency
            bridge_url = os.environ.get("BRIDGE_URL", "http://lm-studio-bridge:3000")
            try:
                import httpx
                with httpx.Client(timeout=5.0) as client:
                    bridge_response = client.get(f"{bridge_url}/health")
                    if bridge_response.status_code == 200:
                        bridge_data = bridge_response.json()
                        health_status["dependencies"]["lm_studio_bridge"] = {
                            "status": bridge_data.get("status", "unknown"),
                            "url": bridge_url,
                            "response_time_ms": round(bridge_response.elapsed.total_seconds() * 1000, 2),
                            "last_check": datetime.now().isoformat()
                        }
                        if bridge_data.get("status") != "healthy":
                            health_status["orchestration"]["dependencies_healthy"] = False
                    else:
                        health_status["dependencies"]["lm_studio_bridge"] = {
                            "status": "unhealthy",
                            "url": bridge_url,
                            "http_status": bridge_response.status_code,
                            "last_check": datetime.now().isoformat()
                        }
                        health_status["orchestration"]["dependencies_healthy"] = False
            except Exception as e:
                health_status["dependencies"]["lm_studio_bridge"] = {
                    "status": "error",
                    "url": bridge_url,
                    "error": str(e),
                    "last_check": datetime.now().isoformat()
                }
                health_status["orchestration"]["dependencies_healthy"] = False

            # Check discovery client status
            if self.discovery_client:
                try:
                    registry_status = self.discovery_client.get_registry_status()
                    service_count = registry_status.get("healthy_services", 0)
                    total_services = registry_status.get("services", 0)

                    health_status["components"]["discovery_client"] = {
                        "status": "healthy" if service_count > 0 else "no_services",
                        "total_services": total_services,
                        "healthy_services": service_count,
                        "last_discovery": datetime.now().isoformat()
                    }

                    health_status["services"] = {
                        "total": total_services,
                        "healthy": service_count
                    }
                except Exception as e:
                    health_status["components"]["discovery_client"] = {
                        "status": "error",
                        "error": str(e)
                    }
            else:
                health_status["components"]["discovery_client"] = {
                    "status": "not_initialized"
                }

            # Check authentication system
            auth_enabled = os.environ.get("AUTH_ENABLED", "true").lower() == "true"
            api_key = os.environ.get("API_KEY", "changeme")

            if auth_enabled:
                if api_key == "changeme":
                    health_status["components"]["auth_system"] = {
                        "status": "warning",
                        "message": "Using default API key - change for production"
                    }
                else:
                    health_status["components"]["auth_system"] = {
                        "status": "healthy",
                        "enabled": True
                    }
            else:
                health_status["components"]["auth_system"] = {
                    "status": "disabled",
                    "enabled": False
                }

            # Get resource metrics
            try:
                import psutil
                process = psutil.Process()
                health_status["metrics"]["memory_usage_mb"] = round(process.memory_info().rss / 1024 / 1024, 2)
                health_status["metrics"]["cpu_usage_percent"] = round(process.cpu_percent(), 2)
            except Exception as e:
                health_status["metrics"]["error"] = str(e)

            # Determine overall status
            component_statuses = []
            for comp in health_status["components"].values():
                if isinstance(comp, dict):
                    component_statuses.append(comp.get("status", "unknown"))
                else:
                    component_statuses.append(comp)

            if not health_status["orchestration"]["dependencies_healthy"]:
                health_status["status"] = "degraded"
            elif any(status in ["error", "unhealthy"] for status in component_statuses):
                health_status["status"] = "degraded"
            elif any(status in ["not_initialized", "starting"] for status in component_statuses):
                health_status["status"] = "starting"
                health_status["orchestration"]["ready_for_traffic"] = False

            # Mark readiness in shared state for orchestration
            import os
            shared_dir = os.environ.get("SHARED_STATE_DIR", "/shared")
            if health_status["status"] == "healthy" and health_status["orchestration"]["ready_for_traffic"]:
                try:
                    os.makedirs(shared_dir, exist_ok=True)
                    with open(f"{shared_dir}/gateway.ready", "w") as f:
                        f.write(f"ready_at={datetime.now().isoformat()}\n")
                        f.write(f"status={health_status['status']}\n")
                except:
                    pass  # Non-critical

            return health_status

        except Exception as e:
            logger.error(f"Health check error: {e}")
            return {
                "status": "unhealthy",
                "service": "unified-gateway",
                "version": "1.0.0",
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "orchestration": {
                    "startup_complete": False,
                    "ready_for_traffic": False,
                    "dependencies_healthy": False
                }
            }

# Global health manager instance
health_manager = HealthManager()

def create_health_router() -> APIRouter:
    """Create health router"""
    router = APIRouter()

    @router.get("/health")
    async def health_check():
        """Health check endpoint"""
        return health_manager.get_health_status()

    return router

def set_discovery_client(discovery_client):
    """Set discovery client for health manager"""
    health_manager.discovery_client = discovery_client
