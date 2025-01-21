from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base

from config import ASYNC_DB_URL


engine = create_async_engine(ASYNC_DB_URL, echo=False)
async_session = async_sessionmaker(bind=engine, class_= AsyncSession)

Base = declarative_base()

async def get_db():
	async with async_session() as session:
		yield session
		
