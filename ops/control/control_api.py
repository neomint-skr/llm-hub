"""
Control API for LLM Hub Control Center
Provides one-click fixes and service management
"""

import asyncio
import subprocess
import os
import sys
from pathlib import Path
from typing import Dict, Any
import json
import logging

# Add platform to Python path
platform_path = Path(__file__).parent.parent.parent / "platform"
sys.path.insert(0, str(platform_path))

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


class ControlAPI:
    """Control API for one-click fixes and service management"""
    
    def __init__(self):
        self.app = FastAPI(title="LLM Hub Control API", version="1.0.0")
        self.logger = logging.getLogger(__name__)
        self.project_root = Path(__file__).parent.parent.parent
        
        # Setup CORS
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Mount static files
        self.app.mount("/static", StaticFiles(directory=str(Path(__file__).parent)), name="static")
        
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup API routes"""
        
        @self.app.get("/", response_class=HTMLResponse)
        async def serve_control_center():
            """Serve the control center interface"""
            with open(Path(__file__).parent / "index.html", "r") as f:
                return HTMLResponse(content=f.read())
        
        @self.app.post("/api/commands/{command}")
        async def execute_command(command: str):
            """Execute a control command"""
            try:
                result = await self._execute_command(command)
                return {"success": True, "message": result["message"], "details": result.get("details", {})}
            except Exception as e:
                self.logger.error(f"Command {command} failed: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/api/status")
        async def get_system_status():
            """Get comprehensive system status"""
            try:
                status = await self._get_system_status()
                return status
            except Exception as e:
                self.logger.error(f"Status check failed: {e}")
                raise HTTPException(status_code=500, detail=str(e))
    
    async def _execute_command(self, command: str) -> Dict[str, Any]:
        """Execute a control command"""
        commands = {
            "start-services": self._start_services,
            "restart-services": self._restart_services,
            "stop-services": self._stop_services,
            "fix-docker": self._fix_docker_issues,
            "fix-lmstudio": self._fix_lmstudio_connection,
            "fix-ports": self._fix_port_conflicts,
            "reset-config": self._reset_configuration,
            "run-diagnostics": self._run_diagnostics,
            "setup-autostart": self._setup_autostart
        }
        
        if command not in commands:
            raise ValueError(f"Unknown command: {command}")
        
        return await commands[command]()
    
    async def _start_services(self) -> Dict[str, Any]:
        """Start all LLM Hub services"""
        try:
            # Change to compose directory and start services
            compose_dir = self.project_root / "ops" / "compose"
            result = await self._run_command(
                ["docker-compose", "up", "-d"],
                cwd=compose_dir
            )
            
            if result.returncode == 0:
                return {"message": "All services started successfully"}
            else:
                raise Exception(f"Docker compose failed: {result.stderr}")
        except Exception as e:
            raise Exception(f"Failed to start services: {e}")
    
    async def _restart_services(self) -> Dict[str, Any]:
        """Restart all LLM Hub services"""
        try:
            compose_dir = self.project_root / "ops" / "compose"
            
            # Stop services
            await self._run_command(["docker-compose", "down"], cwd=compose_dir)
            
            # Wait a moment
            await asyncio.sleep(2)
            
            # Start services
            result = await self._run_command(
                ["docker-compose", "up", "-d"],
                cwd=compose_dir
            )
            
            if result.returncode == 0:
                return {"message": "All services restarted successfully"}
            else:
                raise Exception(f"Docker compose restart failed: {result.stderr}")
        except Exception as e:
            raise Exception(f"Failed to restart services: {e}")
    
    async def _stop_services(self) -> Dict[str, Any]:
        """Stop all LLM Hub services"""
        try:
            compose_dir = self.project_root / "ops" / "compose"
            result = await self._run_command(
                ["docker-compose", "down"],
                cwd=compose_dir
            )
            
            if result.returncode == 0:
                return {"message": "All services stopped successfully"}
            else:
                raise Exception(f"Docker compose stop failed: {result.stderr}")
        except Exception as e:
            raise Exception(f"Failed to stop services: {e}")
    
    async def _fix_docker_issues(self) -> Dict[str, Any]:
        """Fix common Docker issues"""
        try:
            fixes_applied = []
            
            # Check if Docker is running
            docker_check = await self._run_command(["docker", "version"])
            if docker_check.returncode != 0:
                fixes_applied.append("Docker Desktop not running - please start Docker Desktop")
                return {"message": "Docker Desktop needs to be started manually", "details": {"fixes": fixes_applied}}
            
            # Clean up stopped containers
            await self._run_command(["docker", "container", "prune", "-f"])
            fixes_applied.append("Cleaned up stopped containers")
            
            # Clean up unused networks
            await self._run_command(["docker", "network", "prune", "-f"])
            fixes_applied.append("Cleaned up unused networks")
            
            # Restart Docker services
            compose_dir = self.project_root / "ops" / "compose"
            await self._run_command(["docker-compose", "down"], cwd=compose_dir)
            await asyncio.sleep(2)
            await self._run_command(["docker-compose", "up", "-d"], cwd=compose_dir)
            fixes_applied.append("Restarted LLM Hub services")
            
            return {"message": "Docker issues fixed", "details": {"fixes": fixes_applied}}
        except Exception as e:
            raise Exception(f"Failed to fix Docker issues: {e}")
    
    async def _fix_lmstudio_connection(self) -> Dict[str, Any]:
        """Fix LM Studio connection issues"""
        try:
            fixes_applied = []
            
            # Check if LM Studio is running
            lm_check = await self._run_command(["curl", "-s", "http://localhost:1234/v1/models"])
            if lm_check.returncode != 0:
                fixes_applied.append("LM Studio not responding - please start LM Studio and enable Local Server")
            
            # Restart bridge service to reconnect
            compose_dir = self.project_root / "ops" / "compose"
            await self._run_command(["docker-compose", "restart", "lm-studio-bridge"], cwd=compose_dir)
            fixes_applied.append("Restarted LM Studio Bridge")
            
            return {"message": "LM Studio connection fixed", "details": {"fixes": fixes_applied}}
        except Exception as e:
            raise Exception(f"Failed to fix LM Studio connection: {e}")
    
    async def _fix_port_conflicts(self) -> Dict[str, Any]:
        """Fix port conflicts"""
        try:
            fixes_applied = []
            
            # Check for port conflicts on common ports
            ports_to_check = [8080, 3000, 1234]
            
            for port in ports_to_check:
                if os.name == 'nt':  # Windows
                    result = await self._run_command(["netstat", "-an"])
                    if f":{port}" in result.stdout:
                        fixes_applied.append(f"Port {port} is in use")
                
            if not fixes_applied:
                fixes_applied.append("No port conflicts detected")
            
            return {"message": "Port conflicts checked", "details": {"fixes": fixes_applied}}
        except Exception as e:
            raise Exception(f"Failed to check port conflicts: {e}")
    
    async def _reset_configuration(self) -> Dict[str, Any]:
        """Reset configuration to defaults"""
        try:
            fixes_applied = []
            
            # Copy default environment file
            env_example = self.project_root / "ops" / "compose" / ".env.example"
            env_file = self.project_root / "ops" / "compose" / ".env"
            
            if env_example.exists():
                with open(env_example, 'r') as src, open(env_file, 'w') as dst:
                    dst.write(src.read())
                fixes_applied.append("Reset environment configuration")
            
            return {"message": "Configuration reset to defaults", "details": {"fixes": fixes_applied}}
        except Exception as e:
            raise Exception(f"Failed to reset configuration: {e}")
    
    async def _run_diagnostics(self) -> Dict[str, Any]:
        """Run system diagnostics"""
        try:
            diagnostics = []
            
            # Check Docker
            docker_result = await self._run_command(["docker", "version"])
            diagnostics.append(f"Docker: {'✅ OK' if docker_result.returncode == 0 else '❌ Error'}")
            
            # Check LM Studio
            lm_result = await self._run_command(["curl", "-s", "http://localhost:1234/v1/models"])
            diagnostics.append(f"LM Studio: {'✅ OK' if lm_result.returncode == 0 else '❌ Not responding'}")
            
            # Check services
            gateway_result = await self._run_command(["curl", "-s", "http://localhost:8080/health"])
            diagnostics.append(f"Gateway: {'✅ OK' if gateway_result.returncode == 0 else '❌ Not responding'}")
            
            bridge_result = await self._run_command(["curl", "-s", "http://localhost:3000/health"])
            diagnostics.append(f"Bridge: {'✅ OK' if bridge_result.returncode == 0 else '❌ Not responding'}")
            
            return {"message": "Diagnostics completed", "details": {"diagnostics": diagnostics}}
        except Exception as e:
            raise Exception(f"Failed to run diagnostics: {e}")
    
    async def _setup_autostart(self) -> Dict[str, Any]:
        """Setup autostart configuration"""
        try:
            autostart_script = self.project_root / "setup-autostart.bat"
            
            if autostart_script.exists():
                result = await self._run_command([str(autostart_script)], cwd=self.project_root)
                if result.returncode == 0:
                    return {"message": "Autostart configured successfully"}
                else:
                    raise Exception(f"Autostart setup failed: {result.stderr}")
            else:
                raise Exception("Autostart script not found")
        except Exception as e:
            raise Exception(f"Failed to setup autostart: {e}")
    
    async def _get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        status = {
            "docker": await self._check_docker_status(),
            "lm_studio": await self._check_lm_studio_status(),
            "gateway": await self._check_service_status("http://localhost:8080/health"),
            "bridge": await self._check_service_status("http://localhost:3000/health")
        }
        
        status["overall"] = "healthy" if all(s["status"] == "healthy" for s in status.values()) else "unhealthy"
        
        return status
    
    async def _check_docker_status(self) -> Dict[str, Any]:
        """Check Docker status"""
        try:
            result = await self._run_command(["docker", "version"])
            return {"status": "healthy" if result.returncode == 0 else "unhealthy"}
        except:
            return {"status": "unhealthy"}
    
    async def _check_lm_studio_status(self) -> Dict[str, Any]:
        """Check LM Studio status"""
        try:
            result = await self._run_command(["curl", "-s", "http://localhost:1234/v1/models"])
            return {"status": "healthy" if result.returncode == 0 else "unhealthy"}
        except:
            return {"status": "unhealthy"}
    
    async def _check_service_status(self, url: str) -> Dict[str, Any]:
        """Check service status via HTTP"""
        try:
            result = await self._run_command(["curl", "-s", url])
            return {"status": "healthy" if result.returncode == 0 else "unhealthy"}
        except:
            return {"status": "unhealthy"}
    
    async def _run_command(self, command, cwd=None):
        """Run a shell command asynchronously"""
        process = await asyncio.create_subprocess_exec(
            *command,
            cwd=cwd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        return type('Result', (), {
            'returncode': process.returncode,
            'stdout': stdout.decode(),
            'stderr': stderr.decode()
        })()


def main():
    """Run the Control API server"""
    control_api = ControlAPI()
    
    print("🚀 Starting LLM Hub Control Center...")
    print("📊 Control Center: http://localhost:9000")
    print("🔧 API Documentation: http://localhost:9000/docs")
    
    uvicorn.run(
        control_api.app,
        host="0.0.0.0",
        port=9000,
        log_level="info"
    )


if __name__ == "__main__":
    main()
