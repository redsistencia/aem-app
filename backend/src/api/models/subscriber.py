from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, model_validator
from sqlalchemy import Boolean, Column, Integer, String, Text, TIMESTAMP, func

from src.db.base import Base


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
    newsletter = Column(Boolean, nullable=False, default=False)
    active = Column(Boolean, nullable=False, default=True)
    termination_date = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())


class SubscriberCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    name: str = Field(min_length=1, max_length=150)
    lastname: str = Field(min_length=1, max_length=150)
    email: EmailStr = Field(max_length=150)
    address: str | None = None
    nationality: str | None = Field(default=None, max_length=30)
    document_id: str | None = Field(default=None, max_length=50)
    phone: str | None = Field(default=None, max_length=30)
    privacy_policy: Literal[True]
    newsletter: bool = False

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return value.lower()


class SubscriberRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    lastname: str
    email: EmailStr
    active: bool
    newsletter: bool
    created_at: datetime


class SubscriberUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    name: str | None = Field(default=None, min_length=1, max_length=150)
    lastname: str | None = Field(default=None, min_length=1, max_length=150)
    email: EmailStr | None = Field(default=None, max_length=150)
    address: str | None = None
    nationality: str | None = Field(default=None, max_length=30)
    document_id: str | None = Field(default=None, max_length=50)
    phone: str | None = Field(default=None, max_length=30)
    privacy_policy: Literal[True] | None = None
    newsletter: bool | None = None
    active: bool | None = None
    termination_date: datetime | None = None

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str | None) -> str | None:
        return value.lower() if value else value

    @model_validator(mode="after")
    def reject_null_required_fields(self):
        required = {"name", "lastname", "email", "privacy_policy", "newsletter", "active"}
        for field in self.model_fields_set & required:
            if getattr(self, field) is None:
                raise ValueError(f"{field} cannot be null")
        return self


class UnsubscribeRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    email: EmailStr
    document_id: str = Field(min_length=1, max_length=50)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return value.lower()
