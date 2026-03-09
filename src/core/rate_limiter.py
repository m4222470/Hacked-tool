"""
Adaptive rate limiter with jitter and 429 handling
"""

import threading
import time
import random
from typing import Dict

class AdaptiveRateLimiter:
    """
    Adaptive rate limiter with:
    - Variable time intervals (Jitter)
    - Adaptive delay on 429 responses
    - Concurrent request limit
    """
    def __init__(self, max_concurrent: int = 5, rate_per_sec: float = 10, adaptive_delay_multiplier: float = 0.5):
        """
        Initialize rate limiter
        
        Args:
            max_concurrent: Maximum concurrent requests
            rate_per_sec: Maximum requests per second
            adaptive_delay_multiplier: Multiplier for 429 response delay
        """
        self.max_concurrent = max_concurrent
        self.semaphore = threading.Semaphore(max_concurrent)
        self.rate_per_sec = rate_per_sec
        self.lock = threading.Lock()
        self.last_calls = []
        self.min_interval = 1.0 / rate_per_sec if rate_per_sec > 0 else 0
        
        # Adaptive tracking
        self.consecutive_429s = 0
        self.adaptive_delay = 0
        self.adaptive_delay_multiplier = adaptive_delay_multiplier
        self.total_requests = 0
        self.http_429_count = 0
    
    def record_429(self):
        """Record 429 Too Many Requests response"""
        with self.lock:
            self.consecutive_429s += 1
            self.http_429_count += 1
            self.adaptive_delay = min(
                self.consecutive_429s * self.adaptive_delay_multiplier,
                5.0
            )
    
    def record_success(self):
        """Record successful request"""
        with self.lock:
            if self.consecutive_429s > 0:
                self.consecutive_429s = max(0, self.consecutive_429s - 1)
                self.adaptive_delay = max(0, self.adaptive_delay - 0.1)
    
    def _wait_for_rate(self):
        """Wait for rate limit with jitter"""
        if self.min_interval <= 0:
            return
        
        with self.lock:
            now = time.time()
            # Remove old calls
            self.last_calls = [t for t in self.last_calls if now - t < 1.0]
            
            # Wait if at rate limit
            while len(self.last_calls) >= self.rate_per_sec:
                # Add random jitter
                jitter = random.uniform(-0.05, 0.05)
                delay = max(0.01, self.min_interval + jitter)
                delay += self.adaptive_delay
                time.sleep(delay)
                now = time.time()
                self.last_calls = [t for t in self.last_calls if now - t < 1.0]
            
            self.last_calls.append(now)
            self.total_requests += 1
    
    def acquire(self):
        """Acquire rate limit token"""
        self._wait_for_rate()
        self.semaphore.acquire()
    
    def release(self):
        """Release rate limit token"""
        self.semaphore.release()
    
    def __enter__(self):
        self.acquire()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
    
    def get_stats(self) -> Dict[str, any]:
        """Get rate limiter statistics"""
        return {
            "total_requests": self.total_requests,
            "http_429_count": self.http_429_count,
            "adaptive_delay": self.adaptive_delay,
            "consecutive_429s": self.consecutive_429s
        }
