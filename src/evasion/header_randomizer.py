"""
HTTP header randomization for request obfuscation
"""

import random
from typing import Dict

VARIED_USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
]

VARIED_ACCEPT_LANGUAGES = [
    "en-US,en;q=0.9",
    "en-GB,en;q=0.8",
    "fr-FR,fr;q=0.9,en;q=0.8",
    "de-DE,de;q=0.9,en;q=0.8",
    "es-ES,es;q=0.9,en;q=0.8",
]

CACHE_CONTROL_VALUES = [
    "max-age=0",
    "no-cache",
    "no-store",
    "must-revalidate",
]

class HeaderRandomizer:
    """HTTP header randomization for request obfuscation"""
    
    @staticmethod
    def get_random_headers() -> Dict[str, str]:
        """Get randomized HTTP headers"""
        return {
            "User-Agent": random.choice(VARIED_USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": random.choice(VARIED_ACCEPT_LANGUAGES),
            "Accept-Encoding": "gzip, deflate",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": random.choice(CACHE_CONTROL_VALUES),
        }
    
    @staticmethod
    def get_random_user_agent() -> str:
        """Get random User-Agent header"""
        return random.choice(VARIED_USER_AGENTS)
    
    @staticmethod
    def get_random_accept_language() -> str:
        """Get random Accept-Language header"""
        return random.choice(VARIED_ACCEPT_LANGUAGES)
