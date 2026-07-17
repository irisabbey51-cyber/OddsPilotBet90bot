import time
from typing import Any, Dict
from collections import OrderedDict

class CacheService:
    def __init__(self, max_size=100):
        self.cache: Dict[str, Dict[str, Any]] = OrderedDict()
        self.max_size = max_size
    
    def get(self, key: str) -> Any:
        """Get cached value"""
        if key in self.cache:
            cache_item = self.cache[key]
            if time.time() - cache_item['timestamp'] < cache_item['ttl']:
                return cache_item['value']
            else:
                del self.cache[key]
        return None
    
    def set(self, key: str, value: Any, ttl: int = 300):
        """Set cache value with TTL in seconds"""
        if len(self.cache) >= self.max_size:
            self.cache.popitem(last=False)
        
        self.cache[key] = {
            'value': value,
            'timestamp': time.time(),
            'ttl': ttl
        }
    
    def clear(self):
        """Clear all cache"""
        self.cache.clear()
