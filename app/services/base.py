from typing import (
    Generic,
    TypeVar,
    Type,
    Optional
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.db.base import Base


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseService(
    Generic[ModelType, CreateSchemaType, UpdateSchemaType]
):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get_all(self, db: AsyncSession) -> list[ModelType]:
        result = await db.execute(select(self.model))
        return list(result.scalars().all())

    async def get_by_id(
            self,
            db: AsyncSession,
            obj_id: int
    ) -> Optional[ModelType]:
        return await db.get(self.model, obj_id)

    async def create(
            self,
            db: AsyncSession,
            *,
            obj_in: CreateSchemaType
    ) -> ModelType:
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
            self,
            db: AsyncSession,
            *,
            obj_id: int,
            obj_in: UpdateSchemaType
    ) -> Optional[ModelType]:
        db_obj = await self.get_by_id(db, obj_id)
        if db_obj:
            update_data = obj_in.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_obj, key, value)
            await db.commit()
            await db.refresh(db_obj)
        return db_obj

    async def delete(
            self,
            db: AsyncSession,
            *,
            obj_id: int
    ) -> bool:
        db_obj = await self.get_by_id(db, obj_id)
        if db_obj:
            await db.delete(db_obj)
            await db.commit()
            return True
        return False
