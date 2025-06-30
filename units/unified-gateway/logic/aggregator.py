"""
Response Aggregator
Handles multi-service responses with error consolidation
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class ResponseAggregator:
    """Aggregates responses from multiple services"""
    
    def __init__(self):
        self.timeout = 30.0  # 30 second timeout
        
    async def aggregate_responses(self, service_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Aggregate responses from multiple service calls"""
        if not service_calls:
            return {
                "error": "No service calls provided",
                "status": "no_calls"
            }
        
        if len(service_calls) == 1:
            # Single service call - direct return
            return await self._execute_single_call(service_calls[0])
        
        # Multiple service calls - parallel execution
        return await self._execute_parallel_calls(service_calls)
    
    async def _execute_single_call(self, call_info: Dict[str, Any]) -> Dict[str, Any]:
        """Execute single service call"""
        try:
            # This would be called by the router
            # For now, return the call info as placeholder
            return {
                "result": "Single call executed",
                "service": call_info.get("service", "unknown"),
                "status": "success"
            }
        except Exception as e:
            logger.error(f"Single call error: {e}")
            return {
                "error": str(e),
                "status": "execution_error"
            }
    
    async def _execute_parallel_calls(self, service_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Execute multiple service calls in parallel"""
        try:
            # Create tasks for parallel execution
            tasks = [
                self._execute_call_with_timeout(call_info)
                for call_info in service_calls
            ]
            
            # Wait for first successful response or all failures
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Find first successful result
            for result in results:
                if isinstance(result, dict) and result.get("status") == "success":
                    return result
            
            # All failed - return error array
            errors = []
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    errors.append({
                        "service": service_calls[i].get("service", "unknown"),
                        "error": str(result)
                    })
                elif isinstance(result, dict) and "error" in result:
                    errors.append({
                        "service": result.get("service", "unknown"),
                        "error": result.get("error", "Unknown error")
                    })
            
            return {
                "error": "All services failed",
                "errors": errors,
                "status": "all_failed"
            }
            
        except Exception as e:
            logger.error(f"Parallel execution error: {e}")
            return {
                "error": f"Aggregation failed: {str(e)}",
                "status": "aggregation_error"
            }
    
    async def _execute_call_with_timeout(self, call_info: Dict[str, Any]) -> Dict[str, Any]:
        """Execute single call with timeout"""
        try:
            # Simulate service call with timeout
            await asyncio.wait_for(
                self._simulate_service_call(call_info),
                timeout=self.timeout
            )
            
            return {
                "result": "Call executed successfully",
                "service": call_info.get("service", "unknown"),
                "status": "success"
            }
            
        except asyncio.TimeoutError:
            logger.warning(f"Service call timeout: {call_info.get('service', 'unknown')}")
            return {
                "error": "Service timeout",
                "service": call_info.get("service", "unknown"),
                "status": "timeout"
            }
        except Exception as e:
            logger.error(f"Service call error: {e}")
            return {
                "error": str(e),
                "service": call_info.get("service", "unknown"),
                "status": "service_error"
            }
    
    async def _simulate_service_call(self, call_info: Dict[str, Any]):
        """Simulate service call (placeholder)"""
        # This would be replaced with actual service call logic
        await asyncio.sleep(0.1)  # Simulate network delay
