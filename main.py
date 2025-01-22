from fastapi import Depends, FastAPI
import asyncio
import uvicorn

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from database.connect import get_db
from database.creater import create_database

from app.utils.redis import RedisClient
from tests.perfomance_tests import PerformanceTester


app = FastAPI()

redis_client = RedisClient()
performance_tester = PerformanceTester(redis_client)

@app.get("/check_db")
async def check_db(session: AsyncSession = Depends(get_db)):
    result = await session.execute(text("SELECT 1"))
    return {"status": "connected" if result.scalar() == 1 else "disconnected"}

@app.get("/test_redis")
async def test_redis():
    redis_client.set_key("test_key", "test_value")
    return redis_client.get_key("test_key")

@app.get("/test_performance_db_write")
async def test_performance_db_write(session: AsyncSession = Depends(get_db)):
    """Тест производительности записи в PostgreSQL."""
    result = await performance_tester.test_db_write(session)
    return result


@app.get("/test_performance_db_read")
async def test_performance_db_read(session: AsyncSession = Depends(get_db)):
    """Тест производительности чтения из PostgreSQL."""
    result = await performance_tester.test_db_read(session)
    return result


@app.get("/test_performance_redis_write")
def test_performance_redis_write():
    """Тест производительности записи в Redis."""
    result = performance_tester.test_redis_write()
    return result


@app.get("/test_performance_redis_read")
def test_performance_redis_read():
    """Тест производительности чтения из Redis."""
    result = performance_tester.test_redis_read()
    return result


async def main():
    await create_database()
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    asyncio.run(main())