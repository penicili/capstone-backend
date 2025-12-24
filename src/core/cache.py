"""
Redis cache implementation untuk KPI caching
Fallback ke in-memory cache jika Redis tidak tersedia
"""
import json
from typing import Optional, Any
from decimal import Decimal
from redis import Redis
from redis.exceptions import RedisError, ConnectionError as RedisConnectionError
from core.logging import logger
from config import settings


class DecimalEncoder(json.JSONEncoder):
    """Custom JSON encoder untuk handle Decimal types"""
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)


class RedisCache:
    """Redis cache manager dengan fallback ke in-memory cache"""
    
    def __init__(self):
        """Initialize Redis connection"""
        self.redis_client: Optional[Redis] = None
        self._in_memory_cache: dict = {}  # Fallback cache
        
        try:
            self.redis_client = Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
                password=settings.REDIS_PASSWORD if settings.REDIS_PASSWORD else None,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5
            )
            # Test connection
            self.redis_client.ping()
            logger.success(f"Redis connected: {settings.REDIS_HOST}:{settings.REDIS_PORT}")
        except (RedisError, RedisConnectionError) as e:
            logger.warning(f"Redis connection failed: {e}. Using in-memory cache fallback.")
            self.redis_client = None
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None
        """
        if self.redis_client:
            try:
                value = self.redis_client.get(key)
                if value:
                    logger.debug(f"Cache HIT (Redis): {key}")
                    # Ensure value is string before JSON parsing
                    if isinstance(value, str):
                        return json.loads(value)
                    elif isinstance(value, bytes):
                        return json.loads(value.decode('utf-8'))
                    else:
                        logger.warning(f"Unexpected value type from Redis: {type(value)}")
                        return None
                logger.debug(f"Cache MISS (Redis): {key}")
                return None
            except RedisError as e:
                logger.warning(f"Redis GET error: {e}. Falling back to in-memory.")
                return self._in_memory_cache.get(key)
        else:
            # In-memory fallback
            value = self._in_memory_cache.get(key)
            if value:
                logger.debug(f"Cache HIT (Memory): {key}")
            else:
                logger.debug(f"Cache MISS (Memory): {key}")
            return value
    
    def set(self, key: str, value: Any, ttl: int = 300) -> bool:
        """
        Set value in cache with TTL
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds (default: 300 = 5 minutes)
            
        Returns:
            True if successful, False otherwise
        """
        if self.redis_client:
            try:
                # Use custom encoder to handle Decimal types
                serialized = json.dumps(value, cls=DecimalEncoder)
                self.redis_client.setex(key, ttl, serialized)
                logger.debug(f"Cache SET (Redis): {key} [TTL: {ttl}s]")
                return True
            except (RedisError, TypeError, ValueError) as e:
                logger.warning(f"Redis SET error: {e}. Falling back to in-memory.")
                self._in_memory_cache[key] = value
                return False
        else:
            # In-memory fallback (no TTL support)
            self._in_memory_cache[key] = value
            logger.debug(f"Cache SET (Memory): {key}")
            return True
    
    def delete(self, key: str) -> bool:
        """
        Delete key from cache
        
        Args:
            key: Cache key
            
        Returns:
            True if key existed, False otherwise
        """
        if self.redis_client:
            try:
                result = self.redis_client.delete(key)
                logger.debug(f"Cache DELETE (Redis): {key}")
                return int(result) > 0
            except RedisError as e:
                logger.warning(f"Redis DELETE error: {e}. Falling back to in-memory.")
                return self._in_memory_cache.pop(key, None) is not None
        else:
            existed = key in self._in_memory_cache
            self._in_memory_cache.pop(key, None)
            logger.debug(f"Cache DELETE (Memory): {key}")
            return existed
    
    def clear(self) -> bool:
        """
        Clear all cache keys with KPI prefix
        
        Returns:
            True if successful
        """
        if self.redis_client:
            try:
                # Delete all keys matching kpi:*
                keys = self.redis_client.keys("kpi:*")
                # Convert ResponseT to list to handle type properly
                keys_list = list(keys) if keys else []
                if keys_list:
                    self.redis_client.delete(*keys_list)
                    logger.info(f"Cache CLEAR (Redis): Deleted {len(keys_list)} keys")
                else:
                    logger.info("Cache CLEAR (Redis): No keys to delete")
                return True
            except RedisError as e:
                logger.error(f"Redis CLEAR error: {e}")
                self._in_memory_cache.clear()
                return False
        else:
            self._in_memory_cache.clear()
            logger.info("Cache CLEAR (Memory): All keys deleted")
            return True
    
    def get_stats(self) -> dict:
        """
        Get cache statistics
        
        Returns:
            Dict with cache stats
        """
        if self.redis_client:
            try:
                info = self.redis_client.info()
                keys = self.redis_client.keys("kpi:*")
                # Convert ResponseT to proper types
                keys_list = list(keys) if keys else []
                info_dict = dict(info) if isinstance(info, dict) else {}
                
                return {
                    "backend": "redis",
                    "connected": True,
                    "host": settings.REDIS_HOST,
                    "port": settings.REDIS_PORT,
                    "db": settings.REDIS_DB,
                    "kpi_keys_count": len(keys_list),
                    "memory_used": info_dict.get("used_memory_human", "N/A"),
                    "total_keys": info_dict.get("db0", {}).get("keys", 0) if "db0" in info_dict else 0
                }
            except RedisError as e:
                logger.error(f"Redis STATS error: {e}")
                return {
                    "backend": "redis",
                    "connected": False,
                    "error": str(e)
                }
        else:
            return {
                "backend": "memory",
                "connected": True,
                "kpi_keys_count": len([k for k in self._in_memory_cache.keys() if k.startswith("kpi:")]),
                "total_keys": len(self._in_memory_cache)
            }
    
    def health_check(self) -> bool:
        """
        Check if cache backend is healthy
        
        Returns:
            True if healthy
        """
        if self.redis_client:
            try:
                self.redis_client.ping()
                return True
            except RedisError:
                return False
        return True  # In-memory is always healthy


# Global cache instance
cache = RedisCache()
