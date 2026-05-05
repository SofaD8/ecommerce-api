from pydantic import (
    BaseModel,
    EmailStr,
    ConfigDict,
    Field
)

from app.models.user_db import UserRole


class UserSchema(BaseModel):
    email: EmailStr
    full_name: str | None = Field(None, min_length=3, max_length=50)
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserSchema):
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters long")


class UserRead(UserSchema):
    id: int
    role: UserRole


class UserUpdate(BaseModel):
    email: EmailStr = Field(default=None)
    full_name: str = Field(default=None)
    password: str = Field(default=None)
    role: UserRole = Field(default=None)
