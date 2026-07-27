#!/usr/bin/env python3
"""
Case sensitivity bypass techniques
"""

class CaseSensitivityBypass:
    def __init__(self, manager):
        self.manager = manager
        
    def get_tests(self):
        """Generate case sensitivity bypass tests"""
        tests = []
        base_url = self.manager.target_url
        parsed = self.manager.parsed_url if hasattr(self.manager, 'parsed_url') else None
        
        if not parsed:
            import urllib.parse
            parsed = urllib.parse.urlparse(base_url)
        
        path = parsed.path if parsed.path else '/'
        
        # Case variations
        case_variations = [
            path.lower(),
            path.upper(),
            path.title(),
            path.swapcase(),
            path.capitalize(),
            path.replace('/', '/'),
            path.replace('\\', '\\'),
        ]
        
        # Generate case variants for each part
        for variant in case_variations:
            if variant != path:
                tests.append({
                    'name': f'Case Bypass: {variant[:30]}...',
                    'url': base_url.replace(path, variant),
                    'headers': {},
                    'method': 'GET'
                })
        
        # Case variants with different extensions
        extensions = ['.php', '.html', '.txt', '.asp', '.aspx', '.jsp', '.do', '.action', '.cgi', '.pl']
        
        for ext in extensions:
            for case in ['lower', 'upper', 'title']:
                base_path = path
                if base_path.endswith('/'):
                    base_path = base_path[:-1]
                
                if case == 'lower':
                    new_path = (base_path + ext).lower()
                elif case == 'upper':
                    new_path = (base_path + ext).upper()
                else:
                    new_path = (base_path + ext).title()
                
                tests.append({
                    'name': f'Case + Extension: {new_path[:30]}...',
                    'url': base_url.replace(path, new_path),
                    'headers': {},
                    'method': 'GET'
                })
        
        # Mixed case in different parts
        if '/' in path:
            parts = path.split('/')
            mixed_parts = []
            
            for i in range(len(parts)):
                if parts[i]:
                    mixed_parts.append(parts[i][0].upper() + parts[i][1:].lower())
                else:
                    mixed_parts.append('')
            
            mixed_path = '/'.join(mixed_parts)
            if mixed_path != path:
                tests.append({
                    'name': 'Mixed Case Bypass',
                    'url': base_url.replace(path, mixed_path),
                    'headers': {},
                    'method': 'GET'
                })
        
        return tests
