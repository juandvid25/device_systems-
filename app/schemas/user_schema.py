from enum import Enum

from pydantic import BaseModel, EmailStr, Field


class UserRole(str, Enum):
    ADMIN = "admin"
    SUPPORT = "support"
    USER = "user"


class UserCreate(BaseModel):
    name: str = Field(min_length=3)
    email: EmailStr
    role: UserRole
    is_active: bool


class UserUpdate(BaseModel):
    name: str = Field(min_length=3)
    email: EmailStr
    role: UserRole
    is_active: bool


class UserPatch(BaseModel):
    name: str | None = Field(default=None, min_length=3)
    email: EmailStr | None = None
    role: UserRole | None = None
    is_active: bool | None = None


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole
    is_active: bool