#!/usr/bin/env python3
"""
Standalone Health Monitor Startup Script
Starts predictive maintenance monitoring as a background service
"""

import asyncio
import signal
import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from predictive_maintenance import PredictiveMaintenance


class HealthMonitorService:
    """Standalone health monitor service"""
    
    def __init__(self):
        self.predictive_maintenance = PredictiveMaintenance()
        self.running = False
        
    async def start(self):
        """Start the health monitor service"""
        print("🔮 Starting LLM Hub Health Monitor...")
        print("📊 Predictive Maintenance Dashboard: file://" + str(Path(__file__).parent / "dashboard.html"))
        print("⚡ Monitoring system resources and predicting issues...")
        print("Press Ctrl+C to stop")
        
        self.running = True
        
        # Setup signal handlers for graceful shutdown
        if os.name != 'nt':  # Unix systems
            signal.signal(signal.SIGINT, self._signal_handler)
            signal.signal(signal.SIGTERM, self._signal_handler)
        
        try:
            # Start predictive maintenance
            await self.predictive_maintenance.start_monitoring()
            
            # Keep running until shutdown
            while self.running:
                await asyncio.sleep(1)
                
        except KeyboardInterrupt:
            print("\n🛑 Shutdown requested...")
        finally:
            await self.stop()
    
    async def stop(self):
        """Stop the health monitor service"""
        print("🔄 Stopping health monitor...")
        self.running = False
        
        if self.predictive_maintenance:
            await self.predictive_maintenance.stop_monitoring()
        
        print("✅ Health monitor stopped")
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print(f"\n🛑 Received signal {signum}, shutting down...")
        self.running = False


async def main():
    """Main entry point"""
    service = HealthMonitorService()
    await service.start()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"❌ Health monitor failed: {e}")
        sys.exit(1)
