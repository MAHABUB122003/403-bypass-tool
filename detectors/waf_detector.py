#!/usr/bin/env python3
"""
WAF detection and fingerprinting
"""

import re

class WAFDetector:
    def __init__(self):
        self.waf_signatures = {
            'Cloudflare': [
                r'cloudflare',
                r'cf-ray',
                r'cf-request-id',
                r'__cfduid',
                r'cf-connecting-ip',
                r'cloudflare-nginx',
                r'x-cf-',
            ],
            'AWS WAF': [
                r'x-amz-request-id',
                r'x-amz-id-2',
                r'x-amz-cf-id',
                r'x-amzn-requestid',
                r'aws-waf',
                r'x-amz-security-token',
            ],
            'Akamai': [
                r'akamai',
                r'akamaitech',
                r'x-akamai-transformed',
                r'x-akamai-request-id',
                r'akamai-ghost',
            ],
            'Fastly': [
                r'fastly',
                r'x-fastly-',
                r'x-served-by',
                r'x-cache',
                r'x-cache-hits',
                r'x-timer',
            ],
            'CloudFront': [
                r'cloudfront',
                r'x-amz-cf-id',
                r'x-amz-cf-pop',
                r'x-cache',
                r'via.*cloudfront',
            ],
            'ModSecurity': [
                r'mod_security',
                r'modsecurity',
                r'owasp',
                r'sec-',
                r'this\s*error\s*was\s*generated\s*by\s*mod_security',
            ],
            'Sucuri': [
                r'sucuri',
                r'x-sucuri-id',
                r'x-sucuri-cache',
                r'sucuri-firewall',
            ],
            'Barracuda': [
                r'barracuda',
                r'cuda',
                r'x-cuda-',
            ],
            'F5 BIG-IP': [
                r'big-ip',
                r'f5',
                r'x-waf',
                r'ts\s*=\s*',
                r'bigip',
            ],
            'Imperva': [
                r'imperva',
                r'incapsula',
                r'x-iinfo',
                r'x-cdn',
                r'incap-',
            ],
            'Wordfence': [
                r'wordfence',
                r'wf-',
                r'wordfence\s*security',
            ],
            'SiteGuard': [
                r'siteguard',
                r'waf.*siteguard',
            ],
            'WebKnight': [
                r'webknight',
                r'web-knight',
            ],
            'NAXSI': [
                r'naxsi',
                r'x-naxsi',
            ],
            'ZScaler': [
                r'zscaler',
                r'zscaler-cloud',
            ],
            'Cloudbric': [
                r'cloudbric',
                r'x-cloudbric',
            ],
            'Cisco ACE': [
                r'ace\s*xml\s*gateway',
                r'cisco-ace',
            ],
            'Radware': [
                r'radware',
                r'appwall',
                r'x-aspnet-version',
            ],
            'NSFocus': [
                r'nsfocus',
                r'nsfocus.*waf',
            ],
            'Anquanbao': [
                r'anquanbao',
                r'x-waf-qz',
            ],
            'Yundun': [
                r'yundun',
                r'yd-',
            ],
            'SafeDog': [
                r'safedog',
                r'waf.*safedog',
            ],
            'DDoS-GUARD': [
                r'ddos-guard',
                r'ddosguard',
            ],
            'Viettel': [
                r'viettel',
                r'viettel-cloud',
            ],
        }
    
    def detect(self, headers, body):
        """Detect WAF from headers and body"""
        detected = []
        confidence = {}
        
        # Convert headers to lowercase
        headers_lower = {k.lower(): v.lower() for k, v in headers.items()}
        body_lower = body.lower()
        
        for waf_name, signatures in self.waf_signatures.items():
            score = 0
            
            for signature in signatures:
                # Check in headers
                for key, value in headers_lower.items():
                    if re.search(signature, key) or re.search(signature, value):
                        score += 2
                        break
                
                # Check in body
                if re.search(signature, body_lower):
                    score += 1
            
            if score >= 2:
                detected.append(waf_name)
                confidence[waf_name] = score
        
        return {
            'detected_wafs': detected,
            'confidence': confidence,
            'waf_present': len(detected) > 0,
            'likely_waf': detected[0] if detected else None
        }
