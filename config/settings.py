#!/usr/bin/env python3
"""
Configuration settings
"""

import os

class Config:
    def __init__(self):
        # API Keys (for external services)
        self.SHODAN_API_KEY = os.environ.get('SHODAN_API_KEY', '')
        self.CENSYS_API_KEY = os.environ.get('CENSYS_API_KEY', '')
        self.SECURITYTRAILS_API_KEY = os.environ.get('SECURITYTRAILS_API_KEY', '')
        
        # Network settings
        self.DEFAULT_TIMEOUT = 10
        self.DEFAULT_THREADS = 20
        self.MAX_RETRIES = 3
        self.USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        
        # Wordlist paths
        self.WORDLIST_DIR = os.path.join(os.path.dirname(__file__), 'wordlists')
        self.PATHS_WORDLIST = os.path.join(self.WORDLIST_DIR, 'paths.txt')
        self.HEADERS_WORDLIST = os.path.join(self.WORDLIST_DIR, 'headers.txt')
        self.USER_AGENTS_WORDLIST = os.path.join(self.WORDLIST_DIR, 'user-agents.txt')
        
        # Output settings
        self.OUTPUT_DIR = os.path.join(os.getcwd(), 'output')
        self.REPORT_FORMAT = 'json'  # json, text, html
        
        # Bypass settings
        self.ENABLE_ALL_BYPASSES = True
        self.ENABLE_CDN_BYPASS = True
        self.ENABLE_CACHE_BYPASS = True
        self.ENABLE_WAF_BYPASS = True
        self.ENABLE_HEADER_BYPASS = True
        self.ENABLE_PATH_BYPASS = True
        self.ENABLE_METHOD_BYPASS = True
        
        # Rate limiting
        self.ENABLE_RATE_LIMITING = True
        self.REQUESTS_PER_SECOND = 10
