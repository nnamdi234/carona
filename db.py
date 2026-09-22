import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import AsyncGenerator

load_dotenv()

DATABASE_URL=os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL)
session_factory = async_sessionmaker(engine)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        try:
            yield session
            await session.commit()  # Added `await`
        except Exception:            # Changed bare `except:` to `except Exception:`
            await session.rollback()
            raise