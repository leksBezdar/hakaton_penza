from typing import Any, Dict, Generic, List, Optional, TypeVar, Union

from sqlalchemy import delete, insert, select, update, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from .database import Base


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseDAO(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    model = None

    @classmethod
    async def add(
        cls,
        db: AsyncSession,
        obj_in: Union[CreateSchemaType, Dict[str, Any]]
    ) -> Optional[ModelType]:

        if isinstance(obj_in, dict):
            create_data = obj_in
        else:
            create_data = obj_in.model_dump(exclude_unset=True)

        try:
            stmt = insert(cls.model).values(
                **create_data).returning(cls.model)
            result = await db.execute(stmt)
            return result.scalars().first()
        except (SQLAlchemyError, Exception) as e:
            print(e)
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc: Cannot insert data into table"
            elif isinstance(e, Exception):
                msg = "Unknown Exc: Cannot insert data into table"
            print(msg)

            return None

    @classmethod
    async def find_one_or_none(cls, db: AsyncSession, *filter, **filter_by) -> Optional[ModelType]:

        stmt = select(cls.model).filter(*filter).filter_by(**filter_by)
        result = await db.execute(stmt)

        return result.scalars().one_or_none()

    @classmethod
    async def find_three_or_none(cls, db: AsyncSession, *filter, limit: int = 3) -> Optional[ModelType]:

        stmt = (
            select(cls.model)
            .filter(func.lower((cls.model.title)).contains(*filter))
            .limit(limit)
        )
        result = await db.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def find_all(
        cls,
        db: AsyncSession,
        *filter,
        offset: int = 0,
        limit: int = 10000,
        **filter_by
    ) -> List[ModelType]:
        stmt = (
            select(cls.model)
            .filter(*filter)
            .filter_by(**filter_by)
            .offset(offset)
            .limit(limit)
        )
        result = await db.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def update(
        cls,
        session: AsyncSession,
        *where,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> Optional[ModelType]:

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        stmt = (
            update(cls.model).
            where(*where).
            values(**update_data).
            returning(cls.model)
        )
        result = await session.execute(stmt)

        return result.scalars().one()

    @classmethod
    async def delete(cls, session: AsyncSession, *filter, **filter_by) -> None:
        stmt = delete(cls.model).filter(*filter).filter_by(**filter_by)

        await session.execute(stmt)
