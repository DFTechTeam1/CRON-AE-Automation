from src.secret import POSTGRES_URL
from sqlalchemy.ext.asyncio import create_async_engine


def database_connection(POSTGRES_URL: str = POSTGRES_URL):
    engine = create_async_engine(url=POSTGRES_URL)
    return engine


async def get_db():
    async with database_connection().connect() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
