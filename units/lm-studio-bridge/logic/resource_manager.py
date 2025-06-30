"""
Intelligent Resource Management for LM Studio Bridge
Automatically adjusts resources to never impact user's other activities
"""

import asyncio
import os
import psutil
import platform
from typing import Dict, Any, Optional
from pathlib import Path
import sys

# Add platform to Python path
platform_path = Path(__file__).parent.parent.parent.parent / "platform"
sys.path.insert(0, str(platform_path))

from platform.runtime.bootstrap import get_logger


class ResourceManager:
    """Manages system resources intelligently to avoid impacting user activities"""
    
    def __init__(self):
        """Initialize resource manager"""
        self.logger = get_logger(__name__)
        
        # Resource monitoring state
        self._monitoring_active = False
        self._monitoring_task = None
        self._monitoring_interval = 10  # seconds
        
        # Resource limits (50% rule)
        self._max_cpu_percent = 50.0
        self._max_memory_percent = 50.0
        
        # Current resource usage
        self._current_cpu_usage = 0.0
        self._current_memory_usage = 0.0
        self._system_cpu_usage = 0.0
        self._system_memory_usage = 0.0
        
        # Throttling state
        self._is_throttled = False
        self._throttle_level = 0  # 0 = no throttle, 1-5 = increasing throttle
        
        # Windows activity detection
        self._is_windows = platform.system() == "Windows"
        self._user_activity_detected = False
        
        # Process tracking
        self._process = psutil.Process()
        
    async def start_monitoring(self):
        """Start resource monitoring"""
        if self._monitoring_active:
            self.logger.warning("Resource monitoring already active")
            return
        
        self.logger.info("Starting intelligent resource monitoring")
        self._monitoring_active = True
        self._monitoring_task = asyncio.create_task(self._monitoring_loop())
    
    async def stop_monitoring(self):
        """Stop resource monitoring"""
        if not self._monitoring_active:
            return
        
        self.logger.info("Stopping resource monitoring")
        self._monitoring_active = False
        
        if self._monitoring_task:
            self._monitoring_task.cancel()
            try:
                await self._monitoring_task
            except asyncio.CancelledError:
                pass
    
    async def _monitoring_loop(self):
        """Main monitoring loop"""
        while self._monitoring_active:
            try:
                await self._check_system_resources()
                await self._detect_user_activity()
                await self._adjust_resource_limits()
                
                await asyncio.sleep(self._monitoring_interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error in resource monitoring: {e}")
                await asyncio.sleep(self._monitoring_interval)
    
    async def _check_system_resources(self):
        """Check current system resource usage"""
        try:
            # Get system-wide CPU and memory usage
            self._system_cpu_usage = psutil.cpu_percent(interval=1)
            memory_info = psutil.virtual_memory()
            self._system_memory_usage = memory_info.percent
            
            # Get our process resource usage
            try:
                self._current_cpu_usage = self._process.cpu_percent()
                memory_info = self._process.memory_info()
                system_memory = psutil.virtual_memory().total
                self._current_memory_usage = (memory_info.rss / system_memory) * 100
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                # Process might have been restarted
                self._process = psutil.Process()
                self._current_cpu_usage = 0.0
                self._current_memory_usage = 0.0
            
            self.logger.debug(f"System CPU: {self._system_cpu_usage:.1f}%, "
                            f"System Memory: {self._system_memory_usage:.1f}%, "
                            f"Our CPU: {self._current_cpu_usage:.1f}%, "
                            f"Our Memory: {self._current_memory_usage:.1f}%")
            
        except Exception as e:
            self.logger.error(f"Failed to check system resources: {e}")
    
    async def _detect_user_activity(self):
        """Detect if user is actively using the system"""
        try:
            # Simple heuristic: high CPU usage by other processes indicates user activity
            other_cpu_usage = max(0, self._system_cpu_usage - self._current_cpu_usage)
            
            # If other processes are using significant CPU, user is likely active
            self._user_activity_detected = other_cpu_usage > 20.0
            
            # On Windows, could also check for active windows, mouse movement, etc.
            if self._is_windows:
                # Additional Windows-specific activity detection could go here
                pass
            
            self.logger.debug(f"User activity detected: {self._user_activity_detected}")
            
        except Exception as e:
            self.logger.error(f"Failed to detect user activity: {e}")
            # Default to assuming user is active (conservative approach)
            self._user_activity_detected = True
    
    async def _adjust_resource_limits(self):
        """Adjust resource usage based on system state and user activity"""
        try:
            should_throttle = False
            new_throttle_level = 0
            
            # Check if we should throttle based on system resources
            if self._system_cpu_usage > 80.0:
                should_throttle = True
                new_throttle_level = max(new_throttle_level, 3)
                self.logger.info(f"High system CPU usage ({self._system_cpu_usage:.1f}%), throttling")
            
            if self._system_memory_usage > 85.0:
                should_throttle = True
                new_throttle_level = max(new_throttle_level, 2)
                self.logger.info(f"High system memory usage ({self._system_memory_usage:.1f}%), throttling")
            
            # Check if our own usage is too high
            if self._current_cpu_usage > self._max_cpu_percent:
                should_throttle = True
                new_throttle_level = max(new_throttle_level, 2)
                self.logger.info(f"Our CPU usage too high ({self._current_cpu_usage:.1f}%), throttling")
            
            if self._current_memory_usage > self._max_memory_percent:
                should_throttle = True
                new_throttle_level = max(new_throttle_level, 1)
                self.logger.info(f"Our memory usage too high ({self._current_memory_usage:.1f}%), throttling")
            
            # Increase throttling if user is active
            if self._user_activity_detected and should_throttle:
                new_throttle_level = min(new_throttle_level + 1, 5)
                self.logger.info("User activity detected, increasing throttle level")
            
            # Apply throttling changes
            if new_throttle_level != self._throttle_level:
                await self._apply_throttling(new_throttle_level)
            
        except Exception as e:
            self.logger.error(f"Failed to adjust resource limits: {e}")
    
    async def _apply_throttling(self, throttle_level: int):
        """Apply throttling based on level (0-5)"""
        try:
            self._throttle_level = throttle_level
            self._is_throttled = throttle_level > 0
            
            if throttle_level == 0:
                self.logger.info("Removing resource throttling")
                # Remove any throttling
                await self._set_process_priority("normal")
                
            elif throttle_level == 1:
                self.logger.info("Applying light throttling")
                await self._set_process_priority("below_normal")
                
            elif throttle_level == 2:
                self.logger.info("Applying moderate throttling")
                await self._set_process_priority("low")
                
            elif throttle_level >= 3:
                self.logger.info("Applying heavy throttling")
                await self._set_process_priority("idle")
                # Could also add delays to processing loops here
            
        except Exception as e:
            self.logger.error(f"Failed to apply throttling: {e}")
    
    async def _set_process_priority(self, priority: str):
        """Set process priority (Windows/Linux compatible)"""
        try:
            if self._is_windows:
                priority_map = {
                    "idle": psutil.IDLE_PRIORITY_CLASS,
                    "low": psutil.BELOW_NORMAL_PRIORITY_CLASS,
                    "below_normal": psutil.BELOW_NORMAL_PRIORITY_CLASS,
                    "normal": psutil.NORMAL_PRIORITY_CLASS
                }
            else:
                # Linux nice values (lower = higher priority)
                priority_map = {
                    "idle": 19,
                    "low": 15,
                    "below_normal": 10,
                    "normal": 0
                }
            
            if priority in priority_map:
                if self._is_windows:
                    self._process.nice(priority_map[priority])
                else:
                    os.nice(priority_map[priority])
                
                self.logger.debug(f"Set process priority to {priority}")
            
        except Exception as e:
            self.logger.warning(f"Failed to set process priority: {e}")
    
    def get_resource_status(self) -> Dict[str, Any]:
        """Get current resource status and metrics"""
        return {
            "monitoring_active": self._monitoring_active,
            "system_resources": {
                "cpu_percent": self._system_cpu_usage,
                "memory_percent": self._system_memory_usage
            },
            "process_resources": {
                "cpu_percent": self._current_cpu_usage,
                "memory_percent": self._current_memory_usage
            },
            "limits": {
                "max_cpu_percent": self._max_cpu_percent,
                "max_memory_percent": self._max_memory_percent
            },
            "throttling": {
                "is_throttled": self._is_throttled,
                "throttle_level": self._throttle_level,
                "user_activity_detected": self._user_activity_detected
            }
        }
    
    def should_throttle_operation(self) -> bool:
        """Check if operations should be throttled"""
        return self._is_throttled and self._throttle_level >= 2
    
    async def get_recommended_delay(self) -> float:
        """Get recommended delay for throttled operations"""
        if not self._is_throttled:
            return 0.0
        
        # Progressive delays based on throttle level
        delay_map = {
            1: 0.1,   # 100ms
            2: 0.25,  # 250ms
            3: 0.5,   # 500ms
            4: 1.0,   # 1s
            5: 2.0    # 2s
        }
        
        return delay_map.get(self._throttle_level, 0.0)
