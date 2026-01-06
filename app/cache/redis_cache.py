import hashlib
import json
from typing import Any, Optional
from datetime import timedelta

from redis.asyncio import Redis
from redis.exceptions import RedisError

from app.config import settings


class CacheManager:
    def __init__(self):
        self.redis_client: Optional[Redis] = None
        self.memory_cache: dict[str, Any] = {}
        self.enabled = settings.redis_enabled

    async def connect(self):
        if not self.enabled:
            return
        
        try:
            self.redis_client = await Redis.from_url(
                settings.redis_url,
                encoding="utf-8",
                decode_responses=True
            )
            await self.redis_client.ping()
        except (RedisError, Exception):
            self.redis_client = None

    async def disconnect(self):
        if self.redis_client:
            await self.redis_client.aclose()

    def _generate_key(self, data: str, prefix: str = "") -> str:
        hash_object = hashlib.sha256(data.encode())
        return f"{prefix}:{hash_object.hexdigest()}"

    async def get(self, key: str) -> Optional[str]:
        if self.redis_client:
            try:
                return await self.redis_client.get(key)
            except RedisError:
                pass
        
        return self.memory_cache.get(key)

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        ttl = ttl or settings.cache_ttl
        value_str = json.dumps(value) if not isinstance(value, str) else value

        if self.redis_client:
            try:
                await self.redis_client.setex(key, timedelta(seconds=ttl), value_str)
                return True
            except RedisError:
                pass

        self.memory_cache[key] = value_str
        return True

    async def delete(self, key: str) -> bool:
        if self.redis_client:
            try:
                await self.redis_client.delete(key)
            except RedisError:
                pass

        self.memory_cache.pop(key, None)
        return True

    async def exists(self, key: str) -> bool:
        if self.redis_client:
            try:
                return await self.redis_client.exists(key) > 0
            except RedisError:
                pass

        return key in self.memory_cache


cache_manager = CacheManager()

