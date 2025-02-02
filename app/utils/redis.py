from typing import Optional
import redis.asyncio as redis
from config import REDIS_HOST, REDIS_PORT

class RedisClient:
    def __init__(self, host: str = REDIS_HOST, port: int = REDIS_PORT, db: int = 0):
        self.client = redis.Redis(host=host, port=port, db=db, decode_responses=True)

    async def set_key(self, key: str, value: str, expire: Optional[int] = None) -> bool:
        try:
            await self.client.set(key, value, ex=expire)
            return True
        except redis.RedisError as e:
            print(f"Ошибка Redis: {e}")
            return False

    async def get_key(self, key: str):
        try:
            return await self.client.get(key)
        except redis.RedisError as e:
            print(f"Ошибка Redis: {e}")
            return False

    async def delete_key(self, key: str):
        try:
            return await self.client.delete(key)
        except redis.RedisError as e:
            print(f"Ошибка Redis: {e}")
            return False
