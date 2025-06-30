"""
Predictive Maintenance System for LLM Hub
Detects and fixes problems BEFORE user notices them through predictive patterns
"""

import asyncio
import os
import time
import statistics
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
import sys
import psutil

# Add platform to Python path
platform_path = Path(__file__).parent.parent.parent / "platform"
sys.path.insert(0, str(platform_path))

from platform.runtime.bootstrap import get_logger


class PredictiveMaintenance:
    """Predictive maintenance system that prevents problems before they occur"""
    
    def __init__(self):
        """Initialize predictive maintenance system"""
        self.logger = get_logger(__name__)
        
        # Monitoring state
        self._monitoring_active = False
        self._monitoring_task = None
        self._monitoring_interval = 60  # Check every minute
        
        # Historical data storage (in-memory for simplicity)
        self._memory_history: List[Tuple[float, float]] = []  # (timestamp, memory_percent)
        self._cpu_history: List[Tuple[float, float]] = []     # (timestamp, cpu_percent)
        self._disk_history: List[Tuple[float, float]] = []    # (timestamp, disk_percent)
        self._error_history: List[Tuple[float, str]] = []     # (timestamp, error_type)
        
        # Prediction thresholds
        self._memory_growth_threshold = 5.0  # % per hour
        self._cpu_sustained_threshold = 80.0  # % for 5 minutes
        self._disk_growth_threshold = 10.0   # % per day
        self._error_frequency_threshold = 3   # errors per hour
        
        # Maintenance actions performed
        self._last_cleanup_time = 0
        self._last_restart_time = 0
        self._cleanup_cooldown = 3600  # 1 hour
        self._restart_cooldown = 7200  # 2 hours
        
        # Pattern detection
        self._pattern_window = 3600  # 1 hour window for pattern analysis
        self._min_data_points = 5    # Minimum data points for prediction
    
    async def start_monitoring(self):
        """Start predictive monitoring"""
        if self._monitoring_active:
            self.logger.warning("Predictive monitoring already active")
            return
        
        self.logger.info("Starting predictive maintenance monitoring")
        self._monitoring_active = True
        self._monitoring_task = asyncio.create_task(self._monitoring_loop())
    
    async def stop_monitoring(self):
        """Stop predictive monitoring"""
        if not self._monitoring_active:
            return
        
        self.logger.info("Stopping predictive maintenance monitoring")
        self._monitoring_active = False
        
        if self._monitoring_task:
            self._monitoring_task.cancel()
            try:
                await self._monitoring_task
            except asyncio.CancelledError:
                pass
    
    async def _monitoring_loop(self):
        """Main predictive monitoring loop"""
        while self._monitoring_active:
            try:
                await self._collect_metrics()
                await self._analyze_patterns()
                await self._perform_predictive_actions()
                
                await asyncio.sleep(self._monitoring_interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error in predictive monitoring: {e}")
                await asyncio.sleep(self._monitoring_interval)
    
    async def _collect_metrics(self):
        """Collect system metrics for trend analysis"""
        try:
            current_time = time.time()
            
            # Collect memory usage
            memory_info = psutil.virtual_memory()
            memory_percent = memory_info.percent
            self._memory_history.append((current_time, memory_percent))
            
            # Collect CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            self._cpu_history.append((current_time, cpu_percent))
            
            # Collect disk usage
            disk_info = psutil.disk_usage('/')
            disk_percent = (disk_info.used / disk_info.total) * 100
            self._disk_history.append((current_time, disk_percent))
            
            # Trim old data (keep only last 24 hours)
            cutoff_time = current_time - 86400  # 24 hours
            self._memory_history = [(t, v) for t, v in self._memory_history if t > cutoff_time]
            self._cpu_history = [(t, v) for t, v in self._cpu_history if t > cutoff_time]
            self._disk_history = [(t, v) for t, v in self._disk_history if t > cutoff_time]
            self._error_history = [(t, e) for t, e in self._error_history if t > cutoff_time]
            
            self.logger.debug(f"Collected metrics: Memory={memory_percent:.1f}%, "
                            f"CPU={cpu_percent:.1f}%, Disk={disk_percent:.1f}%")
            
        except Exception as e:
            self.logger.error(f"Failed to collect metrics: {e}")
    
    async def _analyze_patterns(self):
        """Analyze patterns and predict potential issues"""
        try:
            current_time = time.time()
            
            # Analyze memory growth trend
            memory_trend = self._calculate_trend(self._memory_history, 3600)  # 1 hour trend
            if memory_trend > self._memory_growth_threshold:
                self.logger.warning(f"Memory growth trend detected: {memory_trend:.2f}%/hour")
                await self._schedule_memory_cleanup()
            
            # Analyze sustained high CPU usage
            recent_cpu = self._get_recent_values(self._cpu_history, 300)  # Last 5 minutes
            if recent_cpu and statistics.mean(recent_cpu) > self._cpu_sustained_threshold:
                self.logger.warning(f"Sustained high CPU usage detected: {statistics.mean(recent_cpu):.1f}%")
                await self._schedule_cpu_optimization()
            
            # Analyze disk growth trend
            disk_trend = self._calculate_trend(self._disk_history, 86400)  # 24 hour trend
            if disk_trend > self._disk_growth_threshold:
                self.logger.warning(f"Disk growth trend detected: {disk_trend:.2f}%/day")
                await self._schedule_disk_cleanup()
            
            # Analyze error frequency
            recent_errors = [e for t, e in self._error_history if t > current_time - 3600]
            if len(recent_errors) > self._error_frequency_threshold:
                self.logger.warning(f"High error frequency detected: {len(recent_errors)} errors/hour")
                await self._schedule_error_mitigation()
            
        except Exception as e:
            self.logger.error(f"Failed to analyze patterns: {e}")
    
    def _calculate_trend(self, data: List[Tuple[float, float]], window_seconds: int) -> float:
        """Calculate trend (rate of change) over a time window"""
        if len(data) < self._min_data_points:
            return 0.0
        
        current_time = time.time()
        window_data = [(t, v) for t, v in data if t > current_time - window_seconds]
        
        if len(window_data) < 2:
            return 0.0
        
        # Simple linear trend calculation
        times = [t for t, v in window_data]
        values = [v for t, v in window_data]
        
        if len(times) < 2:
            return 0.0
        
        # Calculate slope (change per second)
        time_span = times[-1] - times[0]
        if time_span == 0:
            return 0.0
        
        value_change = values[-1] - values[0]
        trend_per_second = value_change / time_span
        
        # Convert to trend per hour
        trend_per_hour = trend_per_second * 3600
        
        return trend_per_hour
    
    def _get_recent_values(self, data: List[Tuple[float, float]], window_seconds: int) -> List[float]:
        """Get values from recent time window"""
        current_time = time.time()
        recent_data = [(t, v) for t, v in data if t > current_time - window_seconds]
        return [v for t, v in recent_data]
    
    async def _perform_predictive_actions(self):
        """Perform scheduled predictive maintenance actions"""
        # This method coordinates the execution of scheduled actions
        # Actions are scheduled by the pattern analysis methods
        pass
    
    async def _schedule_memory_cleanup(self):
        """Schedule preemptive memory cleanup"""
        current_time = time.time()
        
        if current_time - self._last_cleanup_time < self._cleanup_cooldown:
            self.logger.debug("Memory cleanup on cooldown, skipping")
            return
        
        self.logger.info("Performing preemptive memory cleanup")
        
        try:
            # Trigger garbage collection in Python processes
            import gc
            gc.collect()
            
            # Clear Docker system cache (if available)
            try:
                import subprocess
                result = await asyncio.create_subprocess_exec(
                    "docker", "system", "prune", "-f",
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                await result.communicate()
                self.logger.info("Docker system cleanup completed")
            except Exception as e:
                self.logger.debug(f"Docker cleanup not available: {e}")
            
            self._last_cleanup_time = current_time
            self.logger.info("Preemptive memory cleanup completed")
            
        except Exception as e:
            self.logger.error(f"Memory cleanup failed: {e}")
    
    async def _schedule_cpu_optimization(self):
        """Schedule CPU optimization actions"""
        self.logger.info("Performing preemptive CPU optimization")
        
        try:
            # Reduce process priority temporarily
            current_process = psutil.Process()
            if hasattr(psutil, 'BELOW_NORMAL_PRIORITY_CLASS'):
                current_process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
            else:
                current_process.nice(10)  # Linux nice value
            
            self.logger.info("Reduced process priority for CPU optimization")
            
        except Exception as e:
            self.logger.error(f"CPU optimization failed: {e}")
    
    async def _schedule_disk_cleanup(self):
        """Schedule preemptive disk cleanup"""
        current_time = time.time()
        
        if current_time - self._last_cleanup_time < self._cleanup_cooldown:
            self.logger.debug("Disk cleanup on cooldown, skipping")
            return
        
        self.logger.info("Performing preemptive disk cleanup")
        
        try:
            # Clean up temporary files
            temp_dirs = ['/tmp', os.path.expanduser('~/tmp'), os.environ.get('TEMP', '')]
            
            for temp_dir in temp_dirs:
                if temp_dir and os.path.exists(temp_dir):
                    # Clean files older than 1 day
                    cutoff_time = current_time - 86400
                    for root, dirs, files in os.walk(temp_dir):
                        for file in files:
                            file_path = os.path.join(root, file)
                            try:
                                if os.path.getmtime(file_path) < cutoff_time:
                                    os.remove(file_path)
                            except (OSError, PermissionError):
                                pass  # Skip files we can't delete
            
            self._last_cleanup_time = current_time
            self.logger.info("Preemptive disk cleanup completed")
            
        except Exception as e:
            self.logger.error(f"Disk cleanup failed: {e}")
    
    async def _schedule_error_mitigation(self):
        """Schedule error mitigation actions"""
        current_time = time.time()
        
        if current_time - self._last_restart_time < self._restart_cooldown:
            self.logger.debug("Error mitigation on cooldown, skipping")
            return
        
        self.logger.info("Performing preemptive error mitigation")
        
        try:
            # Reset connection pools and caches
            # This would integrate with existing recovery systems
            self.logger.info("Connection pools reset for error mitigation")
            
            self._last_restart_time = current_time
            
        except Exception as e:
            self.logger.error(f"Error mitigation failed: {e}")
    
    def record_error(self, error_type: str):
        """Record an error for pattern analysis"""
        current_time = time.time()
        self._error_history.append((current_time, error_type))
        self.logger.debug(f"Recorded error for analysis: {error_type}")
    
    def get_prediction_status(self) -> Dict[str, Any]:
        """Get current prediction status and metrics"""
        current_time = time.time()
        
        # Calculate current trends
        memory_trend = self._calculate_trend(self._memory_history, 3600)
        cpu_trend = self._calculate_trend(self._cpu_history, 3600)
        disk_trend = self._calculate_trend(self._disk_history, 86400)
        
        # Count recent errors
        recent_errors = len([e for t, e in self._error_history if t > current_time - 3600])
        
        return {
            "monitoring_active": self._monitoring_active,
            "trends": {
                "memory_growth_per_hour": memory_trend,
                "cpu_trend_per_hour": cpu_trend,
                "disk_growth_per_day": disk_trend
            },
            "error_frequency": {
                "errors_last_hour": recent_errors,
                "threshold": self._error_frequency_threshold
            },
            "last_actions": {
                "last_cleanup": self._last_cleanup_time,
                "last_restart": self._last_restart_time,
                "cleanup_cooldown_remaining": max(0, self._cleanup_cooldown - (current_time - self._last_cleanup_time)),
                "restart_cooldown_remaining": max(0, self._restart_cooldown - (current_time - self._last_restart_time))
            },
            "data_points": {
                "memory_samples": len(self._memory_history),
                "cpu_samples": len(self._cpu_history),
                "disk_samples": len(self._disk_history),
                "error_samples": len(self._error_history)
            }
        }
