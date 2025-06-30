#!/usr/bin/env python3
"""
LLM Hub Python API Examples
Basic usage examples for interacting with LLM Hub services
"""

import asyncio
import httpx
import json
from typing import Dict, Any, List, Optional


class LLMHubClient:
    """Simple client for LLM Hub API"""
    
    def __init__(self, gateway_url: str = "http://localhost:8080", api_key: str = "changeme"):
        """Initialize the client
        
        Args:
            gateway_url: URL to the LLM Hub gateway
            api_key: API key for authentication
        """
        self.gateway_url = gateway_url.rstrip('/')
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    async def check_health(self) -> Dict[str, Any]:
        """Check the health status of the gateway"""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.gateway_url}/health")
            response.raise_for_status()
            return response.json()
    
    async def list_tools(self) -> List[Dict[str, Any]]:
        """Get list of available MCP tools"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.gateway_url}/mcp/tools",
                headers=self.headers
            )
            response.raise_for_status()
            data = response.json()
            return data.get("tools", [])
    
    async def generate_text(
        self, 
        prompt: str, 
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """Generate text using the inference tool
        
        Args:
            prompt: Text prompt for generation
            model: Model name to use
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text
        """
        async with httpx.AsyncClient(timeout=60.0) as client:
            payload = {
                "parameters": {
                    "prompt": prompt,
                    "model": model,
                    "temperature": temperature,
                    "max_tokens": max_tokens
                }
            }
            
            response = await client.post(
                f"{self.gateway_url}/tools/inference",
                json=payload,
                headers=self.headers
            )
            response.raise_for_status()
            data = response.json()
            return data.get("result", "")
    
    async def list_models(self) -> List[Dict[str, Any]]:
        """Get list of available models"""
        async with httpx.AsyncClient() as client:
            payload = {"parameters": {}}
            
            response = await client.post(
                f"{self.gateway_url}/tools/list_models",
                json=payload,
                headers=self.headers
            )
            response.raise_for_status()
            data = response.json()
            result = data.get("result", {})
            return result.get("models", [])


async def main():
    """Main example function"""
    # Initialize client
    client = LLMHubClient()
    
    print("LLM Hub Python API Examples")
    print("=" * 40)
    
    try:
        # Check health
        print("\n1. Checking health status...")
        health = await client.check_health()
        print(f"   Status: {health.get('status', 'unknown')}")
        print(f"   Version: {health.get('version', 'unknown')}")
        
        # List available tools
        print("\n2. Listing available tools...")
        tools = await client.list_tools()
        print(f"   Found {len(tools)} tools:")
        for tool in tools:
            print(f"   - {tool.get('name', 'unknown')}: {tool.get('description', 'No description')}")
        
        # List available models
        print("\n3. Listing available models...")
        models = await client.list_models()
        print(f"   Found {len(models)} models:")
        for model in models:
            print(f"   - {model.get('id', 'unknown')}: {model.get('name', 'No name')}")
        
        # Generate text (if models are available)
        if models:
            print("\n4. Generating text...")
            model_id = models[0].get('id', 'unknown')
            prompt = "Write a short poem about artificial intelligence."
            
            print(f"   Using model: {model_id}")
            print(f"   Prompt: {prompt}")
            
            result = await client.generate_text(
                prompt=prompt,
                model=model_id,
                temperature=0.8,
                max_tokens=200
            )
            
            print(f"   Generated text:")
            print(f"   {result}")
        else:
            print("\n4. No models available for text generation")
            
    except httpx.HTTPStatusError as e:
        print(f"\nHTTP Error: {e.response.status_code} - {e.response.text}")
    except httpx.RequestError as e:
        print(f"\nRequest Error: {e}")
    except Exception as e:
        print(f"\nUnexpected Error: {e}")


# Synchronous wrapper for easier usage
def run_example():
    """Run the async example in a synchronous context"""
    asyncio.run(main())


if __name__ == "__main__":
    run_example()


# Additional utility functions
class LLMHubError(Exception):
    """Custom exception for LLM Hub errors"""
    pass


async def simple_chat_example():
    """Simple chat example with error handling"""
    client = LLMHubClient()
    
    try:
        # Get available models
        models = await client.list_models()
        if not models:
            raise LLMHubError("No models available")
        
        model_id = models[0]['id']
        print(f"Using model: {model_id}")
        
        # Simple chat loop
        print("\nSimple Chat (type 'quit' to exit)")
        print("-" * 30)
        
        while True:
            user_input = input("You: ").strip()
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
            
            if not user_input:
                continue
            
            try:
                response = await client.generate_text(
                    prompt=user_input,
                    model=model_id,
                    temperature=0.7,
                    max_tokens=500
                )
                print(f"AI: {response}")
            except Exception as e:
                print(f"Error: {e}")
                
    except Exception as e:
        print(f"Chat setup error: {e}")


async def batch_processing_example():
    """Example of processing multiple prompts"""
    client = LLMHubClient()
    
    prompts = [
        "What is machine learning?",
        "Explain quantum computing in simple terms.",
        "Write a haiku about programming."
    ]
    
    try:
        models = await client.list_models()
        if not models:
            print("No models available for batch processing")
            return
        
        model_id = models[0]['id']
        print(f"Batch processing with model: {model_id}")
        
        # Process prompts concurrently
        tasks = [
            client.generate_text(prompt, model_id, temperature=0.5, max_tokens=200)
            for prompt in prompts
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for i, (prompt, result) in enumerate(zip(prompts, results)):
            print(f"\nPrompt {i+1}: {prompt}")
            if isinstance(result, Exception):
                print(f"Error: {result}")
            else:
                print(f"Response: {result}")
                
    except Exception as e:
        print(f"Batch processing error: {e}")


# Example usage patterns
if __name__ == "__main__":
    print("Choose an example to run:")
    print("1. Basic usage")
    print("2. Simple chat")
    print("3. Batch processing")
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == "1":
        asyncio.run(main())
    elif choice == "2":
        asyncio.run(simple_chat_example())
    elif choice == "3":
        asyncio.run(batch_processing_example())
    else:
        print("Invalid choice")
