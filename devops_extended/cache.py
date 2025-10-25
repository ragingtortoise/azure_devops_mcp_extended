"""
Metadata caching layer for Azure DevOps API responses.
Reduces API calls and improves performance.
"""

import threading
import time
from typing import Any, Dict, Optional, Callable


class MetadataCache:
    """
    Thread-safe in-memory cache with TTL support for metadata.
    
    Caches:
    - Work item type definitions (states, fields, transitions)
    - Available work item types
    - Field schemas
    - Process template information
    """
    
    def __init__(self, default_ttl: int = 3600):
        """
        Initialize cache.
        
        Args:
            default_ttl: Default time-to-live in seconds (default: 1 hour)
        """
        self.default_ttl = default_ttl
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache if not expired.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found/expired
        """
        with self._lock:
            if key not in self._cache:
                return None
            
            entry = self._cache[key]
            
            # Check if expired
            if time.time() > entry["expires_at"]:
                del self._cache[key]
                return None
            
            return entry["value"]
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """
        Set value in cache with TTL.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds (uses default if not specified)
        """
        with self._lock:
            expires_at = time.time() + (ttl if ttl is not None else self.default_ttl)
            self._cache[key] = {
                "value": value,
                "expires_at": expires_at,
            }
    
    def get_or_fetch(
        self,
        key: str,
        fetch_func: Callable[[], Any],
        ttl: Optional[int] = None
    ) -> Any:
        """
        Get value from cache or fetch it if not cached/expired.
        
        Args:
            key: Cache key
            fetch_func: Function to call to fetch value if not cached
            ttl: Time-to-live in seconds (uses default if not specified)
            
        Returns:
            Cached or freshly fetched value
        """
        # Try to get from cache first
        cached_value = self.get(key)
        if cached_value is not None:
            return cached_value
        
        # Fetch and cache
        value = fetch_func()
        self.set(key, value, ttl)
        return value
    
    def invalidate(self, key: str) -> None:
        """
        Remove value from cache.
        
        Args:
            key: Cache key to invalidate
        """
        with self._lock:
            if key in self._cache:
                del self._cache[key]
    
    def invalidate_pattern(self, pattern: str) -> None:
        """
        Invalidate all keys matching pattern (simple prefix match).
        
        Args:
            pattern: Key prefix to match
        """
        with self._lock:
            keys_to_delete = [k for k in self._cache.keys() if k.startswith(pattern)]
            for key in keys_to_delete:
                del self._cache[key]
    
    def clear(self) -> None:
        """Clear entire cache."""
        with self._lock:
            self._cache.clear()
    
    def size(self) -> int:
        """Get number of items in cache."""
        with self._lock:
            return len(self._cache)


# Global cache instance
_global_cache: Optional[MetadataCache] = None
_cache_lock = threading.Lock()


def get_cache() -> MetadataCache:
    """
    Get the global metadata cache instance.
    
    Returns:
        MetadataCache instance
    """
    global _global_cache
    
    if _global_cache is None:
        with _cache_lock:
            if _global_cache is None:
                _global_cache = MetadataCache()
    
    return _global_cache
