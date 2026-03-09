"""
URL manipulation utilities
"""

from urllib.parse import urljoin, urlparse, parse_qs
from typing import Set, List

class URLUtils:
    """URL operations helper"""
    
    @staticmethod
    def extract_domain(url: str) -> str:
        """Extract domain from URL"""
        try:
            parsed = urlparse(url)
            return parsed.netloc
        except Exception:
            return ""
    
    @staticmethod
    def extract_path(url: str) -> str:
        """Extract path from URL"""
        try:
            parsed = urlparse(url)
            return parsed.path or "/"
        except Exception:
            return "/"
    
    @staticmethod
    def extract_parameters(url: str) -> dict:
        """Extract parameters from URL"""
        try:
            parsed = urlparse(url)
            return parse_qs(parsed.query)
        except Exception:
            return {}
    
    @staticmethod
    def normalize_urls(urls: List[str]) -> Set[str]:
        """Normalize and deduplicate URLs"""
        normalized = set()
        for url in urls:
            url_clean = url.split('#')[0].rstrip('/')
            if url_clean:
                normalized.add(url_clean)
        return normalized
    
    @staticmethod
    def is_same_domain(url1: str, url2: str) -> bool:
        """Check if URLs are from same domain"""
        try:
            domain1 = urlparse(url1).netloc
            domain2 = urlparse(url2).netloc
            return domain1 == domain2
        except Exception:
            return False
    
    @staticmethod
    def get_base_url(url: str) -> str:
        """Get base URL (protocol + domain)"""
        try:
            parsed = urlparse(url)
            return f"{parsed.scheme}://{parsed.netloc}"
        except Exception:
            return ""
