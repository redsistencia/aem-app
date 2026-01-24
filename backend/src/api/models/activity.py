from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, func
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from db.base import Base

# Definición del modelo de actividad
class Activity(Base):
    __tablename__ = "activities"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(30), nullable=False)
    description = Column(String(255), nullable=True)
    location = Column(String(255), nullable=True)
    activity_date = Column(TIMESTAMP, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(TIMESTAMP, server_default=func.now())

# Pydantic schemas
class ActivityCreate(BaseModel):
    title: str
    description: str
    location: str | None = None
    activity_date: str
    created_by: int

class ActivityRead(BaseModel):
    id: int
    title: str
    description: str
    location: str
    activity_date: datetime
    created_by: Optional[int]
    created_at: datetime

class ActivityUpdate(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    activity_date: Optional[datetime] = None
    created_by: Optional[int] = None
    created_at: Optional[datetime] = None


    class Config:
        from_attributes = True
