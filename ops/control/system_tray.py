"""
System Tray Integration for LLM Hub Control Center
Provides quick access to control functions from Windows system tray
"""

import sys
import os
import webbrowser
import subprocess
import threading
import time
from pathlib import Path

try:
    import pystray
    from pystray import MenuItem as item
    from PIL import Image, ImageDraw
except ImportError:
    print("Required packages not installed. Install with:")
    print("pip install pystray pillow")
    sys.exit(1)


class LLMHubTray:
    """System tray application for LLM Hub control"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.control_url = "http://localhost:9000"
        self.icon = None
        self.status_healthy = False
        
        # Create tray icon
        self.create_icon()
        
        # Start status monitoring
        self.start_status_monitor()
    
    def create_icon(self):
        """Create system tray icon"""
        # Create a simple icon
        image = Image.new('RGB', (64, 64), color='blue')
        draw = ImageDraw.Draw(image)
        
        # Draw LLM Hub logo (simple representation)
        draw.ellipse([8, 8, 56, 56], fill='white', outline='blue', width=2)
        draw.text((20, 25), "LLM", fill='blue')
        
        # Create menu
        menu = pystray.Menu(
            item('LLM Hub Control Center', self.open_control_center, default=True),
            item('Status', self.show_status),
            pystray.Menu.SEPARATOR,
            item('Start Services', self.start_services),
            item('Restart Services', self.restart_services),
            item('Stop Services', self.stop_services),
            pystray.Menu.SEPARATOR,
            item('Quick Fixes', pystray.Menu(
                item('Fix Docker Issues', self.fix_docker),
                item('Fix LM Studio Connection', self.fix_lmstudio),
                item('Fix Port Conflicts', self.fix_ports),
                item('Reset Configuration', self.reset_config)
            )),
            pystray.Menu.SEPARATOR,
            item('Open Dashboard', self.open_dashboard),
            item('View Logs', self.view_logs),
            item('Run Diagnostics', self.run_diagnostics),
            pystray.Menu.SEPARATOR,
            item('Setup Autostart', self.setup_autostart),
            item('Documentation', self.open_docs),
            pystray.Menu.SEPARATOR,
            item('Exit', self.quit_application)
        )
        
        self.icon = pystray.Icon("llm_hub", image, "LLM Hub Control", menu)
    
    def start_status_monitor(self):
        """Start background status monitoring"""
        def monitor():
            while True:
                try:
                    self.check_system_status()
                    time.sleep(30)  # Check every 30 seconds
                except Exception as e:
                    print(f"Status monitor error: {e}")
                    time.sleep(60)  # Wait longer on error
        
        monitor_thread = threading.Thread(target=monitor, daemon=True)
        monitor_thread.start()
    
    def check_system_status(self):
        """Check system status and update icon"""
        try:
            # Simple status check - ping the gateway
            result = subprocess.run(
                ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "http://localhost:8080/health"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            self.status_healthy = result.stdout.strip() == "200"
            self.update_icon_status()
            
        except Exception:
            self.status_healthy = False
            self.update_icon_status()
    
    def update_icon_status(self):
        """Update icon based on status"""
        if not self.icon:
            return
        
        # Create status-aware icon
        color = 'green' if self.status_healthy else 'red'
        image = Image.new('RGB', (64, 64), color=color)
        draw = ImageDraw.Draw(image)
        
        # Draw status indicator
        draw.ellipse([8, 8, 56, 56], fill='white', outline=color, width=3)
        draw.text((18, 25), "LLM", fill=color)
        
        # Add status dot
        dot_color = 'green' if self.status_healthy else 'red'
        draw.ellipse([45, 45, 60, 60], fill=dot_color)
        
        self.icon.icon = image
        
        # Update tooltip
        status_text = "Healthy" if self.status_healthy else "Issues Detected"
        self.icon.title = f"LLM Hub Control - {status_text}"
    
    def run_command_async(self, command):
        """Run a command asynchronously"""
        def run():
            try:
                subprocess.run([
                    "curl", "-X", "POST", 
                    f"{self.control_url}/api/commands/{command}"
                ], check=True, capture_output=True)
                self.show_notification(f"✅ {command.replace('-', ' ').title()} completed successfully")
            except Exception as e:
                self.show_notification(f"❌ {command.replace('-', ' ').title()} failed: {e}")
        
        threading.Thread(target=run, daemon=True).start()
    
    def show_notification(self, message):
        """Show system notification"""
        try:
            if os.name == 'nt':  # Windows
                import win10toast
                toaster = win10toast.ToastNotifier()
                toaster.show_toast("LLM Hub", message, duration=3)
        except ImportError:
            print(f"Notification: {message}")
    
    # Menu action methods
    def open_control_center(self, icon, item):
        """Open the control center web interface"""
        webbrowser.open(self.control_url)
    
    def show_status(self, icon, item):
        """Show current status"""
        status = "System is healthy" if self.status_healthy else "System has issues"
        self.show_notification(f"LLM Hub Status: {status}")
    
    def start_services(self, icon, item):
        """Start all services"""
        self.run_command_async("start-services")
    
    def restart_services(self, icon, item):
        """Restart all services"""
        self.run_command_async("restart-services")
    
    def stop_services(self, icon, item):
        """Stop all services"""
        self.run_command_async("stop-services")
    
    def fix_docker(self, icon, item):
        """Fix Docker issues"""
        self.run_command_async("fix-docker")
    
    def fix_lmstudio(self, icon, item):
        """Fix LM Studio connection"""
        self.run_command_async("fix-lmstudio")
    
    def fix_ports(self, icon, item):
        """Fix port conflicts"""
        self.run_command_async("fix-ports")
    
    def reset_config(self, icon, item):
        """Reset configuration"""
        self.run_command_async("reset-config")
    
    def open_dashboard(self, icon, item):
        """Open the health dashboard"""
        webbrowser.open("http://localhost:8080")
    
    def view_logs(self, icon, item):
        """View system logs"""
        try:
            if os.name == 'nt':  # Windows
                logs_script = self.project_root / "logs.bat"
                subprocess.Popen([str(logs_script)], shell=True)
        except Exception as e:
            self.show_notification(f"Failed to open logs: {e}")
    
    def run_diagnostics(self, icon, item):
        """Run system diagnostics"""
        self.run_command_async("run-diagnostics")
    
    def setup_autostart(self, icon, item):
        """Setup autostart"""
        self.run_command_async("setup-autostart")
    
    def open_docs(self, icon, item):
        """Open documentation"""
        docs_path = self.project_root / "docs" / "README.md"
        webbrowser.open(f"file://{docs_path}")
    
    def quit_application(self, icon, item):
        """Quit the tray application"""
        icon.stop()
    
    def run(self):
        """Run the tray application"""
        print("🚀 LLM Hub System Tray started")
        print("📊 Control Center: http://localhost:9000")
        print("Right-click the tray icon for quick actions")
        
        self.icon.run()


def main():
    """Main entry point"""
    try:
        tray = LLMHubTray()
        tray.run()
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
