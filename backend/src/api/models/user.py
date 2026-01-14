from sqlalchemy import Column, Integer, String, TIMESTAMP, func, Enum
from sqlalchemy.orm import Mapped, mapped_column
from db.base import Base
from pydantic import BaseModel, EmailStr
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
    password: Mapped[str] = mapped_column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())


# Pydantic schemas
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: UserRole

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
