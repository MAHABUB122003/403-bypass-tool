#!/usr/bin/env python3
"""
Response analyzer for 403 bypass detection
"""

import re
import json
from difflib import SequenceMatcher

class ResponseAnalyzer:
    def __init__(self, base_response):
        self.base_response = base_response
        self.base_text = base_response.text if base_response else ''
        self.base_headers = dict(base_response.headers) if base_response else {}
        self.base_status = base_response.status_code if base_response else 0
        
    def analyze(self, response):
        """Analyze response and determine if bypass was successful"""
        if not response:
            return {'success': False, 'reason': 'No response'}
        
        # Check status code
        if response.status_code != 403:
            # Check if it's a real bypass
            if response.status_code in [200, 201, 202, 204, 301, 302, 303, 307, 308]:
                # Check content difference
                similarity = self.calculate_similarity(response.text)
                if similarity < 0.9:  # Different content
                    return {
                        'success': True,
                        'status': response.status_code,
                        'content_changed': True,
                        'similarity': similarity,
                        'headers_diff': self.compare_headers(response.headers)
                    }
                else:
                    return {
                        'success': False,
                        'status': response.status_code,
                        'reason': 'Similar content to base response',
                        'similarity': similarity
                    }
            else:
                return {
                    'success': False,
                    'status': response.status_code,
                    'reason': 'Not a success status code'
                }
        else:
            return {
                'success': False,
                'status': 403,
                'reason': 'Still 403'
            }
    
    def calculate_similarity(self, text):
        """Calculate similarity between two texts"""
        if not self.base_text or not text:
            return 0
        return SequenceMatcher(None, self.base_text[:1000], text[:1000]).ratio()
    
    def compare_headers(self, headers):
        """Compare headers with base response"""
        diff = {}
        for key, value in headers.items():
            if key in self.base_headers:
                if self.base_headers[key] != value:
                    diff[key] = {'base': self.base_headers[key], 'new': value}
            else:
                diff[key] = {'base': None, 'new': value}
        return diff
    
    def detect_403_patterns(self, text):
        """Detect common 403 patterns"""
        patterns = {
            '403 forbidden': re.compile(r'403\s*forbidden', re.I),
            'access denied': re.compile(r'access\s*denied', re.I),
            'unauthorized': re.compile(r'unauthorized', re.I),
            'not authorized': re.compile(r'not\s*authorized', re.I),
            'permission denied': re.compile(r'permission\s*denied', re.I),
            'forbidden': re.compile(r'forbidden', re.I),
            'blocked': re.compile(r'blocked', re.I),
            'restricted': re.compile(r'restricted', re.I),
        }
        
        found = []
        for name, pattern in patterns.items():
            if pattern.search(text):
                found.append(name)
        
        return found
