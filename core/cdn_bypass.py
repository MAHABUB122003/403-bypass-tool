#!/usr/bin/env python3
"""
CDN-specific bypass techniques
"""

import socket
import urllib.parse

class CDNBypass:
    def __init__(self, manager):
        self.manager = manager
        
    def get_tests(self):
        """Generate CDN bypass tests"""
        tests = []
        base_url = self.manager.target_url
        parsed = urllib.parse.urlparse(base_url)
        domain = parsed.netloc.split(':')[0] if parsed.netloc else ''
        
        # Try to find origin IP
        origin_ips = self.find_origin_ips(domain)
        
        # Test with origin IP
        for ip in origin_ips:
            ip_url = base_url.replace(domain, ip)
            tests.append({
                'name': f'CDN Origin IP Bypass: {ip}',
                'url': ip_url,
                'headers': {'Host': domain},
                'method': 'GET'
            })
            
            # Try with different Host header
            tests.append({
                'name': f'CDN Origin IP + Host: {ip}',
                'url': ip_url,
                'headers': {'Host': domain, 'X-Forwarded-Host': domain},
                'method': 'GET'
            })
        
        # Cloudflare specific bypass
        cf_headers = [
            {'CF-Connecting-IP': '127.0.0.1'},
            {'CF-Connecting-IP': '0.0.0.0'},
            {'CF-Connecting-IP': 'localhost'},
            {'True-Client-IP': '127.0.0.1'},
            {'X-Forwarded-For': '127.0.0.1, 10.0.0.1'},
            {'X-Forwarded-For': '127.0.0.1, 192.168.1.1'},
            {'X-Forwarded-For': '127.0.0.1, 172.16.0.1'},
            {'CDN-Loop': 'cloudflare'},
            {'CDN-Loop': 'cloudflare; loops=1'},
        ]
        
        for headers in cf_headers:
            tests.append({
                'name': f'Cloudflare Bypass: {list(headers.keys())[0]}={list(headers.values())[0]}',
                'url': base_url,
                'headers': headers,
                'method': 'GET'
            })
        
        # AWS CloudFront bypass
        aws_headers = [
            {'X-Forwarded-For': '127.0.0.1, 10.0.0.1'},
            {'X-Forwarded-For': '127.0.0.1, 172.16.0.1'},
            {'X-Forwarded-For': '127.0.0.1, 192.168.1.1'},
            {'CloudFront-Forwarded-Proto': 'http'},
            {'CloudFront-Forwarded-Proto': 'https'},
            {'CloudFront-Is-Desktop-Viewer': 'true'},
            {'CloudFront-Is-Mobile-Viewer': 'false'},
            {'CloudFront-Is-Tablet-Viewer': 'false'},
            {'CloudFront-Is-SmartTV-Viewer': 'false'},
        ]
        
        for headers in aws_headers:
            tests.append({
                'name': f'AWS CloudFront Bypass: {list(headers.keys())[0]}={list(headers.values())[0]}',
                'url': base_url,
                'headers': headers,
                'method': 'GET'
            })
        
        # Akamai bypass
        akamai_headers = [
            {'X-Akamai-Transformed': '1'},
            {'X-Akamai-Transformed': '9'},
            {'X-Akamai-Transformed': '100'},
            {'True-Client-IP': '127.0.0.1'},
            {'X-Forwarded-For': '127.0.0.1, 10.0.0.1'},
        ]
        
        for headers in akamai_headers:
            tests.append({
                'name': f'Akamai Bypass: {list(headers.keys())[0]}={list(headers.values())[0]}',
                'url': base_url,
                'headers': headers,
                'method': 'GET'
            })
        
        # Fastly bypass
        fastly_headers = [
            {'X-Forwarded-For': '127.0.0.1, 10.0.0.1'},
            {'X-Forwarded-For': '127.0.0.1, 192.168.1.1'},
            {'Fastly-Client-IP': '127.0.0.1'},
            {'Fastly-Client-IP': '0.0.0.0'},
            {'X-Cache': 'HIT'},
            {'X-Cache': 'MISS'},
        ]
        
        for headers in fastly_headers:
            tests.append({
                'name': f'Fastly Bypass: {list(headers.keys())[0]}={list(headers.values())[0]}',
                'url': base_url,
                'headers': headers,
                'method': 'GET'
            })
        
        return tests
    
    def find_origin_ips(self, domain):
        """Find origin IPs for CDN bypass"""
        ips = []
        
        # Try DNS resolution
        try:
            ips.append(socket.gethostbyname(domain))
        except:
            pass
        
        # Common origin IP patterns
        common_ips = [
            '1.1.1.1', '8.8.8.8', '8.8.4.4',
            '192.168.1.1', '192.168.0.1', '10.0.0.1',
            '172.16.0.1', '172.31.255.255',
            '127.0.0.1', '0.0.0.0'
        ]
        
        ips.extend(common_ips)
        
        # Try to get historical IPs (simplified)
        # In real implementation, you'd use services like SecurityTrails, Censys, etc.
        
        return list(set(ips))
