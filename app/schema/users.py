from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional


class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: str | None = None
    email: Optional[EmailStr] = None


class UserRead(UserBase):
    id: UUID

    class Config:
        orm_mode = True
