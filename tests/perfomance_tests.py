from time import time
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from typing import Dict
from app.utils.redis import RedisClient

class PerformanceTester:
    def __init__(self, redis_client: RedisClient):
        self.redis_client = redis_client
        

    async def test_db_write(self, session: AsyncSession, iterations: int = 1000) -> Dict[str, float]:
        """Тест записи данных в PostgreSQL."""
        start_time = time()
        for i in range(iterations):
            await session.execute(
                text("INSERT INTO test_table (key, value) VALUES (:key, :value)"),
                {"key": f"key_{i}", "value": f"value_{i}"}
            )
        await session.commit()
        end_time = time()
        return {"db_write_time": round((end_time - start_time), 2)}

    async def test_db_read(self, session: AsyncSession, iterations: int = 1000) -> Dict[str, float]:
        """Тест чтения данных из PostgreSQL."""
        start_time = time()
        for i in range(iterations):
            await session.execute(
                text("SELECT value FROM test_table WHERE key = :key"),
                {"key": f"key_{i}"}
            )
        end_time = time()
        return {"db_read_time": round((end_time - start_time), 2)}

    def test_redis_write(self, iterations: int = 1000000) -> Dict[str, float]:
        """Тест записи данных в Redis."""
        start_time = time()
        for i in range(iterations):
            self.redis_client.set_key(f"key_{i}", f"value_{i}", 60)
        end_time = time()
        return {"redis_write_time": round((end_time - start_time), 2)}

    def test_redis_read(self, iterations: int = 1000000) -> Dict[str, float]:
        """Тест чтения данных из Redis."""
        start_time = time()
        keys  = [f"key_{i}" for i in range(iterations)]
        values = self.redis_client.mget()
        for i in range(iterations):
            self.redis_client.get_key(f"key_{i}")
        end_time = time()
        return {"redis_read_time": round((end_time - start_time), 2)}
