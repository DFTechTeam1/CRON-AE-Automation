from datetime import datetime
from utils.helper import local_time
from sqlmodel import SQLModel, Field
from services.postgre.connection import database_connection


class Automation(SQLModel, table=True):
    __tablename__ = 'automation'
    id: int = Field(primary_key=True)
    created_at: datetime = Field(default=local_time())
    source_path: str = Field(default=None)
    destination_path: str = Field(default=None)
    is_processed: bool = Field(default=False)


async def database_migration():
    engine = database_connection()
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
