from fastapi import (
    APIRouter,
    Depends,
    status,
    HTTPException
)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.schemas.user import (
    UserCreate,
    UserRead,
    UserUpdate
)
from app.services.user_service import user_service
from app.db.session import get_db
from app.models.user_db import UserModel, UserRole
from app.api.dependencies import role_required
from app.services.auth_service import auth_service


router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserRead
)
async def create_user(
        user_in: UserCreate,
        db: AsyncSession = Depends(get_db)
):
    user = await user_service.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered",
        )
    return await user_service.create(db, obj_in=user_in)

@router.post("/login")
async def login(
        db: AsyncSession = Depends(get_db),
        form_data: OAuth2PasswordRequestForm = Depends()
):
    user = await auth_service.authenticate_user(
        db,
        email=form_data.username,
        password=form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = auth_service.create_token_for_user(user)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/", response_model=List[UserRead])
async def get_all_users(
    db: AsyncSession = Depends(get_db),
    _: UserModel = Depends(role_required(UserRole.ADMIN))
):
    return await user_service.get_all(db)

@router.patch("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: AsyncSession = Depends(get_db),
    _: UserModel = Depends(role_required(UserRole.ADMIN))
):
    user = await user_service.get_by_id(db, obj_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return await user_service.update(db, db_obj=user_id, obj_in=user_in)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    _: UserModel = Depends(role_required(UserRole.ADMIN))
):
    user = await user_service.get_by_id(db, obj_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await user_service.delete(db, obj_id=user_id)
    return None
