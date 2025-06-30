"""
Translation Layer for OpenAI API to MCP Tool Calls
Handles request/response mapping and streaming
"""

import json
from typing import Dict, Any, Optional, AsyncGenerator
from pathlib import Path
import sys

# Add platform to Python path
platform_path = Path(__file__).parent.parent.parent.parent / "platform"
sys.path.insert(0, str(platform_path))

from platform.runtime.bootstrap import get_logger
from platform.runtime.error_handler import ValidationError, NetworkError
from pydantic import BaseModel, Field
from .http_client import LMStudioClient


class CompletionRequest(BaseModel):
    """OpenAI-compatible completion request"""
    prompt: str
    model: str
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=1000, ge=1)
    stream: bool = False


class CompletionResponse(BaseModel):
    """OpenAI-compatible completion response"""
    id: str
    object: str = "text_completion"
    created: int
    model: str
    choices: list


class MCPTranslator:
    """Translates between OpenAI API and MCP Tool calls"""
    
    def __init__(self):
        self.logger = get_logger(__name__)
        self.client: Optional[LMStudioClient] = None
    
    async def initialize(self):
        """Initialize the translator with HTTP client"""
        self.client = LMStudioClient()
        self.logger.info("MCP Translator initialized")
    
    async def close(self):
        """Close the translator and cleanup resources"""
        if self.client:
            await self.client.close()
    
    def validate_completion_request(self, request_data: Dict[str, Any]) -> CompletionRequest:
        """Validate and parse completion request
        
        Args:
            request_data: Raw request data
            
        Returns:
            Validated completion request
            
        Raises:
            ValidationError: If request is invalid
        """
        try:
            return CompletionRequest(**request_data)
        except Exception as e:
            raise ValidationError(f"Invalid completion request: {e}")
    
    async def translate_mcp_to_openai(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Translate MCP tool call to OpenAI completion request
        
        Args:
            tool_name: Name of the MCP tool
            parameters: Tool parameters
            
        Returns:
            OpenAI-compatible response
            
        Raises:
            ValidationError: If tool or parameters are invalid
        """
        if not self.client:
            raise ValidationError("Translator not initialized")
        
        self.logger.info(f"Translating MCP tool call: {tool_name}")
        
        if tool_name == "inference":
            return await self._handle_inference_tool(parameters)
        elif tool_name == "list_models":
            return await self._handle_list_models_tool(parameters)
        else:
            raise ValidationError(f"Unknown tool: {tool_name}")
    
    async def _handle_inference_tool(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle inference tool call
        
        Args:
            parameters: Tool parameters
            
        Returns:
            Completion response
        """
        # Validate parameters
        request = self.validate_completion_request(parameters)
        
        try:
            # Call LM Studio API
            response = await self.client.create_completion(
                prompt=request.prompt,
                model=request.model,
                temperature=request.temperature,
                max_tokens=request.max_tokens
            )
            
            # Map to OpenAI format
            return self._map_completion_response(response, request.model)
            
        except Exception as e:
            self.logger.error(f"Inference failed: {e}")
            raise NetworkError(f"Failed to generate completion: {e}")
    
    async def _handle_list_models_tool(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle list models tool call
        
        Args:
            parameters: Tool parameters (unused)
            
        Returns:
            Models list response
        """
        try:
            models = await self.client.get_models()
            
            # Map to OpenAI format
            return {
                "object": "list",
                "data": models
            }
            
        except Exception as e:
            self.logger.error(f"List models failed: {e}")
            raise NetworkError(f"Failed to list models: {e}")
    
    def _map_completion_response(self, lm_response: Dict[str, Any], model: str) -> Dict[str, Any]:
        """Map LM Studio response to OpenAI format
        
        Args:
            lm_response: LM Studio API response
            model: Model identifier
            
        Returns:
            OpenAI-compatible response
        """
        # Extract completion text
        choices = lm_response.get("choices", [])
        if not choices:
            text = lm_response.get("text", "")
            choices = [{"text": text, "index": 0, "finish_reason": "stop"}]
        
        return {
            "id": f"cmpl-{lm_response.get('id', 'unknown')}",
            "object": "text_completion",
            "created": lm_response.get("created", 0),
            "model": model,
            "choices": choices,
            "usage": lm_response.get("usage", {})
        }
    
    async def stream_completion(self, request: CompletionRequest) -> AsyncGenerator[str, None]:
        """Stream completion response (placeholder for future implementation)
        
        Args:
            request: Completion request
            
        Yields:
            Server-sent events for streaming
        """
        # Placeholder for streaming implementation
        self.logger.info("Streaming not yet implemented, falling back to non-streaming")
        
        # For now, return single response as stream
        response = await self._handle_inference_tool(request.dict())
        
        # Format as SSE
        yield f"data: {json.dumps(response)}\n\n"
        yield "data: [DONE]\n\n"
    
    def map_error_to_openai(self, error: Exception) -> Dict[str, Any]:
        """Map internal errors to OpenAI error format
        
        Args:
            error: Internal error
            
        Returns:
            OpenAI-compatible error response
        """
        if isinstance(error, ValidationError):
            error_type = "invalid_request_error"
            code = "invalid_request"
        elif isinstance(error, NetworkError):
            error_type = "api_error"
            code = "api_error"
        else:
            error_type = "api_error"
            code = "internal_error"
        
        return {
            "error": {
                "message": str(error),
                "type": error_type,
                "code": code
            }
        }
