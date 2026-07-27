#!/usr/bin/env python3
"""
Extension trick bypass techniques
"""

import urllib.parse

class ExtensionTricks:
    def __init__(self, manager):
        self.manager = manager
        
    def get_tests(self):
        """Generate extension trick tests"""
        tests = []
        base_url = self.manager.target_url
        parsed = urllib.parse.urlparse(base_url)
        path = parsed.path if parsed.path else '/'
        
        # Common extensions
        extensions = [
            '.html', '.htm', '.php', '.asp', '.aspx', '.jsp', '.jspx',
            '.do', '.action', '.cgi', '.pl', '.py', '.rb', '.go',
            '.txt', '.xml', '.json', '.yml', '.yaml', '.ini',
            '.conf', '.config', '.htaccess', '.htpasswd', '.env',
            '.bak', '.backup', '.old', '.orig', '.tmp', '.temp',
            '.swp', '.swo', '.save', '.sav', '.~', '.~1',
            '.php3', '.php4', '.php5', '.php7', '.phps',
            '.phtml', '.php~', '.phar', '.inc', '.class',
            '.module', '.theme', '.info', '.install', '.profile',
            '.test', '.sample', '.example', '.demo',
        ]
        
        # Extension variations
        for ext in extensions:
            # Add extension to path
            new_path = path + ext
            url = urllib.parse.urlunparse((
                parsed.scheme,
                parsed.netloc,
                new_path,
                parsed.params,
                parsed.query,
                parsed.fragment
            ))
            tests.append({
                'name': f'Extension Trick: {ext}',
                'url': url,
                'headers': {},
                'method': 'GET'
            })
            
            # Replace extension
            if '.' in path:
                base = path.rsplit('.', 1)[0]
                new_path = base + ext
                url = urllib.parse.urlunparse((
                    parsed.scheme,
                    parsed.netloc,
                    new_path,
                    parsed.params,
                    parsed.query,
                    parsed.fragment
                ))
                tests.append({
                    'name': f'Extension Replace: {ext}',
                    'url': url,
                    'headers': {},
                    'method': 'GET'
                })
        
        # Double extensions
        double_extensions = [
            '.php.html', '.html.php', '.php.jpg', '.jpg.php',
            '.png.php', '.gif.php', '.php.txt', '.txt.php',
            '.php.bak', '.php.backup', '.php.old', '.php~',
            '.asp.html', '.aspx.html', '.jsp.html',
        ]
        
        for ext in double_extensions:
            new_path = path + ext
            url = urllib.parse.urlunparse((
                parsed.scheme,
                parsed.netloc,
                new_path,
                parsed.params,
                parsed.query,
                parsed.fragment
            ))
            tests.append({
                'name': f'Double Extension: {ext}',
                'url': url,
                'headers': {},
                'method': 'GET'
            })
        
        # URL rewriting tricks
        rewrite_tricks = [
            path + '/?',
            path + '?',
            path + '#',
            path + '/*',
            path + '/%00',
            path + '/%20',
            path + '/%09',
            path + '/%0a',
            path + '/%0d',
            path + '/.',
            path + '/..',
            path + '/;',
            path + '/%3b',
            path + '/?test',
            path + '?test=1',
            path + '?id=1',
            path + '?q=1',
            path + '?page=1',
            path + '?file=1',
            path + '?dir=1',
        ]
        
        for trick in rewrite_tricks:
            if trick != path:
                url = urllib.parse.urlunparse((
                    parsed.scheme,
                    parsed.netloc,
                    trick,
                    parsed.params,
                    parsed.query,
                    parsed.fragment
                ))
                tests.append({
                    'name': f'Rewrite Trick: {trick[:30]}...',
                    'url': url,
                    'headers': {},
                    'method': 'GET'
                })
        
        # Path with different separators
        separators = ['/', '\\', '//', '\\\\', '/\\', '\\/', '///']
        for sep in separators:
            new_path = path.replace('/', sep)
            if new_path != path:
                url = urllib.parse.urlunparse((
                    parsed.scheme,
                    parsed.netloc,
                    new_path,
                    parsed.params,
                    parsed.query,
                    parsed.fragment
                ))
                tests.append({
                    'name': f'Separator Trick: {sep}',
                    'url': url,
                    'headers': {},
                    'method': 'GET'
                })
        
        return tests
