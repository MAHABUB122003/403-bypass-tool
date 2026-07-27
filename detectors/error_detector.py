#!/usr/bin/env python3
"""
Error detection and analysis
"""

import re

class ErrorDetector:
    def __init__(self):
        self.error_patterns = {
            '403': [
                r'403\s*forbidden',
                r'forbidden\s*403',
                r'access\s*denied',
                r'not\s*authorized',
                r'unauthorized',
                r'permission\s*denied',
                r'restricted\s*access',
                r'access\s*restricted',
            ],
            '404': [
                r'404\s*not\s*found',
                r'not\s*found\s*404',
                r'page\s*not\s*found',
                r'file\s*not\s*found',
                r'does\s*not\s*exist',
                r'no\s*such\s*file',
            ],
            '500': [
                r'500\s*internal\s*server\s*error',
                r'internal\s*server\s*error',
                r'fatal\s*error',
                r'exception\s*occurred',
                r'traceback',
            ],
            '502': [
                r'502\s*bad\s*gateway',
                r'bad\s*gateway',
            ],
            '503': [
                r'503\s*service\s*unavailable',
                r'service\s*unavailable',
            ],
            '504': [
                r'504\s*gateway\s*timeout',
                r'gateway\s*timeout',
            ],
        }
        
        self.technology_patterns = {
            'PHP': [
                r'\.php',
                r'php\s*error',
                r'PHP\s*Warning',
                r'PHP\s*Notice',
                r'PHP\s*Fatal\s*error',
            ],
            'ASP.NET': [
                r'\.asp',
                r'\.aspx',
                r'viewstate',
                r'__viewstate',
                r'ASP\.NET',
            ],
            'JSP': [
                r'\.jsp',
                r'\.jspx',
                r'Java\s*Server\s*Pages',
                r'javax\.servlet',
            ],
            'Python': [
                r'\.py',
                r'\.pyc',
                r'Django',
                r'Flask',
                r'wsgi',
            ],
            'Ruby': [
                r'\.rb',
                r'\.erb',
                r'Ruby\s*on\s*Rails',
                r'Rails',
            ],
            'Node.js': [
                r'\.js',
                r'\.node',
                r'Express',
                r'Node\.js',
            ],
            'WordPress': [
                r'wp-content',
                r'wp-includes',
                r'wp-admin',
                r'wordpress',
            ],
            'Drupal': [
                r'Drupal',
                r'drupal',
                r'sites/default',
            ],
            'Joomla': [
                r'Joomla',
                r'joomla',
                r'components/com_',
            ],
        }
    
    def detect(self, response):
        """Detect errors and technologies in response"""
        detected = {
            'errors': [],
            'technologies': [],
            'response_code': response.status_code if response else None,
            'response_length': len(response.text) if response else 0,
        }
        
        if not response:
            return detected
        
        text = response.text.lower()
        headers = {k.lower(): v.lower() for k, v in response.headers.items()}
        
        # Detect errors
        for error_type, patterns in self.error_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    detected['errors'].append(error_type)
                    break
        
        # Detect technologies
        for tech, patterns in self.technology_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE) or any(re.search(pattern, v) for v in headers.values()):
                    detected['technologies'].append(tech)
                    break
        
        # Detect from headers
        if 'server' in headers:
            detected['server'] = headers['server']
        if 'x-powered-by' in headers:
            detected['powered_by'] = headers['x-powered-by']
        
        return detected
