#!/usr/bin/env python3
"""
Cache-based bypass techniques
"""

import time
import random
import urllib.parse

class CacheBypass:
    def __init__(self, manager):
        self.manager = manager
        
    def get_tests(self):
        """Generate cache bypass tests"""
        tests = []
        base_url = self.manager.target_url
        
        # Cache buster parameters
        cache_busters = [
            f'?cache={int(time.time())}',
            f'?ts={int(time.time())}',
            f'?t={int(time.time())}',
            f'?_={int(time.time())}',
            f'?random={random.randint(1, 999999)}',
            f'?nocache={random.randint(1, 999999)}',
            f'?refresh={random.randint(1, 999999)}',
            f'?v={random.randint(1, 999999)}',
            f'?ver={random.randint(1, 999999)}',
            f'?version={random.randint(1, 999999)}',
            f'?cb={random.randint(1, 999999)}',
            f'?cachebuster={random.randint(1, 999999)}',
            f'?r={random.randint(1, 999999)}',
            f'?rand={random.randint(1, 999999)}',
            f'?{random.randint(1, 999999)}',
            f'?x={random.randint(1, 999999)}',
            f'?test={random.randint(1, 999999)}',
            f'?a={random.randint(1, 999999)}',
            f'?b={random.randint(1, 999999)}',
            f'?c={random.randint(1, 999999)}',
        ]
        
        # Cache bypass headers
        cache_headers = [
            {'Cache-Control': 'no-cache'},
            {'Cache-Control': 'no-store'},
            {'Cache-Control': 'max-age=0'},
            {'Cache-Control': 'must-revalidate'},
            {'Cache-Control': 'no-cache, no-store, must-revalidate'},
            {'Pragma': 'no-cache'},
            {'Expires': '0'},
            {'Expires': '-1'},
            {'If-Modified-Since': 'Thu, 01 Jan 1970 00:00:00 GMT'},
            {'If-None-Match': '0'},
            {'If-None-Match': '*'},
            {'X-Cache-Status': 'BYPASS'},
            {'X-Cache-Status': 'MISS'},
            {'Cache-Status': 'BYPASS'},
            {'Cache-Status': 'MISS'},
            {'X-HTTP-Cache': 'BYPASS'},
        ]
        
        # Test cache busters
        for buster in cache_busters:
            # Add to URL
            url = base_url
            if '?' in base_url:
                url = base_url + '&' + buster.lstrip('?')
            else:
                url = base_url + buster
            
            tests.append({
                'name': f'Cache Buster: {buster[:20]}...',
                'url': url,
                'headers': {},
                'method': 'GET'
            })
        
        # Test cache headers
        for headers in cache_headers:
            tests.append({
                'name': f'Cache Header: {list(headers.keys())[0]}={list(headers.values())[0]}',
                'url': base_url,
                'headers': headers,
                'method': 'GET'
            })
        
        # Test double parameters
        double_params = [
            '?cache=1&cache=2',
            '?random=1&random=2',
            '?a=1&a=2',
            '?b=1&b=2',
            '?x=1&x=2',
            '?test=1&test=2',
            '?ver=1&ver=2',
            '?v=1&v=2',
            '?nocache=1&nocache=2',
            '?refresh=1&refresh=2',
        ]
        
        for params in double_params:
            url = base_url + params
            tests.append({
                'name': f'Double Parameter: {params[:20]}...',
                'url': url,
                'headers': {},
                'method': 'GET'
            })
        
        # Test with different methods
        cache_methods = ['GET', 'POST', 'HEAD']
        for method in cache_methods:
            tests.append({
                'name': f'Cache Method: {method}',
                'url': base_url,
                'headers': {'Cache-Control': 'no-cache'},
                'method': method
            })
        
        return tests
