#!/usr/bin/env python3
"""
HTTP method-based bypass techniques
"""

class MethodBypass:
    def __init__(self, manager):
        self.manager = manager
        
    def get_tests(self):
        """Generate HTTP method bypass tests"""
        tests = []
        base_url = self.manager.target_url
        
        # All HTTP methods to test
        methods = [
            'GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 
            'OPTIONS', 'TRACE', 'CONNECT', 'PROPFIND', 'PROPPATCH',
            'MKCOL', 'COPY', 'MOVE', 'LOCK', 'UNLOCK',
            'SEARCH', 'REPORT', 'MERGE', 'UPDATE', 'PURGE',
            'ACL', 'BIND', 'CHECKOUT', 'LINK', 'UNLINK',
            'NOTIFY', 'SUBSCRIBE', 'UNSUBSCRIBE', 'POLL',
            'XCMS', 'XMS', 'INDEX', 'TRACK', 'MGET',
            'HEADER', 'GETALL', 'LIST', 'FIND', 'VIEW',
            'BASELINE-CONTROL', 'ORDERPATCH', 'PATCH',
            'CHECKIN', 'CHECKOUT', 'UNCHECKOUT', 'VERSION-CONTROL'
        ]
        
        # Test each method
        for method in methods:
            tests.append({
                'name': f'HTTP Method Bypass: {method}',
                'url': base_url,
                'headers': {},
                'method': method
            })
            
            # Test with parameter
            tests.append({
                'name': f'HTTP Method + Param: {method}',
                'url': base_url + '?test=1',
                'headers': {},
                'method': method
            })
        
        # Method override via headers
        override_headers = [
            {'X-HTTP-Method-Override': 'GET'},
            {'X-HTTP-Method-Override': 'POST'},
            {'X-HTTP-Method-Override': 'PUT'},
            {'X-HTTP-Method-Override': 'DELETE'},
            {'X-HTTP-Method-Override': 'PATCH'},
            {'X-Method-Override': 'GET'},
            {'X-Method-Override': 'POST'},
            {'X-Original-Method': 'GET'},
            {'X-Original-Method': 'POST'},
            {'_method': 'GET'},
            {'_method': 'POST'},
            {'method': 'GET'},
            {'method': 'POST'},
            {'X-HTTP-Method': 'GET'},
            {'X-HTTP-Method': 'POST'},
            {'HTTP-Method-Override': 'GET'},
            {'HTTP-Method-Override': 'POST'},
        ]
        
        for headers in override_headers:
            tests.append({
                'name': f'Method Override: {list(headers.keys())[0]}={list(headers.values())[0]}',
                'url': base_url,
                'headers': headers,
                'method': 'POST'
            })
            
            # Also test with GET
            tests.append({
                'name': f'Method Override GET: {list(headers.keys())[0]}={list(headers.values())[0]}',
                'url': base_url,
                'headers': headers,
                'method': 'GET'
            })
        
        return tests
