from sqlalchemy import Column, Integer, String, TIMESTAMP, func, Enum
from sqlalchemy.orm import Mapped, mapped_column
from src.db.base import Base
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime
import enum

# Enum para los roles de usuario
class UserRole(str, enum.Enum):
    admin = "admin"
    editor = "editor"

# Definición del modelo de usuario
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(20), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column()
    active: Mapped[bool] = mapped_column(default=True)
    role = Column(Enum(UserRole), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())


# Pydantic schemas
class UserCreate(BaseModel):
    username: str = Field(min_length=1, max_length=20)
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8)
    role: UserRole

    @field_validator("password")
    @classmethod
    def password_fits_bcrypt(cls, value: str) -> str:
        if len(value.encode("utf-8")) > 72:
            raise ValueError("Password must contain at most 72 UTF-8 bytes")
        return value

class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: UserRole
    created_at: Optional[datetime]

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str
