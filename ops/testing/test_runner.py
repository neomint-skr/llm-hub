#!/usr/bin/env python3
"""
Enhanced Test Runner for LLM Hub
Supports multiple visual styles and output formats
"""

import asyncio
import sys
import argparse
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from show_me_framework import ShowMeTestFramework
from visual_indicators import IndicatorStyle


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="LLM Hub 'Show Me!' Test Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Visual Styles:
  minimal   - Simple text output, no colors or animations
  standard  - Standard visual feedback with icons and progress
  rich      - Enhanced visuals with detailed information
  animated  - Full animations and dynamic progress indicators

Examples:
  python test_runner.py                    # Run with standard visuals
  python test_runner.py --style minimal   # Run with minimal output
  python test_runner.py --style animated  # Run with full animations
  python test_runner.py --quiet           # Suppress non-essential output
        """
    )
    
    parser.add_argument(
        '--style',
        choices=['minimal', 'standard', 'rich', 'animated'],
        default='standard',
        help='Visual style for test output (default: standard)'
    )
    
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Suppress non-essential output'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output with detailed information'
    )
    
    parser.add_argument(
        '--no-color',
        action='store_true',
        help='Disable color output'
    )
    
    parser.add_argument(
        '--timeout',
        type=int,
        default=30,
        help='Timeout for individual tests in seconds (default: 30)'
    )
    
    return parser.parse_args()


def get_visual_style(args) -> IndicatorStyle:
    """Get visual style based on arguments"""
    if args.quiet:
        return IndicatorStyle.MINIMAL
    elif args.verbose:
        return IndicatorStyle.RICH
    else:
        style_map = {
            'minimal': IndicatorStyle.MINIMAL,
            'standard': IndicatorStyle.STANDARD,
            'rich': IndicatorStyle.RICH,
            'animated': IndicatorStyle.ANIMATED
        }
        return style_map[args.style]


async def run_tests_with_timeout(framework: ShowMeTestFramework, timeout: int) -> bool:
    """Run tests with timeout"""
    try:
        return await asyncio.wait_for(framework.run_all_tests(), timeout=timeout * 10)
    except asyncio.TimeoutError:
        print(f"\n❌ Tests timed out after {timeout * 10} seconds")
        return False


def print_usage_info(style: IndicatorStyle):
    """Print usage information"""
    if style == IndicatorStyle.MINIMAL:
        print("LLM Hub Test Runner")
        print("Testing system functionality...")
        return
    
    print("🚀 LLM Hub Enhanced Test Runner")
    print("=" * 50)
    print("Testing all components with visual feedback")
    print()


def print_environment_info(args):
    """Print environment information"""
    if args.style == 'minimal':
        return
    
    print("🔧 Test Configuration")
    print("-" * 30)
    print(f"Visual Style: {args.style}")
    print(f"Timeout: {args.timeout}s per test")
    print(f"Verbose: {'Yes' if args.verbose else 'No'}")
    print(f"Quiet Mode: {'Yes' if args.quiet else 'No'}")
    print()


async def main():
    """Main entry point"""
    args = parse_arguments()
    
    # Get visual style
    visual_style = get_visual_style(args)
    
    # Print environment info
    if not args.quiet:
        print_usage_info(visual_style)
        print_environment_info(args)
    
    # Create and run test framework
    framework = ShowMeTestFramework(visual_style)
    
    try:
        success = await run_tests_with_timeout(framework, args.timeout)
        
        if success:
            if not args.quiet:
                print("\n✅ All tests completed successfully!")
            sys.exit(0)
        else:
            if not args.quiet:
                print("\n❌ Some tests failed or timed out")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Tests interrupted by user")
        framework.indicators.cleanup()
        sys.exit(130)
    except Exception as e:
        print(f"\n💥 Test runner error: {e}")
        framework.indicators.cleanup()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
