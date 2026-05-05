from typing import Any
import bcrypt
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_db import UserModel
from app.schemas.user import UserCreate, UserUpdate
from app.services.base import BaseService


def hash_password(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )


class UserService(BaseService[UserModel, UserCreate, UserUpdate]):
    def __init__(self):
        super().__init__(UserModel)

    async def get_by_email(
            self,
            db: AsyncSession,
            email: str
    ) -> UserModel | None:
        query = select(self.model).where(self.model.email == email)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def create(
            self,
            db: AsyncSession,
            *,
            obj_in: UserCreate
    ) -> UserModel:
        user_data = obj_in.model_dump()
        password = user_data.pop("password")

        if await self.get_by_email(db, email=obj_in.email):
            raise HTTPException(status_code=400, detail="Email already registered")

        user_data["hashed_password"] = hash_password(password)

        db_obj = self.model(**user_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
            self,
            db: AsyncSession,
            *,
            obj_id: int,
            obj_in: UserUpdate | dict[str, Any]
    ) -> UserModel:
        update_data = obj_in if isinstance(obj_in, dict) else obj_in.model_dump(exclude_unset=True)

        if "password" in update_data and update_data["password"]:
            password = update_data.pop("password")
            update_data["hashed_password"] = hash_password(password)

        db_obj = await self.get_by_id(db, obj_id=obj_id)
        if db_obj:
            for key, value in update_data.items():
                setattr(db_obj, key, value)
            await db.commit()
            await db.refresh(db_obj)
        return db_obj # noqa


user_service = UserService()
