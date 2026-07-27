#!/usr/bin/env python3
"""
403.py - Advanced 403 Bypass Tool for Bug Bounty & Pentesting
"""

import argparse
import sys
import os
import time
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from core.bypass_manager import BypassManager
    from utils.reporter import Reporter
    from utils.logger import Logger
except ImportError as e:
    print(f"{Fore.RED}[!] Error importing modules: {e}")
    print(f"{Fore.YELLOW}[*] Make sure you're in the correct directory")
    sys.exit(1)

class Main:
    def __init__(self):
        self.args = None
        self.reporter = None
        self.logger = None
        
    def parse_arguments(self):
        parser = argparse.ArgumentParser(
            description=f'{Fore.CYAN}🔥 Advanced 403 Bypass Tool for Bug Bounty{Fore.RESET}',
            epilog=f'{Fore.GREEN}Example: ./403.py -u https://target.com/admin -v -t 20{Fore.RESET}',
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        
        parser.add_argument('-u', '--url', required=True,
                          help='Target URL (e.g., https://target.com/admin)')
        parser.add_argument('-v', '--verbose', action='store_true',
                          help='Enable verbose output')
        parser.add_argument('-t', '--threads', type=int, default=20,
                          help='Number of threads (default: 20)')
        parser.add_argument('--timeout', type=int, default=10,
                          help='Request timeout in seconds (default: 10)')
        parser.add_argument('--proxy', type=str,
                          help='Proxy (e.g., http://127.0.0.1:8080)')
        parser.add_argument('-o', '--output', type=str,
                          help='Output file for results')
        parser.add_argument('--format', choices=['json', 'html', 'text', 'csv'],
                          default='text', help='Output format (default: text)')
        parser.add_argument('--quick', action='store_true',
                          help='Quick scan (limited techniques)')
        parser.add_argument('--no-cdn', action='store_true',
                          help='Disable CDN bypass techniques')
        parser.add_argument('--no-waf', action='store_true',
                          help='Disable WAF bypass techniques')
        parser.add_argument('--no-cache', action='store_true',
                          help='Disable cache bypass techniques')
        
        self.args = parser.parse_args()
        
        # Validate URL
        if not self.args.url.startswith(('http://', 'https://')):
            self.args.url = 'https://' + self.args.url
        
        return self.args
    
    def print_banner(self):
        """Print tool banner"""
        banner = f"""
{Fore.RED}  _____   _____   _____  
{Fore.YELLOW} |  __ \\ |  __ \\ |  __ \\ 
{Fore.GREEN} | |__) || |__) || |__) |
{Fore.CYAN} |  ___/ |  ___/ |  ___/ 
{Fore.BLUE} | |     | |     | |     
{Fore.MAGENTA} |_|     |_|     |_|     
{Fore.RESET}
{Style.BRIGHT}🔥 403 BYPASS TOOL v3.0 🔥{Fore.RESET}
{Fore.CYAN}⚡ Advanced Bug Bounty & Pentesting Tool{Fore.RESET}
{Fore.YELLOW}📡 50+ Bypass Techniques | 7 Bypass Categories{Fore.RESET}
        """
        print(banner)
    
    def run(self):
        """Main execution"""
        try:
            # Parse arguments
            self.args = self.parse_arguments()
            
            # Print banner
            self.print_banner()
            
            # Initialize logger
            self.logger = Logger()
            
            # Initialize reporter
            self.reporter = Reporter()
            
            # Print configuration
            print(f"{Fore.CYAN}[*] Target: {self.args.url}")
            print(f"{Fore.CYAN}[*] Threads: {self.args.threads}")
            print(f"{Fore.CYAN}[*] Timeout: {self.args.timeout}s")
            if self.args.proxy:
                print(f"{Fore.CYAN}[*] Proxy: {self.args.proxy}")
            if self.args.verbose:
                print(f"{Fore.CYAN}[*] Verbose mode: ON")
            
            print()
            
            # Initialize bypass manager
            manager = BypassManager(
                target_url=self.args.url,
                verbose=self.args.verbose,
                threads=self.args.threads,
                timeout=self.args.timeout,
                proxy=self.args.proxy
            )
            
            # Run bypasses
            start_time = time.time()
            results = manager.run_all_bypasses()
            duration = time.time() - start_time
            
            # Store results in reporter
            for result in results:
                self.reporter.add_result(result)
            
            # Print final summary
            print(f"\n{Style.BRIGHT}{'='*70}")
            print(f"{Style.BRIGHT}FINAL SUMMARY")
            print(f"{Style.BRIGHT}{'='*70}")
            print(f"{Fore.GREEN}[+] Target: {self.args.url}")
            print(f"{Fore.GREEN}[+] Total Bypasses Found: {len(results)}")
            print(f"{Fore.GREEN}[+] Duration: {duration:.2f} seconds")
            
            if results:
                print(f"{Fore.GREEN}[+] Success Rate: {len(results)} bypasses found!")
                print(f"{Fore.GREEN}[+] Unique Techniques: {len(set(r.get('technique', 'Unknown') for r in results))}")
            else:
                print(f"{Fore.RED}[!] No bypasses found")
            
            print(f"{Style.BRIGHT}{'='*70}\n")
            
            # Generate report
            if self.args.output:
                report_content = self.reporter.generate_report(
                    format=self.args.format,
                    output_file=self.args.output
                )
            
            # Successful bypasses
            if results:
                print(f"{Fore.GREEN}{Style.BRIGHT}✅ SUCCESSFUL BYPASSES:{Fore.RESET}")
                for i, result in enumerate(results[:5], 1):
                    print(f"{Fore.GREEN}{i}. {result.get('technique', 'Unknown')}")
                    print(f"   {Fore.CYAN}URL: {result.get('url', 'N/A')}")
                    print(f"   {Fore.YELLOW}Status: {result.get('status_code', 'N/A')}")
                    print()
                
                if len(results) > 5:
                    print(f"{Fore.YELLOW}[!] ... and {len(results) - 5} more bypasses")
            
            print(f"{Style.BRIGHT}{'='*70}")
            print(f"{Fore.GREEN}✅ Scan completed!{Fore.RESET}")
            
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[!] Scan interrupted by user")
            sys.exit(0)
        except Exception as e:
            print(f"{Fore.RED}[!] Error: {str(e)}")
            if self.args and self.args.verbose:
                import traceback
                traceback.print_exc()
            sys.exit(1)

if __name__ == "__main__":
    tool = Main()
    tool.run()
