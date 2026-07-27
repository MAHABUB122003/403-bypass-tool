#!/usr/bin/env python3
"""
Core bypass manager - Orchestrates all bypass techniques
"""

import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse, urljoin, quote, unquote
from colorama import Fore, Style, init
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

init(autoreset=True)

class Color:
    RED = Fore.RED
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE
    MAGENTA = Fore.MAGENTA
    CYAN = Fore.CYAN
    WHITE = Fore.WHITE
    RESET = Style.RESET_ALL
    BOLD = Style.BRIGHT

class BypassManager:
    def __init__(self, target_url, verbose=False, threads=10, timeout=10, proxy=None):
        self.target_url = target_url.rstrip('/')
        self.verbose = verbose
        self.threads = threads
        self.timeout = timeout
        self.proxy = proxy
        self.results = []
        self.successful_bypasses = []
        self.base_response = None
        
    def get_base_response(self):
        """Get initial response for comparison"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive'
            }
            
            # Make the request
            resp = requests.get(
                self.target_url,
                headers=headers,
                verify=False,
                timeout=self.timeout,
                allow_redirects=True
            )
            
            # Store and return the response
            self.base_response = resp
            if self.verbose:
                print(f"{Color.GREEN}[+] Connected successfully! Status: {resp.status_code}")
            
            # CRITICAL: Return the response
            return resp
            
        except requests.exceptions.Timeout:
            if self.verbose:
                print(f"{Color.RED}[!] Connection timeout after {self.timeout}s")
            return None
        except requests.exceptions.ConnectionError as e:
            if self.verbose:
                print(f"{Color.RED}[!] Connection error: {e}")
            return None
        except Exception as e:
            if self.verbose:
                print(f"{Color.RED}[!] Unexpected error: {e}")
            return None

    def test_bypass(self, technique_name, modified_url, headers=None, method='GET', data=None):
        """Test a single bypass technique"""
        try:
            # Base headers
            base_headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive'
            }
            
            if headers:
                base_headers.update(headers)
            
            # Make request
            if method.upper() == 'POST':
                resp = requests.post(
                    modified_url,
                    headers=base_headers,
                    data=data,
                    verify=False,
                    timeout=self.timeout,
                    allow_redirects=True
                )
            else:
                resp = requests.get(
                    modified_url,
                    headers=base_headers,
                    verify=False,
                    timeout=self.timeout,
                    allow_redirects=True
                )

            # Check if bypass successful
            if resp.status_code != 403:
                result = {
                    'technique': technique_name,
                    'url': modified_url,
                    'method': method,
                    'status_code': resp.status_code,
                    'headers': dict(resp.headers),
                    'content_length': len(resp.text),
                    'success': True
                }

                if resp.status_code in [200, 201, 202, 204, 301, 302, 303, 307, 308]:
                    result['bypass_type'] = 'SUCCESS'
                    self.successful_bypasses.append(result)
                else:
                    result['bypass_type'] = 'PARTIAL'

                if self.verbose:
                    print(f"{Color.GREEN}[+] BYPASS FOUND: {technique_name} -> {resp.status_code}")

                return result
            else:
                if self.verbose:
                    print(f"{Color.YELLOW}[-] {technique_name} -> 403")
                return None

        except Exception as e:
            if self.verbose:
                print(f"{Color.RED}[!] Error in {technique_name}: {e}")
            return None

    def run_all_bypasses(self):
        """Run all bypass techniques"""
        print(f"{Color.CYAN}[*] Connecting to target...")
        
        # Get base response
        response = self.get_base_response()
        
        if response is None:
            print(f"{Color.RED}[!] Target unreachable or not responding")
            print(f"{Color.YELLOW}[!] Try: --timeout 30 or check your internet connection")
            return []

        print(f"{Color.CYAN}[*] Target: {self.target_url}")
        print(f"{Color.CYAN}[*] Base Status: {response.status_code}")
        print(f"{Color.CYAN}[*] Server: {response.headers.get('Server', 'Unknown')}")

        if response.status_code != 403:
            print(f"{Color.GREEN}[+] Target is accessible! Status: {response.status_code}")
            return []

        print(f"{Color.YELLOW}[*] Starting 403 bypass techniques...")
        print(f"{Color.YELLOW}[*] This may take a few minutes...")

        # Import bypass modules
        try:
            from core.headers import HeaderBypass
            from core.paths import PathBypass
            from core.methods import MethodBypass
            from core.protocols import ProtocolBypass
            from core.cdn_bypass import CDNBypass
            from core.cache_bypass import CacheBypass
            from core.waf_bypass import WAFBypass
        except ImportError as e:
            print(f"{Color.RED}[!] Error importing bypass modules: {e}")
            return []

        # Initialize bypass modules
        bypass_modules = [
            HeaderBypass(self),
            PathBypass(self),
            MethodBypass(self),
            ProtocolBypass(self),
            CDNBypass(self),
            CacheBypass(self),
            WAFBypass(self)
        ]

        all_tests = []
        for module in bypass_modules:
            try:
                tests = module.get_tests()
                all_tests.extend(tests)
            except Exception as e:
                if self.verbose:
                    print(f"{Color.RED}[!] Error getting tests: {e}")

        print(f"{Color.CYAN}[*] Total bypass techniques: {len(all_tests)}")
        print(f"{Color.YELLOW}[*] Running bypass tests...")

        # Run tests with thread pool
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = []
            for test in all_tests:
                future = executor.submit(
                    self.test_bypass,
                    test['name'],
                    test['url'],
                    test.get('headers', {}),
                    test.get('method', 'GET'),
                    test.get('data', None)
                )
                futures.append(future)

            # Process results
            for future in as_completed(futures):
                try:
                    result = future.result()
                    if result and result.get('success'):
                        self.results.append(result)
                except Exception as e:
                    if self.verbose:
                        print(f"{Color.RED}[!] Error processing result: {e}")

        self.print_summary()
        return self.results

    def print_summary(self):
        """Print summary"""
        print(f"\n{Color.BOLD}{'='*60}")
        print(f"{Color.BOLD}BYPASS SUMMARY")
        print(f"{Color.BOLD}{'='*60}")

        if not self.results:
            print(f"{Color.RED}[!] No bypass techniques worked")
            return

        print(f"{Color.GREEN}[+] Total successful bypasses: {len(self.results)}")
        print(f"{Color.GREEN}[+] Unique bypass types: {len(set(r['technique'] for r in self.results))}")

        print(f"\n{Color.BOLD}SUCCESSFUL BYPASSES:")
        for i, result in enumerate(self.results, 1):
            print(f"{Color.GREEN}{i}. {result['technique']}")
            print(f"   URL: {result['url']}")
            print(f"   Status: {result['status_code']}")
            print(f"   Content Length: {result['content_length']}")
            print()

        print(f"{Color.BOLD}{'='*60}")
