#!/usr/bin/env python3
"""
Encoding bypass techniques
"""

import urllib.parse
import base64
import binascii

class EncodingBypass:
    def __init__(self, manager):
        self.manager = manager
        
    def get_tests(self):
        """Generate encoding bypass tests"""
        tests = []
        base_url = self.manager.target_url
        parsed = urllib.parse.urlparse(base_url)
        path = parsed.path if parsed.path else '/'
        
        # Different encodings
        encodings = [
            # URL encoding
            urllib.parse.quote(path, safe=''),
            urllib.parse.quote(path, safe='/'),
            urllib.parse.quote(path, safe=' /?=&'),
            urllib.parse.quote(path, safe='/:'),
            urllib.parse.quote_plus(path, safe=''),
            urllib.parse.quote_plus(path, safe='/'),
            
            # Double URL encoding
            urllib.parse.quote(urllib.parse.quote(path, safe=''), safe=''),
            urllib.parse.quote(urllib.parse.quote(path, safe='/'), safe='/'),
            urllib.parse.quote(urllib.parse.quote_plus(path, safe=''), safe=''),
            
            # Triple URL encoding
            urllib.parse.quote(urllib.parse.quote(urllib.parse.quote(path, safe=''), safe=''), safe=''),
            
            # UTF-8 encoding
            path.encode('utf-8').decode('unicode_escape'),
            path.encode('utf-8').decode('string_escape'),
            
            # Base64 encoding
            base64.b64encode(path.encode()).decode(),
            base64.b64encode(path.encode()).decode().rstrip('='),
            base64.urlsafe_b64encode(path.encode()).decode(),
            
            # Hex encoding
            path.encode('utf-8').hex(),
            binascii.hexlify(path.encode()).decode(),
            
            # HTML encoding
            path.replace('/', '&#47;'),
            path.replace('/', '&#x2F;'),
            path.replace('.', '&#46;'),
            path.replace('.', '&#x2E;'),
            
            # Unicode encoding
            path.replace('/', '\\u002f'),
            path.replace('/', '\\u2215'),
            path.replace('/', '\\u2044'),
            path.replace('/', '\\uFF0F'),
            
            # Unicode escape
            path.replace('/', '%u002f'),
            path.replace('/', '%u2215'),
            path.replace('/', '%u2044'),
            path.replace('/', '%uFF0F'),
            
            # IP encoding
            path.replace('.', '%2e'),
            path.replace('.', '%252e'),
            path.replace('.', '..'),
            path.replace('.', '/'),
            path.replace(':', '%3a'),
            path.replace(':', '%253a'),
            
            # Character encoding
            path.replace('a', '%61'),
            path.replace('b', '%62'),
            path.replace('c', '%63'),
            path.replace('d', '%64'),
            path.replace('e', '%65'),
            
            # Mixed encoding
            path.replace('/', '\\u002f').replace('.', '%2e'),
            path.replace('/', '%2f').replace('.', '\\u002e'),
        ]
        
        # Test encodings
        for encoded in set(encodings):
            if encoded != path:
                url = urllib.parse.urlunparse((
                    parsed.scheme,
                    parsed.netloc,
                    encoded,
                    parsed.params,
                    parsed.query,
                    parsed.fragment
                ))
                tests.append({
                    'name': f'Encoding Bypass: {encoded[:30]}...',
                    'url': url,
                    'headers': {},
                    'method': 'GET'
                })
        
        # Encoding with query parameters
        params = ['test', 'page', 'file', 'dir', 'path', 'include', 'template']
        values = ['test', 'admin', 'index', 'config', 'settings', 'passwd']
        
        for param in params:
            for value in values:
                encoded_value = urllib.parse.quote(value, safe='')
                url = base_url + '?' + param + '=' + encoded_value
                tests.append({
                    'name': f'Encoded Param: {param}={encoded_value}',
                    'url': url,
                    'headers': {},
                    'method': 'GET'
                })
        
        return tests
