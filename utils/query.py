from utils.logger import logging
from typing import Literal, Any, Union
from sqlmodel import SQLModel
from sqlalchemy import select, insert, update, delete, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession


class QueryDatabase:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def find(
        self,
        table: type[SQLModel],
        fetch: Literal['one', 'all'] = 'one',
        filter: Literal['and', 'or'] = 'and',
        order_by: Literal['asc', 'desc'] = 'asc',
        limit: int = None,
        offset: int = None,
        **kwargs: Any,
    ) -> Union[list[dict], dict, None]:
        condition = []

        if kwargs:
            for col, value in kwargs.items():
                col_attr = getattr(table, col, None)
                if not col_attr:
                    raise ValueError(f'Column {col} not found in {table.__tablename__} table!')
                condition.append(col_attr == value)
        try:
            filter_condition = or_(*condition) if filter == 'or' else and_(*condition)
            order_clause = table.id.asc() if order_by == 'asc' else table.id.desc()

            query = select(table).where(filter_condition).order_by(order_clause)

            if limit:
                query = query.limit(limit)
            if offset:
                query = query.offset(offset)

            result = await self._session.execute(query)

            if fetch == 'all':
                rows = result.fetchall()
                return [dict(row._mapping) for row in rows] if rows else None
            else:
                entry = result.fetchone()
                return dict(entry._mapping) if entry else None
        except Exception as e:
            logging.error(f'Failed to find record in table {table.__name__}: {e}')
            await self._session.rollback()
            raise Exception(detail='Database query error.')

    async def insert(self, table: type[SQLModel], data: dict) -> None:
        for column in data.keys():
            if not hasattr(table, column):
                raise ValueError(f"Column '{column}' not found in {table.__tablename__} table!")

        try:
            query = insert(table).values(**data)
            await self._session.execute(query)
            await self._session.commit()
            logging.info(f'New record inserted in table {table.__name__}.')
        except Exception as e:
            logging.error(f'Failed to insert record in table {table.__name__}: {e}')
            await self._session.rollback()
            raise Exception(detail='Database query error.')

    async def update(self, table: type[SQLModel], condition: dict, data: dict) -> None:
        record = await self.find(table=table, **condition)

        try:
            if not condition:
                raise ValueError('Conditions must be a non-empty dictionary.')

            if not data:
                raise ValueError('Data must be a non-empty dictionary.')

            if not record:
                raise FileNotFoundError('Data not found.')

            for column in data.keys():
                if not hasattr(table, column):
                    raise ValueError(f'Column {column} not found in {table.__tablename__} table!')

            for column in condition.keys():
                if not hasattr(table, column):
                    raise ValueError(f'Column {column} not found in {table.__tablename__} table!')

            query = (
                update(table)
                .where(*(getattr(table, column) == value for column, value in condition.items()))
                .values(**data)
            )
            await self._session.execute(query)
            await self._session.commit()
            logging.info(f'Updated record in table {table.__name__}.')

        except ValueError:
            raise
        except FileNotFoundError:
            raise
        except Exception as e:
            logging.error(
                f'Failed to update record in table {table.__name__} with conditions {condition}: {e}'
            )
            raise Exception(detail='Database query error.')

    async def delete(self, table: type[SQLModel]) -> None:
        try:
            query = delete(table)
            await self._session.execute(query)
            await self._session.commit()
            logging.info(f'Successfully deleted all records in table {table.__name__}.')
        except Exception as e:
            logging.error(f'Failed to delete all records in table {table.__name__}: {e}')
            await self._session.rollback()
            raise Exception(detail='Database query error.')
