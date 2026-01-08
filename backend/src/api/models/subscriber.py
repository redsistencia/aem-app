from sqlalchemy import Column, Integer, String, Text, Boolean, TIMESTAMP, func
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from db.base import Base

# Definición del modelo de suscriptor
class Subscriber(Base):
    __tablename__ = "subscribers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    lastname = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    address = Column(Text, nullable=True)
    nationality = Column(String(30), nullable=True)
    document_id = Column(String(50), nullable=True)
    phone = Column(String(30), nullable=True)
    privacy_policy = Column(Boolean, nullable=False)
    newsletter = Column(Boolean, nullable=False)
    active = Column(Boolean, nullable=False)
    termination_date = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

# Pydantic schemas
class SubscriberCreate(BaseModel):
    name: str
    lastname: str
    email: EmailStr
    address: Optional[str]
    nationality: Optional[str]
    document_id: Optional[str]
    phone: Optional[str]
    privacy_policy: bool
    newsletter: bool
    active: bool
    termination_date: Optional[str]

class SubscriberRead(BaseModel):
    id: int
    name: str
    lastname: str
    email: EmailStr
    active: bool
    created_at: datetime

    class Config:
        orm_mode = True
