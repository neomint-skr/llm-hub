#!/usr/bin/env python3
"""
LLM Hub Perfect Orchestration Integration Test
Comprehensive testing framework to validate orchestration works perfectly under all conditions
Implements 4D Methodology: GUTWILLIG, INTELLIGENT, KONTEXT-AWARE, FAUL
"""

import os
import sys
import time
import json
import subprocess
import requests
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class TestResult(Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    SKIP = "SKIP"
    WARNING = "WARNING"

@dataclass
class TestCase:
    name: str
    description: str
    result: TestResult
    duration: float
    details: Dict
    error: Optional[str] = None

class OrchestrationTester:
    """Comprehensive orchestration testing framework"""
    
    def __init__(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.compose_file = os.path.join(self.script_dir, "docker-compose.yml")
        self.orchestrate_script = os.path.join(self.script_dir, "orchestrate.bat" if os.name == 'nt' else "orchestrate.sh")
        
        self.gateway_url = "http://localhost:8080"
        self.bridge_url = "http://localhost:3000"
        
        self.test_results: List[TestCase] = []
        self.start_time = datetime.now()
        
        # Test configuration
        self.startup_timeout = 180  # 3 minutes
        self.health_check_timeout = 30
        self.shutdown_timeout = 60
        
    def log(self, message: str, level: str = "INFO"):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")
    
    def run_command(self, command: List[str], timeout: int = 30) -> Tuple[int, str, str]:
        """Run command and return exit code, stdout, stderr"""
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=self.script_dir
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -1, "", f"Command timed out after {timeout}s"
        except Exception as e:
            return -1, "", str(e)
    
    def check_service_health(self, url: str, timeout: int = 10) -> Tuple[bool, Dict]:
        """Check service health endpoint"""
        try:
            response = requests.get(f"{url}/health", timeout=timeout)
            if response.status_code == 200:
                return True, response.json()
            else:
                return False, {"error": f"HTTP {response.status_code}"}
        except Exception as e:
            return False, {"error": str(e)}
    
    def wait_for_service_health(self, url: str, service_name: str, timeout: int = 120) -> bool:
        """Wait for service to become healthy"""
        self.log(f"Waiting for {service_name} to become healthy...")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            healthy, data = self.check_service_health(url)
            if healthy and data.get("status") == "healthy":
                self.log(f"✅ {service_name} is healthy")
                return True
            
            time.sleep(2)
            elapsed = int(time.time() - start_time)
            if elapsed % 15 == 0:
                self.log(f"⏳ Still waiting for {service_name}... ({elapsed}/{timeout}s)")
        
        self.log(f"❌ {service_name} did not become healthy within {timeout}s")
        return False
    
    def test_prerequisites(self) -> TestCase:
        """Test: Prerequisites validation"""
        start_time = time.time()
        
        try:
            # Check Docker
            exit_code, _, _ = self.run_command(["docker", "--version"])
            if exit_code != 0:
                return TestCase(
                    "prerequisites", "Prerequisites validation", TestResult.FAIL,
                    time.time() - start_time, {}, "Docker not available"
                )
            
            # Check Docker Compose
            exit_code, _, _ = self.run_command(["docker-compose", "--version"])
            if exit_code != 0:
                return TestCase(
                    "prerequisites", "Prerequisites validation", TestResult.FAIL,
                    time.time() - start_time, {}, "Docker Compose not available"
                )
            
            # Check compose file
            if not os.path.exists(self.compose_file):
                return TestCase(
                    "prerequisites", "Prerequisites validation", TestResult.FAIL,
                    time.time() - start_time, {}, "Compose file not found"
                )
            
            # Check orchestration script
            if not os.path.exists(self.orchestrate_script):
                return TestCase(
                    "prerequisites", "Prerequisites validation", TestResult.FAIL,
                    time.time() - start_time, {}, "Orchestration script not found"
                )
            
            return TestCase(
                "prerequisites", "Prerequisites validation", TestResult.PASS,
                time.time() - start_time, {"docker": True, "compose": True, "scripts": True}
            )
            
        except Exception as e:
            return TestCase(
                "prerequisites", "Prerequisites validation", TestResult.FAIL,
                time.time() - start_time, {}, str(e)
            )
    
    def test_clean_startup(self) -> TestCase:
        """Test: Clean startup from stopped state"""
        start_time = time.time()
        
        try:
            self.log("🚀 Testing clean startup...")
            
            # Ensure clean state
            self.run_command([self.orchestrate_script, "stop"], timeout=60)
            time.sleep(2)
            
            # Start services
            exit_code, stdout, stderr = self.run_command([self.orchestrate_script, "start"], timeout=self.startup_timeout)
            
            if exit_code != 0:
                return TestCase(
                    "clean_startup", "Clean startup from stopped state", TestResult.FAIL,
                    time.time() - start_time, {"stdout": stdout, "stderr": stderr}, 
                    f"Startup failed with exit code {exit_code}"
                )
            
            # Verify services are healthy
            bridge_healthy = self.wait_for_service_health(self.bridge_url, "Bridge", 60)
            gateway_healthy = self.wait_for_service_health(self.gateway_url, "Gateway", 60)
            
            if not bridge_healthy or not gateway_healthy:
                return TestCase(
                    "clean_startup", "Clean startup from stopped state", TestResult.FAIL,
                    time.time() - start_time, {"bridge_healthy": bridge_healthy, "gateway_healthy": gateway_healthy},
                    "Services did not become healthy"
                )
            
            return TestCase(
                "clean_startup", "Clean startup from stopped state", TestResult.PASS,
                time.time() - start_time, {"bridge_healthy": True, "gateway_healthy": True}
            )
            
        except Exception as e:
            return TestCase(
                "clean_startup", "Clean startup from stopped state", TestResult.FAIL,
                time.time() - start_time, {}, str(e)
            )
    
    def test_health_endpoints(self) -> TestCase:
        """Test: Health endpoints comprehensive validation"""
        start_time = time.time()
        
        try:
            self.log("🔍 Testing health endpoints...")
            
            # Test Bridge health
            bridge_healthy, bridge_data = self.check_service_health(self.bridge_url)
            if not bridge_healthy:
                return TestCase(
                    "health_endpoints", "Health endpoints validation", TestResult.FAIL,
                    time.time() - start_time, {"bridge_data": bridge_data}, "Bridge health check failed"
                )
            
            # Test Gateway health
            gateway_healthy, gateway_data = self.check_service_health(self.gateway_url)
            if not gateway_healthy:
                return TestCase(
                    "health_endpoints", "Health endpoints validation", TestResult.FAIL,
                    time.time() - start_time, {"gateway_data": gateway_data}, "Gateway health check failed"
                )
            
            # Validate health data structure
            required_fields = ["status", "service", "version", "timestamp", "orchestration"]
            
            for field in required_fields:
                if field not in bridge_data:
                    return TestCase(
                        "health_endpoints", "Health endpoints validation", TestResult.FAIL,
                        time.time() - start_time, {"bridge_data": bridge_data}, 
                        f"Bridge health missing field: {field}"
                    )
                
                if field not in gateway_data:
                    return TestCase(
                        "health_endpoints", "Health endpoints validation", TestResult.FAIL,
                        time.time() - start_time, {"gateway_data": gateway_data}, 
                        f"Gateway health missing field: {field}"
                    )
            
            return TestCase(
                "health_endpoints", "Health endpoints validation", TestResult.PASS,
                time.time() - start_time, {
                    "bridge_status": bridge_data.get("status"),
                    "gateway_status": gateway_data.get("status"),
                    "bridge_ready": bridge_data.get("orchestration", {}).get("ready_for_traffic"),
                    "gateway_ready": gateway_data.get("orchestration", {}).get("ready_for_traffic")
                }
            )
            
        except Exception as e:
            return TestCase(
                "health_endpoints", "Health endpoints validation", TestResult.FAIL,
                time.time() - start_time, {}, str(e)
            )
    
    def test_dependency_validation(self) -> TestCase:
        """Test: Service dependency validation"""
        start_time = time.time()
        
        try:
            self.log("🔗 Testing dependency validation...")
            
            # Get Gateway health to check Bridge dependency
            gateway_healthy, gateway_data = self.check_service_health(self.gateway_url)
            if not gateway_healthy:
                return TestCase(
                    "dependency_validation", "Service dependency validation", TestResult.FAIL,
                    time.time() - start_time, {}, "Gateway not healthy for dependency test"
                )
            
            # Check if Gateway reports Bridge dependency
            dependencies = gateway_data.get("dependencies", {})
            bridge_dep = dependencies.get("lm_studio_bridge", {})
            
            if bridge_dep.get("status") != "healthy":
                return TestCase(
                    "dependency_validation", "Service dependency validation", TestResult.FAIL,
                    time.time() - start_time, {"bridge_dependency": bridge_dep}, 
                    "Gateway does not report Bridge as healthy dependency"
                )
            
            return TestCase(
                "dependency_validation", "Service dependency validation", TestResult.PASS,
                time.time() - start_time, {"bridge_dependency": bridge_dep}
            )
            
        except Exception as e:
            return TestCase(
                "dependency_validation", "Service dependency validation", TestResult.FAIL,
                time.time() - start_time, {}, str(e)
            )
    
    def test_graceful_shutdown(self) -> TestCase:
        """Test: Graceful shutdown"""
        start_time = time.time()
        
        try:
            self.log("🛑 Testing graceful shutdown...")
            
            # Stop services
            exit_code, stdout, stderr = self.run_command([self.orchestrate_script, "stop"], timeout=self.shutdown_timeout)
            
            if exit_code != 0:
                return TestCase(
                    "graceful_shutdown", "Graceful shutdown", TestResult.FAIL,
                    time.time() - start_time, {"stdout": stdout, "stderr": stderr}, 
                    f"Shutdown failed with exit code {exit_code}"
                )
            
            # Verify services are stopped
            time.sleep(5)
            
            bridge_healthy, _ = self.check_service_health(self.bridge_url, timeout=5)
            gateway_healthy, _ = self.check_service_health(self.gateway_url, timeout=5)
            
            if bridge_healthy or gateway_healthy:
                return TestCase(
                    "graceful_shutdown", "Graceful shutdown", TestResult.FAIL,
                    time.time() - start_time, {"bridge_still_running": bridge_healthy, "gateway_still_running": gateway_healthy},
                    "Services still responding after shutdown"
                )
            
            return TestCase(
                "graceful_shutdown", "Graceful shutdown", TestResult.PASS,
                time.time() - start_time, {"shutdown_clean": True}
            )
            
        except Exception as e:
            return TestCase(
                "graceful_shutdown", "Graceful shutdown", TestResult.FAIL,
                time.time() - start_time, {}, str(e)
            )
    
    def run_all_tests(self) -> bool:
        """Run all orchestration tests"""
        self.log("🧪 Starting LLM Hub Perfect Orchestration Tests")
        self.log("=" * 60)
        
        # Define test sequence
        tests = [
            self.test_prerequisites,
            self.test_clean_startup,
            self.test_health_endpoints,
            self.test_dependency_validation,
            self.test_graceful_shutdown
        ]
        
        # Run tests
        for test_func in tests:
            self.log(f"Running: {test_func.__doc__.split(':')[1].strip()}")
            result = test_func()
            self.test_results.append(result)
            
            if result.result == TestResult.PASS:
                self.log(f"✅ PASS: {result.name} ({result.duration:.2f}s)")
            elif result.result == TestResult.FAIL:
                self.log(f"❌ FAIL: {result.name} - {result.error} ({result.duration:.2f}s)")
            elif result.result == TestResult.WARNING:
                self.log(f"⚠️  WARNING: {result.name} - {result.error} ({result.duration:.2f}s)")
            
            # Stop on critical failures
            if result.result == TestResult.FAIL and result.name in ["prerequisites", "clean_startup"]:
                self.log(f"💥 Critical test failed, stopping test suite")
                break
        
        return self.generate_report()
    
    def generate_report(self) -> bool:
        """Generate test report"""
        total_duration = (datetime.now() - self.start_time).total_seconds()
        
        passed = sum(1 for r in self.test_results if r.result == TestResult.PASS)
        failed = sum(1 for r in self.test_results if r.result == TestResult.FAIL)
        warnings = sum(1 for r in self.test_results if r.result == TestResult.WARNING)
        total = len(self.test_results)
        
        self.log("=" * 60)
        self.log("🎯 LLM Hub Perfect Orchestration Test Report")
        self.log("=" * 60)
        self.log(f"Total Tests: {total}")
        self.log(f"✅ Passed: {passed}")
        self.log(f"❌ Failed: {failed}")
        self.log(f"⚠️  Warnings: {warnings}")
        self.log(f"⏱️  Total Duration: {total_duration:.2f}s")
        self.log("")
        
        # Detailed results
        for result in self.test_results:
            status_icon = "✅" if result.result == TestResult.PASS else "❌" if result.result == TestResult.FAIL else "⚠️"
            self.log(f"{status_icon} {result.name}: {result.description} ({result.duration:.2f}s)")
            if result.error:
                self.log(f"   Error: {result.error}")
        
        self.log("=" * 60)
        
        if failed == 0:
            self.log("🎉 ALL TESTS PASSED - Perfect Orchestration Validated!")
            return True
        else:
            self.log("💥 TESTS FAILED - Orchestration Issues Detected")
            return False

def main():
    """Main test runner"""
    tester = OrchestrationTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
