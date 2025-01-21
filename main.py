from fastapi import Depends, FastAPI
import asyncio
import uvicorn

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from database.connect import get_db
from database.creater import create_database


app = FastAPI()

@app.get("/check_db")
async def check_db(session: AsyncSession = Depends(get_db)):
    result = await session.execute(text("SELECT 1"))
    return {"status": "connected" if result.scalar() == 1 else "disconnected"}


async def main():
    await create_database()
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    asyncio.run(main())