from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, EmailStr


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    FARMACIA = "farmacia"


class UserBase(BaseModel):

    name: str
    email: EmailStr


class UserCreate(UserBase):

    role: UserRole = UserRole.USER
    is_active: bool = True


class UserUpdate(BaseModel):

    name: str
    email: EmailStr
    role: UserRole = UserRole.USER
    is_active: bool = True


class UserPatch(BaseModel):

    name: str | None = None
    email: EmailStr | None = None
    role: UserRole | None = None
    is_active: bool | None = None


class UserResponse(BaseModel):

    id: int
    name: str
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )