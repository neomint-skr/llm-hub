"""
Request Router
Routes tool calls to correct backend services with load balancing
"""

import httpx
import logging
from typing import Dict, Optional, Any
from .discovery_client import ServiceDiscovery

logger = logging.getLogger(__name__)

class RequestRouter:
    """Request router for tool calls"""
    
    def __init__(self, discovery: ServiceDiscovery):
        self.discovery = discovery
        self.round_robin_counters: Dict[str, int] = {}
        
    async def route_tool_request(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Route tool request to appropriate service"""
        try:
            # Find service for tool
            service_url = self.discovery.get_service_for_tool(tool_name)
            if not service_url:
                return {
                    "error": f"No service available for tool: {tool_name}",
                    "status": "service_not_found"
                }
            
            # Forward request to service
            return await self._forward_request(service_url, tool_name, parameters)
            
        except Exception as e:
            logger.error(f"Routing error for tool {tool_name}: {e}")
            return {
                "error": f"Routing failed: {str(e)}",
                "status": "routing_error"
            }
    
    async def _forward_request(self, service_url: str, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Forward request to backend service"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                # Construct target URL
                target_url = f"{service_url}/mcp/tools/{tool_name}"
                
                # Forward request with headers
                response = await client.post(
                    target_url,
                    json={"parameters": parameters},
                    headers={
                        "Content-Type": "application/json",
                        "User-Agent": "unified-gateway/1.0.0"
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return {
                        "result": result,
                        "service": service_url,
                        "status": "success"
                    }
                else:
                    return {
                        "error": f"Service returned {response.status_code}",
                        "service": service_url,
                        "status": "service_error"
                    }
                    
        except httpx.TimeoutException:
            logger.warning(f"Timeout forwarding to {service_url}")
            return {
                "error": "Service timeout",
                "service": service_url,
                "status": "timeout"
            }
        except Exception as e:
            logger.error(f"Forward error to {service_url}: {e}")
            return {
                "error": f"Forward failed: {str(e)}",
                "service": service_url,
                "status": "forward_error"
            }
    
    def _get_next_service(self, services: list) -> str:
        """Round-robin load balancing"""
        if not services:
            raise ValueError("No services available")
            
        service_key = ",".join(sorted(services))
        counter = self.round_robin_counters.get(service_key, 0)
        selected_service = services[counter % len(services)]
        self.round_robin_counters[service_key] = counter + 1
        
        return selected_service
    
    def get_routing_stats(self) -> Dict[str, Any]:
        """Get routing statistics"""
        return {
            "active_routes": len(self.round_robin_counters),
            "discovery_status": self.discovery.get_registry_status()
        }
