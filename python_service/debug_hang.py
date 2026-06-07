import asyncio
import os

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.models import CareGroup

async def main():
    print("creating engine")
    engine = create_async_engine(f"postgresql+asyncpg://postgres:password@localhost:5432/orquestracao", echo=True, future=True)
    async_session_maker = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    print("entering session context")
    async with async_session_maker() as session:
        print("created group object")
        group = CareGroup(name="Test Group")
        session.add(group)
        print("committing...")
        await session.commit()
        print("refreshing...")
        await session.refresh(group)
        print("done!")

if __name__ == "__main__":
    asyncio.run(main())
