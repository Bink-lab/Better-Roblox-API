import random
from typing import List, Dict, Optional, Union
import os
import requests
import configparser
import re
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("proxy_manager")

class ProxyManager:
    """
    Manages a pool of proxies and provides rotation functionality.
    """
    def __init__(self):
        self.proxies = []
        self.current_index = 0
        self.enabled = False
        self.failed_proxies = {}  # Track failing proxies and their failure timestamps
        self.max_failures = 3     # Maximum consecutive failures before temporary blacklisting
        self.blacklist_time = 300  # Time in seconds (5 minutes) to blacklist a proxy
        self.direct_fallback = True  # Fall back to direct connection if all proxies fail
        self.load_config()
    
    def load_config(self):
        """Load configuration from settings.config file"""
        config = configparser.ConfigParser()
        config_path = os.path.join(os.path.dirname(__file__), 'settings.config')
        
        # Set defaults in case config file is missing
        self.enabled = False
        
        if os.path.exists(config_path):
            config.read(config_path)
            if 'ProxySettings' in config:
                self.enabled = config.getboolean('ProxySettings', 'use_proxies', fallback=False)
                proxy_file = config.get('ProxySettings', 'proxy_file', fallback='proxies.txt')
                self.direct_fallback = config.getboolean('ProxySettings', 'direct_fallback', fallback=True)
                self.max_failures = config.getint('ProxySettings', 'max_failures', fallback=3)
                self.blacklist_time = config.getint('ProxySettings', 'blacklist_time', fallback=300)  # in seconds
                
                if self.enabled and os.path.exists(proxy_file):
                    self.load_from_file(proxy_file)
    
    def enable(self, enabled: bool = True) -> None:
        """Enable or disable proxy usage."""
        self.enabled = enabled
    
    def add_proxy(self, proxy: str) -> None:
        """Add a single proxy to the pool."""
        if proxy and proxy not in self.proxies:
            # Format proxy string if not already formatted
            if not proxy.startswith(('http://', 'https://', 'socks4://', 'socks5://')):
                # Default to http if protocol not specified
                proxy = f"http://{proxy}"
            self.proxies.append(proxy)
            logger.debug(f"Added proxy: {proxy}")
    
    def add_proxies(self, proxies: List[str]) -> None:
        """Add multiple proxies to the pool."""
        for proxy in proxies:
            self.add_proxy(proxy)
    
    def load_from_file(self, filepath: str) -> None:
        """Load proxies from a file (one proxy per line)."""
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                proxies = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
                self.add_proxies(proxies)
    
    def get_proxy(self) -> Optional[Dict[str, str]]:
        """Get the next proxy in rotation format for requests."""
        if not self.enabled or not self.proxies:
            return None
            
        # Try to find a working proxy
        attempts = 0
        while attempts < len(self.proxies):
            proxy = self.proxies[self.current_index]
            self.current_index = (self.current_index + 1) % len(self.proxies)
            attempts += 1
            
            # Skip if proxy is blacklisted
            if proxy in self.failed_proxies:
                failures, last_failure_time = self.failed_proxies[proxy]
                # Check if blacklist period is over
                if failures < self.max_failures or (time.time() - last_failure_time) > self.blacklist_time:
                    # Remove from blacklist if time expired
                    if (time.time() - last_failure_time) > self.blacklist_time:
                        self.failed_proxies.pop(proxy, None)
                    break
            else:
                break
        
        # If we've gone through all proxies and they're all blacklisted, use the first one
        if attempts >= len(self.proxies):
            if self.direct_fallback:
                logger.warning("All proxies are currently blacklisted, falling back to direct connection")
                return None
            
            # Reset a blacklisted proxy and try again
            proxy = self.proxies[0]
            self.failed_proxies.pop(proxy, None)
            logger.warning(f"Using previously blacklisted proxy: {proxy}")
            
        # Return appropriate proxy configuration
        if proxy.startswith(('socks4://', 'socks5://')):
            return {"http": proxy, "https": proxy}
        else:
            return {"http": proxy, "https": proxy}
    
    def mark_proxy_failed(self, proxy_config: Dict[str, str]) -> None:
        """Mark a proxy as failed"""
        if not proxy_config:
            return
            
        # Get the proxy URL from the config (use either http or https)
        proxy_url = proxy_config.get("http") or proxy_config.get("https")
        if not proxy_url:
            return
            
        # Update failure count
        if proxy_url in self.failed_proxies:
            failures, _ = self.failed_proxies[proxy_url]
            self.failed_proxies[proxy_url] = (failures + 1, time.time())
        else:
            self.failed_proxies[proxy_url] = (1, time.time())
            
        failures = self.failed_proxies[proxy_url][0]
        if failures >= self.max_failures:
            logger.warning(f"Proxy {proxy_url} temporarily blacklisted after {failures} failures")
    
    def make_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """Make a request using a proxy from the pool if enabled."""
        if not self.enabled:
            return requests.request(method, url, **kwargs)
            
        # Try with proxy first
        proxy = self.get_proxy()
        if proxy:
            try:
                kwargs["proxies"] = proxy
                kwargs["timeout"] = kwargs.get("timeout", 10)  # Set a default timeout
                
                response = requests.request(method, url, **kwargs)
                response.raise_for_status()
                return response
            except (requests.RequestException, ConnectionResetError, ConnectionError) as e:
                logger.warning(f"Proxy request failed: {str(e)}")
                self.mark_proxy_failed(proxy)
                
                # Fall back to direct connection if configured
                if self.direct_fallback:
                    logger.info("Falling back to direct connection")
                    return requests.request(method, url, **{k: v for k, v in kwargs.items() if k != 'proxies'})
                else:
                    # Try another proxy from the pool
                    return self.make_request(method, url, **{k: v for k, v in kwargs.items() if k != 'proxies'})
        else:
            # No available proxy, make direct request
            logger.info("No available proxies, making direct request")
            return requests.request(method, url, **kwargs)

# Global instance
proxy_manager = ProxyManager()

# Proxy-enabled request methods
def get(url, **kwargs):
    return proxy_manager.make_request("GET", url, **kwargs)

def post(url, **kwargs):
    return proxy_manager.make_request("POST", url, **kwargs)
