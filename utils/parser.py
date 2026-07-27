#!/usr/bin/env python3
"""
URL and response parser utilities
"""

import urllib.parse
import re
import json
from bs4 import BeautifulSoup

class Parser:
    @staticmethod
    def parse_url(url):
        """Parse URL into components"""
        parsed = urllib.parse.urlparse(url)
        return {
            'scheme': parsed.scheme,
            'netloc': parsed.netloc,
            'hostname': parsed.hostname,
            'port': parsed.port,
            'path': parsed.path,
            'params': parsed.params,
            'query': parsed.query,
            'fragment': parsed.fragment,
        }
    
    @staticmethod
    def extract_links(html, base_url=''):
        """Extract all links from HTML"""
        soup = BeautifulSoup(html, 'html.parser')
        links = []
        
        for tag in soup.find_all(['a', 'link', 'script', 'img']):
            href = tag.get('href') or tag.get('src')
            if href:
                # Normalize URL
                if base_url:
                    href = urllib.parse.urljoin(base_url, href)
                links.append(href)
        
        return list(set(links))
    
    @staticmethod
    def extract_forms(html, base_url=''):
        """Extract all forms from HTML"""
        soup = BeautifulSoup(html, 'html.parser')
        forms = []
        
        for form in soup.find_all('form'):
            action = form.get('action', '')
            if base_url:
                action = urllib.parse.urljoin(base_url, action)
            
            method = form.get('method', 'GET').upper()
            inputs = []
            
            for input_tag in form.find_all('input'):
                input_data = {
                    'name': input_tag.get('name'),
                    'type': input_tag.get('type', 'text'),
                    'value': input_tag.get('value', ''),
                }
                inputs.append(input_data)
            
            forms.append({
                'action': action,
                'method': method,
                'inputs': inputs,
            })
        
        return forms
    
    @staticmethod
    def extract_js_variables(html):
        """Extract JavaScript variables from HTML"""
        variables = {}
        patterns = [
            r'var\s+(\w+)\s*=\s*["\']([^"\']+)["\']',
            r'const\s+(\w+)\s*=\s*["\']([^"\']+)["\']',
            r'let\s+(\w+)\s*=\s*["\']([^"\']+)["\']',
            r'(\w+)\s*:\s*["\']([^"\']+)["\']',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, html)
            for key, value in matches:
                variables[key] = value
        
        return variables
    
    @staticmethod
    def extract_meta_tags(html):
        """Extract meta tags from HTML"""
        soup = BeautifulSoup(html, 'html.parser')
        meta_tags = {}
        
        for meta in soup.find_all('meta'):
            name = meta.get('name') or meta.get('property')
            content = meta.get('content')
            if name and content:
                meta_tags[name] = content
        
        return meta_tags
    
    @staticmethod
    def parse_headers(headers_string):
        """Parse headers from string to dict"""
        headers = {}
        lines = headers_string.strip().split('\n')
        
        for line in lines:
            if ': ' in line:
                key, value = line.split(': ', 1)
                headers[key.strip()] = value.strip()
        
        return headers
    
    @staticmethod
    def parse_cookies(cookie_string):
        """Parse cookies from string to dict"""
        cookies = {}
        for cookie in cookie_string.split(';'):
            if '=' in cookie:
                key, value = cookie.split('=', 1)
                cookies[key.strip()] = value.strip()
        return cookies
    
    @staticmethod
    def extract_comments(html):
        """Extract HTML comments"""
        comments = []
        pattern = r'<!--(.*?)-->'
        matches = re.findall(pattern, html, re.DOTALL)
        for match in matches:
            match = match.strip()
            if match:
                comments.append(match)
        return comments
    
    @staticmethod
    def normalize_url(url):
        """Normalize URL"""
        parsed = urllib.parse.urlparse(url)
        # Remove default ports
        if parsed.port in [80, 443]:
            netloc = parsed.netloc.split(':')[0]
        else:
            netloc = parsed.netloc
        
        # Normalize path
        path = parsed.path
        if path and not path.endswith('/'):
            path += '/'
        
        return urllib.parse.urlunparse((
            parsed.scheme,
            netloc,
            path,
            parsed.params,
            parsed.query,
            parsed.fragment
        ))
