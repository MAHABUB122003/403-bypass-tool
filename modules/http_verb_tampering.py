#!/usr/bin/env python3
"""
HTTP verb tampering bypass techniques
"""

class HTTPVerbTampering:
    def __init__(self, manager):
        self.manager = manager
        
    def get_tests(self):
        """Generate HTTP verb tampering tests"""
        tests = []
        base_url = self.manager.target_url
        
        # HTTP methods
        methods = [
            'GET', 'POST', 'PUT', 'DELETE', 'PATCH', 
            'HEAD', 'OPTIONS', 'TRACE', 'CONNECT',
            'PROPFIND', 'PROPPATCH', 'MKCOL', 'COPY', 'MOVE',
            'LOCK', 'UNLOCK', 'SEARCH', 'REPORT', 'MERGE',
            'UPDATE', 'PURGE', 'ACL', 'BIND', 'CHECKOUT',
            'LINK', 'UNLINK', 'NOTIFY', 'SUBSCRIBE', 'UNSUBSCRIBE',
            'POLL', 'XCMS', 'XMS', 'INDEX', 'TRACK',
            'MGET', 'HEADER', 'GETALL', 'LIST', 'FIND',
            'VIEW', 'BASELINE-CONTROL', 'ORDERPATCH', 'CHECKIN',
            'UNCHECKOUT', 'VERSION-CONTROL'
        ]
        
        # Test each method
        for method in methods:
            # Normal request
            tests.append({
                'name': f'HTTP Verb: {method}',
                'url': base_url,
                'headers': {},
                'method': method
            })
            
            # With parameter
            tests.append({
                'name': f'HTTP Verb + Param: {method}',
                'url': base_url + '?test=1',
                'headers': {},
                'method': method
            })
            
            # With custom header
            tests.append({
                'name': f'HTTP Verb + Header: {method}',
                'url': base_url,
                'headers': {'X-Test': 'bypass'},
                'method': method
            })
        
        # Method override via headers
        override_methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS']
        override_headers = [
            'X-HTTP-Method-Override',
            'X-Method-Override',
            'X-Original-Method',
            'X-HTTP-Method',
            'HTTP-Method-Override',
            '_method',
            'method',
            'X-FORWARDED-METHOD'
        ]
        
        for override_header in override_headers:
            for override_method in override_methods:
                tests.append({
                    'name': f'Method Override: {override_header}={override_method}',
                    'url': base_url,
                    'headers': {override_header: override_method},
                    'method': 'POST'
                })
                
                # Also test with GET
                tests.append({
                    'name': f'Method Override GET: {override_header}={override_method}',
                    'url': base_url,
                    'headers': {override_header: override_method},
                    'method': 'GET'
                })
        
        # Method tampering with body
        methods_with_body = ['POST', 'PUT', 'PATCH']
        for method in methods_with_body:
            tests.append({
                'name': f'Method + Body: {method}',
                'url': base_url,
                'headers': {'Content-Type': 'application/x-www-form-urlencoded'},
                'method': method,
                'data': 'test=1&bypass=2'
            })
        
        # Verb tampering with different content types
        content_types = [
            'application/x-www-form-urlencoded',
            'multipart/form-data',
            'application/json',
            'application/xml',
            'text/plain',
            'text/html'
        ]
        
        for content_type in content_types:
            tests.append({
                'name': f'Verb + Content-Type: {content_type}',
                'url': base_url,
                'headers': {'Content-Type': content_type},
                'method': 'POST',
                'data': 'test=1'
            })
        
        return tests
