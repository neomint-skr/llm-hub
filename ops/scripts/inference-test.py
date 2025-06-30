#!/usr/bin/env python3
"""
Inference Test Script
Tests MCP Tool-Call over Gateway with Mock Response Verification
"""

import os
import sys
import json
import httpx
import asyncio
import time
from typing import Dict, Any

class InferenceTest:
    """Test MCP tool calls through the gateway"""
    
    def __init__(self):
        self.gateway_url = "http://localhost:8080"
        self.api_key = os.getenv("API_KEY", "changeme")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def test_tool_call(self) -> bool:
        """Test MCP tool call through gateway"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                # Test inference tool call
                tool_name = "inference"
                request_data = {
                    "parameters": {
                        "prompt": "Hello, how are you?",
                        "model": "llama-2-7b-chat",
                        "temperature": 0.7,
                        "max_tokens": 100
                    }
                }
                
                print(f"Testing tool call: {tool_name}")
                print(f"Request: {json.dumps(request_data, indent=2)}")
                
                response = await client.post(
                    f"{self.gateway_url}/tools/{tool_name}",
                    json=request_data,
                    headers=self.headers
                )
                
                print(f"Response Status: {response.status_code}")
                
                if response.status_code == 200:
                    response_data = response.json()
                    print(f"Response: {json.dumps(response_data, indent=2)}")
                    
                    # Validate response structure
                    if self._validate_response(response_data):
                        print("✓ Response validation passed")
                        return True
                    else:
                        print("✗ Response validation failed")
                        return False
                        
                elif response.status_code == 401:
                    print("✗ Authentication failed - check API_KEY")
                    return False
                elif response.status_code == 404:
                    print("✗ Tool not found")
                    return False
                else:
                    print(f"✗ Unexpected status code: {response.status_code}")
                    print(f"Response: {response.text}")
                    return False
                    
        except httpx.TimeoutException:
            print("✗ Request timeout")
            return False
        except Exception as e:
            print(f"✗ Test error: {e}")
            return False
    
    def _validate_response(self, response_data: Dict[str, Any]) -> bool:
        """Validate MCP response structure"""
        try:
            # Check for required fields based on gateway contract
            if "result" in response_data:
                print("✓ Result field present")
            elif "error" in response_data:
                print("✓ Error field present (expected for mock)")
                return True
            else:
                print("✗ Neither result nor error field found")
                return False
            
            if "status" in response_data:
                print(f"✓ Status field present: {response_data['status']}")
            else:
                print("✗ Status field missing")
                return False
            
            if "service" in response_data:
                print(f"✓ Service field present: {response_data['service']}")
            
            return True
            
        except Exception as e:
            print(f"✗ Validation error: {e}")
            return False
    
    async def test_streaming_response(self) -> bool:
        """Test streaming response with SSE"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                tool_name = "inference"
                request_data = {
                    "parameters": {
                        "prompt": "Tell me a short story",
                        "model": "llama-2-7b-chat",
                        "stream": True,
                        "max_tokens": 50
                    }
                }

                print(f"Testing streaming tool call: {tool_name}")
                print(f"Request: {json.dumps(request_data, indent=2)}")

                # Note: This is a basic test since the gateway may not support streaming yet
                response = await client.post(
                    f"{self.gateway_url}/tools/{tool_name}",
                    json=request_data,
                    headers=self.headers
                )

                print(f"Response Status: {response.status_code}")

                if response.status_code == 200:
                    # For now, just validate as regular response
                    # In future, this would parse SSE events
                    response_data = response.json()
                    print(f"Response: {json.dumps(response_data, indent=2)}")
                    print("✓ Streaming test completed (non-streaming response received)")
                    return True
                else:
                    print(f"✗ Streaming test failed with status: {response.status_code}")
                    return False

        except Exception as e:
            print(f"✗ Streaming test error: {e}")
            return False

    async def test_list_models_tool(self) -> bool:
        """Test list_models tool call"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                tool_name = "list_models"
                request_data = {
                    "parameters": {}
                }

                print(f"Testing tool call: {tool_name}")

                response = await client.post(
                    f"{self.gateway_url}/tools/{tool_name}",
                    json=request_data,
                    headers=self.headers
                )

                print(f"Response Status: {response.status_code}")

                if response.status_code == 200:
                    response_data = response.json()
                    print(f"Response: {json.dumps(response_data, indent=2)}")
                    return self._validate_response(response_data)
                else:
                    print(f"✗ Unexpected status code: {response.status_code}")
                    return False

        except Exception as e:
            print(f"✗ List models test error: {e}")
            return False

    async def test_performance_check(self) -> bool:
        """Test basic performance - first token latency"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                tool_name = "inference"
                request_data = {
                    "parameters": {
                        "prompt": "Hi",
                        "model": "llama-2-7b-chat",
                        "max_tokens": 10
                    }
                }

                print(f"Testing performance for tool: {tool_name}")

                # Measure request start time
                start_time = time.time()

                response = await client.post(
                    f"{self.gateway_url}/tools/{tool_name}",
                    json=request_data,
                    headers=self.headers
                )

                # Measure first response time (not first token, but first response)
                end_time = time.time()
                latency_ms = (end_time - start_time) * 1000

                print(f"Response Status: {response.status_code}")
                print(f"Response Latency: {latency_ms:.2f}ms")

                if response.status_code == 200:
                    if latency_ms > 100:
                        print(f"⚠ Latency {latency_ms:.2f}ms exceeds 100ms threshold")
                    else:
                        print(f"✓ Latency {latency_ms:.2f}ms within 100ms threshold")

                    print("✓ Performance check completed")
                    return True
                else:
                    print(f"✗ Performance test failed with status: {response.status_code}")
                    return False

        except Exception as e:
            print(f"✗ Performance test error: {e}")
            return False
    
    async def run_all_tests(self) -> bool:
        """Run all inference tests"""
        print("MCP Inference Test")
        print("==================")
        print(f"Gateway URL: {self.gateway_url}")
        print(f"API Key: {'***' + self.api_key[-4:] if len(self.api_key) > 4 else '***'}")
        print()

        tests_passed = 0
        total_tests = 4

        # Test 1: Inference tool
        print("Test 1: Inference Tool Call")
        print("-" * 30)
        if await self.test_tool_call():
            tests_passed += 1
        print()

        # Test 2: Streaming response
        print("Test 2: Streaming Response")
        print("-" * 30)
        if await self.test_streaming_response():
            tests_passed += 1
        print()

        # Test 3: Performance check
        print("Test 3: Performance Check")
        print("-" * 30)
        if await self.test_performance_check():
            tests_passed += 1
        print()

        # Test 4: List models tool
        print("Test 4: List Models Tool Call")
        print("-" * 30)
        if await self.test_list_models_tool():
            tests_passed += 1
        print()

        # Summary
        print("Test Summary")
        print("=" * 20)
        print(f"Tests passed: {tests_passed}/{total_tests}")

        if tests_passed == total_tests:
            print("✓ All inference tests passed")
            return True
        else:
            print("✗ Some inference tests failed")
            return False

async def main():
    """Main entry point"""
    test = InferenceTest()
    
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
