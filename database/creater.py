from database.connect import  Base, engine
from database.models.user import User


async def create_database():
    async with engine.begin() as session:
        await session.run_sync(Base.metadata.create_all)
        print("База данных создана")