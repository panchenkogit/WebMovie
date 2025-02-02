from fastapi import Depends, FastAPI
import asyncio
import uvicorn

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from database.connect import get_db
from database.creater import create_database

from app.operations.users.router import router as UsersRouter
from app.utils.authorization import router as AuthRouter
from app.operations.films.router import router as FilmsRouter
from app.operations.directors.router import router as DirectorsRouter
from app.operations.recommendations.router import router as RecRouter
from app.operations.user_library.router import router as LibraryRouter

from app.utils.redis import RedisClient



app = FastAPI(title="WebMovie",
              version="1.0.0")

app.include_router(AuthRouter)
app.include_router(UsersRouter)
app.include_router(FilmsRouter)
app.include_router(DirectorsRouter)
app.include_router(RecRouter)
app.include_router(LibraryRouter)


redis_client = RedisClient()

@app.get("/check_db")
async def check_db(session: AsyncSession = Depends(get_db)):
    result = await session.execute(text("SELECT 1"))
    return {"status": "connected" if result.scalar() == 1 else "disconnected"}

@app.get("/test_redis")
async def test_redis():
    redis_client.set_key("test_key", "test_value")
    return redis_client.get_key("test_key")



async def main():
    await create_database()
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    asyncio.run(main())