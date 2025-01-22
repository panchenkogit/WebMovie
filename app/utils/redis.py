from typing import Optional

import redis.client
from config import REDIS_HOST, REDIS_PORT
import redis


class RedisClient():
    def __init__(self, host: str = REDIS_HOST, port: int = REDIS_PORT, db: id = 0):
        self.client = redis.Redis(host=host, port=port, db=db, decode_responses=True)

    def set_key(self, key: str, value: str, expire: Optional[int] = None) -> bool:
        try:
            self.client.set(key, value, ex=expire)
            return True

        except redis.RedisError as e:
            print(f"Ошибка Redis: {e}")
            return False
    

    def get_key(self, key: str):
        try:
            return self.client.get(key)

        except redis.RedisError as e:
            print(f"Ошибка Redis: {e}")
            return False


    def delete_key(self, key: str):
        try:
            return self.client.delete(key)

        except redis.RedisError as e:
            print(f"Ошибка Redis: {e}")
            return False
