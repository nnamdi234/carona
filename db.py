import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import AsyncGenerator

load_dotenv()

DATABASE_URL=os.getenv("DATABASE_URL")

# Render's Postgres drops idle connections, so test each pooled connection
# before use (pool_pre_ping) and replace any older than 5 minutes (pool_recycle).
engine = create_async_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
)
session_factory = async_sessionmaker(engine)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        try:
            yield session
            await session.commit()  # Added `await`
        except Exception:            # Changed bare `except:` to `except Exception:`
            await session.rollback()
            raise