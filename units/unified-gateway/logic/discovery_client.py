"""
Service Discovery Client
Finds Bridge services and maintains their tools in registry
"""

import asyncio
import httpx
import logging
import os
from typing import Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class ServiceDiscovery:
    """Service discovery client for bridge services"""
    
    def __init__(self):
        self.bridge_url = os.getenv("BRIDGE_URL", "http://lm-studio-bridge:3000")
        self.discovery_interval = int(os.getenv("DISCOVERY_INTERVAL", "30"))
        self.service_registry: Dict[str, Dict] = {}
        self.running = False
        
    async def start(self):
        """Start periodic service discovery"""
        self.running = True
        logger.info("Starting service discovery")
        
        # Start discovery loop
        asyncio.create_task(self._discovery_loop())
        
    async def stop(self):
        """Stop service discovery"""
        self.running = False
        logger.info("Stopping service discovery")
        
    async def _discovery_loop(self):
        """Periodic discovery loop"""
        while self.running:
            try:
                await self._discover_services()
                await asyncio.sleep(self.discovery_interval)
            except Exception as e:
                logger.error(f"Discovery loop error: {e}")
                await asyncio.sleep(self.discovery_interval)
                
    async def _discover_services(self):
        """Discover available services and their tools"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # Check bridge health
                health_response = await client.get(f"{self.bridge_url}/health")
                if health_response.status_code != 200:
                    self._remove_service("lm-studio-bridge")
                    return
                    
                # Get available tools
                tools_response = await client.get(f"{self.bridge_url}/mcp/tools")
                if tools_response.status_code == 200:
                    tools_data = tools_response.json()
                    self._update_service_registry("lm-studio-bridge", tools_data)
                    logger.debug(f"Updated registry for lm-studio-bridge")
                else:
                    self._remove_service("lm-studio-bridge")
                    
        except Exception as e:
            logger.warning(f"Failed to discover services: {e}")
            self._remove_service("lm-studio-bridge")
            
    def _update_service_registry(self, service_name: str, tools_data: Dict):
        """Update service registry with discovered tools"""
        self.service_registry[service_name] = {
            "url": self.bridge_url,
            "tools": tools_data,
            "last_seen": datetime.now(),
            "healthy": True
        }
        
    def _remove_service(self, service_name: str):
        """Remove service from registry"""
        if service_name in self.service_registry:
            del self.service_registry[service_name]
            logger.info(f"Removed {service_name} from registry")
            
    def get_service_for_tool(self, tool_name: str) -> Optional[str]:
        """Get service URL for a specific tool"""
        for service_info in self.service_registry.values():
            if service_info["healthy"]:
                tools = service_info.get("tools", {})
                if isinstance(tools, dict) and tool_name in tools:
                    return service_info["url"]
        return None
        
    def get_registry_status(self) -> Dict:
        """Get current registry status"""
        return {
            "services": len(self.service_registry),
            "healthy_services": len([s for s in self.service_registry.values() if s["healthy"]]),
            "last_discovery": datetime.now().isoformat()
        }
