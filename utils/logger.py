#!/usr/bin/env python3
"""
Logging utilities
"""

import datetime
import json
import os

class Logger:
    def __init__(self, log_file=None):
        self.log_file = log_file
        self.logs = []
        
    def info(self, message):
        self.log('INFO', message)
        
    def error(self, message):
        self.log('ERROR', message)
        
    def success(self, message):
        self.log('SUCCESS', message)
        
    def warning(self, message):
        self.log('WARNING', message)
        
    def debug(self, message):
        self.log('DEBUG', message)
        
    def log(self, level, message):
        timestamp = datetime.datetime.now().isoformat()
        log_entry = {
            'timestamp': timestamp,
            'level': level,
            'message': message
        }
        self.logs.append(log_entry)
        
        # Print to console
        print(f"[{timestamp}] [{level}] {message}")
        
        # Write to file if specified
        if self.log_file:
            with open(self.log_file, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
    
    def get_logs(self):
        return self.logs
