"""
Input validation utilities
"""

import re
from urllib.parse import urlparse

class URLValidator:
    """URL and domain validation"""
    
    @staticmethod
    def is_valid_domain(domain: str) -> bool:
        """Validate domain format"""
        domain_pattern = r'^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$'
        return re.match(domain_pattern, domain.lower()) is not None
    
    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Validate URL format"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False
    
    @staticmethod
    def normalize_domain(domain: str) -> str:
        """Normalize domain format"""
        domain = domain.lower().strip()
        if domain.startswith('www.'):
            domain = domain[4:]
        return domain
    
    @staticmethod
    def normalize_url(url: str) -> str:
        """Normalize URL format"""
        url = url.strip()
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        return url.rstrip('/')

class ParameterValidator:
    """Parameter validation"""
    
    @staticmethod
    def is_suspicious_parameter(param: str) -> bool:
        """Check if parameter looks suspicious"""
        suspicious = ['admin', 'debug', 'internal', 'test', 'stage', 'secret', 'token']
        return any(sus in param.lower() for sus in suspicious)
    
    @staticmethod
    def validate_parameter_name(name: str) -> bool:
        """Validate parameter name format"""
        return re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', name) is not None
