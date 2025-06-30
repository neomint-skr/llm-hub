#!/usr/bin/env python3
"""
Direct Access Test Script
Tests direct LM Studio access to verify both access modes
"""

import os
import sys
import json
import httpx
import asyncio
from typing import Dict, Any

class DirectAccessTest:
    """Test direct LM Studio access vs Gateway access"""
    
    def __init__(self):
        self.lm_studio_url = "http://localhost:1234"
        self.gateway_url = "http://localhost:8080"
        self.api_key = os.getenv("API_KEY", "changeme")
    
    async def test_direct_models(self) -> tuple[bool, Dict[str, Any]]:
        """Test direct LM Studio models endpoint"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                print("Testing direct LM Studio /v1/models")
                
                response = await client.get(f"{self.lm_studio_url}/v1/models")
                
                print(f"Response Status: {response.status_code}")
                
                if response.status_code == 200:
                    response_data = response.json()
                    print(f"Models found: {len(response_data.get('data', []))}")
                    
                    # Extract model names for comparison
                    model_names = [model.get('id', '') for model in response_data.get('data', [])]
                    print(f"Model names: {model_names}")
                    
                    return True, {"models": model_names, "response": response_data}
                else:
                    print(f"✗ Direct models request failed: {response.status_code}")
                    return False, {}
                    
        except Exception as e:
            print(f"✗ Direct models test error: {e}")
            return False, {}
    
    async def test_direct_completion(self) -> tuple[bool, Dict[str, Any]]:
        """Test direct LM Studio completion endpoint"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                request_data = {
                    "model": "llama-2-7b-chat",
                    "prompt": "Hello, how are you?",
                    "max_tokens": 50,
                    "temperature": 0.7
                }
                
                print("Testing direct LM Studio /v1/completions")
                print(f"Request: {json.dumps(request_data, indent=2)}")
                
                response = await client.post(
                    f"{self.lm_studio_url}/v1/completions",
                    json=request_data,
                    headers={"Content-Type": "application/json"}
                )
                
                print(f"Response Status: {response.status_code}")
                
                if response.status_code == 200:
                    response_data = response.json()
                    print("✓ Direct completion successful")
                    
                    # Extract completion text
                    completion_text = ""
                    if "choices" in response_data and len(response_data["choices"]) > 0:
                        completion_text = response_data["choices"][0].get("text", "")
                    
                    return True, {"completion": completion_text, "response": response_data}
                else:
                    print(f"✗ Direct completion failed: {response.status_code}")
                    print(f"Response: {response.text}")
                    return False, {}
                    
        except Exception as e:
            print(f"✗ Direct completion test error: {e}")
            return False, {}
    
    async def test_gateway_access(self) -> tuple[bool, Dict[str, Any]]:
        """Test gateway access for comparison"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                # Test gateway tools endpoint
                print("Testing Gateway /mcp/tools")
                
                response = await client.get(
                    f"{self.gateway_url}/mcp/tools",
                    headers=headers
                )
                
                print(f"Response Status: {response.status_code}")
                
                if response.status_code == 200:
                    response_data = response.json()
                    tools = response_data.get("tools", [])
                    tool_names = [tool.get("name", "") for tool in tools]
                    
                    print(f"Tools found: {len(tools)}")
                    print(f"Tool names: {tool_names}")
                    
                    return True, {"tools": tool_names, "response": response_data}
                else:
                    print(f"✗ Gateway tools request failed: {response.status_code}")
                    return False, {}
                    
        except Exception as e:
            print(f"✗ Gateway access test error: {e}")
            return False, {}
    
    async def test_gateway_inference(self) -> tuple[bool, Dict[str, Any]]:
        """Test gateway inference for comparison"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            request_data = {
                "parameters": {
                    "prompt": "Hello, how are you?",
                    "model": "llama-2-7b-chat",
                    "max_tokens": 50,
                    "temperature": 0.7
                }
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                print("Testing Gateway inference tool")
                
                response = await client.post(
                    f"{self.gateway_url}/tools/inference",
                    json=request_data,
                    headers=headers
                )
                
                print(f"Response Status: {response.status_code}")
                
                if response.status_code == 200:
                    response_data = response.json()
                    print("✓ Gateway inference successful")
                    return True, {"response": response_data}
                else:
                    print(f"✗ Gateway inference failed: {response.status_code}")
                    return False, {}
                    
        except Exception as e:
            print(f"✗ Gateway inference test error: {e}")
            return False, {}
    
    def compare_responses(self, direct_data: Dict[str, Any], gateway_data: Dict[str, Any]):
        """Compare direct vs gateway responses"""
        print("Comparing Access Modes")
        print("-" * 30)
        
        # Compare models vs tools
        direct_models = direct_data.get("models", [])
        gateway_tools = gateway_data.get("tools", [])
        
        print(f"Direct models: {len(direct_models)}")
        print(f"Gateway tools: {len(gateway_tools)}")
        
        # Check if models appear as tools
        models_as_tools = 0
        for model in direct_models:
            if any(model in tool for tool in gateway_tools):
                models_as_tools += 1
        
        print(f"Models appearing as tools: {models_as_tools}/{len(direct_models)}")
        
        if models_as_tools > 0:
            print("✓ Models successfully exposed through gateway")
        else:
            print("⚠ Models may not be exposed through gateway yet")
    
    async def run_all_tests(self) -> bool:
        """Run all direct access tests"""
        print("Direct Access Test")
        print("==================")
        print(f"LM Studio URL: {self.lm_studio_url}")
        print(f"Gateway URL: {self.gateway_url}")
        print()
        
        tests_passed = 0
        total_tests = 4
        
        # Test 1: Direct models
        print("Test 1: Direct LM Studio Models")
        print("-" * 30)
        direct_models_success, direct_models_data = await self.test_direct_models()
        if direct_models_success:
            tests_passed += 1
        print()
        
        # Test 2: Direct completion
        print("Test 2: Direct LM Studio Completion")
        print("-" * 30)
        direct_completion_success, direct_completion_data = await self.test_direct_completion()
        if direct_completion_success:
            tests_passed += 1
        print()
        
        # Test 3: Gateway tools
        print("Test 3: Gateway Tools Access")
        print("-" * 30)
        gateway_tools_success, gateway_tools_data = await self.test_gateway_access()
        if gateway_tools_success:
            tests_passed += 1
        print()
        
        # Test 4: Gateway inference
        print("Test 4: Gateway Inference Access")
        print("-" * 30)
        gateway_inference_success, gateway_inference_data = await self.test_gateway_inference()
        if gateway_inference_success:
            tests_passed += 1
        print()
        
        # Compare responses if both direct and gateway succeeded
        if direct_models_success and gateway_tools_success:
            self.compare_responses(direct_models_data, gateway_tools_data)
            print()
        
        # Summary
        print("Test Summary")
        print("=" * 20)
        print(f"Tests passed: {tests_passed}/{total_tests}")
        
        if tests_passed >= 2:  # At least direct OR gateway working
            print("✓ Access mode verification completed")
            return True
        else:
            print("✗ Both access modes failed")
            return False

async def main():
    """Main entry point"""
    test = DirectAccessTest()
    
    try:
        success = await test.run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\nTest interrupted")
        sys.exit(1)
    except Exception as e:
        print(f"Test failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
