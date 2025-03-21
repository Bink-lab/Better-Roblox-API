from typing import Dict, Optional
import time
import threading
from collections import defaultdict
import configparser
import os

class RateLimiter:
    """
    IP-based rate limiter to control API request rates
    """
    def __init__(self):
        self.ip_requests = defaultdict(list)  # Store timestamp of requests per IP
        self.lock = threading.RLock()  # Thread-safe access
        self.rate_limit = 60  # Default requests per minute
        self.enabled = True
        self.window_size = 60  # Time window in seconds (1 minute)
        self.load_config()
    
    def load_config(self):
        """Load configuration from settings.config file"""
        config = configparser.ConfigParser()
        config_path = os.path.join(os.path.dirname(__file__), 'settings.config')
        
        if os.path.exists(config_path):
            config.read(config_path)
            if 'ApiSettings' in config:
                self.rate_limit = config.getint('ApiSettings', 'rate_limit', fallback=60)
                self.enabled = config.getboolean('ApiSettings', 'enable_rate_limit', fallback=True)
                # Window size is fixed at 60 seconds (1 minute)
    
    def is_rate_limited(self, ip_address: str) -> bool:
        """
        Check if the IP address has exceeded the rate limit
        Returns True if rate limited, False otherwise
        """
        if not self.enabled:
            return False
            
        now = time.time()
        one_minute_ago = now - self.window_size  # 60 seconds window
        
        with self.lock:
            # Clean old requests
            self.ip_requests[ip_address] = [
                timestamp for timestamp in self.ip_requests[ip_address]
                if timestamp > one_minute_ago
            ]
            
            # Check if under rate limit
            if len(self.ip_requests[ip_address]) >= self.rate_limit:
                return True
                
            # Add current request timestamp
            self.ip_requests[ip_address].append(now)
            return False
    
    def get_remaining_requests(self, ip_address: str) -> int:
        """Get remaining requests allowed for this IP address"""
        if not self.enabled:
            return -1  # Unlimited
            
        with self.lock:
            now = time.time()
            one_minute_ago = now - self.window_size  # 60 seconds window
            
            # Clean old requests
            current_requests = [
                timestamp for timestamp in self.ip_requests.get(ip_address, [])
                if timestamp > one_minute_ago
            ]
            
            return max(0, self.rate_limit - len(current_requests))
    
    def get_reset_time(self, ip_address: str) -> Optional[float]:
        """Get time in seconds until the rate limit resets for this IP"""
        if not self.enabled or ip_address not in self.ip_requests:
            return None
            
        with self.lock:
            if not self.ip_requests[ip_address]:
                return None
                
            oldest_timestamp = min(self.ip_requests[ip_address])
            return max(0, self.window_size - (time.time() - oldest_timestamp))

# Global instance
rate_limiter = RateLimiter()
