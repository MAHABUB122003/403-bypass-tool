#!/usr/bin/env python3
"""
Network utilities
"""

import socket
import requests
import dns.resolver
import ipaddress

class NetworkUtils:
    def __init__(self):
        self.session = requests.Session()
        self.session.verify = False
        
    def resolve_domain(self, domain):
        """Resolve domain to IP address"""
        try:
            ips = []
            answers = dns.resolver.resolve(domain, 'A')
            for rdata in answers:
                ips.append(str(rdata))
            return ips
        except:
            try:
                return [socket.gethostbyname(domain)]
            except:
                return []
    
    def resolve_cname(self, domain):
        """Resolve domain CNAME record"""
        try:
            answers = dns.resolver.resolve(domain, 'CNAME')
            return [str(rdata.target) for rdata in answers]
        except:
            return []
    
    def resolve_mx(self, domain):
        """Resolve domain MX records"""
        try:
            answers = dns.resolver.resolve(domain, 'MX')
            return [str(rdata.exchange) for rdata in answers]
        except:
            return []
    
    def check_port(self, host, port, timeout=5):
        """Check if port is open"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except:
            return False
    
    def get_ip_geolocation(self, ip):
        """Get IP geolocation (simplified)"""
        try:
            response = requests.get(f'http://ip-api.com/json/{ip}', timeout=10)
            if response.status_code == 200:
                data = response.json()
                return {
                    'country': data.get('country'),
                    'city': data.get('city'),
                    'region': data.get('regionName'),
                    'isp': data.get('isp'),
                    'org': data.get('org'),
                    'timezone': data.get('timezone'),
                }
        except:
            pass
        return {}
    
    def is_cloudflare(self, domain):
        """Check if domain uses Cloudflare"""
        try:
            ips = self.resolve_domain(domain)
            for ip in ips:
                if ip in ['104.16.0.0/12', '104.24.0.0/13', '172.64.0.0/13', '131.0.72.0/22']:
                    return True
        except:
            pass
        
        # Check HTTP response
        try:
            response = requests.get(f'http://{domain}', timeout=10, allow_redirects=False)
            if 'cloudflare' in response.headers.get('Server', '').lower():
                return True
            if 'cf-ray' in response.headers:
                return True
        except:
            pass
        
        return False
    
    def get_cdn_provider(self, domain):
        """Detect CDN provider"""
        try:
            # Check Cloudflare
            if self.is_cloudflare(domain):
                return 'Cloudflare'
            
            # Check AWS CloudFront
            cname = self.resolve_cname(domain)
            for record in cname:
                if 'cloudfront.net' in record:
                    return 'AWS CloudFront'
                if 'akamai.net' in record:
                    return 'Akamai'
                if 'fastly.net' in record:
                    return 'Fastly'
                if 'cdn.net' in record:
                    return 'CDN'
            
            # Check from headers
            try:
                response = requests.get(f'http://{domain}', timeout=10, allow_redirects=False)
                headers = {k.lower(): v.lower() for k, v in response.headers.items()}
                
                if 'x-served-by' in headers and 'fastly' in headers['x-served-by']:
                    return 'Fastly'
                if 'x-amz-cf-id' in headers:
                    return 'AWS CloudFront'
                if 'cf-ray' in headers:
                    return 'Cloudflare'
                if 'akamai' in headers.get('server', ''):
                    return 'Akamai'
            except:
                pass
        except:
            pass
        
        return 'Unknown'
