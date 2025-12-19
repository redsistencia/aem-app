from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from src.db.base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(150), unique=True)
    password_hash: Mapped[str] = mapped_column(String)
    role: Mapped[str] = mapped_column(String, default="admin")
    active: Mapped[bool] = mapped_column(Boolean, default=True)
