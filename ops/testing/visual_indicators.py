"""
Visual Test Indicators for LLM Hub
Enhanced visual feedback system with progress bars, animations, and rich status displays
"""

import time
import sys
import threading
from typing import Dict, Any, Optional, List
from enum import Enum
import os


class IndicatorStyle(Enum):
    """Visual indicator styles"""
    MINIMAL = "minimal"
    STANDARD = "standard"
    RICH = "rich"
    ANIMATED = "animated"


class VisualIndicators:
    """Enhanced visual feedback system for tests"""
    
    def __init__(self, style: IndicatorStyle = IndicatorStyle.STANDARD):
        self.style = style
        self.terminal_width = self._get_terminal_width()
        self.supports_color = self._supports_color()
        self.supports_unicode = self._supports_unicode()
        
        # Animation state
        self._animation_active = False
        self._animation_thread = None
        
        # Progress tracking
        self._current_progress = 0
        self._total_steps = 0
        
        # Status tracking
        self._test_results = {}
        
    def _get_terminal_width(self) -> int:
        """Get terminal width for progress bars"""
        try:
            return os.get_terminal_size().columns
        except OSError:
            return 80  # Default width
    
    def _supports_color(self) -> bool:
        """Check if terminal supports color"""
        return (
            hasattr(sys.stdout, 'isatty') and sys.stdout.isatty() and
            os.environ.get('TERM', '').lower() != 'dumb' and
            os.name != 'nt'  # Simplified for Windows
        )
    
    def _supports_unicode(self) -> bool:
        """Check if terminal supports Unicode"""
        try:
            sys.stdout.write('✓')
            sys.stdout.flush()
            return True
        except UnicodeEncodeError:
            return False
    
    def get_status_icon(self, status: str, animated: bool = False) -> str:
        """Get status icon based on style and capabilities"""
        if not self.supports_unicode:
            # ASCII fallback
            icons = {
                'pending': '?',
                'running': '.',
                'passed': '+',
                'failed': 'X',
                'skipped': '-',
                'warning': '!',
                'info': 'i'
            }
            return icons.get(status, '?')
        
        # Unicode icons
        if animated and status == 'running':
            return self._get_animated_icon()
        
        icons = {
            'pending': '⏳',
            'running': '🔄',
            'passed': '✅',
            'failed': '❌',
            'skipped': '⏭️',
            'warning': '⚠️',
            'info': 'ℹ️',
            'success': '🎉',
            'error': '💥',
            'loading': '⏳'
        }
        
        return icons.get(status, '❓')
    
    def _get_animated_icon(self) -> str:
        """Get animated running icon"""
        if not self.supports_unicode:
            return '.'
        
        # Simple spinner animation
        spinner_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        return spinner_chars[int(time.time() * 4) % len(spinner_chars)]
    
    def print_test_header(self, title: str, total_tests: int = 0):
        """Print enhanced test header"""
        self._total_steps = total_tests
        
        if self.style == IndicatorStyle.MINIMAL:
            print(f"Running {title}")
            return
        
        # Standard and rich headers
        separator = "=" * min(50, self.terminal_width - 10)
        
        print()
        print(f"🚀 {title}")
        print(separator)
        
        if total_tests > 0:
            print(f"Running {total_tests} tests with visual feedback")
        
        print()
    
    def print_test_start(self, test_name: str, step: int = 0):
        """Print test start with enhanced visuals"""
        self._current_progress = step
        
        if self.style == IndicatorStyle.MINIMAL:
            print(f"Running {test_name}...")
            return
        
        # Progress indicator
        progress_bar = self._create_progress_bar(step, self._total_steps) if self._total_steps > 0 else ""
        
        running_icon = self.get_status_icon('running', animated=True)
        print(f"{running_icon} {test_name}... {progress_bar}")
        
        # Start animation for rich style
        if self.style == IndicatorStyle.ANIMATED:
            self._start_animation(test_name)
    
    def print_test_result(self, test_name: str, status: str, duration: float, 
                         message: str = "", details: Optional[Dict[str, Any]] = None):
        """Print test result with enhanced visuals"""
        
        # Stop animation
        if self._animation_active:
            self._stop_animation()
        
        # Clear the current line and move up to overwrite the "running" line
        if self.style != IndicatorStyle.MINIMAL:
            print('\r' + ' ' * self.terminal_width, end='\r')
        
        status_icon = self.get_status_icon(status)
        duration_str = f"({duration:.2f}s)" if duration > 0 else ""
        
        # Basic result line
        result_line = f"{status_icon} {test_name} {duration_str}"
        
        if self.style == IndicatorStyle.MINIMAL:
            print(result_line)
            return
        
        print(result_line)
        
        # Add message with proper indentation
        if message:
            message_icon = self.get_status_icon('info')
            print(f"   {message_icon} {message}")
        
        # Add details for rich style
        if details and self.style in [IndicatorStyle.RICH, IndicatorStyle.ANIMATED]:
            for key, value in details.items():
                detail_icon = "📊" if self.supports_unicode else ">"
                print(f"   {detail_icon} {key}: {value}")
        
        print()  # Add spacing
        
        # Store result for summary
        self._test_results[test_name] = {
            'status': status,
            'duration': duration,
            'message': message,
            'details': details
        }
    
    def _create_progress_bar(self, current: int, total: int, width: int = 20) -> str:
        """Create a progress bar"""
        if total == 0:
            return ""
        
        progress = min(current / total, 1.0)
        filled = int(progress * width)
        
        if self.supports_unicode:
            bar = '█' * filled + '░' * (width - filled)
        else:
            bar = '#' * filled + '-' * (width - filled)
        
        percentage = int(progress * 100)
        return f"[{bar}] {percentage}%"
    
    def _start_animation(self, test_name: str):
        """Start animated indicator for long-running tests"""
        if self._animation_active:
            return
        
        self._animation_active = True
        
        def animate():
            while self._animation_active:
                for char in ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']:
                    if not self._animation_active:
                        break
                    
                    # Update the line with animated character
                    print(f'\r{char} {test_name}...', end='', flush=True)
                    time.sleep(0.1)
        
        self._animation_thread = threading.Thread(target=animate, daemon=True)
        self._animation_thread.start()
    
    def _stop_animation(self):
        """Stop animated indicator"""
        self._animation_active = False
        if self._animation_thread:
            self._animation_thread.join(timeout=0.5)
    
    def print_progress_update(self, message: str, percentage: Optional[int] = None):
        """Print progress update during long operations"""
        if self.style == IndicatorStyle.MINIMAL:
            print(f"  {message}")
            return
        
        progress_icon = self.get_status_icon('info')
        
        if percentage is not None:
            progress_bar = self._create_progress_bar(percentage, 100, 15)
            print(f"   {progress_icon} {message} {progress_bar}")
        else:
            print(f"   {progress_icon} {message}")
    
    def print_summary(self, total_tests: int, passed: int, failed: int, 
                     total_duration: float, success_rate: float):
        """Print enhanced test summary"""
        
        if self.style == IndicatorStyle.MINIMAL:
            print(f"Tests: {passed}/{total_tests} passed ({success_rate:.1f}%)")
            return
        
        # Rich summary
        separator = "=" * min(50, self.terminal_width - 10)
        
        print()
        print("📊 Test Summary")
        print(separator)
        
        # Summary metrics
        summary_items = [
            ("Total Tests", str(total_tests)),
            ("✅ Passed", str(passed)),
            ("❌ Failed", str(failed)),
            ("⏱️ Duration", f"{total_duration:.2f}s"),
            ("📈 Success Rate", f"{success_rate:.1f}%")
        ]
        
        for label, value in summary_items:
            print(f"{label}: {value}")
        
        print()
        
        # Failed tests details
        if failed > 0:
            print("❌ Failed Tests:")
            for test_name, result in self._test_results.items():
                if result['status'] == 'failed':
                    print(f"   • {test_name}: {result['message']}")
            print()
        
        # Overall status
        if failed == 0:
            status_icon = self.get_status_icon('success')
            status_text = "ALL TESTS PASSED"
        else:
            status_icon = self.get_status_icon('failed')
            status_text = f"{failed} TEST(S) FAILED"
        
        print(f"🎯 Overall Status: {status_icon} {status_text}")
        print(separator)
    
    def print_section_header(self, section_name: str):
        """Print section header for test categories"""
        if self.style == IndicatorStyle.MINIMAL:
            print(f"\n{section_name}:")
            return
        
        print(f"\n📋 {section_name}")
        print("-" * min(30, self.terminal_width - 10))
    
    def print_info_box(self, title: str, items: List[str]):
        """Print information box with items"""
        if self.style == IndicatorStyle.MINIMAL:
            print(f"\n{title}:")
            for item in items:
                print(f"  {item}")
            return
        
        print(f"\n💡 {title}")
        for item in items:
            bullet = "•" if self.supports_unicode else "*"
            print(f"   {bullet} {item}")
        print()
    
    def print_success_celebration(self, message: str):
        """Print success celebration message"""
        if self.style == IndicatorStyle.MINIMAL:
            print(f"Success: {message}")
            return
        
        celebration_icon = self.get_status_icon('success')
        print(f"\n{celebration_icon} {message}")
        
        if self.style in [IndicatorStyle.RICH, IndicatorStyle.ANIMATED]:
            # Add some visual flair
            if self.supports_unicode:
                print("🚀 Your LLM Hub is ready to use!")
            else:
                print("Your LLM Hub is ready to use!")
    
    def cleanup(self):
        """Clean up any active animations or threads"""
        if self._animation_active:
            self._stop_animation()


# Global instance for easy access
default_indicators = VisualIndicators()


def set_indicator_style(style: IndicatorStyle):
    """Set the global indicator style"""
    global default_indicators
    default_indicators = VisualIndicators(style)


def get_indicators() -> VisualIndicators:
    """Get the global indicators instance"""
    return default_indicators
