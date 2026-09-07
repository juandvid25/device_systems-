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


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole
    is_active: bool