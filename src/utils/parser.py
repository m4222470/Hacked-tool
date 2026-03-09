"""
CLI argument parsing utilities
"""

import argparse
from core.config_manager import (
    DEFAULT_REQUEST_DELAY,
    DEFAULT_SCORE_THRESHOLD_HIGH,
    DEFAULT_SCORE_THRESHOLD_MEDIUM,
    DEFAULT_MAX_CONCURRENT,
    DEFAULT_RATE_LIMIT,
    DEFAULT_GLOBAL_TIMEOUT,
    TOOL_VERSION,
    TOOL_NAME,
)

def create_parser() -> argparse.ArgumentParser:
    """Create CLI argument parser"""
    parser = argparse.ArgumentParser(
        description=f"{TOOL_NAME} v{TOOL_VERSION}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py -d example.com
  python main.py -d example.com --allowed sub.example.com --threshold-high 70
  python main.py -d example.com --max-concurrent 20 --rate-limit 15
        """
    )
    
    # Required arguments
    parser.add_argument("-d", "--domain", required=True, help="Target domain (required)")
    parser.add_argument("--allowed", nargs='+', help="Allowed domains to scan")
    
    # Performance options
    parser.add_argument("--delay", type=float, default=DEFAULT_REQUEST_DELAY, 
                       help=f"Request delay in seconds (default: {DEFAULT_REQUEST_DELAY})")
    parser.add_argument("--max-concurrent", type=int, default=DEFAULT_MAX_CONCURRENT,
                       help=f"Max concurrent requests (default: {DEFAULT_MAX_CONCURRENT})")
    parser.add_argument("--rate-limit", type=int, default=DEFAULT_RATE_LIMIT,
                       help=f"Requests per second (default: {DEFAULT_RATE_LIMIT})")
    parser.add_argument("--global-timeout", type=int, default=DEFAULT_GLOBAL_TIMEOUT,
                       help=f"Global timeout in seconds (default: {DEFAULT_GLOBAL_TIMEOUT})")
    
    # Output options
    parser.add_argument("--output", default="output/reports/results_final.json",
                       help="Output file path")
    parser.add_argument("--log-file", default="output/logs/scan.log", help="Log file path")
    
    # Scanning options
    parser.add_argument("--threshold-high", type=int, default=DEFAULT_SCORE_THRESHOLD_HIGH,
                       help=f"High score threshold (default: {DEFAULT_SCORE_THRESHOLD_HIGH})")
    parser.add_argument("--threshold-medium", type=int, default=DEFAULT_SCORE_THRESHOLD_MEDIUM,
                       help=f"Medium score threshold (default: {DEFAULT_SCORE_THRESHOLD_MEDIUM})")
    
    # Feature toggles
    parser.add_argument("--no-js", action="store_true", help="Disable JavaScript analysis")
    parser.add_argument("--no-hidden", action="store_true", help="Disable hidden file scanning")
    parser.add_argument("--hidden-scan", action="store_true", help="Enable deep hidden file scanning")
    parser.add_argument("--no-auth", action="store_true", help="Disable auth flow analysis")
    parser.add_argument("--max-js-domains", type=int, default=0, help="Max JS domains to scan")
    
    # Debug options
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--insecure", action="store_true", help="Disable SSL verification")
    parser.add_argument("-v", "--version", action="version", version=f"{TOOL_NAME} {TOOL_VERSION}")
    
    return parser

def parse_arguments():
    """Parse and return arguments"""
    parser = create_parser()
    return parser.parse_args()
