#!/usr/bin/env python3
"""
Error Test Script
Tests various error scenarios like invalid models and auth errors
"""

import os
import sys
import json
import httpx
import asyncio
from typing import Dict, Any

class ErrorTest:
    """Test error handling scenarios"""
    
    def __init__(self):
        self.gateway_url = "http://localhost:8080"
        self.valid_api_key = os.getenv("API_KEY", "changeme")
        self.invalid_api_key = "invalid_token_12345"
    
    async def test_invalid_model(self) -> bool:
        """Test invalid model name returns 404"""
        try:
            headers = {
                "Authorization": f"Bearer {self.valid_api_key}",
                "Content-Type": "application/json"
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                tool_name = "nonexistent_model"
                request_data = {
                    "parameters": {
                        "prompt": "Hello",
                        "model": "invalid-model-name"
                    }
                }
                
                print(f"Testing invalid model: {tool_name}")
                
                response = await client.post(
                    f"{self.gateway_url}/tools/{tool_name}",
                    json=request_data,
                    headers=headers
                )
                
                print(f"Response Status: {response.status_code}")
                
                if response.status_code == 404:
                    print("✓ Invalid model correctly returned 404")
                    return True
                else:
                    print(f"✗ Expected 404, got {response.status_code}")
                    print(f"Response: {response.text}")
                    return False
                    
        except Exception as e:
            print(f"✗ Invalid model test error: {e}")
            return False
    
    async def test_missing_auth(self) -> bool:
        """Test missing auth returns 401"""
        try:
            # No Authorization header
            headers = {
                "Content-Type": "application/json"
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                tool_name = "inference"
                request_data = {
                    "parameters": {
                        "prompt": "Hello",
                        "model": "llama-2-7b-chat"
                    }
                }
                
                print("Testing missing authentication")
                
                response = await client.post(
                    f"{self.gateway_url}/tools/{tool_name}",
                    json=request_data,
                    headers=headers
                )
                
                print(f"Response Status: {response.status_code}")
                
                if response.status_code == 401:
                    print("✓ Missing auth correctly returned 401")
                    return True
                elif response.status_code == 403:
                    print("✓ Missing auth correctly returned 403")
                    return True
                else:
                    print(f"✗ Expected 401/403, got {response.status_code}")
                    return False
                    
        except Exception as e:
            print(f"✗ Missing auth test error: {e}")
            return False
    
    async def test_invalid_auth(self) -> bool:
        """Test invalid auth token returns 401"""
        try:
            headers = {
                "Authorization": f"Bearer {self.invalid_api_key}",
                "Content-Type": "application/json"
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                tool_name = "inference"
                request_data = {
                    "parameters": {
                        "prompt": "Hello",
                        "model": "llama-2-7b-chat"
                    }
                }
                
                print("Testing invalid authentication token")
                
                response = await client.post(
                    f"{self.gateway_url}/tools/{tool_name}",
                    json=request_data,
                    headers=headers
                )
                
                print(f"Response Status: {response.status_code}")
                
                if response.status_code == 401:
                    print("✓ Invalid auth correctly returned 401")
                    return True
                else:
                    print(f"✗ Expected 401, got {response.status_code}")
                    return False
                    
        except Exception as e:
            print(f"✗ Invalid auth test error: {e}")
            return False
    
    async def test_invalid_json(self) -> bool:
        """Test invalid JSON returns 400"""
        try:
            headers = {
                "Authorization": f"Bearer {self.valid_api_key}",
                "Content-Type": "application/json"
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                tool_name = "inference"
                invalid_json = '{"parameters": {"prompt": "Hello", "model": "llama-2-7b-chat"'  # Missing closing braces
                
                print("Testing invalid JSON request")
                
                response = await client.post(
                    f"{self.gateway_url}/tools/{tool_name}",
                    content=invalid_json,
                    headers=headers
                )
                
                print(f"Response Status: {response.status_code}")
                
                if response.status_code == 400:
                    print("✓ Invalid JSON correctly returned 400")
                    return True
                elif response.status_code == 422:
                    print("✓ Invalid JSON correctly returned 422")
                    return True
                else:
                    print(f"✗ Expected 400/422, got {response.status_code}")
                    return False
                    
        except Exception as e:
            print(f"✗ Invalid JSON test error: {e}")
            return False
    
    def _validate_error_format(self, response_data: Dict[str, Any]) -> bool:
        """Validate error response format"""
        try:
            if "error" in response_data:
                print("✓ Error field present")
                return True
            elif "detail" in response_data:
                print("✓ Detail field present (FastAPI format)")
                return True
            else:
                print("✗ No error/detail field found")
                return False
                
        except Exception as e:
            print(f"✗ Error format validation failed: {e}")
            return False
    
    async def run_all_tests(self) -> bool:
        """Run all error handling tests"""
        print("MCP Error Handling Test")
        print("======================")
        print(f"Gateway URL: {self.gateway_url}")
        print()
        
        tests_passed = 0
        total_tests = 4
        
        # Test 1: Invalid model
        print("Test 1: Invalid Model Name")
        print("-" * 30)
        if await self.test_invalid_model():
            tests_passed += 1
        print()
        
        # Test 2: Missing auth
        print("Test 2: Missing Authentication")
        print("-" * 30)
        if await self.test_missing_auth():
            tests_passed += 1
        print()
        
        # Test 3: Invalid auth
        print("Test 3: Invalid Authentication")
        print("-" * 30)
        if await self.test_invalid_auth():
            tests_passed += 1
        print()
        
        # Test 4: Invalid JSON
        print("Test 4: Invalid JSON")
        print("-" * 30)
        if await self.test_invalid_json():
            tests_passed += 1
        print()
        
        # Summary
        print("Test Summary")
        print("=" * 20)
        print(f"Tests passed: {tests_passed}/{total_tests}")
        
        if tests_passed == total_tests:
            print("✓ All error handling tests passed")
            return True
        else:
            print("✗ Some error handling tests failed")
            return False

async def main():
    """Main entry point"""
    test = ErrorTest()
    
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
