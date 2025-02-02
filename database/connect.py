from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base

from config import ASYNC_DB_URL, SYNC_DB_URL


engine = create_async_engine(ASYNC_DB_URL, echo=False)
sync_engine = create_engine(SYNC_DB_URL)

sync_session = sessionmaker(bind=sync_engine)
async_session = async_sessionmaker(bind=engine, class_= AsyncSession)

Base = declarative_base()


async def get_db():
	async with async_session() as session:
		yield session
		

def get_sync_db():
    session = sync_session()
    try:
        yield session
    finally:
        session.close()
